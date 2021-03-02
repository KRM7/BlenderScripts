import bpy
import math
import operators as op
import utils

class Haircomb:
    EPSILON = 1E-6

    def __init__(self,
                 width = 135.5,
                 thickness = 3.0,
                 base_height = 10.0,
                 side_width = 7.0,
                 tooth_height = 20.0,
                 tooth_count = 40):
        #set parameters (mm)
        self.width = width                  #overall width of haircomb
        self.thickness = thickness          #overall thickness of haircomb
        self.base_height = base_height      #height of the base/head part
        self.side_width = side_width        #width of 1 of the 2 side parts
        self.tooth_height = tooth_height    #the length of the teeth
        self.tooth_count = tooth_count      #number of teeth of the haircomb
        #derived parameters
        self.height = base_height + tooth_height    #overall height of the haircomb
        self.radius = thickness/5.0                 #standard rounding for most edges
        self.base_radius = base_height              #radius of upper corners of the base/head
        self.side_height = tooth_height             #length of the 2 side parts
        self.side_thickness = thickness             #thickness of the 2 side parts
        self.side_radius = 0.85*side_width          #radius of the rounding on the 2 sides
        self.tooth_width = (width - 2*side_width)/(2*tooth_count + 1)   #width of one tooth
        self.tooth_spacing = self.tooth_width       #distance between 2 teeth
        self.middle_width = width                   #width of middle part (between the teeth)
        self.middle_thickness = thickness/3.0       #thickness of the middle part
        self.middle_height = base_height/3.0        #height of the middle part

    def __createBase(self):
        #create object
        bpy.ops.mesh.primitive_cube_add(location = (self.base_height/2.0, 0.0, self.thickness/2.0), 
                                        scale = (self.base_height, self.width, self.thickness))
        base = bpy.context.object

        #round the 2 vertical edges
        verts = base.vertex_groups.new(name = "topleft")
        verts.add([0, 1], 1.0, "REPLACE")
        verts = base.vertex_groups.new(name = "topright")
        verts.add([2, 3], 1.0, "REPLACE")
        op.roundEdges(base, "topleft", self.base_radius, 10)
        op.roundEdges(base, "topright", self.base_radius, 10)

        return base

    def __createSide(self):
        #create object
        scaling_factor = 2.5 #this is for the uneven beveling later
        bpy.ops.mesh.primitive_cube_add(scale = (self.side_height/scaling_factor, self.side_width, self.thickness))
        side = bpy.context.object
        side.scale[0] = scaling_factor

        #round the 2 vertical edges
        #left
        verts = side.vertex_groups.new(name = "left_edge")
        verts.add([4, 5], 1.0, "REPLACE")
        op.roundEdges(side, "left_edge", self.side_radius, 10)
        #right
        verts = side.vertex_groups.new(name = "right_edge")
        verts.add([4, 5], 1.0, "REPLACE")
        op.roundEdges(side, "right_edge", self.radius)

        return side

    def __createMiddle(self):
        #create object
        scaling_factor = 6.0 #for uneven rounding
        bpy.ops.mesh.primitive_cube_add(location = (self.base_height + self.middle_height/2.0,
                                                    0.0,
                                                    self.thickness/2.0),
                                        scale = (self.middle_height/scaling_factor,
                                                 self.middle_width,
                                                 self.middle_thickness))
        middle = bpy.context.object
        middle.scale[0] = scaling_factor

        #round the edges
        verts = middle.vertex_groups.new(name = "front")
        verts.add([4, 6, 5, 7], 1.0, "REPLACE")
        op.roundEdges(middle, "front", self.middle_thickness/2.0)

        return middle

    def __createTooth(self):
        #create object
        bpy.ops.mesh.primitive_cone_add(scale = (0.9*self.thickness/2.0,
                                                 1.0,
                                                 1.1*self.tooth_height),
                                        radius1 = 1.25*self.tooth_width,
                                        radius2 = 0.75*self.tooth_width,
                                        vertices = 20)
        tooth = bpy.context.object

        #round top edge
        verts = tooth.vertex_groups.new(name = "top")
        for vert in tooth.data.vertices:
            if (vert.co.z + self.EPSILON >= 1.1*self.tooth_height/2.0):
                verts.add([vert.index], 1.0, "ADD")
        op.roundEdges(tooth, "top", self.radius)

        return tooth

    def createHaircomb(self):
        #add base part
        self.base = self.__createBase()

        #add side parts
        #left side
        side = self.__createSide()
        bpy.context.view_layer.objects.active = side
        bpy.ops.transform.translate(value = (self.base_height + self.side_height/2.0,
                                             -self.width/2.0 + self.side_width/2.0,
                                             self.thickness/2.0))
        op.exactMerge(self.base, side)
        #right side
        bpy.ops.transform.translate(value = (0.0, self.width - self.side_width, 0.0))
        bpy.ops.transform.rotate(value = math.pi, orient_axis = "X")
        op.exactMerge(self.base, side)
        bpy.data.objects.remove(side)

        #round horizontal edges
        top = self.base.vertex_groups.new(name = "top")
        bottom = self.base.vertex_groups.new(name = "bottom")
        for vert in self.base.data.vertices:
            if (vert.co.z - self.EPSILON <= -self.thickness/2.0):
                bottom.add([vert.index], 1.0, "ADD")
            elif (vert.co.z + self.EPSILON >= self.thickness/2.0):
                top.add([vert.index], 1.0, "ADD")
            else:
                continue
        op.roundEdges(self.base, "top", self.radius)
        op.roundEdges(self.base, "bottom", self.radius)
        
        #add teeth
        tooth = self.__createTooth()
        #move into pos
        bpy.ops.transform.rotate(value = 90.0*math.pi/180.0, orient_axis = "Y")
        bpy.ops.transform.translate(value = (self.base_height + (1.0/1.1)*self.tooth_height/2.0,
                                             -self.width/2.0 + self.side_width + self.tooth_spacing + self.tooth_width/2.0,
                                             self.thickness/2.0))
        for i in range(self.tooth_count):
            op.fastMerge(self.base, tooth)
            #move to next teeth position
            bpy.context.view_layer.objects.active = tooth
            bpy.ops.transform.translate(value = (0.0, self.tooth_spacing + self.tooth_width, 0.0))
        bpy.data.objects.remove(tooth)

        #enable smooth shading
        utils.enableSmoothShading(self.base)

        #add middle part
        middle = self.__createMiddle()
        op.fastMerge(self.base, middle)
        bpy.data.objects.remove(middle)

        #add material
        self.mat = bpy.data.materials.new(name = "Mat")
        self.base.data.materials.append(self.mat)

    def getMaterial(self):
        return self.mat