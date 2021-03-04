import bpy

COLORS = {
    "BLACK": (0.0, 0.0, 0.0, 1.0),
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
COLORSETS = {
    "BLACK": [(0.07, 0.07, 0.07, 1.0), (0.24, 0.24, 0.24, 1.0), (0.3, 0.3, 0.3, 1.0)],
    "GREEN": [(0.14, 0.65, 0.14, 1.0), (0.42, 0.85, 0.38, 1.0), (0.19, 0.85, 0.19, 1.0)]
}

def applyPlasticRough(mat, colors):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_mix2 = nodes.new(type = "ShaderNodeMixShader")
    node_mix1 = nodes.new(type = "ShaderNodeMixShader")
    node_translucent = nodes.new(type = "ShaderNodeBsdfTranslucent")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")
    node_fresnel = nodes.new(type = "ShaderNodeLayerWeight")
    node_glossy = nodes.new(type = "ShaderNodeBsdfGlossy")
    node_diffuse = nodes.new(type = "ShaderNodeBsdfDiffuse")

    #connect shader nodes
    links.new(node_mix2.outputs[0], node_output.inputs[0])

    links.new(node_mix1.outputs[0], node_mix2.inputs[1])
    links.new(node_translucent.outputs[0], node_mix2.inputs[2])

    links.new(node_noise.outputs[0], node_bump.inputs[2])
    links.new(node_bump.outputs[0], node_translucent.inputs[1])
    links.new(node_bump.outputs[0], node_glossy.inputs[2])
    links.new(node_bump.outputs[0], node_diffuse.inputs[2])

    links.new(node_fresnel.outputs[0], node_mix1.inputs[0])
    links.new(node_glossy.outputs[0], node_mix1.inputs[1])
    links.new(node_diffuse.outputs[0], node_mix1.inputs[2])

    #set shader parameters
    node_mix2.inputs["Fac"].default_value = 0.1
    #translucent shader
    node_translucent.inputs["Color"].default_value = colors[2]
    #noise texture shader
    node_noise.inputs["Scale"].default_value = 1000.0
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.0
    #bump shader
    node_bump.inputs["Strength"].default_value = 1.0
    node_bump.inputs["Distance"].default_value = 0.2
    #fresnel shader
    node_fresnel.inputs["Blend"].default_value = 0.9
    #glossy shader
    node_glossy.inputs["Color"].default_value = colors[1]
    node_glossy.inputs["Roughness"].default_value = 0.5
    #diffuse shader
    node_diffuse.inputs["Color"].default_value = colors[0]
    node_diffuse.inputs["Roughness"].default_value = 0.0

def applyBase(mat, colors):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    links = mat.node_tree.links
    links.clear()

    #create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_mix2 = nodes.new(type = "ShaderNodeMixShader")
    node_mix1 = nodes.new(type = "ShaderNodeMixShader")
    node_translucent = nodes.new(type = "ShaderNodeBsdfTranslucent")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")
    node_fresnel = nodes.new(type = "ShaderNodeLayerWeight")
    node_glossy = nodes.new(type = "ShaderNodeBsdfGlossy")
    node_diffuse = nodes.new(type = "ShaderNodeBsdfDiffuse")

    #connect shader nodes
    links.new(node_mix2.outputs[0], node_output.inputs[0])

    links.new(node_mix1.outputs[0], node_mix2.inputs[1])
    links.new(node_translucent.outputs[0], node_mix2.inputs[2])

    links.new(node_noise.outputs[0], node_bump.inputs[2])
    links.new(node_bump.outputs[0], node_translucent.inputs[1])
    links.new(node_bump.outputs[0], node_glossy.inputs[2])
    links.new(node_bump.outputs[0], node_diffuse.inputs[2])

    links.new(node_fresnel.outputs[0], node_mix1.inputs[0])
    links.new(node_glossy.outputs[0], node_mix1.inputs[1])
    links.new(node_diffuse.outputs[0], node_mix1.inputs[2])

    #set shader parameters
    node_mix2.inputs["Fac"].default_value = 0.1
    #translucent shader
    node_translucent.inputs["Color"].default_value = colors[2]
    #noise texture shader
    node_noise.inputs["Scale"].default_value = 1000.0
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.1
    node_noise.inputs["Distortion"].default_value = -10.0
    #bump shader
    node_bump.inputs["Strength"].default_value = 0.7
    node_bump.inputs["Distance"].default_value = 0.1
    #fresnel shader
    node_fresnel.inputs["Blend"].default_value = 0.8
    #glossy shader
    node_glossy.inputs["Color"].default_value = colors[1]
    node_glossy.inputs["Roughness"].default_value = 0.0
    #diffuse shader
    node_diffuse.inputs["Color"].default_value = colors[0]
    node_diffuse.inputs["Roughness"].default_value = 0.0

def applyPlasticMatte(mat, color):
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
    node_bump.inputs["Strength"].default_value = 0.3
    node_bump.inputs["Distance"].default_value = 0.2
    #principled shader
    node_principled.distribution = "MULTI_GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Subsurface"].default_value = 0.0
    node_principled.inputs["Subsurface Color"].default_value = color
    node_principled.inputs["Metallic"].default_value = 0.0
    node_principled.inputs["Specular"].default_value = 0.8
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.6
    node_principled.inputs["Anisotropic"].default_value = 0.2
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.0
    node_principled.inputs["Sheen Tint"].default_value = 0.0
    node_principled.inputs["Clearcoat"].default_value = 0.0
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.0
    node_principled.inputs["IOR"].default_value = 1.45
    node_principled.inputs["Transmission"].default_value = 0.2
    node_principled.inputs["Emission"].default_value = color
    node_principled.inputs["Emission Strength"].default_value = 0.0
    node_principled.inputs["Alpha"].default_value = 1.0

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
    node_bump.inputs["Strength"].default_value = 0.1
    node_bump.inputs["Distance"].default_value = 0.1
    #principled shader
    node_principled.distribution = "MULTI_GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Subsurface"].default_value = 0.05
    node_principled.inputs["Subsurface Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    node_principled.inputs["Metallic"].default_value = 0.15
    node_principled.inputs["Specular"].default_value = 0.8
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.2
    node_principled.inputs["Anisotropic"].default_value = 0.4
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.0
    node_principled.inputs["Sheen Tint"].default_value = 0.5
    node_principled.inputs["Clearcoat"].default_value = 1.0
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.1
    node_principled.inputs["IOR"].default_value = 1.45
    node_principled.inputs["Transmission"].default_value = 0.0
    node_principled.inputs["Emission"].default_value = color
    node_principled.inputs["Emission Strength"].default_value = 0.02
    node_principled.inputs["Alpha"].default_value = 1.0

def applyMetal(mat, color):
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
    node_bump.inputs["Strength"].default_value = 0.1
    node_bump.inputs["Distance"].default_value = 0.05
    #principled shader
    node_principled.distribution = "MULTI_GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Subsurface"].default_value = 0.0
    node_principled.inputs["Subsurface Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    node_principled.inputs["Metallic"].default_value = 1.0
    node_principled.inputs["Specular"].default_value = 0.5
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.25
    node_principled.inputs["Anisotropic"].default_value = 0.0
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.0
    node_principled.inputs["Sheen Tint"].default_value = 0.5
    node_principled.inputs["Clearcoat"].default_value = 0.0
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.0
    node_principled.inputs["IOR"].default_value = 1.45
    node_principled.inputs["Transmission"].default_value = 0.0
    node_principled.inputs["Emission"].default_value = color
    node_principled.inputs["Emission Strength"].default_value = 0.0
    node_principled.inputs["Alpha"].default_value = 1.0