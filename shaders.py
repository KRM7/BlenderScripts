project_path = "C:\\Users\\Krisztián\\source\\repos\\BlenderScripts"
import sys
sys.path.append(project_path)

import bpy
import random, math

COLORS = {
    #"BLACK": (0.0, 0.0, 0.0, 1.0),
    "BLUE": (0.0, 0.0, 0.4, 1.0),
    "PINK": (0.4, 0.0, 0.3, 1.0),
    "GREEN": (0.0, 0.3, 0.0, 1.0),
    "RED": (0.4, 0.0, 0.0, 1.0),
    "YELLOW": (0.6, 0.6, 0.0, 1.0),
    "WHITE": (0.8, 0.8, 0.8, 1.0),
    "GRAY": (0.1, 0.1, 0.1, 1.0),
    "LIGHTGRAY": (0.5, 0.5, 0.5, 1.0),
    "ORANGE": (0.8, 0.16, 0.0, 1.0)
}

#custom
def applyBase(mat, color, randomize = False):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_bump.outputs["Normal"], node_principled.inputs["Normal"])
    links.new(node_noise.outputs["Fac"], node_bump.inputs["Height"])

    #noise texture shader
    node_noise.inputs["Scale"].default_value = 10000.0 + random.uniform(-2000, 2000)
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.0
    node_noise.inputs["Distortion"].default_value = 0.0
    
    #bump shader
    node_bump.inputs["Strength"].default_value = 0.1 + random.uniform(-0.05, 0.05)
    node_bump.inputs["Distance"].default_value = 0.05 + random.uniform(-0.02, 0.02)
    
    #principled shader
    node_principled.distribution = "GGX"
    node_principled.subsurface_method = "BURLEY"
    if randomize:
        node_principled.inputs["Base Color"].default_value = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 1.0)
    else:
        node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Subsurface"].default_value = 0.0
    node_principled.inputs["Metallic"].default_value = 0.0
    node_principled.inputs["Specular"].default_value = 0.3 + random.uniform(-0.1, 0.1)
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.4 + random.uniform(-0.1, 0.1)
    node_principled.inputs["Anisotropic"].default_value = 0.0
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.0
    node_principled.inputs["Sheen Tint"].default_value = 0.5
    node_principled.inputs["Clearcoat"].default_value = 0.1 + random.uniform(-0.1, 0.1)
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.15 + random.uniform(-0.05, 0.05)
    node_principled.inputs["Transmission"].default_value = 0.0
    node_principled.inputs["Emission Strength"].default_value = 0.0


def applyPlasticRough(mat, color):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_bump.outputs["Normal"], node_principled.inputs["Normal"])
    links.new(node_noise.outputs["Fac"], node_bump.inputs["Height"])

    #noise texture shader
    node_noise.inputs["Scale"].default_value = 1000.0
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.0
    node_noise.inputs["Distortion"].default_value = 0.0
    
    #bump shader
    node_bump.inputs["Strength"].default_value = 1.0
    node_bump.inputs["Distance"].default_value = 0.2
    
    #principled shader
    node_principled.distribution = "GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Subsurface"].default_value = 0.0
    node_principled.inputs["Subsurface Color"].default_value = color
    node_principled.inputs["Metallic"].default_value = 0.0
    node_principled.inputs["Specular"].default_value = 0.8
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.47
    node_principled.inputs["Anisotropic"].default_value = 0.0
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.0
    node_principled.inputs["Sheen Tint"].default_value = 0.5
    node_principled.inputs["Clearcoat"].default_value = 0.0
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.0
    node_principled.inputs["IOR"].default_value = 1.45
    node_principled.inputs["Transmission"].default_value = 0.0
    node_principled.inputs["Emission"].default_value = (0.0, 0.0, 0.0, 1.0)
    node_principled.inputs["Emission Strength"].default_value = 2.0
    node_principled.inputs["Alpha"].default_value = 1.0


