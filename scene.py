"""Blender 2.91

Functions to set up the scene for rendering (cameras and lights).
"""

import bpy, mathutils

import math
import random
from typing import List


# Available HDRIs for lighting and some of their properties.
hdris = [{"name": "peppermint_powerplant.hdr",  "light_min": 0.65,  "light_max": 1.65},
         {"name": "reinforced_concrete.hdr",    "light_min": 0.75,  "light_max": 1.85},
         {"name": "lebombo.hdr",                "light_min": 0.65,  "light_max": 1.3},
         {"name": "killesberg_park.hdr",        "light_min": 0.55,  "light_max": 1.05},
         {"name": "paul_lobe_haus.hdr",         "light_min": 0.45,  "light_max": 0.95},]

# The size of the ground plane in the scene.
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
        max_view_angle_x: The maximum view angle along the x axis. (in degrees) [0.0, 90.0)
        max_view_angle_y: The maximum view angle along the y axis. (in degrees) [0.0, 90.0)
        max_roll_angle: The maximum roll angle of the camera. (in degrees)
    Returns:
        The created camera.
    """

    cam_height = 100.0  # Irrelevant, the distance will be determined by the fit_coords function.
    bpy.ops.object.camera_add(location = (0.0, 0.0, cam_height))
    camera = bpy.context.object
    camera.data.clip_end = 1500.0
    bpy.context.scene.camera = camera

    # Random camera view angle
    max_x = cam_height*math.tan(max_view_angle_x*math.pi/180)
    max_y = cam_height*math.tan(max_view_angle_y*math.pi/180)
    x = random.uniform(-max_x, max_x)
    y = random.uniform(-max_y, max_y)

    pointCameraTo(camera, mathutils.Vector((x, y, 0.0)))

    # Random camera roll
    roll = random.uniform(-max_roll_angle*math.pi/180, max_roll_angle*math.pi/180)
    roll_matrix = mathutils.Matrix.Rotation(roll, 4, "Z")

    rot_matrix_old = camera.rotation_euler.to_matrix().to_4x4()
    rot_matrix_new = rot_matrix_old @ roll_matrix
    camera.rotation_euler = rot_matrix_new.to_euler()

    # Fit the object into the view
    loc, scale = camera.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), target_coords)
    camera.location = loc

    return camera


def placeLights(num_lights : int,
                height_min : float,
                height_max : float,
                hdistance_min : float,
                hdistance_max : float,
                strength_min : float,
                strength_max : float) -> None:
    """ Places a number of point lights randomly in the scene within the specified bounds.
    
    Params:
        num_lights: The number of lights to place in the scene.
        height_min: The minimum height at which the lights are placed.
        height_max: The maximum height at which the lights are placed.
        hdistance_min: The minimum horizontal distance from the origin at which the lights can be placed.
        hdistance_max: The maximum horizontal distance from the origin at which the lights can be placed.
        strength_min: The minimum energy of the light sources in megawatts.
        strength_max: The maximum energy of the light sources in megawatts.
    """

    for light in range(num_lights):
        angle = random.uniform(0.0, 2.0*math.pi)
        hdistance = random.uniform(hdistance_min, hdistance_max)
        loc_x = hdistance*math.cos(angle)
        loc_y = hdistance*math.sin(angle)
        bpy.ops.object.light_add(type = "POINT", location = (loc_x, loc_y, random.uniform(height_min, height_max)))
        light = bpy.context.object
        light.data.energy = random.uniform(strength_min, strength_max) * 1E6