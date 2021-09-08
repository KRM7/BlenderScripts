"""Blender 2.91

Haircomb class to create the object in blender.
"""

#project_path = "S:\\source\\image-generator"
#import sys
#sys.path.append(project_path)

import bpy, mathutils

import math
import random
from copy import deepcopy
from typing import List

import numpy as np
import operators as op
import utils


def calcAngles(count : int, indexes, angle : float) -> dict:
    """Calculates the angles for each of the bent teeth of the haircomb.

    Params:
        count: The number of bent teeth.
        indexes: The indexes of the bent teeth.
        angle: The max angle to bend the teeth by.
    Returns:
        Dict with indexes as keys and the bending angles as values (in radians).
    """

    angles = {}
    id_list = [*indexes]
    middle = int(count/2)
    
    # Calc bending angles with clamping to prevent clipping.
    for i in range(count):
        if i < middle:
            angles[id_list[i]] = min((5+3*i)*math.pi/180, angle)
        else:
            angles[id_list[i]] = min((5+3*(count-1 - i))*math.pi/180, angle)
        
        # Randomize slightly.
        if not ((i == 0) or (i == (count - 1))):
            angles[id_list[i]] += random.uniform(-1*math.pi/180, 1*math.pi/180)

    return angles


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
        # Set parameters (mm)
        self.width = width                  # Overall width of haircomb.
        self.thickness = thickness          # Overall thickness of haircomb.
        self.base_height = base_height      # Height of the base/head part.
        self.side_width = side_width        # Width of 1 of the 2 side parts.
        self.tooth_height = tooth_height    # The length of the teeth.
        self.tooth_count = tooth_count      # The number of teeth of the haircomb.
        # Defects
        self.missing_teeth = missing_teeth
        self.bent_teeth = bent_teeth
        self.warping = warping
        self.ejector_marks = ejector_marks
        # Derived parameters
        self.__calcDerivedParams()

    def __calcDerivedParams(self) -> None:
        """Calculates all other derived parameters of the haircomb from the init parameters."""

        self.height = self.base_height + self.tooth_height  # Overall height of the haircomb.
        self.general_radius = self.thickness/5              # Standard rounding for most edges.
        self.base_radius = self.base_height                 # Radius of upper corners of the base/head.
        self.side_height = self.tooth_height                # Length of the 2 side parts.
        self.side_thickness = self.thickness                # Thickness of the 2 side parts.
        self.side_radius = 0.85*self.side_width             # Radius of the rounding on the 2 side parts.
        self.tooth_width = (self.width - 2*self.side_width)/(2*self.tooth_count + 1)   # Width of one tooth.
        self.tooth_spacing = self.tooth_width               # Distance between 2 teeth.
        self.middle_width = self.width                      # Width of middle part (between the teeth).
        self.middle_thickness = self.thickness/3            # Thickness of the middle part.
        self.middle_height = self.base_height/3             # Height of the middle part.


    def createHaircomb(self) -> None:
        self.__calcDerivedParams()

        #region BASE_PART

        # Create the base object
        bpy.ops.mesh.primitive_cube_add(location = (self.base_height/2, 0, self.thickness/2), 
                                        scale = (self.base_height, self.width, self.thickness))
        self.base = bpy.context.object

        # Round the 2 vertical edges of the base part
        verts = self.base.vertex_groups.new(name = "topleft")
        verts.add(index = [0, 1], weight = 1, type = "REPLACE")

        verts = self.base.vertex_groups.new(name = "topright")
        verts.add(index = [2, 3], weight = 1, type = "REPLACE")

        op.roundEdges(object = self.base, edges = "topleft", radius = self.base_radius, segments = 10)
        op.roundEdges(object = self.base, edges = "topright", radius = self.base_radius, segments = 10)
        #endregion BASE_PART


        #region SIDE_PARTS

        # Create the side object
        scaling_factor = 2.5    # Used for the uneven beveling later
        bpy.ops.mesh.primitive_cube_add(scale = (self.side_height/scaling_factor, self.side_width, self.thickness))
        side = bpy.context.object
        side.scale[0] = scaling_factor

        # Round the 2 vertical edges of the side part
        verts = side.vertex_groups.new(name = "outer_edge")
        verts.add(index = [4, 5], weight = 1, type = "REPLACE")
        op.roundEdges(object = side, edges = "outer_edge", radius = self.side_radius, segments = 10)

        verts = side.vertex_groups.new(name = "inner_edge")
        verts.add(index = [4, 5], weight = 1, type = "REPLACE")
        op.roundEdges(object = side, edges = "inner_edge", radius = self.general_radius)

        # Add side parts
        bpy.context.view_layer.objects.active = side
        # Move into pos for left side
        side.location += mathutils.Vector((self.side_height/2 + self.base_height,
                                           self.side_width/2 - self.width/2,
                                           self.thickness/2))
        op.merge(self.base, side, solver = "EXACT")

        # Move into pos for right side
        side.location[1] += self.width - self.side_width
        bpy.ops.transform.rotate(value = math.pi, orient_axis = "X")    #mirror
        op.merge(self.base, side, solver = "EXACT")

        bpy.data.objects.remove(side)
        #endregion SIDE_PARTS


        #region EDGES
        # Round horizontal edges
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

        # Create the tooth object
        radius_scaling_factor = 1.5     # > 1.0 scale between r_x/r_y
        height_scaling_factor = 1.1     # > 1.0 so the tooth reaches into the base part (needed for the union operator)
        bpy.ops.mesh.primitive_cone_add(radius1 = self.thickness/radius_scaling_factor,
                                        radius2 = 0.75*self.thickness/2,
                                        vertices = 20,
                                        scale = (radius_scaling_factor,
                                                 1,
                                                 height_scaling_factor*self.tooth_height))
        tooth = bpy.context.object

        # Round the edges on the tip of the teeth
        verts = tooth.vertex_groups.new(name = "tip")
        for vert in tooth.data.vertices:
            if (vert.co.z + self.__EPSILON >= height_scaling_factor*self.tooth_height/2):
                verts.add(index = [vert.index], weight = 1, type = "ADD")
        op.roundEdges(object = tooth, edges = "tip", radius = self.general_radius)

        # Rotate and move the teeth into pos
        tooth.rotation_euler = mathutils.Vector((0, 90*math.pi/180, 0))
        tooth.location += mathutils.Vector((self.base_height + self.tooth_height/2 - (height_scaling_factor - 1)*self.tooth_height/2,
                                            self.tooth_width/2 - self.width/2 + self.side_width + self.tooth_spacing,
                                            self.thickness/2))
        tooth_pos = deepcopy(tooth.location)

        #region BENT_TEETH

        # Params for the bent teeth
        bent_idx = []
        if self.bent_teeth:
            bent_num = random.randrange(1, 21)
            bent_start = random.randrange(0, self.tooth_count - bent_num + 1)
            bent_idx = range(bent_start, bent_start + bent_num)     # Indices of bent teeth

            bend_dir = math.pi/180 * random.uniform(-20.0, 200.0)

            origin_p = random.uniform(0.2, 0.6)

            angle = random.uniform(6.0, 15.0)*math.pi/180
            angles = calcAngles(count = bent_num, indexes = bent_idx, angle = angle)

            # Create origin for bending
            bpy.ops.object.empty_add(type = "PLAIN_AXES")
            axis = bpy.context.object
        #endregion BENT_TEETH

        #region MISSING_TEETH

        # Params for the missing teeth
        missing_idx = []
        if self.missing_teeth:
            missing_num = min(np.random.geometric(0.2), self.tooth_count)       # Number of missing teeth
            missing_idx = random.sample(range(self.tooth_count), missing_num)   # indexes of missing teeth

            # Ceate cutter for missing teeth
            bpy.ops.mesh.primitive_cube_add(scale = (self.tooth_height, 1.5*self.tooth_width, 1.5*self.thickness))
            cutter = bpy.context.object
            cutter.location += mathutils.Vector((self.tooth_height/2 + self.base_height + self.middle_height + self.tooth_height/30,
                                                 tooth_pos[1],
                                                 tooth_pos[2]))
            cutter_base_x = cutter.location[0]
        #endregion MISSING_TEETH
        
        # Add all of the teeth
        for i in range(self.tooth_count):
            if (i in bent_idx) and not (i in missing_idx): # Bent teeth
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

            elif (i in missing_idx): # Broken teeth
                bpy.context.view_layer.objects.active = tooth
                bpy.ops.object.select_all(action = "DESELECT")
                tooth.select_set(1)
                bpy.ops.object.duplicate()
                duplicate_tooth = bpy.context.object

                # Cut copied tooth
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

            else:   # Normal teeth
                op.merge(self.base, tooth, solver = "FAST")

            # Move to next teeth position
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

        # Create middle part
        scaling_factor = 6.0    # For the uneven rounding
        bpy.ops.mesh.primitive_cube_add(scale = (self.middle_height/scaling_factor,
                                                 self.middle_width,
                                                 self.middle_thickness))
        middle = bpy.context.object
        middle.location += mathutils.Vector((self.middle_height/2 + self.base_height,
                                             0,
                                             self.thickness/2))
        middle.scale[0] = scaling_factor

        # Round the edges of the middle part
        verts = middle.vertex_groups.new(name = "front")
        verts.add(index = [4, 6, 5, 7], weight = 1, type = "REPLACE")
        op.roundEdges(object = middle, edges = "front", radius = self.middle_thickness/2)

        op.merge(self.base, middle, solver = "FAST")
        bpy.data.objects.remove(middle)
        #endregion MIDDLE_PART


        #region EJECTOR_MARKS

        if (self.ejector_marks > 0):
            # Params
            ejector_radius = 0.3*self.base_height   # min: 0.15*self.base_height / max: 0.5*self.base_height
            ejector_depth = 0.2                     # Cutting depth
            ejector_pos_y = 0.37*self.width         # y_min = +-0.15*self.width, y_max: +-0.4*self.width
        
            # Create ejector pin for cutting
            bpy.ops.mesh.primitive_cylinder_add(radius = ejector_radius, depth = 5*ejector_depth)
            ejector = bpy.context.object
            ejector.location = mathutils.Vector((self.base_height/2, 0.0, self.thickness + 1.5*ejector_depth))

            # Create ejector marks
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

            # Delete ejector object
            bpy.data.objects.remove(ejector)

        #endregion EJECTOR_MARKS


        # Remesh
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

        # Add material
        self.mat = bpy.data.materials.new(name = "HaircombMaterial")
        self.base.data.materials.append(self.mat)


    def getObject(self) -> bpy.types.Object:
        return self.base


    def getMaterial(self) -> bpy.types.Material:
        return self.mat


    def getBoundingBox(self) -> List[float]:
        """Returns a list containing the vertices of the objects bounding box.)"""

        return ( # This format is needed for a Blender function (camera_fit_coords)
                -self.height/40,   -21/40*self.width,  self.thickness,  #x1, y1, z1
                -self.height/40,   -21/40*self.width,  0,               #x2, y2, z2 ...
                41/40*self.height, -21/40*self.width,  self.thickness,
                41/40*self.height, -21/40*self.width,  0,
                -self.height/40,    21/40*self.width,  self.thickness,
                -self.height/40,    21/40*self.width,  0,
                41/40*self.height,  21/40*self.width,  self.thickness,
                41/40*self.height,  21/40*self.width,  0                #x8, y8, z8
               )



# DEBUG (this never runs while generating the images)
def main():
    
    bpy.ops.object.select_all(action = "SELECT")
    bpy.ops.object.delete()
    utils.removeMeshes()

    # CREATE GROUND OBJECT
    bpy.ops.mesh.primitive_plane_add(size = 20000)
    ground = bpy.context.object
    ground_mat = bpy.data.materials.new(name = "ground")
    ground.data.materials.append(ground_mat)
    shaders.applyRandomTextures(ground_mat, "S:\\source\\image-generator\\textures")

    # CREATE OBJECT
    hc = Haircomb(missing_teeth = True, bent_teeth = True, warping = True, ejector_marks = 2)
    hc.createHaircomb()

    shaders.applyPlastic(mat = hc.getMaterial(),
                         color = (0.0, 0.0, 0.0, 1.0),
                         surface = "matte",
                         randomize = True,
                         textures_path = "S:\\source\\image-generator\\textures",
                         tex_defect = "contamination",
                         gloss_defect = True,
                         discoloration = True)


if __name__ == "__main__":
    
    project_path = "S:\\source\\image-generator"
    import sys
    sys.path.append(project_path)
    import shaders, utils

    main()