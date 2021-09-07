"""Blender 2.91

Shader setup functions for different materials.

"""

import bpy

from os import path
import math
import random
from typing import List

import scene


# Some predefined colors.
COLORS = {  "BLACK": (0.0, 0.0, 0.0, 1.0),
            "BLUE": (0.0, 0.0, 0.4, 1.0),
            "PINK": (0.4, 0.0, 0.3, 1.0),
            "GREEN": (0.0, 0.3, 0.0, 1.0),
            "RED": (0.4, 0.0, 0.0, 1.0),
            "YELLOW": (0.6, 0.6, 0.0, 1.0),
            "WHITE": (0.8, 0.8, 0.8, 1.0),
            "GRAY": (0.1, 0.1, 0.1, 1.0),
            "LIGHTGRAY": (0.5, 0.5, 0.5, 1.0),
            "ORANGE": (0.8, 0.16, 0.0, 1.0) }

# Properties of the available material textures.
textures = [ {"name": "Asphalt",    "scale": 0.035*scene.ground_plane_size, "light_correction": 0.0},
             {"name": "Porcelain",  "scale": 0.025*scene.ground_plane_size, "light_correction": -0.1},
             {"name": "Metal",      "scale": 0.025*scene.ground_plane_size, "light_correction": 0.2} ]


def clearShaderNodes(mat : bpy.types.Material) -> None:
    """Clears all the existing shader nodes and links of the material."""

    mat.use_nodes = True
    mat.node_tree.nodes.clear()
    mat.node_tree.links.clear()


# Custom shaders

def applyBase(mat : bpy.types.Material,
              color : List[float],
              randomize : bool = False) -> None:
    """Apply a generic material to mat. (for the ground object)
    
    Params:
        mat: The material to apply the shaders to.
        color: The base color of the material (R,G,B,A).
        randomize: Randomize material params.
    """

    # Clear nodes and links
    clearShaderNodes(mat)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")

    # Connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_bump.outputs["Normal"], node_principled.inputs["Normal"])
    links.new(node_noise.outputs["Fac"], node_bump.inputs["Height"])

    # Noise texture shader params
    node_noise.inputs["Scale"].default_value = 8000.0 + int(randomize)*random.uniform(0.0, 4000.0)
    node_noise.inputs["Roughness"].default_value = 0.0
    
    # Bump shader params
    node_bump.inputs["Strength"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.1)
    node_bump.inputs["Distance"].default_value = 0.03 + int(randomize)*random.uniform(0.0, 0.04)
    
    # Principled shader params
    if randomize:
        node_principled.inputs["Base Color"].default_value = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 1.0)
    else:
        node_principled.inputs["Base Color"].default_value = color

    node_principled.inputs["Specular"].default_value = 0.2 + random.uniform(0.0, 0.2)
    node_principled.inputs["Roughness"].default_value = 0.3 + random.uniform(0.0, 0.2)
    node_principled.inputs["Clearcoat"].default_value = 0.0 + random.uniform(0.0, 0.2)
    node_principled.inputs["Clearcoat Roughness"].default_value = 0.1 + random.uniform(0.0, 0.1)
    node_principled.inputs["Emission Strength"].default_value = 0.0


