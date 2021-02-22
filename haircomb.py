import bpy, bmesh
import math

def init():
    #delete everything
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    #set units to mm
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"

def union(target, object):
    mod = target.modifiers.new("add", type="BOOLEAN")
    mod.operation = "UNION"
    mod.object = object
    bpy.context.view_layer.objects.active = target #the modifier is applied to the active object
    bpy.ops.object.modifier_apply(modifier = "add")
    
def difference(target, object):
    mod = target.modifiers.new("sub", type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "sub")

def intersect(target, object):
    mod = target.modifiers.new("and", type="BOOLEAN")
    mod.operation = "INTERSECT"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "and")
    
def bevel(object, vgroup, radius):
    mod = object.modifiers.new("bevel", type="BEVEL")
    mod.limit_method = "VGROUP"
    mod.vertex_group = vgroup
    mod.width = radius
    mod.segments = 15
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "bevel")

#params
width = 135.5
height = 30.0
thickness = 3.0

base_height = 10.0

side_width = 7.0
side_radius = 7.0

tooth_height = 20.0
tooth_width = 1.5
tooth_spacing = 1.5
tooth_count = 40

init()

#create object
#base
bpy.ops.mesh.primitive_cube_add(location=(base_height/2.0, 0.0, 0.0), scale=(base_height, width, thickness))
base = bpy.context.object
#add modify base shape here

#2 sides #left side
bpy.ops.mesh.primitive_cube_add(scale=(tooth_height/2.5, side_width, thickness))
side = bpy.context.object
side.scale[0] = 2.5 #this is for the uneven beveling later
bpy.ops.transform.translate(value=(base_height+tooth_height/2.0, -width/2.0+side_width/2.0, 0.0))
#bevel left edge
l_edge = side.vertex_groups.new(name="l_edge")
l_edge.add([4,5], 1.0, "REPLACE")
bevel(side,"l_edge",side_radius)

union(base, side)

#right side
bpy.ops.transform.translate(value=(0.0,width-side_width,0.0))
bpy.ops.transform.rotate(value=math.pi,orient_axis="X")
union(base, side)
bpy.data.objects.remove(side)

#add teeth
#create teeth
bpy.ops.mesh.primitive_cube_add(scale=(tooth_height,tooth_width,thickness))
tooth = bpy.context.object
bpy.ops.transform.translate(value=(base_height+tooth_height/2.0,-width/2.0+side_width+tooth_spacing+tooth_width/2.0,0.0))
#add modify tooth shape here
for i in range(tooth_count):
    union(base, tooth)
    
    bpy.context.view_layer.objects.active = tooth
    bpy.ops.transform.translate(value=(0.0,tooth_spacing+tooth_width,0.0))
bpy.data.objects.remove(tooth)