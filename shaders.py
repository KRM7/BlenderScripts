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

def applyBase(mat, color):
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
    node_noise.inputs["Scale"].default_value = 10000.0
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.0
    node_noise.inputs["Distortion"].default_value = 0.0
    #bump shader
    node_bump.inputs["Strength"].default_value = 0.1
    node_bump.inputs["Distance"].default_value = 0.1
    #principled shader
    node_principled.distribution = "GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Base Color"].default_value = color
    node_principled.inputs["Subsurface"].default_value = 0.0
    node_principled.inputs["Subsurface Color"].default_value = color
    node_principled.inputs["Metallic"].default_value = 0.0
    node_principled.inputs["Specular"].default_value = 1.0
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.1
    node_principled.inputs["Anisotropic"].default_value = 0.4
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.0
    node_principled.inputs["Sheen Tint"].default_value = 0.5
    node_principled.inputs["Clearcoat"].default_value = 0.5
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.05
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

def applyWood(mat):
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
    node_vor = nodes.new(type = "ShaderNodeTexVoronoi")
    node_wave = nodes.new(type = "ShaderNodeTexWave")
    node_color = nodes.new(type = "ShaderNodeValToRGB")

    #connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_bump.outputs["Normal"], node_principled.inputs["Normal"])
    links.new(node_noise.outputs["Fac"], node_bump.inputs["Height"])
    links.new(node_vor.outputs["Position"], node_wave.inputs["Vector"])
    links.new(node_wave.outputs["Fac"], node_color.inputs["Fac"])
    links.new(node_color.outputs["Color"], node_principled.inputs["Base Color"])

    #voronoi texture shader
    node_vor.voronoi_dimensions = "2D"
    node_vor.feature = "F2"
    node_vor.distance = "MINKOWSKI"
    node_vor.inputs["Scale"].default_value = 60.0
    node_vor.inputs["Exponent"].default_value = 0.4
    #wave texture shader
    node_wave.wave_type = "BANDS"
    node_wave.bands_direction = "DIAGONAL"
    node_wave.wave_profile = "TRI"
    node_wave.inputs["Scale"].default_value = 50.0
    #color ramp
    node_color.color_ramp.interpolation = "B_SPLINE"
    node_color.color_ramp.elements[0].position = 0.21
    node_color.color_ramp.elements[0].color = (0.16, 0.09, 0.05, 1.0)
    node_color.color_ramp.elements[1].position = 0.76
    node_color.color_ramp.elements[1].color = (0.42, 0.29, 0.15, 1.0)
    #noise texture shader
    node_noise.inputs["Scale"].default_value = 1000.0
    node_noise.inputs["Detail"].default_value = 2.0
    node_noise.inputs["Roughness"].default_value = 0.0
    node_noise.inputs["Distortion"].default_value = 0.0
    #bump shader
    node_bump.inputs["Strength"].default_value = 1.0
    node_bump.inputs["Distance"].default_value = 0.3
    #principled shader
    node_principled.distribution = "MULTI_GGX"
    node_principled.subsurface_method = "BURLEY"
    node_principled.inputs["Subsurface"].default_value = 0.0
    node_principled.inputs["Metallic"].default_value = 0.0
    node_principled.inputs["Specular"].default_value = 0.5
    node_principled.inputs["Specular Tint"].default_value = 0.0
    node_principled.inputs["Roughness"].default_value = 0.5
    node_principled.inputs["Anisotropic"].default_value = 0.0
    node_principled.inputs["Anisotropic Rotation"].default_value = 0.0
    node_principled.inputs["Sheen"].default_value = 0.5
    node_principled.inputs["Sheen Tint"].default_value = 0.0
    node_principled.inputs["Clearcoat"].default_value = 0.5
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.1
    node_principled.inputs["IOR"].default_value = 1.45
    node_principled.inputs["Transmission"].default_value = 0.0
    node_principled.inputs["Emission Strength"].default_value = 0.0
    node_principled.inputs["Alpha"].default_value = 1.0