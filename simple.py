import bpy

#1. add cube from primitive
#bpy.ops.mesh.primitive_cube_add()


#2. build an arbitrary object from vertexes and faces
#verts = [(-1,  1,   0),
#         ( 1,  1,   0),
#         ( 2, -3,   0),
#         (-2, -1,   0),
#         (-1,  1.5, 1),
#         ( 1,  1.5, 1),
#        ]

## faces are a list of indices to each vertex from the above list
#faces = [[0, 1, 2, 3], [0, 1, 5, 4]]

#mesh = bpy.data.meshes.new(name="New Mesh")
#mesh.from_pydata(verts, [], faces)
#obj = bpy.data.objects.new('New object', mesh)
#bpy.context.collection.objects.link(obj)


#3. build cube
#cube_verts = [(0,0,0),
#              (1,0,0),
#              (1,1,0),
#              (0,1,0),
#              (0,0,-1),
#              (1,0,-1),
#              (1,1,-1),
#              (0,1,-1)
#             ]
#             
#cube_faces = [[0,1,2,3], [1,2,6,5], [4,5,6,7], [0,4,7,3], [0,1,5,4], [3,2,6,7]]
##create the mesh
#cube_mesh = bpy.data.meshes.new(name="TestCube")
#cube_mesh.from_pydata(cube_verts, [], cube_faces)
##create the object
#cube = bpy.data.objects.new("TestCube", cube_mesh)
#bpy.context.collection.objects.link(cube)

#4.
#add cube
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.object
cube.name = "TestCube"
bpy.ops.transform.resize(value=(1, 2, 1))

#add cylinder
bpy.ops.mesh.primitive_cylinder_add(radius = 0.3) #the cylinder is selected after this
cylinder = bpy.context.object
cylinder.name = "TestCylinder"
bpy.ops.transform.rotate(value=1.5708, orient_axis="Y") #rotate the selected object
bpy.ops.transform.resize(value=(2,1,1))

#modifier
mod = cube.modifiers.new("sub", type="BOOLEAN") #the object it is used on
mod.operation = "DIFFERENCE"
mod.object = cylinder
bpy.context.view_layer.objects.active = cube
bpy.ops.object.modifier_apply(modifier = "sub")

bpy.context.view_layer.objects.active = cylinder
bpy.ops.transform.translate(value=(0,-2,1))
mod.object = cylinderbpy.ops.object.modifier_apply(modifier = "sub")

#bpy.context.view_layer.objects.active = cylinder
#bpy.ops.transform.translate(value=(0,0,-2))
#bpy.context.view_layer.objects.active = cube
#bpy.ops.object.modifier_apply(modifier = "sub")

#bpy.context.view_layer.objects.active = cylinder
#bpy.ops.transform.translate(value=(0,4,0))
#bpy.context.view_layer.objects.active = cube
#bpy.ops.object.modifier_apply(modifier = "sub")

#bpy.context.view_layer.objects.active = cylinder
#bpy.ops.transform.translate(value=(0,0,2))
#bpy.context.view_layer.objects.active = cube
#bpy.ops.object.modifier_apply(modifier = "sub")

#bpy.data.objects.remove(cylinder)