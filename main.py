import sys
sys.path.append("C:\\Users\\Krisztián\\source\\repos\\BlenderScripts")

import bpy, bmesh
import math
import time

import utils
import haircomb as hc


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
                          scale = (0.5, 0.5, 1.0))
bpy.context.scene.camera = bpy.context.object

#BACKGROUND
bpy.ops.mesh.primitive_plane_add(size = 2000)
background = bpy.context.object
mat = bpy.data.materials.new(name = "back")
mat.diffuse_color = (0.5, 0.5, 0.5, 1.0)
mat.metallic = 0.4
mat.roughness = 0.4
background.data.materials.append(mat)

#RENDER
bpy.data.scenes["Scene"].render.engine = "CYCLES"
bpy.data.scenes["Scene"].cycles.device = "GPU"
bpy.data.scenes["Scene"].cycles.samples = 8
bpy.data.scenes["Scene"].cycles.use_denoising = True
bpy.data.scenes["Scene"].cycles.denoiser = "OPTIX"
bpy.data.scenes["Scene"].cycles.debug_use_spatial_splits
bpy.data.scenes["Scene"].render.tile_x = 128
bpy.data.scenes["Scene"].render.tile_y = 128
bpy.data.scenes["Scene"].cycles.volume_max_steps = 64

bpy.data.scenes["Scene"].render.resolution_x = 1920
bpy.data.scenes["Scene"].render.resolution_y = 1080
bpy.data.scenes["Scene"].render.image_settings.file_format = "JPEG"
bpy.data.scenes["Scene"].render.image_settings.quality = 90
bpy.data.scenes["Scene"].render.filepath = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts\\imgs\\test"
bpy.ops.render.render(write_still = True)

print("%s seconds" % round((time.time() - start_time), 4))