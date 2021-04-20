project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"
import sys
sys.path.append(project_path)

import bpy, mathutils
import math, random, time
import utils, shaders, render, haircomb

num_objects = 1
num_images = 20
missing_teeth = False
bent_teeth = False
warping = False


start_time = time.time()
#INIT
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete()
utils.removeMeshes()
utils.removeMaterials()
utils.removeLights()
utils.removeCameras()


#SETUP ENVIRONMENT
#ground material
gmat = bpy.data.materials.new(name = "ground")

materials = [
             {"f": shaders.applyAsphalt, "scale": 700, "light_diff": -0.1},
             {"f": shaders.applyPorcelain, "scale": 500, "light_diff": -0.3},
             {"f": shaders.applyMetal, "scale": 500, "light_diff": 0.25},
             {"f": shaders.applyTiles, "scale": 400, "light_diff": 0.0}
            ]

#world, hdri
world = bpy.context.scene.world
node_env = world.node_tree.nodes.new(type = "ShaderNodeTexEnvironment")
world.node_tree.links.new(node_env.outputs["Color"], world.node_tree.nodes["Background"].inputs["Color"])

hdris = [
         {"path": project_path + "\\hdris\\peppermint_powerplant.hdr", "light_min": 0.4, "light_max": 1.5},
         {"path": project_path + "\\hdris\\reinforced_concrete.hdr", "light_min": 0.6, "light_max": 1.8},     #some edges
         {"path": project_path + "\\hdris\\lebombo.hdr", "light_min": 0.4, "light_max": 0.9},                 #some edges
         {"path": project_path + "\\hdris\\killesberg_park.hdr", "light_min": 0.25, "light_max": 0.75},
         {"path": project_path + "\\hdris\\paul_lobe_haus.hdr", "light_min": 0.4, "light_max": 0.9},
        ]

print("Environment done.")


#GENERATE OBJECTS
for obj in range(num_objects):
    #INIT
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()
    utils.removeMeshes()
    
    #CREATE GROUND OBJECT
    bpy.ops.mesh.primitive_plane_add(size = 20000)
    ground = bpy.context.object
    ground.data.materials.append(gmat)
    
    #CREATE OBJECT
    hc = haircomb.Haircomb(missing_teeth = missing_teeth, bent_teeth = bent_teeth, warping = warping)
    hc.createHaircomb()
    mat = hc.getMaterial()
    color = random.uniform(0.0, 0.005)
    shaders.applyPlasticMatte(mat, (color, color, color, 1.0), randomize = True)

    print("Object" + str(obj) + " generation done.")

    #GENERATE IMAGES
    for img in range(num_images):

        #ADD RANDOM GROUND MAT
        mat_idx = random.choice(range(len(materials)))
        materials[mat_idx]["f"](gmat, materials[mat_idx]["scale"])

        #shaders.applyBase(gmat, random.sample(shaders.COLORS.values(), 1), randomize = True)
    
        #region ADD CAMERA
        utils.removeCameras()

        cam_max_view_angle_x = 60
        cam_max_view_angle_y = 30
        cam_max_roll_angle = 15

        coords = hc.getBoundingBox()
        coords = utils.randomExtendBoundingBox(bounding_box = coords, max_x = hc.width/6, max_y = hc.width/4)

        camera = utils.placeCamera(coords, cam_max_view_angle_x, cam_max_view_angle_y, cam_max_roll_angle)
        #endregion

        #region ADD LIGHTING

        #random hdri lighting
        hdri_idx = random.choice(range(len(hdris)))
        node_env.image = bpy.data.images.load(hdris[hdri_idx]["path"], check_existing = True)
        world.node_tree.nodes["Background"].inputs["Strength"].default_value = random.uniform(hdris[hdri_idx]["light_min"], hdris[hdri_idx]["light_max"])

        #adjust light strength based on material
        world.node_tree.nodes["Background"].inputs["Strength"].default_value += materials[mat_idx]["light_diff"]
        #endregion

        #RENDER
        render.cyclesRender(project_path + "\\imgs\\batch\\" + str(obj) + "_" + str(img), samples = 64, bounces = 32)


print("Overall time: %s seconds" % round((time.time() - start_time), 2))