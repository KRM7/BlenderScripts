project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"
import sys
sys.path.append(project_path)

import bpy
import math
import time

import utils
import haircomb as hc
import shaders
import render

start_time = time.time()

#INIT
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete() 

#CREATE OBJECT
haircomb = hc.Haircomb()
haircomb.createHaircomb()
mat = haircomb.getMaterial()
shaders.applyPlasticMatte(mat, shaders.COLORS["BLACK"])

print("\nObject done.")
gen_time = time.time()
print("Object generation time: %s seconds" % round(gen_time - start_time, 2))

#ADD ENVIRONMENT
bpy.ops.mesh.primitive_plane_add(size = 2000)
ground = bpy.context.object
mat = bpy.data.materials.new(name = "ground")
shaders.applyBase(mat, shaders.COLORS["GREEN"])
ground.data.materials.append(mat)

#world = bpy.context.scene.world
#world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.1
#node_env = world.node_tree.nodes.new(type = "ShaderNodeTexEnvironment")
#img_path = project_path + "\\hdris\\empty_warehouse_01_1k.hdr"
#node_env.image = bpy.data.images.load(img_path)

#ADD LIGHT
bpy.ops.object.light_add(type = "POINT", location = (110, 50, 160))
light = bpy.context.object
light.data.color = (1.0, 0.84, 0.45)
light.data.energy = 1E+6
light.data.cycles.max_bounces = 16
light.data.shadow_soft_size = 0.1

#ADD CAMERA
bpy.ops.object.camera_add(location = (100, -100, 150),
                          rotation = (25*math.pi/180, -30*math.pi/180, 90*math.pi/180),
                          scale = (1.0, 1.0, 1.0))
bpy.context.scene.camera = bpy.context.object

print("Scene done.")
scene_time = time.time()
print("Scene generation time: %s seconds" % round(scene_time - gen_time, 2))

#RENDER
render.eeveeRender(project_path + "\\imgs\\test")

print("Render done.")
render_time = time.time()
print("Render time: %s seconds" % round(render_time - scene_time, 2))

print("Overall time: %s seconds" % round((time.time() - start_time), 2))