import bpy, mathutils
import math
import random

def removeCameras():
    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)

def removeLights():
    for light in bpy.data.lights:
        bpy.data.lights.remove(light)

def removeMaterials():
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

def removeMeshes():
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

def pointCameraTo(cam, target):
    cam_pos = cam.matrix_world.to_translation()
    
    dir = target - cam_pos
    rot = dir.to_track_quat("-Z", "Y")
    cam.rotation_euler = rot.to_euler()

def placeCamera(target_coords, max_view_angle, max_roll_angle):
    cam_height = 100
    bpy.ops.object.camera_add(location = (0, 0, cam_height))
    camera = bpy.context.object
    bpy.context.scene.camera = camera

    #random camera view angle
    max_co = cam_height*math.tan(max_view_angle*math.pi/180)
    x = random.uniform(-max_co, max_co)
    y = random.uniform(-max_co, max_co)
    aim = mathutils.Vector((x, y, 0))
    pointCameraTo(camera, aim)

    #random camera roll
    roll = random.uniform(-max_roll_angle*math.pi/180, max_roll_angle*math.pi/180)
    roll_matrix = mathutils.Matrix.Rotation(roll, 4, 'Z')

    rot_matrix = camera.rotation_euler.to_matrix().to_4x4()
    rot_matrix = rot_matrix @ roll_matrix
    camera.rotation_euler = rot_matrix.to_euler()

    #fit object into view
    loc, scale = camera.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), target_coords)
    camera.location = loc

    return camera