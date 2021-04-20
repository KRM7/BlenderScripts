import bpy, mathutils
import math, random

def removeCameras():
    #removes every camera
    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)


def removeLights():
    #removes all lights
    for light in bpy.data.lights:
        bpy.data.lights.remove(light)


def removeMaterials():
    #removes all materials
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)


def removeMeshes():
    #removes all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


def pointCameraTo(cam, target):
    #points camera towards the target coordinates
    cam_pos = cam.matrix_world.to_translation()
    
    dir = target - cam_pos
    rot = dir.to_track_quat("-Z", "Y")
    cam.rotation_euler = rot.to_euler()


def placeCamera(target_coords, max_view_angle_x, max_view_angle_y, max_roll_angle):
    #places a camera randomly with the target_coords always being in frame
    cam_height = 100
    bpy.ops.object.camera_add(location = (0, 0, cam_height))
    camera = bpy.context.object
    camera.data.clip_end = 1500
    bpy.context.scene.camera = camera

    #random camera view angle
    max_x = cam_height*math.tan(max_view_angle_x*math.pi/180)
    max_y = cam_height*math.tan(max_view_angle_y*math.pi/180)
    x = random.uniform(-max_x, max_x)
    y = random.uniform(-max_y, max_y)
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


def randomExtendBoundingBox(bounding_box, max_x, max_y):
    #randomly extends bounding box coordinates in the x and y direction
    x_pos = random.uniform(0, max_x)
    x_neg = random.uniform(0, max_x)
    y_pos = random.uniform(0, max_y)
    y_neg = random.uniform(0, max_y)

    bb = (
          bounding_box[0] - x_neg,  bounding_box[1] - y_neg,  bounding_box[2],
          bounding_box[3] - x_neg,  bounding_box[4] - y_neg,  bounding_box[5],
          bounding_box[6] + x_pos,  bounding_box[7] - y_neg,  bounding_box[8],
          bounding_box[9] + x_pos,  bounding_box[10] - y_neg, bounding_box[11],
          bounding_box[12] - x_neg, bounding_box[13] + y_pos, bounding_box[14],
          bounding_box[15] - x_neg, bounding_box[16] + y_pos, bounding_box[17],
          bounding_box[18] + x_pos, bounding_box[19] + y_pos, bounding_box[20],
          bounding_box[21] + x_pos, bounding_box[22] + y_pos, bounding_box[23]
         )

    return bb


def calcAngles(count, indexes, angle):
    #calculates angles for the bent teeth of the haircomb
    angles = {}
    id_list = [*indexes]
    middle = int(count/2)

    for i in range(count):
        if i < middle:
            angles[id_list[i]] = min((5+3*i)*math.pi/180, angle)
        else:
            angles[id_list[i]] = min((5+3*(count-1 - i))*math.pi/180, angle)
        if not ((i == 0) or (i == (count - 1))):
            angles[id_list[i]] += random.uniform(-1*math.pi/180, 1*math.pi/180)

    return angles