def applyPlastic(mat : bpy.types.Material,
                 color : List[float],
                 surface : str,
                 randomize : bool,
                 textures_path : str,
                 tex_defect : str = None,
                 gloss_defect : bool = False,
                 discoloration : bool = False) -> None:
    """Applies a matte looking plastic material to mat with slightly random parameters and possible defects.
    
    Params:
        mat: The material to apply the shaders to.
        color: The base color of the material (R, G, B, A).
        surface: The type of the plastics surface (one of "Rough", "Matte", or "Shiny").
        randomize: Randomize material params.
        textures_path: The directory which contains the textures used for the defects.
        tex_defect: Possible texture defects (one of "contamination", "splay", or "cloudy").
        gloss_defect: Apply gloss defect to the material if True.
        discoloration: Apply discoloration defect to the material if True.
    """

    clearShaderNodes(mat)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")
    node_bump = nodes.new(type = "ShaderNodeBump")
    node_noise = nodes.new(type = "ShaderNodeTexNoise")

    # Connect shader nodes
    links.new(node_principled.outputs["BSDF"], node_output.inputs["Surface"])
    links.new(node_bump.outputs["Normal"], node_principled.inputs["Normal"])
    links.new(node_noise.outputs["Fac"], node_bump.inputs["Height"])

    # Noise texture params
    if surface == "Matte":
        node_noise.inputs["Scale"].default_value = 2000.0
        node_noise.inputs["Roughness"].default_value = 0.0
    elif surface == "Rough":
        node_noise.inputs["Scale"].default_value = 350.0
        node_noise.inputs["Roughness"].default_value = 1.0
        node_noise.inputs["Distortion"].default_value = 0.4
    elif surface == "Shiny":
        node_noise.inputs["Scale"].default_value = 1000.0
        node_noise.inputs["Roughness"].default_value = 0.0
    else:
        raise ValueError("Invalid surface type.")
    
    # Bump shader params
    if surface == "Matte":
        node_bump.inputs["Strength"].default_value = 0.1 + int(randomize)*random.uniform(0.0, 0.05)
        node_bump.inputs["Distance"].default_value = 0.1 + int(randomize)*random.uniform(0.0, 0.05)
    elif surface == "Rough":
        node_bump.inputs["Strength"].default_value = 1.5 + int(randomize)*random.uniform(0.0, 1.0)
        node_bump.inputs["Distance"].default_value = 0.2 + int(randomize)*random.uniform(0.0, 0.1)
    elif surface == "Shiny":
        node_bump.inputs["Strength"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.05)
        node_bump.inputs["Distance"].default_value = 0.1 + int(randomize)*random.uniform(0.0, 0.05)
    else:
        raise ValueError("Invalid surface type.")
   
    # Principled shader params
    node_principled.distribution = "MULTI_GGX"
    node_principled.inputs["Base Color"].default_value = color
    if surface == "Matte":
        node_principled.inputs["Specular"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.08)
        node_principled.inputs["Roughness"].default_value = 0.5 + int(randomize)*random.uniform(0.0, 0.15)
        node_principled.inputs["Anisotropic"].default_value = 0.2
        node_principled.inputs["Clearcoat"].default_value = 0.1 + int(randomize)*random.uniform(0.0, 0.15)
        node_principled.inputs["Clearcoat Roughness"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.05)
        node_principled.inputs["Emission Strength"].default_value = 0.0
    elif surface == "Rough":
        node_principled.inputs["Specular"].default_value = 0.1
        node_principled.inputs["Roughness"].default_value = 0.5 + int(randomize)*random.uniform(0.0, 0.2)
        node_principled.inputs["Anisotropic"].default_value = 0.0
        node_principled.inputs["Clearcoat"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.1)
        node_principled.inputs["Clearcoat Roughness"].default_value = node_principled.inputs["Roughness"].default_value + 0.05
        node_principled.inputs["Emission Strength"].default_value = 0.0
    elif surface == "Shiny":
        node_principled.inputs["Specular"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.1)
        node_principled.inputs["Roughness"].default_value = 0.2 + int(randomize)*random.uniform(0.0, 0.1)
        node_principled.inputs["Anisotropic"].default_value = 0.2
        node_principled.inputs["Clearcoat"].default_value = 0.4 + int(randomize)*random.uniform(0.0, 0.3)
        node_principled.inputs["Clearcoat Roughness"].default_value = node_principled.inputs["Roughness"].default_value - 0.05
        node_principled.inputs["Emission Strength"].default_value = 0.0
    else:
        raise ValueError("Invalid surface type.")

    # Adjust principled shader for the gloss defect.
    if gloss_defect:
        # Principled shader params
        node_principled.inputs["Specular"].default_value = 0.025 + int(randomize)*random.uniform(0.0, 0.05)
        node_principled.inputs["Anisotropic"].default_value = 0.0
        node_principled.inputs["Clearcoat"].default_value = 0.05 + int(randomize)*random.uniform(0.0, 0.1)
        node_principled.inputs["Clearcoat Roughness"].default_value = 0.5 + int(randomize)*random.uniform(0.0, 0.25)
        node_principled.inputs["Roughness"].default_value = node_principled.inputs["Clearcoat Roughness"].default_value + 0.05

        # Noise texture params
        node_noise.inputs["Scale"].default_value = 185.0 + int(randomize)*random.uniform(0.0, 75.0)
        node_noise.inputs["Roughness"].default_value = 1.0
        node_noise.inputs["Distortion"].default_value = 0.5

        # Bump shader params
        node_bump.inputs["Strength"].default_value = 1.5 + int(randomize)*random.uniform(0.0, 1.0)
        node_bump.inputs["Distance"].default_value = 0.25 + int(randomize)*random.uniform(0.0, 0.15)

    # Texture defects
    if tex_defect in ("contamination", "splay", "cloudy"):
        # Add new nodes
        node_coord = nodes.new(type = "ShaderNodeTexCoord")
        node_mapping = nodes.new(type = "ShaderNodeMapping")
        node_color = nodes.new(type = "ShaderNodeTexImage")
        node_add = nodes.new(type = "ShaderNodeMath")

        # Node default values
        node_add.inputs[1].default_value = 0.0

        # Create links
        links.new(node_coord.outputs["Object"], node_mapping.inputs["Vector"])
        links.new(node_mapping.outputs["Vector"], node_color.inputs["Vector"])
        links.new(node_color.outputs["Color"], node_add.inputs[0])
        links.new(node_add.outputs["Value"], node_principled.inputs["Base Color"])

    if tex_defect == None:
        pass

    elif tex_defect == "contamination":
        # Node params
        node_color.image = bpy.data.images.load(path.join(textures_path, "Contamination.png"), check_existing = True)
        node_mapping.inputs["Scale"].default_value[0] = 0.01 + int(randomize)*random.uniform(0.0, 0.005)
        node_mapping.inputs["Scale"].default_value[1] = 0.01 + int(randomize)*random.uniform(0.0, 0.005)
        node_mapping.inputs["Scale"].default_value[2] = 0.01 + int(randomize)*random.uniform(0.0, 0.005)
        node_mapping.inputs["Location"].default_value[0] = 0.0 + int(randomize)*random.uniform(-2.0, 2.0)
        node_mapping.inputs["Location"].default_value[1] = 0.0 + int(randomize)*random.uniform(-2.0, 2.0)
        node_mapping.inputs["Rotation"].default_value[2] = 0.0 + int(randomize)*random.uniform(0.0, 2*math.pi)
    
    elif tex_defect == "splay":
        # Node params
        node_color.image = bpy.data.images.load(path.join(textures_path, "Splay.png"), check_existing = True)
        node_mapping.inputs["Scale"].default_value[0] = 0.04 + int(randomize)*random.uniform(0.0, 0.003)
        node_mapping.inputs["Scale"].default_value[1] = 0.08 + int(randomize)*random.uniform(0.0, 0.004)
        node_mapping.inputs["Scale"].default_value[2] = 1.0
        node_mapping.inputs["Location"].default_value[0] = 0.0 + int(randomize)*random.uniform(-1.0, 1.0)
        node_mapping.inputs["Location"].default_value[1] = 0.0 + int(randomize)*random.uniform(-1.0, 1.0)
        node_mapping.inputs["Rotation"].default_value[2] = 90*math.pi/180

    elif tex_defect == "cloudy":
        # Node params
        node_mapping.inputs["Location"].default_value[0] = 0.0 + int(randomize)*random.uniform(0.0, 1.0)
        node_mapping.inputs["Location"].default_value[1] = 0.0 + int(randomize)*random.uniform(0.0, 1.0)
        node_mapping.inputs["Rotation"].default_value[2] = 0.0 + int(randomize)*random.uniform(0.0, 2*math.pi)
        if (random.random() > 0.5):
            node_color.image = bpy.data.images.load(path.join(textures_path, "Cloudy1.png"), check_existing = True)
            node_mapping.inputs["Scale"].default_value[0] = 0.03 + int(randomize)*random.uniform(0.0, 0.02)
            node_mapping.inputs["Scale"].default_value[1] = 0.03 + int(randomize)*random.uniform(0.0, 0.02)
            node_mapping.inputs["Scale"].default_value[2] = 0.03 + int(randomize)*random.uniform(0.0, 0.02)
        else:
            node_color.image = bpy.data.images.load(path.join(textures_path, "Cloudy2.png"), check_existing = True)
            node_mapping.inputs["Scale"].default_value[0] = 0.008 + int(randomize)*random.uniform(0.0, 0.017)
            node_mapping.inputs["Scale"].default_value[1] = 0.008 + int(randomize)*random.uniform(0.0, 0.017)
            node_mapping.inputs["Scale"].default_value[2] = 0.008 + int(randomize)*random.uniform(0.0, 0.017)

    else:
        raise ValueError("Invalid texture defect. " + tex_defect)

    # Discoloration defect
    if discoloration:
        # Base color
        color_low, color_high = 0.2, 0.8
        clr = color_low + random.expovariate(250.0) % (color_high - color_low)

        node_principled.inputs["Base Color"].default_value = (clr, clr, clr, 1.0)

        # Texture color if used
        if tex_defect != None:
            tex_low, tex_high = 0.03, 0.5
            node_add.inputs[1].default_value = tex_low + random.expovariate(250.0) % (tex_high - tex_low)


