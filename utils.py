"""Blender 2.91

Utility functions.
"""

import bpy, mathutils

import math
import random
from typing import List


def removeCameras() -> None:
    """Removes every camera."""

    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)


def removeLights() -> None:
    """Removes every light."""

    for light in bpy.data.lights:
        bpy.data.lights.remove(light)


def removeMaterials() -> None:
    """Removes all materials."""

    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)


def removeMeshes() -> None:
    """Removes all meshes."""

    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


def randomExtendBoundingBox(bounding_box : List[float], max_x : float, max_y : float) -> List[float]:
    """Randomly extends a bounding box coordinates in the x and y direction.

    Params:
        bounding_box: The bounding box to extend.
        max_x: The maximum distance to extend the bounding box by along the x axis.
        max_y: The maximum distance to extend the bounding box by along the y axis.
    Returns:
        The extended bounding box.
    """

    x_p = random.uniform(0.0, max_x)
    x_n = random.uniform(0.0, max_x)
    y_p = random.uniform(0.0, max_y)
    y_n = random.uniform(0.0, max_y)

    bb = (
          bounding_box[0] - x_n,  bounding_box[1] - y_n,  bounding_box[2],  #point1
          bounding_box[3] - x_n,  bounding_box[4] - y_n,  bounding_box[5],  #point2
          bounding_box[6] + x_p,  bounding_box[7] - y_n,  bounding_box[8],  #...
          bounding_box[9] + x_p,  bounding_box[10] - y_n, bounding_box[11],
          bounding_box[12] - x_n, bounding_box[13] + y_p, bounding_box[14],
          bounding_box[15] - x_n, bounding_box[16] + y_p, bounding_box[17],
          bounding_box[18] + x_p, bounding_box[19] + y_p, bounding_box[20], #...
          bounding_box[21] + x_p, bounding_box[22] + y_p, bounding_box[23]  #point8
         )

    return bb


def clamp(value : float, l_bound : float, u_bound : float) -> float:
    """Clamps value between l_bound and u_bound."""

    return min(max(value, l_bound), u_bound)