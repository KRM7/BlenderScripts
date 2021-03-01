import bpy

def removeDuplicates(object):
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