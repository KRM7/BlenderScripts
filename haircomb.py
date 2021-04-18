project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"
import sys
sys.path.append(project_path)

import bpy
import mathutils
import math
import random
import numpy as np
import operators as op
import utils
from copy import deepcopy

class Haircomb:
    EPSILON = 1E-6

    def __init__(self,
                 width = 135.5,
                 thickness = 3.0,
                 base_height = 10.0,
                 side_width = 7.0,
                 tooth_height = 20.0,
                 tooth_count = 46,
                 missing_teeth = False,
                 bent_teeth = False):
        #set parameters (mm)
        self.width = width                  #overall width of haircomb
        self.thickness = thickness          #overall thickness of haircomb
        self.base_height = base_height      #height of the base/head part
        self.side_width = side_width        #width of 1 of the 2 side parts
        self.tooth_height = tooth_height    #the length of the teeth
        self.tooth_count = tooth_count      #number of teeth of the haircomb
        self.missing_teeth = missing_teeth
        self.bent_teeth = bent_teeth
        #derived parameters
        self.__calcDerivedParams()

    def __calcDerivedParams(self):
        self.height = self.base_height + self.tooth_height  #overall height of the haircomb
        self.general_radius = self.thickness/5              #standard rounding for most edges
        self.base_radius = self.base_height                 #radius of upper corners of the base/head
        self.side_height = self.tooth_height                #length of the 2 side parts
        self.side_thickness = self.thickness                #thickness of the 2 side parts
        self.side_radius = 0.85*self.side_width             #radius of the rounding on the 2 sides
        self.tooth_width = (self.width - 2*self.side_width)/(2*self.tooth_count + 1)   #width of one tooth
        self.tooth_spacing = self.tooth_width               #distance between 2 teeth
        self.middle_width = self.width                      #width of middle part (between the teeth)
        self.middle_thickness = self.thickness/3            #thickness of the middle part
        self.middle_height = self.base_height/3             #height of the middle part

    def createHaircomb(self):
        self.__calcDerivedParams()

        #region BASE_PART

        #create the base object
        bpy.ops.mesh.primitive_cube_add(location = (self.base_height/2, 0, self.thickness/2), 
                                        scale = (self.base_height, self.width, self.thickness))
        self.base = bpy.context.object

        #round the 2 vertical edges of the base part
        verts = self.base.vertex_groups.new(name = "topleft")
        verts.add(index = [0, 1], weight = 1, type = "REPLACE")

        verts = self.base.vertex_groups.new(name = "topright")
        verts.add(index = [2, 3], weight = 1, type = "REPLACE")

        op.roundEdges(object = self.base, vgroup = "topleft", radius = self.base_radius, segments = 10)
        op.roundEdges(object = self.base, vgroup = "topright", radius = self.base_radius, segments = 10)
        #endregion BASE_PART


        #region SIDE_PARTS

        #create the side object
        scaling_factor = 2.5    #used for the uneven beveling later
        bpy.ops.mesh.primitive_cube_add(scale = (self.side_height/scaling_factor, self.side_width, self.thickness))
        side = bpy.context.object
        side.scale[0] = scaling_factor

        #round the 2 vertical edges of the side part
        verts = side.vertex_groups.new(name = "outer_edge")
        verts.add(index = [4, 5], weight = 1, type = "REPLACE")
        op.roundEdges(object = side, vgroup = "outer_edge", radius = self.side_radius, segments = 10)

        verts = side.vertex_groups.new(name = "inner_edge")
        verts.add(index = [4, 5], weight = 1, type = "REPLACE")
        op.roundEdges(object = side, vgroup = "inner_edge", radius = self.general_radius)

        #add side parts
        bpy.context.view_layer.objects.active = side
        #move into pos for left side
        side.location += mathutils.Vector((self.side_height/2 + self.base_height,
                                           self.side_width/2 - self.width/2,
                                           self.thickness/2))
        op.exactMerge(self.base, side)

        #move into pos for right side
        side.location[1] += self.width - self.side_width
        bpy.ops.transform.rotate(value = math.pi, orient_axis = "X")    #mirror
        op.exactMerge(self.base, side)

        bpy.data.objects.remove(side)
        #endregion SIDE_PARTS


        #region EDGES
        #round horizontal edges
        top = self.base.vertex_groups.new(name = "top")
        bottom = self.base.vertex_groups.new(name = "bottom")
        for vert in self.base.data.vertices:
            if (vert.co.z - self.EPSILON <= -self.thickness/2):
                bottom.add(index = [vert.index], weight = 1, type = "ADD")
            elif (vert.co.z + self.EPSILON >= self.thickness/2):
                top.add(index = [vert.index], weight = 1, type = "ADD")
            else:
                continue

        op.roundEdges(object = self.base, vgroup = "top", radius = self.general_radius)
        op.roundEdges(object = self.base, vgroup = "bottom", radius = self.general_radius)
        #endregion EDGES
        

        #region TEETH

        #create the tooth object
        radius_scaling_factor = 1.5 # >1 scale between r_x/r_y
        height_scaling_factor = 1.1 # >1 so the teeth reaches into the base part (for the union operator)
        bpy.ops.mesh.primitive_cone_add(radius1 = self.thickness/radius_scaling_factor,
                                        radius2 = 0.75*self.thickness/2,
                                        vertices = 20,
                                        scale = (radius_scaling_factor,
                                                 1,
                                                 height_scaling_factor*self.tooth_height))
        tooth = bpy.context.object

        #round the edges on the tip of the teeth
        verts = tooth.vertex_groups.new(name = "tip")
        for vert in tooth.data.vertices:
            if (vert.co.z + self.EPSILON >= height_scaling_factor*self.tooth_height/2):
                verts.add(index = [vert.index], weight = 1, type = "ADD")
        op.roundEdges(object = tooth, vgroup = "tip", radius = self.general_radius)

        #rotate and move the teeth into pos
        tooth.rotation_euler = mathutils.Vector((0, 90*math.pi/180, 0))
        tooth.location += mathutils.Vector((self.base_height + self.tooth_height/2 - (height_scaling_factor - 1)*self.tooth_height/2,
                                            self.tooth_width/2 - self.width/2 + self.side_width + self.tooth_spacing,
                                            self.thickness/2))
        tooth_pos = deepcopy(tooth.location)

        #params for bent teeth
        bent_num = min(np.random.geometric(0.1), 20)                    #number of bent teeth
        bent_start = random(range(0, self.tooth_count - bent_num + 1))  #index of first bent teeth

        #params for missing teeth
        missing_num = min(np.random.geometric(0.2), self.tooth_count)
        missing_idx = random.sample(range(self.tooth_count), missing_num)

        #create cutter for missing teeth
        bpy.ops.mesh.primitive_cube_add(scale = (self.tooth_height, 1.5*self.tooth_width, 1.5*self.thickness))
        cutter = bpy.context.object
        cutter.location += mathutils.Vector((self.tooth_height/2 + self.base_height + self.middle_height + self.tooth_height/30,
                                             tooth_pos[1],
                                             tooth_pos[2]))
        cutter_base_x = cutter.location[0]

        #add all of the teeth
        for i in range(self.tooth_count):
            op.fastMerge(self.base, tooth)
            
            #cut teeth if missing/broken
            if(self.missing_teeth and (i in missing_idx)):
                #randomize pos of cutter
                cutter.location[0] += random.uniform(0.0, self.tooth_height/5)
                for v_i in range(4):
                    cutter.data.vertices[v_i].co.x += random.uniform(-self.tooth_height/40, self.tooth_height/40)

                op.cut(self.base, cutter)

                #reset pos of cutter    #this breaks things for some reason
                #for v_i in range(4):
                #    cutter.data.vertices[v_i].co.x = cutter_base_x
                cutter.location[0] = cutter_base_x
           

            #move to next teeth position -> y   x .|-> y
            tooth.location[1] += self.tooth_spacing + self.tooth_width

            cutter.location[1] = tooth.location[1]
        
        bpy.data.objects.remove(tooth)
        bpy.data.objects.remove(cutter)
        #endregion TEETH


        #region MIDDLE_PART

        #create middle part
        scaling_factor = 6.0    #for the uneven rounding
        bpy.ops.mesh.primitive_cube_add(scale = (self.middle_height/scaling_factor,
                                                 self.middle_width,
                                                 self.middle_thickness))
        middle = bpy.context.object
        middle.location += mathutils.Vector((self.middle_height/2 + self.base_height,
                                             0,
                                             self.thickness/2))
        middle.scale[0] = scaling_factor

        #round the edges of the middle part
        verts = middle.vertex_groups.new(name = "front")
        verts.add(index = [4, 6, 5, 7], weight = 1, type = "REPLACE")
        op.roundEdges(object = middle, vgroup = "front", radius = self.middle_thickness/2)

        op.fastMerge(self.base, middle)
        bpy.data.objects.remove(middle)
        #endregion MIDDLE_PART

        #remesh
        op.remesh(self.base, voxel_size = 0.1)

        #add material
        self.mat = bpy.data.materials.new(name = "HaircombMaterial")
        self.base.data.materials.append(self.mat)


    def getObject(self):
        return self.base


    def getMaterial(self):
        return self.mat


    def getBoundingBox(self):
        return ( #this format is needed for a blender function (camera_fit_coords)
                -self.height/40,   -21/40*self.width,  self.thickness,  #x1, y1, z1
                -self.height/40,   -21/40*self.width,  0,               #x2, y2, z2 ...
                41/40*self.height, -21/40*self.width,  self.thickness,
                41/40*self.height, -21/40*self.width,  0,
                -self.height/40,    21/40*self.width,  self.thickness,
                -self.height/40,    21/40*self.width,  0,
                41/40*self.height,  21/40*self.width,  self.thickness,
                41/40*self.height,  21/40*self.width,  0                #x8, y8, z8
               )

#INIT
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete()
utils.removeMeshes()
utils.removeMaterials()
utils.removeLights()
utils.removeCameras()

#CREATE OBJECT
hc = Haircomb(missing_teeth=True)
hc.createHaircomb()