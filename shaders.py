import bpy

def applyPlastic(mat,
                 diffuse_color = (0.025, 0.025, 0.025, 1.0),
                 translucent_color = (0.05, 0.05, 0.05, 1.0)):
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
    links.new(node_translucent.outputs[0], node_mix2.inputs[1])
    links.new(node_bump.outputs[0], node_translucent.inputs[1])
    links.new(node_noise.outputs[0], node_bump.inputs[2])
    links.new(node_mix1.outputs[0], node_mix2.inputs[2])
    links.new(node_fresnel.outputs[0], node_mix1.inputs[0])
    links.new(node_glossy.outputs[0], node_mix1.inputs[1])
    links.new(node_bump.outputs[0], node_glossy.inputs[2])
    links.new(node_diffuse.outputs[0], node_mix1.inputs[2])
    links.new(node_bump.outputs[0], node_diffuse.inputs[2])

    #set shader parameters
    node_mix2.inputs["Fac"].default_value = 0.5 #factor
    #translucent shader
    node_translucent.inputs["Color"].default_value = translucent_color
    #bump shader
    node_bump.inputs["Strength"].default_value = 0.3 #strength
    node_bump.inputs["Distance"].default_value = 0.13 #distance
    #noise texture shader
    node_noise.inputs["Scale"].default_value = 1000.0  #scale
    node_noise.inputs["Detail"].default_value = 2.0 #detail
    node_noise.inputs["Roughness"].default_value = 0.1 #roughness
    #fresnel shader
    node_fresnel.inputs["Blend"].default_value = 0.8 #blend
    #glossy shader
    node_glossy.inputs["Color"].default_value = translucent_color
    node_glossy.inputs["Roughness"].default_value = 0.1 #roughness
    #diffuse shader
    node_diffuse.inputs["Color"].default_value = diffuse_color
    node_diffuse.inputs["Roughness"].default_value = 0.0 #roughness