# Texture based shaders

def applyTextures(mat : bpy.types.Material,
                  textures_path : str,
                  texture_name : str,
                  scale : float = 500.0) -> None:
    """Apply material using textures to mat.
    
    Params:
        mat: The material to apply the shaders to.
        textures_path: The filepath of the directory which contains the different texture files.
        texture_name: The name of the textures to use. Must be a valid texture folder name in the textures_path directory.
        scale: The scale for the textures used.
    """

    # Clear links and nodes
    clearShaderNodes(mat)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Create shader nodes
    node_output = nodes.new(type = "ShaderNodeOutputMaterial")
    node_principled = nodes.new(type = "ShaderNodeBsdfPrincipled")

    node_color = nodes.new(type = "ShaderNodeTexImage")
    node_displacement_t = nodes.new(type = "ShaderNodeTexImage")
    node_normal = nodes.new(type = "ShaderNodeTexImage")
    node_roughness = nodes.new(type = "ShaderNodeTexImage")

    node_displacement = nodes.new(type = "ShaderNodeDisplacement")
    node_coord = nodes.new(type = "ShaderNodeTexCoord")
    node_mapping = nodes.new(type = "ShaderNodeMapping")

    # Connect shader nodes
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

    # Inputs
    node_principled.inputs["Specular"].default_value = 0.33
    node_principled.inputs["Anisotropic"].default_value = 0.0
    node_principled.distribution = "MULTI_GGX"
    node_displacement.inputs["Scale"].default_value = 0.05
    node_mapping.inputs["Scale"].default_value = (scale, scale, scale)

    # Textures
    texture_path = path.join(textures_path, texture_name)
    if not path.exists(texture_path):
        raise ValueError("Invalid texture name.")

    # Basic textures
    node_color.image = bpy.data.images.load(path.join(texture_path, "Color.png"), check_existing = True)
    node_displacement_t.image = bpy.data.images.load(path.join(texture_path, "Displacement.png"), check_existing = True)
    node_normal.image = bpy.data.images.load(path.join(texture_path, "Normal.png"), check_existing = True)
    node_roughness.image = bpy.data.images.load(path.join(texture_path, "Roughness.png"), check_existing = True)

    # Metal texture if metallic
    metal_tex_path = path.join(texture_path, "Metalness.png")
    if path.exists(metal_tex_path):
        node_metalness = nodes.new(type = "ShaderNodeTexImage")
        node_metalness.image = bpy.data.images.load(metal_tex_path, check_existing = True)

        links.new(node_metalness.outputs["Color"], node_principled.inputs["Metallic"])
        links.new(node_mapping.outputs["Vector"], node_metalness.inputs["Vector"])


def applyRandomTextures(mat : bpy.types.Material,
                        textures_path : str) -> dict:
    """Apply a material using a random texture to mat.

    Params:
        mat: The material to apply the shaders to.
        textures_path: The filepath of the directory which contains the different texture files.
    Returns:
        The selected texture from textures.
    """
    
    idx = random.randrange(len(textures))
    texture = textures[idx]
    applyTextures(mat, textures_path, texture["name"], texture["scale"])

    return texture