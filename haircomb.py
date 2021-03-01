import bpy
import bmesh
import math
import operators as op
import utils

EPSILON = 1E-6

#PARAMS (mm)
width = 135.5
thickness = 3.0
base_height = 10.0
side_width = 7.0
tooth_height = 20.0
tooth_count = 40

#DERIVED PARAMS
#general
height = base_height + tooth_height
radius = thickness/10.0    #standard rounding for edges
#base/head params
base_radius = base_height
#side params
side_height = height - base_height
side_thickness = thickness
side_radius = 0.85*side_width
#teeth params
tooth_width = (width - 2*side_width)/(2*tooth_count + 1)
tooth_spacing = tooth_width
#middle part params
middle_width = width
middle_thickness = thickness/3.0
middle_height = base_height/3.0

def createBase():
    bpy.ops.mesh.primitive_cube_add(location = (base_height/2.0, 0.0, thickness/2.0), 
                                    scale = (base_height, width, thickness))
    base = bpy.context.object
    #round the 2 vertical edges
    top_left = base.vertex_groups.new(name = "topleft")
    top_left.add([0, 1], 1.0, "REPLACE")
    top_right = base.vertex_groups.new(name = "topright")
    top_right.add([2, 3], 1.0, "REPLACE")
    op.roundEdges(base, "topleft", base_radius, 10)
    op.roundEdges(base, "topright", base_radius, 10)
    return base

def createSide():
    bpy.ops.mesh.primitive_cube_add(scale = (tooth_height/2.5, side_width, thickness))
    side = bpy.context.object
    side.scale[0] = 2.5 #this is for the uneven beveling later
    #round the 2 vertical edges
    #round left edge
    l_edge = side.vertex_groups.new(name = "l_edge")
    l_edge.add([4, 5], 1.0, "REPLACE")
    op.roundEdges(side, "l_edge", side_radius, 10)
    #round right edge
    r_edge = side.vertex_groups.new(name = "r_edge")
    r_edge.add([4, 5], 1.0, "REPLACE")
    op.roundEdges(side, "r_edge", radius)
    return side

def createMiddle():
    scale_factor = 6.0 #for uneven rounding
    bpy.ops.mesh.primitive_cube_add(location = (base_height + middle_height/2.0,
                                                0.0,
                                                thickness/2.0),
                                    scale = (middle_height/scale_factor,
                                             middle_width,
                                             middle_thickness)) #top
    middle = bpy.context.object
    middle.scale[0] = scale_factor
    verts = middle.vertex_groups.new(name = "edges")
    verts.add([4, 6, 5, 7], 1.0, "REPLACE")
    op.roundEdges(middle, "edges", thickness/6.0)
    return middle

def createTooth():
    #create teeth
    bpy.ops.mesh.primitive_cone_add(scale = (0.9*thickness/2.0,
                                             1.0,
                                             1.1*tooth_height),
                                    radius1 = 1.25*tooth_width,
                                    radius2 = 0.75*tooth_width,
                                    vertices = 20)
    tooth = bpy.context.object
    #select top edge
    top = tooth.vertex_groups.new(name = "top")
    for vert in tooth.data.vertices:
        #print(vert.co.z)
        if (vert.co.z + EPSILON >= 1.1*tooth_height/2.0):
            top.add([vert.index], 1.0, "ADD")
    #round top edge
    op.roundEdges(tooth, "top", radius)
    return tooth

def createHaircomb():
    #base
    base = createBase()
    #left side
    side = createSide()
    bpy.context.view_layer.objects.active = side
    bpy.ops.transform.translate(value = (base_height + tooth_height/2.0,
                                         -width/2.0 + side_width/2.0,
                                         thickness/2.0))
    op.exactMerge(base, side)
    #right side
    bpy.ops.transform.translate(value = (0.0, width-side_width, 0.0))
    bpy.ops.transform.rotate(value = math.pi, orient_axis = "X")
    op.exactMerge(base, side)
    bpy.data.objects.remove(side)
    #round horizontal edges
    top = base.vertex_groups.new(name = "top")
    bottom = base.vertex_groups.new(name = "bottom")
    for vert in base.data.vertices:
        #print(vert.co.z)
        if (vert.co.z - EPSILON <= -thickness/2.0):
            bottom.add([vert.index], 1.0, "ADD")
        elif (vert.co.z + EPSILON >= thickness/2.0):
            top.add([vert.index], 1.0, "ADD")
        else:
            continue
    op.roundEdges(base, "top", radius)
    op.roundEdges(base, "bottom", radius)
    #teeth
    tooth = createTooth()
    #move into pos
    bpy.ops.transform.rotate(value = 90.0*math.pi/180.0, orient_axis = "Y")
    bpy.ops.transform.translate(value = (base_height + (1.0/1.1)*tooth_height/2.0,
                                         -width/2.0 + side_width + tooth_spacing + tooth_width/2.0,
                                         thickness/2.0))
    for i in range(tooth_count):
        op.fastMerge(base, tooth)
        #move to next teeth position
        bpy.context.view_layer.objects.active = tooth
        bpy.ops.transform.translate(value = (0.0, tooth_spacing + tooth_width, 0.0))
    bpy.data.objects.remove(tooth)

    #smooth shading
    utils.enableSmoothShading(base)

    #middle
    middle = createMiddle()
    op.fastMerge(base, middle)
    bpy.data.objects.remove(middle)
    return base