def applyPlasticMatte(mat, color, randomize = False, defect = None):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_bump.outputs["Normal"], node_principled.inputs["Normal"])
    links.new(node_noise.outputs["Fac"], node_bump.inputs["Height"])

    #noise texture shader
    node_noise.inputs["Scale"].default_value = 2000.0
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.0
    node_noise.inputs["Distortion"].default_value = 0.0
    
    #bump shader
    node_bump.inputs["Strength"].default_value = 0.1 + int(randomize)*random.uniform(0.0, 0.05)
    node_bump.inputs["Distance"].default_value = 0.1 + int(randomize)*random.uniform(0.0, 0.05)
   
    #principled shader
    node_principled.distribution = "MULTI_GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Specular"].default_value = 0.15 + int(randomize)*random.uniform(0.0, 0.1)
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.5 + int(randomize)*random.uniform(0.0, 0.15)
    node_principled.inputs["Anisotropic"].default_value = 0.2
    node_principled.inputs["Sheen Tint"].default_value = 0.0
    node_principled.inputs["Clearcoat"].default_value = 0.1 + int(randomize)*random.uniform(0.0, 0.2)
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.05)
    node_principled.inputs["Emission Strength"].default_value = 0.0
    node_principled.inputs["Alpha"].default_value = 1.0

    #texture defects
    if defect == None:
        pass

    elif defect == "contamination":
        node_coord = nodes.new(type = "ShaderNodeTexCoord")
        node_mapping = nodes.new(type = "ShaderNodeMapping")
        node_color = nodes.new(type = "ShaderNodeTexImage")

        links.new(node_coord.outputs["Object"], node_mapping.inputs["Vector"])
        links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
        links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])

        node_color.image = bpy.data.images.load(project_path + "\\textures\\Contamination.png", check_existing=True)
        node_mapping.inputs["Scale"].default_value[0] = 0.01 + int(randomize)*random.uniform(0, 0.005)
        node_mapping.inputs["Scale"].default_value[1] = 0.01 + int(randomize)*random.uniform(0, 0.005)
        node_mapping.inputs["Scale"].default_value[2] = 0.01 + int(randomize)*random.uniform(0, 0.005)
        node_mapping.inputs["Location"].default_value[0] = 0 + int(randomize)*random.uniform(-2, 2)
        node_mapping.inputs["Location"].default_value[1] = 0 + int(randomize)*random.uniform(-2, 2)
        node_mapping.inputs["Rotation"].default_value[2] = 0 + int(randomize)*random.uniform(0, 2*math.pi)
    
    elif defect == "splay":
        node_coord = nodes.new(type = "ShaderNodeTexCoord")
        node_mapping = nodes.new(type = "ShaderNodeMapping")
        node_color = nodes.new(type = "ShaderNodeTexImage")

        links.new(node_coord.outputs["Object"], node_mapping.inputs["Vector"])
        links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
        links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])

        node_color.image = bpy.data.images.load(project_path + "\\textures\\Splay.png", check_existing=True)
        node_mapping.inputs["Scale"].default_value[0] = 0.04 + int(randomize)*random.uniform(0, 0.003)
        node_mapping.inputs["Scale"].default_value[1] = 0.08 + int(randomize)*random.uniform(0, 0.004)
        node_mapping.inputs["Scale"].default_value[2] = 1
        node_mapping.inputs["Location"].default_value[0] = 0 + int(randomize)*random.uniform(-1, 1)
        node_mapping.inputs["Location"].default_value[1] = 0 + int(randomize)*random.uniform(-1, 1)
        node_mapping.inputs["Rotation"].default_value[2] = 90*math.pi/180

    elif defect == "gloss":
        #principled shader
        node_principled.inputs["Specular"].default_value = 0.025 + int(randomize)*random.uniform(0.0, 0.05)
        node_principled.inputs["Anisotropic"].default_value = 0.0
        node_principled.inputs["Clearcoat"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.1)
        node_principled.inputs["Clearcoat Roughness"].default_value = 0.5 + int(randomize)*random.uniform(0.0, 0.25)
        node_principled.inputs["Roughness"].default_value = node_principled.inputs["Clearcoat Roughness"].default_value + 0.05

        #noise texture shader
        node_noise.inputs["Scale"].default_value = 150.0
        node_noise.inputs["Roughness"].default_value = 1.0
        node_noise.inputs["Distortion"].default_value = 0.5

        #bump shader
        node_bump.inputs["Strength"].default_value = 1.5 + int(randomize)*random.uniform(0.0, 1.0)
        node_bump.inputs["Distance"].default_value = 0.25 + int(randomize)*random.uniform(0.0, 0.15)

    else:
        raise ValueError("Invalid defect")


