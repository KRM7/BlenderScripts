"""Blender 2.91

Functions for modifying objects and meshes in Blender.
Used for modeling the objects.
"""

import bpy
import math


def merge(target : bpy.types.Mesh,
          object : bpy.types.Mesh,
          solver : str = "EXACT") -> None:
    """Boolean operator that combines the target and the object meshes.

    Params:
        target: The mesh to attach the object to.
        object: The mesh to attach to the object.
        solver: "EXACT" or "FAST"
    """

    mod = target.modifiers.new("merge", type = "BOOLEAN")
    mod.operation = "UNION"
    mod.solver = solver
    mod.object = object

    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "merge")


def cut(target : bpy.types.Mesh,
        object : bpy.types.Mesh,
        solver : str = "EXACT") -> None:
    """Boolean operator that cuts the object mesh out of the target mesh.

    Params:
        target: The mesh to cut from.
        object: The mesh to cut out from the target.
        solver: "EXACT" or "FAST"
    """

    mod = target.modifiers.new("cut", type = "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = solver
    mod.object = object

    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "cut")


def intersect(target : bpy.types.Mesh,
              object : bpy.types.Mesh,
              solver : str = "EXACT") -> None:
    """Boolean operator that keeps the part of the target that is common between the target and object meshes.

    Params:
        target: The mesh to modify.
        object: The other mesh to use for the intersect operation.
        solver: "EXACT" or "FAST"
    """

    mod = target.modifiers.new("and", type = "BOOLEAN")
    mod.operation = "INTERSECT"
    mod.solver = solver
    mod.object = object

    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "and")

    
def roundEdges(object : bpy.types.Mesh,
               edges : bpy.types.VertexGroup,
               radius : float = 1.0,
               segments : int = 5,
               clamp_overlap : bool = True) -> None:
    """Round the given edges of an object.

    Params:
        object: The target mesh.
        vgroup: The edges of the mesh to round (vertex group).
        radius: The radius of the rounded edges.
        segments: The number of segments to use.
        clamp_overlap: Clamp to avoid overlapping geometry.
    """

    mod = object.modifiers.new("bevel", type = "BEVEL")
    mod.limit_method = "VGROUP"
    mod.vertex_group = edges
    mod.width = radius
    mod.segments = segments
    mod.use_clamp_overlap = clamp_overlap
    mod.miter_outer = "MITER_ARC"

    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "bevel")
 
    
def roundSharpEdges(object : bpy.types.Mesh,
                    radius : float = 1.0,
                    segments : int = 5,
                    angle : float = 60.0,
                    clamp_overlap : bool = True) -> None:
    """Round all edges of a mesh that are sharper than a given angle.
    
    Params:
        object: The target mesh.
        radius: The radius of the rounding.
        segments: The number of segments to use.
        angle: The limit angle in degrees.
        clamp_overlap: Clamp to avoid overlapping geometry.
    """

    mod = object.modifiers.new("bevel", type = "BEVEL")
    mod.limit_method = "ANGLE"
    mod.angle_limit = angle * math.pi/180
    mod.width = radius
    mod.segments = segments
    mod.use_clamp_overlap = clamp_overlap
    mod.miter_outer = "MITER_ARC"

    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "bevel")

    
def chamferEdges(object : bpy.types.Mesh,
                 vgroup : bpy.types.VertexGroup,
                 length : float = 1.0,
                 clamp_overlap : bool = False) -> None:
    """Chamfer the edges of an object.
    
    Params:
        object: The mesh to chamfer the edges of.
        vgroup: The edges of the mesh to chamfer (vertex group).
        length: The size of the chamfer.
        clamp_overlap: Clamp to avoid overlapping geometry.
    """
    
    mod = object.modifiers.new("chamfer", type = "BEVEL")
    mod.limit_method = "VGROUP"
    mod.vertex_group = vgroup
    mod.width = length
    mod.segments = 1
    mod.use_clamp_overlap = clamp_overlap

    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "chamfer")


def removeDuplicateVerts(object : bpy.types.Mesh) -> None:
    """Removes all duplicate vertices from the object mesh."""

    bpy.context.view_layer.objects.active = object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()
 
    
def recalcNormals(object : bpy.types.Mesh) -> None:
    """Make all normals of the mesh point outwards."""

    bpy.context.view_layer.objects.active = object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside = False)
    bpy.ops.object.editmode_toggle()


def enableSmoothShading(object : bpy.types.Mesh) -> None:
    """Enables smooth shading for the object mesh."""

    bpy.context.view_layer.objects.active = object
    mesh = bpy.context.object.data
    for f in mesh.polygons:
        f.use_smooth = True


def disableSmoothShading(object : bpy.types.Mesh) -> None:
    """Disables smooth shading for the object mesh."""

    bpy.context.view_layer.objects.active = object
    mesh = bpy.context.object.data
    for f in mesh.polygons:
        f.use_smooth = False


def remesh(object : bpy.types.Mesh, voxel_size : float = 0.1, adaptivity : float = 0.05) -> None:
    """Remeshes the object based on the current shape.

    Params:
        object: The target mesh.
        voxel_size: Size of the voxels in the new mesh.
        adaptivity: Adaptive voxel size.
    """

    mod = object.modifiers.new("remesh", type = "REMESH")
    mod.mode = "VOXEL"
    mod.voxel_size = voxel_size
    mod.adaptivity = adaptivity
    mod.use_smooth_shade = True

    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "remesh")


def bend(object : bpy.types.Mesh,
         origin : bpy.types.Mesh,
         angle : float,
         l_limit : float = 0.0,
         u_limit : float = 1.0,
         axis : str = "Z") -> None:
    """Bend the object around a point.

    Params:
        object: The target object to bend.
        origin: The object to bend the target around.
        angle:  The bending angle in radians.
        l_limit: The part of the object to start the bending from (0.0-1.0)
        u_limit: The part of the object to stop the bending at (0.0-1.0)
        axis: Axis to bend around ("X", "Y", or "Z")
    """

    mod = object.modifiers.new("bend", type = "SIMPLE_DEFORM")
    mod.deform_method = "BEND"
    mod.angle = angle
    mod.origin = origin
    mod.deform_axis = axis
    mod.limits[0] = l_limit
    mod.limits[1] = u_limit

    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "bend")