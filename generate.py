"""Blender 2.91

This script generates the images based on the config settings.
"""

import bpy, mathutils

import sys
project_path = sys.argv[sys.argv.index("--") + 1]
sys.path.append(project_path)

import os
import math
import random
import time
import configparser
import csv
import numpy as np
import haircomb, scene, shaders, render, utils, defects


config = configparser.ConfigParser()
config.read(os.path.join(project_path, "config.ini"))


# Clear everything in the scene
bpy.ops.object.select_all(action = "SELECT")
bpy.ops.object.delete()
utils.removeMeshes()
utils.removeMaterials()
utils.removeLights()
utils.removeCameras()

# Set the render settings based on the config
if config["Render"]["engine"] == "cycles":
    render.setupCycles(samples = int(config["Render"]["samples"]),
                       bounces = int(config["Render"]["bounces"]),
                       tile_size = int(config["Render"]["tile_size"]),
                       denoising = config["Render"]["denoise"] == "True")
elif config["Render"]["engine"] == "eevee":
    render.setupEevee(samples = int(config["Render"]["samples"]))
else:
    raise ValueError("Invalid render engine: " + str(config["Render"]["engine"]))


# Set the output image settings based on the config
render.setImageSettings(res_x = int(config["Image"]["resolution_x"]),
                        res_y = int(config["Image"]["resolution_y"]),
                        color = config["Image"]["color"] == "True")


# Setup the environment (the parts which won't change between images)
# Ground (only the shaders change between images, the object doesn't)
ground_mat = bpy.data.materials.new(name = "ground")
bpy.ops.mesh.primitive_plane_add(size = scene.ground_plane_size)
ground = bpy.context.object
ground.data.materials.append(ground_mat)

# World/environment
world = bpy.context.scene.world
if config["Lights"]["use_hdris"] == "True":
    node_env = world.node_tree.nodes.new(type = "ShaderNodeTexEnvironment")
    world.node_tree.links.new(node_env.outputs["Color"], world.node_tree.nodes["Background"].inputs["Color"])

# Setup for the defect combination generator
defect_gen = defects.Defects(config["Object"]["enable_missing_teeth"] == "True",
                              config["Object"]["enable_bent_teeth"] == "True",
                              config["Object"]["enable_warping"] == "True",
                              config["Object"]["enable_ejector_marks"] == "True",
                              config["Object"]["enable_gloss"] == "True",
                              config["Object"]["enable_discoloration"] == "True",
                              config["Object"]["enable_contamination"] == "True",
                              config["Object"]["enable_cloudy"] == "True",
                              config["Object"]["enable_splay"] == "True",
                              int(config["Object"]["num_ejector_marks"]))


# Index file
# Either create a new index or if it already exists, append new images
img_name, img_cntr = 0, 0   # img_name is not the same as the img_cntr if there are already images in the output directory and we are adding more
index_filepath = os.path.join(config["Output"]["output_path"], "index.csv")

append_index = os.path.isfile(index_filepath) and config["Output"]["overwrite"] != "True"
if append_index:
    index_file = open(index_filepath, "r")
    img_name = sum(1 for line in index_file)
    index_file.close()

if append_index:
    index_file = open(index_filepath, "a+", newline = "")
    index_writer = csv.writer(index_file)
else:
    index_file = open(index_filepath, "w", newline = "")
    index_writer = csv.writer(index_file)
    index_writer.writerow(["Filenames", "missing_teeth", "bent_teeth", "warped", "ejector_marks", "low_gloss", "discoloration", "contamination", "cloudy", "splay"])

# The overall number of images to generate, and the number of images to generate of 1 object before creating a new object model.
num_imgs = int(config["Output"]["num_imgs"])
imgs_per_object = int(config["Output"]["imgs_per_object"])

for _ in range(int(num_imgs/imgs_per_object)):
    
    # Delete the haircomb if it already exists
    if "hc" in locals():
        bpy.data.objects.remove(hc.getObject())

    # Generate a new defect combination
    defect_gen.updateDefectCombination()
    
    # Create the haircomb with defects if needed
    hc = haircomb.Haircomb(missing_teeth = defect_gen.missing_teeth,
                           bent_teeth = defect_gen.bent_teeth,
                           warping = defect_gen.warping,
                           ejector_marks = defect_gen.ejector_marks)
    hc.createHaircomb()

    # Generate images of the haircomb
    for _ in range(imgs_per_object):

        # Add random materials to the objects in the scene.
        tex_path = os.path.join(project_path, "textures")
        # Apply the plastic texture to the object.
        shaders.applyPlastic(mat = hc.getMaterial(),
                             color = (0.0, 0.0, 0.0, 1.0),
                             surface = config["Object"]["surface"],
                             randomize = config["Object"]["randomize"] == "True",
                             textures_path = tex_path,
                             tex_defect = defect_gen.tex_defect,
                             gloss_defect = defect_gen.gloss,
                             discoloration = defect_gen.discoloration)

        # Apply a random material texture to the ground plane.
        ground_texture = shaders.applyRandomTextures(ground_mat, tex_path)
    

        # Camera setup (so that the object is always in the frame).
        scene.removeCameras()

        coords = hc.getBoundingBox()
        coords = utils.randomExtendBoundingBox(bounding_box = coords,
                                               max_x = hc.width*float(config["Camera"]["extend_x"]),
                                               max_y = hc.width*float(config["Camera"]["extend_y"]))

        camera = scene.placeCamera(coords,
                                   max_view_angle_x = float(config["Camera"]["max_view_angle_x"]),
                                   max_view_angle_y = float(config["Camera"]["max_view_angle_y"]),
                                   max_roll_angle = float(config["Camera"]["max_roll_angle"]))


        # Lighting setup
        if config["Lights"]["use_hdris"] == "True":
            hdri = random.choice(scene.hdris)
            hdri_path = os.path.join(project_path, "hdris", hdri["name"])

            node_env.image = bpy.data.images.load(hdri_path, check_existing = True)
            world.node_tree.nodes["Background"].inputs["Strength"].default_value = random.uniform(hdri["light_min"], hdri["light_max"])
            # Adjust HDRI light strength based on the ground textures
            world.node_tree.nodes["Background"].inputs["Strength"].default_value += ground_texture["light_correction"]
        else:
            scene.removeLights()
            scene.placeLights(num_lights = int(config["Lights"]["num_lights"]),
                              height_min = float(config["Lights"]["height_min"]),
                              height_max = float(config["Lights"]["height_max"]),
                              hdistance_min = float(config["Lights"]["distance_min"]),
                              hdistance_max = float(config["Lights"]["distance_max"]),
                              strength_min = float(config["Lights"]["strength_min"]),
                              strength_max = float(config["Lights"]["strength_max"]))


        # Render and save the image
        img_path = os.path.join(config["Output"]["output_path"], "imgs", str(img_name) + ".png")
        render.render(img_path)

        # Add the generated image to the index
        index_writer.writerow([img_name, str(int(defect_gen.missing_teeth)), str(int(defect_gen.bent_teeth)), str(int(defect_gen.warping)),
                               str(int(defect_gen.ejector_marks != 0)), str(int(defect_gen.gloss)), str(int(defect_gen.discoloration)),
                               str(int(defect_gen.contamination)), str(int(defect_gen.cloudy)), str(int(defect_gen.splay))])

        print("Image " + str(img_cntr + 1) + "/" + str(num_imgs) + " done.\n")
        img_name += 1
        img_cntr += 1


index_file.close()