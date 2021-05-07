"""Blender 2.91

Haircomb class to create the object in blender.
"""

project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"
import sys
sys.path.append(project_path)

import bpy, mathutils
import math, random
from copy import deepcopy
from typing import List
import numpy as np
import operators as op
import utils, globals

class Haircomb:
    __EPSILON = 1E-6

    def __init__(self,
                 width : float = 135.5,
                 thickness : float = 3.0,
                 base_height : float = 10.0,
                 side_width : float = 7.0,
                 tooth_height : float = 20.0,
                 tooth_count : int = 46,
                 missing_teeth : bool = False,
                 bent_teeth : bool = False,
                 warping : bool = False,
                 ejector_marks : int = 0):
        #set parameters (mm)
        self.width = width                  #overall width of haircomb
        self.thickness = thickness          #overall thickness of haircomb
        self.base_height = base_height      #height of the base/head part
        self.side_width = side_width        #width of 1 of the 2 side parts
        self.tooth_height = tooth_height    #the length of the teeth
        self.tooth_count = tooth_count      #number of teeth of the haircomb
        self.missing_teeth = missing_teeth
        self.bent_teeth = bent_teeth
        self.warping = warping
        self.ejector_marks = ejector_marks
        #derived parameters
        self.__calcDerivedParams()

    def __calcDerivedParams(self) -> None:
        """Calculates all other derived parameters of the haircomb from the init parameters."""

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


    def createHaircomb(self) -> None:
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

        op.roundEdges(object = self.base, edges = "topleft", radius = self.base_radius, segments = 10)
        op.roundEdges(object = self.base, edges = "topright", radius = self.base_radius, segments = 10)
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
        op.roundEdges(object = side, edges = "outer_edge", radius = self.side_radius, segments = 10)

        verts = side.vertex_groups.new(name = "inner_edge")
        verts.add(index = [4, 5], weight = 1, type = "REPLACE")
        op.roundEdges(object = side, edges = "inner_edge", radius = self.general_radius)

        #add side parts
        bpy.context.view_layer.objects.active = side
        #move into pos for left side
        side.location += mathutils.Vector((self.side_height/2 + self.base_height,
                                           self.side_width/2 - self.width/2,
                                           self.thickness/2))
        op.merge(self.base, side, solver = "EXACT")

        #move into pos for right side
        side.location[1] += self.width - self.side_width
        bpy.ops.transform.rotate(value = math.pi, orient_axis = "X")    #mirror
        op.merge(self.base, side, solver = "EXACT")

        bpy.data.objects.remove(side)
        #endregion SIDE_PARTS


        #region EDGES
        #round horizontal edges
        top = self.base.vertex_groups.new(name = "top")
        bottom = self.base.vertex_groups.new(name = "bottom")
        for vert in self.base.data.vertices:
            if (vert.co.z - self.__EPSILON <= -self.thickness/2):
                bottom.add(index = [vert.index], weight = 1, type = "ADD")
            elif (vert.co.z + self.__EPSILON >= self.thickness/2):
                top.add(index = [vert.index], weight = 1, type = "ADD")
            else:
                continue

        op.roundEdges(object = self.base, edges = "top", radius = self.general_radius, clamp_overlap = False)
        op.roundEdges(object = self.base, edges = "bottom", radius = self.general_radius, clamp_overlap = False)
        #endregion EDGES
        

        #region TEETH

        #create the tooth object
        radius_scaling_factor = 1.5     # >1 scale between r_x/r_y
        height_scaling_factor = 1.1     # >1 so the teeth reaches into the base part (for the union operator)
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
            if (vert.co.z + self.__EPSILON >= height_scaling_factor*self.tooth_height/2):
                verts.add(index = [vert.index], weight = 1, type = "ADD")
        op.roundEdges(object = tooth, edges = "tip", radius = self.general_radius)

        #rotate and move the teeth into pos
        tooth.rotation_euler = mathutils.Vector((0, 90*math.pi/180, 0))
        tooth.location += mathutils.Vector((self.base_height + self.tooth_height/2 - (height_scaling_factor - 1)*self.tooth_height/2,
                                            self.tooth_width/2 - self.width/2 + self.side_width + self.tooth_spacing,
                                            self.thickness/2))
        tooth_pos = deepcopy(tooth.location)

        #region BENT_TEETH

        #params for bent teeth
        bent_idx = []
        if self.bent_teeth:
            bent_num = random.randrange(1, 21)
            bent_start = random.randrange(0, self.tooth_count - bent_num + 1)
            bent_idx = range(bent_start, bent_start + bent_num)     #indexes of bent teeth

            bend_dir = math.pi/180 * random.uniform(-20.0, 200.0)

            origin_p = random.uniform(0.2, 0.6)

            angle = random.uniform(6.0, 15.0)*math.pi/180
            angles = utils.calcAngles(count = bent_num, indexes = bent_idx, angle = angle)

            #create origin for bending
            bpy.ops.object.empty_add(type = "PLAIN_AXES")
            axis = bpy.context.object
        #endregion BENT_TEETH

        #region MISSING_TEETH

        #params for missing teeth
        missing_idx = []
        if self.missing_teeth:
            missing_num = min(np.random.geometric(0.2), self.tooth_count)       #number of missing teeth
            missing_idx = random.sample(range(self.tooth_count), missing_num)   #indexes of missing teeth

            #create cutter for missing teeth
            bpy.ops.mesh.primitive_cube_add(scale = (self.tooth_height, 1.5*self.tooth_width, 1.5*self.thickness))
            cutter = bpy.context.object
            cutter.location += mathutils.Vector((self.tooth_height/2 + self.base_height + self.middle_height + self.tooth_height/30,
                                                 tooth_pos[1],
                                                 tooth_pos[2]))
            cutter_base_x = cutter.location[0]
        #endregion MISSING_TEETH
        
        #add all of the teeth
        for i in range(self.tooth_count):
            if (i in bent_idx) and not (i in missing_idx): #bent teeth
                bpy.context.view_layer.objects.active = tooth
                bpy.ops.object.select_all(action = "DESELECT")
                tooth.select_set(1)
                bpy.ops.object.duplicate()
                duplicate_tooth = bpy.context.object

                origin_temp = utils.clamp(origin_p + random.uniform(-0.1, 0.1), 0.2, 0.6)
                origin_x = (origin_temp - 0.5)*height_scaling_factor*self.tooth_height
                l_limit = origin_temp
                u_limit = origin_temp + 0.15 + random.uniform(0.0, 0.1)

                axis.location = tooth.location + mathutils.Vector((origin_x, 0.0, 0.0))
                axis.rotation_euler[0] = bend_dir + random.uniform(-10*math.pi/180, 10*math.pi/180)
                
                op.remesh(object = duplicate_tooth, voxel_size = 0.25, adaptivity = 0.0)
                op.bend(object = duplicate_tooth, origin = axis, angle = angles[i], l_limit = l_limit, u_limit = u_limit)
                op.merge(self.base, duplicate_tooth, solver = "EXACT")

                bpy.context.view_layer.objects.active = duplicate_tooth
                bpy.ops.object.delete()

            elif (i in missing_idx): #broken teeth
                bpy.context.view_layer.objects.active = tooth
                bpy.ops.object.select_all(action = "DESELECT")
                tooth.select_set(1)
                bpy.ops.object.duplicate()
                duplicate_tooth = bpy.context.object

                #cut copied tooth
                cutter.location[0] += random.uniform(0.0, self.tooth_height/5)
                vert_base_x = cutter.data.vertices[0].co.x
                for v_i in range(4):
                    cutter.data.vertices[v_i].co.x += random.uniform(-self.tooth_height/40, self.tooth_height/40)

                op.cut(duplicate_tooth, cutter, solver = "FAST")

                for v_i in range(4):
                    cutter.data.vertices[v_i].co.x = vert_base_x
                cutter.location[0] = cutter_base_x

                op.merge(self.base, duplicate_tooth, solver = "FAST")

                bpy.context.view_layer.objects.active = duplicate_tooth
                bpy.ops.object.delete()

            else:   #normal teeth
                op.merge(self.base, tooth, solver = "FAST")

            #move to next teeth position
            tooth.location[1] += self.tooth_spacing + self.tooth_width
            if self.missing_teeth:
                cutter.location[1] = tooth.location[1]
        
        bpy.data.objects.remove(tooth)
        if self.missing_teeth:
            bpy.data.objects.remove(cutter)
        if self.bent_teeth:
            bpy.data.objects.remove(axis)
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
        op.roundEdges(object = middle, edges = "front", radius = self.middle_thickness/2)

        op.merge(self.base, middle, solver = "FAST")
        bpy.data.objects.remove(middle)
        #endregion MIDDLE_PART


        #region EJECTOR_MARKS

        if (self.ejector_marks > 0):
            #params
            ejector_radius = 0.3*self.base_height   #min: 0.15*self.base_height / max: 0.5*self.base_height
            ejector_depth = 0.1                     #cutting depth
            ejector_pos_y = 0.37*self.width         #y_min = +-0.15*self.width, y_max: +-0.4*self.width
        
            #create ejector pin for cutting
            bpy.ops.mesh.primitive_cylinder_add(radius = ejector_radius, depth = 5*ejector_depth)
            ejector = bpy.context.object
            ejector.location = mathutils.Vector((self.base_height/2, 0.0, self.thickness + 1.5*ejector_depth))

            #create ejector marks
            if (self.ejector_marks == 3):
                op.cut(self.base, ejector, solver = "FAST")
            elif (self.ejector_marks == 2):
                pass
            else:
                raise ValueError("Invalid num of ejector marks.")

            ejector.location[1] = ejector_pos_y
            op.cut(self.base, ejector, solver = "FAST")
            ejector.location[1] = -ejector_pos_y
            op.cut(self.base, ejector, solver = "FAST")

            #delete ejector
            bpy.data.objects.remove(ejector)

        #endregion EJECTOR_MARKS


        #remesh
        op.remesh(self.base, voxel_size = 0.1)

        #region WARPING
        if self.warping:
            bpy.ops.object.empty_add(type = "PLAIN_AXES", location = (0.0, 0.0, 0.0), rotation = (90*math.pi/180, 0.0, 0.0))
            axis = bpy.context.object

            angle = random.uniform(6.0, 14.0)*math.pi/180
            l_limit = random.uniform(0.0, 0.5)
            u_limit = random.uniform(max(0.5, l_limit+0.5), 1.0)

            op.bend(object = self.base, origin = axis, angle = angle, l_limit = l_limit, u_limit = u_limit, axis = "X")

            bpy.data.objects.remove(axis)
        #endregion WARPING

        #add material
        self.mat = bpy.data.materials.new(name = "HaircombMaterial")
        self.base.data.materials.append(self.mat)


    def getObject(self) -> bpy.types.Object:
        return self.base


    def getMaterial(self) -> bpy.types.Material:
        return self.mat


    def getBoundingBox(self) -> List[float]:
        """Returns a list containing the vertices of the objects bounding box.)"""

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


#test
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete()
utils.removeMeshes()

#CREATE GROUND OBJECT
bpy.ops.mesh.primitive_plane_add(size = 20000)

#CREATE OBJECT
hc = Haircomb(missing_teeth = True, bent_teeth = True, warping = True, ejector_marks = 3)
hc.createHaircomb()