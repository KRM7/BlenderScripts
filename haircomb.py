import bpy, bmesh
import math
import time

EPSILON = 1E-6

def init():
    #delete everything
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()
    #set units to mm
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"

def merge(target, object):
    mod = target.modifiers.new("add", type = "BOOLEAN")
    mod.operation = "UNION"
    mod.solver = "EXACT"
    mod.object = object
    bpy.context.view_layer.objects.active = target #the modifier is applied to the active object
    bpy.ops.object.modifier_apply(modifier = "add")
    
def fastMerge(target, object):
    mod = target.modifiers.new("add", type = "BOOLEAN")
    mod.operation = "UNION"
    mod.solver = "FAST"
    mod.object = object
    bpy.context.view_layer.objects.active = target 
    bpy.ops.object.modifier_apply(modifier = "add")
    
def cut(target, object):
    mod = target.modifiers.new("sub", type = "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "sub")

def intersect(target, object):
    mod = target.modifiers.new("and", type = "BOOLEAN")
    mod.operation = "INTERSECT"
    mod.object = object
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier = "and")
    
def bevelEdges(object, vgroup, radius, segments = 5):
    mod = object.modifiers.new("bevel", type = "BEVEL")
    mod.limit_method = "VGROUP"
    mod.vertex_group = vgroup
    mod.width = radius
    mod.segments = segments
    mod.use_clamp_overlap = True
    mod.miter_outer = "MITER_ARC"
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.modifier_apply(modifier = "bevel")
    
def bevelSharpEdges(object, radius, segments = 5, angle = 60):
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
    

#PARAMS
#general params
width = 135.5
height = 30.0
thickness = 3.0
radius = 3.0    #standard rounding for edges

#base/head params
base_height = 10.0
base_radius = 10.0

#side part params
side_width = 7.0
side_radius = 6.0
#side_thickness = thickness
#side_height = tooth_height

#teeth parameters
tooth_height = 20.0
tooth_width = 1.5
tooth_spacing = 1.5
tooth_count = 40

start_time = time.time()
init()

#BASE/HEAD PART
bpy.ops.mesh.primitive_cube_add(location = (base_height/2.0, 0.0, thickness/2.0), 
                                scale = (base_height, width, thickness))
base = bpy.context.object
#round the 2 vertical edges
top_left = base.vertex_groups.new(name = "topleft")
top_left.add([0, 1], 1.0, "REPLACE")
top_right = base.vertex_groups.new(name = "topright")
top_right.add([2, 3], 1.0, "REPLACE")
bevelEdges(base, "topleft", base_radius, 10)
bevelEdges(base, "topright", base_radius, 10)


#ADD THE 2 SIDE PARTS
#left side
bpy.ops.mesh.primitive_cube_add(scale = (tooth_height/2.5, side_width, thickness))
side = bpy.context.object
side.scale[0] = 2.5 #this is for the uneven beveling later
bpy.ops.transform.translate(value = (base_height+tooth_height/2.0,
                                     -width/2.0+side_width/2.0,
                                     thickness/2.0))

#round the 2 vertical edges of the side part
#round left edge
l_edge = side.vertex_groups.new(name = "l_edge")
l_edge.add([4, 5], 1.0, "REPLACE")
bevelEdges(side, "l_edge", side_radius, 10)
#round right edge
r_edge = side.vertex_groups.new(name = "r_edge")
r_edge.add([4, 5], 1.0, "REPLACE")
bevelEdges(side, "r_edge", radius)

merge(base, side)

#right side
bpy.ops.transform.translate(value = (0.0, width-side_width, 0.0))
bpy.ops.transform.rotate(value = math.pi, orient_axis = "X")
merge(base, side)
bpy.data.objects.remove(side)

#round horizontal edges
top = base.vertex_groups.new(name = "top")
bottom = base.vertex_groups.new(name = "bottom")
for vert in base.data.vertices:
    #print(vert.co.z)
    if (vert.co.z - EPSILON <= -thickness/2.0):
        bottom.add([vert.index,], 1.0, "ADD")
    if (vert.co.z + EPSILON >= thickness/2.0):
        top.add([vert.index,], 1.0, "ADD")
bevelEdges(base, "top", radius)
bevelEdges(base, "bottom", radius)

#ADD TEETH
#create teeth
bpy.ops.mesh.primitive_cone_add(scale = (0.9*thickness/2.0, 1.0, 1.1*tooth_height),
                                radius1 = 1.25*tooth_width,
                                radius2 = 0.75*tooth_width,
                                vertices = 20)
tooth = bpy.context.object
#select top edge
top = tooth.vertex_groups.new(name = "top")
for vert in tooth.data.vertices:
    #print(vert.co.z)
    if (vert.co.z + EPSILON >= 1.1 * tooth_height / 2.0):
        top.add([vert.index], 1.0, "ADD")
#round top edge
bevelEdges(tooth, "top", radius)
#move into pos
bpy.ops.transform.rotate(value = 90.0*math.pi/180.0, orient_axis = "Y")
bpy.ops.transform.translate(value = (base_height+(1.0/1.1)*tooth_height/2.0,
                                     -width/2.0+side_width+tooth_spacing+tooth_width/2.0,
                                     thickness/2.0))
#add modify tooth shape here
for i in range(tooth_count):
    fastMerge(base, tooth)
    
    bpy.context.view_layer.objects.active = tooth
    bpy.ops.transform.translate(value = (0.0, tooth_spacing+tooth_width, 0.0))
bpy.data.objects.remove(tooth)


#MIDDLE PART
#NOTE: this part should be added last, otherwise fastMerge won't work properly, and
#exact merge will take 10+ seconds
bpy.ops.mesh.primitive_cube_add(location = (base_height+base_height/6.0, 0.0, thickness/2.0),
                                scale = (base_height/18.0, width, thickness/3.0)) #top
middle = bpy.context.object
middle.scale[0] = 6.0
verts = middle.vertex_groups.new(name = "edges")
verts.add([4, 6, 5, 7], 1.0, "REPLACE")
bevelEdges(middle, "edges", thickness/6.0)
fastMerge(base, middle)                              
bpy.data.objects.remove(middle)

print("%s seconds" % round((time.time() - start_time), 4))