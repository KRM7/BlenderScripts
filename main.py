project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"
import sys
sys.path.append(project_path)

import bpy, mathutils
import math, random, time
from os import path
import utils, shaders, render, haircomb, scene

#SETTINGS
#image count
num_objects = 1
num_images = 1

#mechanical and geometry defects (any combination)
missing_teeth = False
bent_teeth = False
warping = False
ejector_marks = 0   #(0, 2, or 3)
#texture defects (max 1 of these)
contamination = False
discoloration = False
splay = False
gloss = False

#camera params (degrees)
cam_max_view_angle_x = 50.0
cam_max_view_angle_y = 35.0
cam_max_roll_angle = 15.0


#INIT
start_time = time.time()
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete()
utils.removeMeshes()
utils.removeMaterials()
utils.removeLights()
utils.removeCameras()

render.setupCycles(samples = 64, bounces = 32)
render.setImageSettings(res_x = 1920, res_y = 1080, color = True)


#SETUP ENVIRONMENT
#ground
ground_mat = bpy.data.materials.new(name = "ground")
bpy.ops.mesh.primitive_plane_add(size = scene.ground_plane_size)
ground = bpy.context.object
ground.data.materials.append(ground_mat)

#world
world = bpy.context.scene.world
node_env = world.node_tree.nodes.new(type = "ShaderNodeTexEnvironment")
world.node_tree.links.new(node_env.outputs["Color"], world.node_tree.nodes["Background"].inputs["Color"])

print("Environment done.")


#GENERATE OBJECTS
for obj in range(num_objects):
    #INIT
    if "hc" in locals():
        bpy.data.objects.remove(hc.getObject())
    
    #CREATE OBJECT
    hc = haircomb.Haircomb(missing_teeth = missing_teeth, bent_teeth = bent_teeth, warping = warping, ejector_marks = ejector_marks)
    hc.createHaircomb()

    print("Object" + str(obj) + " generation done.")

    #GENERATE IMAGES
    for img in range(num_images):

        #ADD RANDOM MATERIALS
        #haircomb mat
        color = random.uniform(0.0, 0.004)
        color = (color, color, color, 1.0)

        if contamination: defect = "contamination"
        elif splay: defect = "splay"
        elif gloss: defect = "gloss"
        elif discoloration: defect = "discoloration"
        else : defect = None

        shaders.applyPlastic(mat = hc.getMaterial(), color = color, surface = "Matte", randomize = True, defect = defect)

        #ground mat
        ground_texture = shaders.applyRandomTextures(ground_mat)
    
        #CAMERA
        utils.removeCameras()

        coords = hc.getBoundingBox()
        coords = utils.randomExtendBoundingBox(bounding_box = coords, max_x = hc.width/6, max_y = hc.width/4)

        camera = scene.placeCamera(coords, cam_max_view_angle_x, cam_max_view_angle_y, cam_max_roll_angle)

        #LIGHTING
        hdri_idx = random.randrange(len(scene.hdris))
        hdri = scene.hdris[hdri_idx]

        node_env.image = bpy.data.images.load(hdri["path"], check_existing = True)
        world.node_tree.nodes["Background"].inputs["Strength"].default_value = random.uniform(hdri["light_min"], hdri["light_max"])

        #adjust light based on material
        world.node_tree.nodes["Background"].inputs["Strength"].default_value += ground_texture["light_correction"]

        #RENDER
        #render.render(project_path + "\\imgs\\batch\\" + str(obj) + "_" + str(img))
        render.render(project_path + "\\imgs\\batch\\" + ground_texture["name"] + "_" + hdri["name"] + "_" + str(world.node_tree.nodes["Background"].inputs["Strength"].default_value))


print("Overall time: %s seconds" % round((time.time() - start_time), 2))