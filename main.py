project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"

import sys
sys.path.append(project_path)

import bpy
import math
import time

import utils
import haircomb as hc
import shaders

def init():
    #delete everything
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()
    #set units to mm
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"   

start_time = time.time()
init()

haircomb = hc.Haircomb()
haircomb.createHaircomb()

#ADD LIGHT
bpy.ops.object.light_add(type = "POINT", location = (110, 50, 160))
light = bpy.context.object
light.data.color = (1.0, 0.84, 0.45)
light.data.energy = 0.5E+6
light.data.cycles.max_bounces = 8
light.data.shadow_soft_size = 0.1

#ADD CAMERA
bpy.ops.object.camera_add(location = (100, -100, 150),
                          rotation = (25*math.pi/180, -30*math.pi/180, 90*math.pi/180),
                          scale = (1.0, 1.0, 1.0))
bpy.context.scene.camera = bpy.context.object

#BACKGROUND
bpy.ops.mesh.primitive_plane_add(size = 2000)
ground = bpy.context.object
mat = bpy.data.materials.new(name = "ground")
shaders.applyPlastic(mat, (0.65, 0.65, 0.65, 1.0), (0.85, 0.85, 0.85, 1.0))
ground.data.materials.append(mat)

#SHADING
mat = haircomb.getMaterial()
shaders.applyPlastic(mat, (0.0, 0.0, 0.0, 1))

#RENDER
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "GPU"
scene.cycles.samples = 8
scene.cycles.use_denoising = True
scene.cycles.denoiser = "OPTIX"
scene.cycles.debug_use_spatial_splits
scene.render.tile_x = 128
scene.render.tile_y = 128
scene.cycles.volume_max_steps = 64

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = "JPEG"
scene.render.image_settings.quality = 90
scene.render.filepath = project_path + "\\imgs\\test"
bpy.ops.render.render(write_still = True)

print("%s seconds" % round((time.time() - start_time), 4))