def applyPlasticShiny(mat, color):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_bump.outputs["Normal"], node_principled.inputs["Normal"])
    links.new(node_noise.outputs["Fac"], node_bump.inputs["Height"])

    #noise texture shader
    node_noise.inputs["Scale"].default_value = 1000.0
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.0
    node_noise.inputs["Distortion"].default_value = 0.0
    
    #bump shader
    node_bump.inputs["Strength"].default_value = 0.02
    node_bump.inputs["Distance"].default_value = 0.05
    
    #principled shader
    node_principled.distribution = "MULTI_GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Subsurface"].default_value = 0.005
    node_principled.inputs["Subsurface Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    node_principled.inputs["Metallic"].default_value = 0.0
    node_principled.inputs["Specular"].default_value = 0.9
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.25
    node_principled.inputs["Anisotropic"].default_value = 0.5
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.0
    node_principled.inputs["Sheen Tint"].default_value = 0.5
    node_principled.inputs["Clearcoat"].default_value = 0.8
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.2
    node_principled.inputs["Transmission"].default_value = 0.0
    node_principled.inputs["Emission Strength"].default_value = 0.0


#textures
def applyAsphalt(mat, scale = 30.0):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])
    links.new(node_displacement_t.outputs["Color"], node_displacement.inputs["Height"])
    links.new(node_displacement.outputs["Displacement"], node_output.inputs["Displacement"])
    links.new(node_normal.outputs["Color"], node_principled.inputs["Normal"])
    links.new(node_roughness.outputs["Color"], node_principled.inputs["Roughness"])
    links.new(node_coord.outputs["UV"], node_mapping.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_displacement_t.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_roughness.inputs["Vector"])

    #inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_displacement.inputs["Scale"].default_value = 0.05
    node_color.image = bpy.data.images.load(project_path + "\\textures\\Asphalt\\Color.png", check_existing=True)
    node_displacement_t.image = bpy.data.images.load(project_path + "\\textures\\Asphalt\\Displacement.png", check_existing=True)
    node_normal.image = bpy.data.images.load(project_path + "\\textures\\Asphalt\\Normal.png", check_existing=True)
    node_roughness.image = bpy.data.images.load(project_path + "\\textures\\Asphalt\\Roughness.png", check_existing=True)

    node_mapping.inputs["Scale"].default_value[0] = scale
    node_mapping.inputs["Scale"].default_value[1] = scale
    node_mapping.inputs["Scale"].default_value[2] = scale


def applyTiles(mat, scale = 25.0):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])
    links.new(node_displacement_t.outputs["Color"], node_displacement.inputs["Height"])
    links.new(node_displacement.outputs["Displacement"], node_output.inputs["Displacement"])
    links.new(node_normal.outputs["Color"], node_principled.inputs["Normal"])
    links.new(node_roughness.outputs["Color"], node_principled.inputs["Roughness"])
    links.new(node_coord.outputs["UV"], node_mapping.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_displacement_t.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_roughness.inputs["Vector"])

    #inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_displacement.inputs["Scale"].default_value = 0.05
    node_color.image = bpy.data.images.load(project_path + "\\textures\\Tiles\\Color.png", check_existing=True)
    node_displacement_t.image = bpy.data.images.load(project_path + "\\textures\\Tiles\\Displacement.png", check_existing=True)
    node_normal.image = bpy.data.images.load(project_path + "\\textures\\Tiles\\Normal.png", check_existing=True)
    node_roughness.image = bpy.data.images.load(project_path + "\\textures\\Tiles\\Roughness.png", check_existing=True)

    node_mapping.inputs["Scale"].default_value[0] = scale
    node_mapping.inputs["Scale"].default_value[1] = scale
    node_mapping.inputs["Scale"].default_value[2] = scale


def applyPorcelain(mat, scale = 45.0):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])
    links.new(node_displacement_t.outputs["Color"], node_displacement.inputs["Height"])
    links.new(node_displacement.outputs["Displacement"], node_output.inputs["Displacement"])
    links.new(node_normal.outputs["Color"], node_principled.inputs["Normal"])
    links.new(node_roughness.outputs["Color"], node_principled.inputs["Roughness"])
    links.new(node_coord.outputs["UV"], node_mapping.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_displacement_t.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_roughness.inputs["Vector"])

    #inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_displacement.inputs["Scale"].default_value = 0.05
    node_color.image = bpy.data.images.load(project_path + "\\textures\\Porcelain\\Color.png", check_existing=True)
    node_displacement_t.image = bpy.data.images.load(project_path + "\\textures\\Porcelain\\Displacement.png", check_existing=True)
    node_normal.image = bpy.data.images.load(project_path + "\\textures\\Porcelain\\Normal.png", check_existing=True)
    node_roughness.image = bpy.data.images.load(project_path + "\\textures\\Porcelain\\Roughness.png", check_existing=True)

    node_mapping.inputs["Scale"].default_value[0] = scale
    node_mapping.inputs["Scale"].default_value[1] = scale
    node_mapping.inputs["Scale"].default_value[2] = scale


