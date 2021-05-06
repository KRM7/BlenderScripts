"""Blender 2.91

Functions to set up the scene for rendering (cameras and lights).
"""

import bpy, mathutils
import math, random
import globals
from typing import List


hdris = [
         {"path": globals.project_path + "\\hdris\\peppermint_powerplant.hdr",  "light_min": 0.65, "light_max": 1.65,   "name": "powerplant"},
         {"path": globals.project_path + "\\hdris\\reinforced_concrete.hdr",    "light_min": 0.75, "light_max": 1.85,   "name": "rconcrete"},
         {"path": globals.project_path + "\\hdris\\lebombo.hdr",                "light_min": 0.65, "light_max": 1.3,    "name": "lebombo"},
         {"path": globals.project_path + "\\hdris\\killesberg_park.hdr",        "light_min": 0.55, "light_max": 1.05,   "name": "killesberg"},
         {"path": globals.project_path + "\\hdris\\paul_lobe_haus.hdr",         "light_min": 0.45, "light_max": 0.95,   "name": "paullobehaus"},
        ]

ground_plane_size = 20000.0


def removeCameras() -> None:
    """Removes every camera."""

    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)


def removeLights() -> None:
    """Removes every light."""

    for light in bpy.data.lights:
        bpy.data.lights.remove(light)


def pointCameraTo(cam : bpy.types.Camera, target : mathutils.Vector) -> None:
    """Points the camera towards the given point.
    
    Param:
        cam: The camera to rotate.
        target: The target coordinates to point to.
    """

    cam_pos = cam.matrix_world.to_translation()
    
    dir = target - cam_pos
    rot = dir.to_track_quat("-Z", "Y")
    cam.rotation_euler = rot.to_euler()


def placeCamera(target_coords : List[float],
                max_view_angle_x : float = 89,
                max_view_angle_y : float = 89,
                max_roll_angle : float = 180) -> bpy.types.Camera:
    """Places a camera in the scene randomly with the target_coords always being visible in frame.

    Params:
        target_coords: The coordinates of the points that are going to be in frame.
        max_view_angle_x: The maximum view angle along the x axis. (in degrees)[0,90)
        max_view_angle_y: The maximum view angle along the y axis. (in degrees)[0,90)
        max_roll_angle: The maximum roll angle of the camera. (in degrees)
    Returns:
        The created camera.
    """

    cam_height = 100.0  #irrelevant
    bpy.ops.object.camera_add(location = (0.0, 0.0, cam_height))
    camera = bpy.context.object
    camera.data.clip_end = 1500.0
    bpy.context.scene.camera = camera

    #random camera view angle
    max_x = cam_height*math.tan(max_view_angle_x*math.pi/180)
    max_y = cam_height*math.tan(max_view_angle_y*math.pi/180)
    x = random.uniform(-max_x, max_x)
    y = random.uniform(-max_y, max_y)

    pointCameraTo(camera, mathutils.Vector((x, y, 0.0)))

    #random camera roll
    roll = random.uniform(-max_roll_angle*math.pi/180, max_roll_angle*math.pi/180)
    roll_matrix = mathutils.Matrix.Rotation(roll, 4, "Z")

    rot_matrix_old = camera.rotation_euler.to_matrix().to_4x4()
    rot_matrix_new = rot_matrix_old @ roll_matrix
    camera.rotation_euler = rot_matrix_new.to_euler()

    #fit object into view
    loc, scale = camera.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), target_coords)
    camera.location = loc

    return camera