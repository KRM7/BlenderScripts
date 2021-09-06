import bpy, mathutils

import sys
project_path = sys.argv[sys.argv.index("--") + 1]
sys.path.append(project_path)

import os
import math
import random
import time
import configparser
import haircomb, scene, shaders, render, utils


config = configparser.ConfigParser()
config.read(os.path.join(project_path, "config.ini"))


start_time = time.time()

# Clear everything in the scene
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete()
utils.removeMeshes()
utils.removeMaterials()
utils.removeLights()
utils.removeCameras()

# Set the render settings
render.setupCycles(samples = int(config["Render"]["samples"]),
                   bounces = int(config["Render"]["bounces"]),
                   tile_size = int(config["Render"]["tile_size"]),
                   denoising = config["Render"]["denoise"] == "True")


# Set the output image settings
render.setImageSettings(res_x = int(config["Image"]["resolution_x"]),
                        res_y = int(config["Image"]["resolution_y"]),
                        color = config["Image"]["color"] == "True")


# Setup the environment (the parts which won't change between images)
# Ground
ground_mat = bpy.data.materials.new(name = "ground")
bpy.ops.mesh.primitive_plane_add(size = scene.ground_plane_size)
ground = bpy.context.object
ground.data.materials.append(ground_mat)

# World/environment
world = bpy.context.scene.world
node_env = world.node_tree.nodes.new(type = "ShaderNodeTexEnvironment")
world.node_tree.links.new(node_env.outputs["Color"], world.node_tree.nodes["Background"].inputs["Color"])


# Classes



# Create the objects
imgs_per_class = int(config["Output"]["imgs_per_class"])
imgs_per_object = int(config["Output"]["imgs_per_object"])

validate_p = float(config["Output"]["validate"])
test_p = float(config["Output"]["test"])

for obj_idx in range(int(imgs_per_class/imgs_per_object)):
    
    # Delete the haircomb if it already exists
    if "hc" in locals():
        bpy.data.objects.remove(hc.getObject())
    
    # Create the haircomb with defects if needed
    hc = haircomb.Haircomb(missing_teeth = False,
                           bent_teeth = False,
                           warping = False,
                           ejector_marks = 0)
    hc.createHaircomb()

    # Generate images of the haircomb
    for img_idx in range(int(config["Output"]["imgs_per_object"])):

        img_num = obj_idx * imgs_per_object + (img_idx + 1)

        # Add random materials
        tex_path = os.path.join(config["Paths"]["project_path"], "textures")
        # Material of the haircomb
        #if contamination: defect = "contamination"
        #elif splay: defect = "splay"
        #elif cloudy: defect = "cloudy"
        #elif gloss: defect = "gloss"
        #elif discoloration: defect = "discoloration"
        #else : defect = None

        shaders.applyPlastic(mat = hc.getMaterial(),
                             color = (0.0, 0.0, 0.0, 1.0),
                             surface = "Matte",
                             randomize = config["Object"]["randomize"] == "True",
                             textures_path = tex_path,
                             defect = None)

        # Apply material to the ground plane
        ground_texture = shaders.applyRandomTextures(ground_mat, tex_path)
    

        # Camera setup
        scene.removeCameras()

        coords = hc.getBoundingBox()
        coords = utils.randomExtendBoundingBox(bounding_box = coords, max_x = hc.width/6, max_y = hc.width/6)

        camera = scene.placeCamera(coords,
                                   max_view_angle_x = float(config["Camera"]["max_view_angle_x"]),
                                   max_view_angle_y = float(config["Camera"]["max_view_angle_y"]),
                                   max_roll_angle = float(config["Camera"]["max_roll_angle"]))


        # Lighting setup
        hdri_idx = random.randrange(len(scene.hdris))
        hdri = scene.hdris[hdri_idx]
        hdri_path = os.path.join(config["Paths"]["project_path"], "hdris", hdri["name"])

        node_env.image = bpy.data.images.load(hdri_path, check_existing = True)
        world.node_tree.nodes["Background"].inputs["Strength"].default_value = random.uniform(hdri["light_min"], hdri["light_max"])

        # Adjust light based on material
        world.node_tree.nodes["Background"].inputs["Strength"].default_value += ground_texture["light_correction"]


        # Render and save the image
        if (img_num <= (1.0 - validate_p - test_p) * imgs_per_class):
            dir = "train"
        elif (img_num <= (1.0 - test_p) * imgs_per_class):
            dir = "validate"
        else:
            dir = "test"

        img_path = os.path.join(config["Paths"]["output_path"], dir, str(img_num))
        render.render(img_path)


print("Overall time: %s seconds" % round((time.time() - start_time), 2))