def applyMetal(mat, scale = 80.0): #render with Eevee
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")
    node_metalness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])
    links.new(node_displacement_t.outputs["Color"], node_displacement.inputs["Height"])
    links.new(node_displacement.outputs["Displacement"], node_output.inputs["Displacement"])
    links.new(node_normal.outputs["Color"], node_principled.inputs["Normal"])
    links.new(node_roughness.outputs["Color"], node_principled.inputs["Roughness"])
    links.new(node_metalness.outputs["Color"], node_principled.inputs["Metallic"])
    links.new(node_coord.outputs["UV"], node_mapping.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_displacement_t.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_roughness.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_metalness.inputs["Vector"])

    #inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_displacement.inputs["Scale"].default_value = 0.05
    node_color.image = bpy.data.images.load(project_path + "\\textures\\Metal\\Color.png", check_existing=True)
    node_displacement_t.image = bpy.data.images.load(project_path + "\\textures\\Metal\\Displacement.png", check_existing=True)
    node_normal.image = bpy.data.images.load(project_path + "\\textures\\Metal\\Normal.png", check_existing=True)
    node_roughness.image = bpy.data.images.load(project_path + "\\textures\\Metal\\Roughness.png", check_existing=True)
    node_metalness.image = bpy.data.images.load(project_path + "\\textures\\Metal\\Metalness.png", check_existing=True)

    node_mapping.inputs["Scale"].default_value[0] = scale
    node_mapping.inputs["Scale"].default_value[1] = scale
    node_mapping.inputs["Scale"].default_value[2] = scale


#not used
def applyPlastic1(mat, scale = 45.0):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])
    links.new(node_displacement_t.outputs["Color"], node_displacement.inputs["Height"])
    links.new(node_displacement.outputs["Displacement"], node_output.inputs["Displacement"])
    links.new(node_normal.outputs["Color"], node_principled.inputs["Normal"])
    links.new(node_roughness.outputs["Color"], node_principled.inputs["Roughness"])
    links.new(node_coord.outputs["UV"], node_mapping.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_displacement_t.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_roughness.inputs["Vector"])

    #inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_displacement.inputs["Scale"].default_value = 0.05
    node_color.image = bpy.data.images.load(project_path + "\\textures\\Plastic1\\Color.png", check_existing=True)
    node_displacement_t.image = bpy.data.images.load(project_path + "\\textures\\Plastic1\\Displacement.png", check_existing=True)
    node_normal.image = bpy.data.images.load(project_path + "\\textures\\Plastic1\\Normal.png", check_existing=True)
    node_roughness.image = bpy.data.images.load(project_path + "\\textures\\Plastic1\\Roughness.png", check_existing=True)

    node_mapping.inputs["Scale"].default_value[0] = scale
    node_mapping.inputs["Scale"].default_value[1] = scale
    node_mapping.inputs["Scale"].default_value[2] = scale


def applyPlastic2(mat, scale = 45.0):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])
    links.new(node_displacement_t.outputs["Color"], node_displacement.inputs["Height"])
    links.new(node_displacement.outputs["Displacement"], node_output.inputs["Displacement"])
    links.new(node_normal.outputs["Color"], node_principled.inputs["Normal"])
    links.new(node_roughness.outputs["Color"], node_principled.inputs["Roughness"])
    links.new(node_coord.outputs["UV"], node_mapping.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_displacement_t.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_roughness.inputs["Vector"])

    #inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_displacement.inputs["Scale"].default_value = 0.05
    node_color.image = bpy.data.images.load(project_path + "\\textures\\Plastic2\\Color.png", check_existing=True)
    node_displacement_t.image = bpy.data.images.load(project_path + "\\textures\\Plastic2\\Displacement.png", check_existing=True)
    node_normal.image = bpy.data.images.load(project_path + "\\textures\\Plastic2\\Normal.png", check_existing=True)
    node_roughness.image = bpy.data.images.load(project_path + "\\textures\\Plastic2\\Roughness.png", check_existing=True)

    node_mapping.inputs["Scale"].default_value[0] = scale
    node_mapping.inputs["Scale"].default_value[1] = scale
    node_mapping.inputs["Scale"].default_value[2] = scale


def applyPlastic3(mat, scale = 45.0):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])
    links.new(node_displacement_t.outputs["Color"], node_displacement.inputs["Height"])
    links.new(node_displacement.outputs["Displacement"], node_output.inputs["Displacement"])
    links.new(node_normal.outputs["Color"], node_principled.inputs["Normal"])
    links.new(node_roughness.outputs["Color"], node_principled.inputs["Roughness"])
    links.new(node_coord.outputs["UV"], node_mapping.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_displacement_t.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_normal.inputs["Vector"])
    links.new(node_mapping.outputs["Vector"], node_roughness.inputs["Vector"])

    #inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_displacement.inputs["Scale"].default_value = 0.05
    node_color.image = bpy.data.images.load(project_path + "\\textures\\Plastic3\\Color.png", check_existing=True)
    node_displacement_t.image = bpy.data.images.load(project_path + "\\textures\\Plastic3\\Displacement.png", check_existing=True)
    node_normal.image = bpy.data.images.load(project_path + "\\textures\\Plastic3\\Normal.png", check_existing=True)
    node_roughness.image = bpy.data.images.load(project_path + "\\textures\\Plastic3\\Roughness.png", check_existing=True)

    node_mapping.inputs["Scale"].default_value[0] = scale
    node_mapping.inputs["Scale"].default_value[1] = scale
    node_mapping.inputs["Scale"].default_value[2] = scale