project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"
import sys
sys.path.append(project_path)

import bpy
import mathutils

import math
import random
import time

import utils
import haircomb
import shaders
import render

start_time = time.time()

#INIT
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete()
utils.removeMeshes()
utils.removeMaterials()
utils.removeLights()
utils.removeCameras()


#CREATE OBJECT
hc = haircomb.Haircomb(missing_teeth = False)
hc.createHaircomb()
mat = hc.getMaterial()
shaders.applyPlasticMatte(mat, shaders.COLORS["BLACK"])

print("\nObject done.")
gen_time = time.time()
print("Object generation time: %s seconds" % round(gen_time - start_time, 2))


#ADD ENVIRONMENT
bpy.ops.mesh.primitive_plane_add(size = 20000)
ground = bpy.context.object
mat = bpy.data.materials.new(name = "ground")
shaders.applyPorcelain(mat)
ground.data.materials.append(mat)

hdris = [
         project_path + "\\hdris\\peppermint_powerplant.hdr",   #light strength 0.3-1.5     #all fine no edges
         project_path + "\\hdris\\reinforced_concrete.hdr",     #light strength 0.3-1.5     #some edges
         project_path + "\\hdris\\lebombo.hdr",                 #light strength 0.1-0.6     #some edges
         project_path + "\\hdris\\killesberg_park.hdr",         #light strength 0.1-0.6     #all fine no edges
         project_path + "\\hdris\\paul_lobe_haus.hdr",          #light strength 0.1-0.6     #all fine no edges
        ]

world = bpy.context.scene.world
node_env = world.node_tree.nodes.new(type = "ShaderNodeTexEnvironment")
world.node_tree.links.new(node_env.outputs["Color"], world.node_tree.nodes["Background"].inputs["Color"])


#GENERATE IMAGES
num_images = 50
for i in range(num_images):
    #ADD CAMERA
    utils.removeCameras()

    cam_max_view_angle_x = 60
    cam_max_view_angle_y = 30
    cam_max_roll_angle = 15

    coords = hc.getBoundingBox()
    coords = utils.randomExtendBoundingBox(bounding_box = coords, max_x = hc.width/6, max_y = hc.width/4)

    camera = utils.placeCamera(coords, cam_max_view_angle_x, cam_max_view_angle_y, cam_max_roll_angle)


    #ADD LIGHTING

    #lamp lighting
    #utils.removeLights()

    #light_pos = random.uniform(0, 2*math.pi)
    #light_distance = hc.width + random.uniform(-hc.width/3, hc.width/1.5)
    #bpy.ops.object.light_add(type = "POINT", 
    #                         location = (light_distance*math.sin(light_pos),
    #                                     light_distance*math.cos(light_pos),
    #                                     1.2*hc.width + random.uniform(-hc.width/3, hc.width/1.5))
    #                        )
    #light1 = bpy.context.object
    #light1.data.color = (1.0 + random.uniform(-0.15, 0),
    #                     0.85 + random.uniform(-0.15, 0.15),
    #                     0.45 + random.uniform(-0.15, 0.15))
    #light1.data.energy = 1E+6 + random.uniform(-0.3E+6, 2.5E+6)
    #light1.data.specular_factor = 0.6 + random.uniform(-0.2, 0.2)
    #light1.data.cycles.max_bounces = 64
    #light1.data.shadow_soft_size = 0.1

    #print("Scene done.")
    #scene_time = time.time()
    #print("Scene generation time: %s seconds" % round(scene_time - gen_time, 2))

    #hdri lighting
    hdri_idx = random.choice(range(len(hdris)))
    node_env.image = bpy.data.images.load(hdris[hdri_idx], check_existing = True)
    if hdri_idx == 0 or hdri_idx == 1:
        world.node_tree.nodes["Background"].inputs["Strength"].default_value = random.uniform(0.3, 1.5)
    else:
        world.node_tree.nodes["Background"].inputs["Strength"].default_value = random.uniform(0.1, 0.6)


    #RENDER
    render.cyclesRender(project_path + "\\imgs\\batch\\" + str(i), samples = 64, bounces = 32)

    #print("Render done.")
    #render_time = time.time()
    #print("Render time: %s seconds" % round(render_time - scene_time, 2))

print("Overall time: %s seconds" % round((time.time() - start_time), 2))