import bpy

def exactMerge(target, object):
    mod = target.modifiers.new("merge", type = "BOOLEAN")
    mod.operation = "UNION"
    mod.solver = "EXACT"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "merge")
    
def fastMerge(target, object):
    mod = target.modifiers.new("fmerge", type = "BOOLEAN")
    mod.operation = "UNION"
    mod.solver = "FAST"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "fmerge")
    
def cut(target, object):
    mod = target.modifiers.new("cut", type = "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "cut")

def intersect(target, object):
    mod = target.modifiers.new("and", type = "BOOLEAN")
    mod.operation = "INTERSECT"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "and")
    
def roundEdges(object, vgroup, radius, segments = 5):
    mod = object.modifiers.new("bevel", type = "BEVEL")
    mod.limit_method = "VGROUP"
    mod.vertex_group = vgroup
    mod.width = radius
    mod.segments = segments
    mod.use_clamp_overlap = True
    mod.miter_outer = "MITER_ARC"
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "bevel")
    
def roundSharpEdges(object, radius, segments = 5, angle = 60):
    mod = object.modifiers.new("beveL", type = "BEVEL")
    mod.limit_method = "ANGLE"
    mod.angle_limit = angle * math.pi / 180.0
    mod.width = radius
    mod.segments = segments
    mod.use_clamp_overlap = True
    mod.miter_outer = "MITER_ARC"
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "bevel")
    
def chamferEdges(object, vgroup, radius):
    mod = object.modifiers.new("chamfer", type = "BEVEL")
    mod.limit_method = "VGROUP"
    mod.vertex_group = vgroup
    mod.width = radius
    mod.segments = 1
    mod.use_clamp_overlap = False
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "chamfer")

def removeDuplicateVerts(object):
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()
    
def recalcNormals(object):
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.editmode_toggle()

def enableSmoothShading(object):
    bpy.context.view_layer.objects.active = object
    mesh = bpy.context.object.data
    for f in mesh.polygons:
        f.use_smooth = True

def disableSmoothShading(object):
    bpy.context.view_layer.objects.active = object
    mesh = bpy.context.object.data
    for f in mesh.polygons:
        f.use_smooth = False

def remesh(object, voxel_size = 0.1):
    mod = object.modifiers.new("remesh", type = "REMESH")
    mod.mode = "VOXEL"
    mod.voxel_size = 0.1
    mod.adaptivity = 0.0
    mod.use_smooth_shade = True
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "remesh")