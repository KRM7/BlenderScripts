"""Blender 2.91

Functions for rendering images.
"""

import bpy

def setImageSettings(res_x : int = 1920,
                     res_y : int = 1080,
                     color : bool = True) -> None:
    """Sets the properties of the rendered image.

    Params:
        res_x: The horizontal resolution of the output image.
        res_y: The vertical resolution of the output image.
        color: True for color image, False for black-white image.
    Returns:
        None
    """

    scene = bpy.context.scene

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90

    scene.render.image_settings.color_mode = ("RGB" if color else "BW")


def setupCycles(samples : int = 64,
                bounces : int = 32,
                tile_size : int = 128,
                use_adaptive_sampling : bool = True,
                denoising : bool = False) -> None:
    """Sets up the all the settings the cycles render engine. (for the active scene only)

    Params:
        samples: The number of samples rendered for each pixel.
        bounces: The max number of bounces for light particles.
        tile_size: The tile size used while rendering (px).
        use_adaptive_sampling: Reduces the number of samples for less noise pixels.
        denoising: Uses denoiser if True.
    Returns:
        None
    """

    #select the cycles render engine
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"

    #device settings (GPU)
    prefs = bpy.context.preferences.addons["cycles"].preferences
    cuda, opencl = prefs.get_devices()

    if cuda:
        prefs.compute_device_type = "CUDA"
        scene.cycles.device = "GPU"
    elif opencl:
        prefs.compute_device_type = "OPENCL"
        scene.cycles.device = "GPU"
    else:
        prefs.compute_device_type = "NONE"
        scene.cylces.dive = "CPU"
    
    scene.cycles.feature_set = "SUPPORTED" #or EXPERIMENTAL

    for device in prefs.devices:
        device["use"] = 1

    #render settings
    scene.cycles.progressive = "PATH"               #integrator (or BRANCHED_PATH)
    scene.cycles.samples = samples
    scene.cycles.max_bounces = bounces

    scene.render.tile_x = tile_size
    scene.render.tile_y = tile_size
    scene.cycles.debug_use_spatial_splits = False

    scene.cycles.volume_max_steps = 16
    scene.cycles.volume_step_rate = 1.0

    scene.cycles.use_adaptive_sampling = use_adaptive_sampling  #faster render
    scene.cycles.adaptive_threshold = 0.0                       #automatic

    #denoiser settings
    if denoising:
        scene.cycles.use_denoising = True
        if cuda:
            scene.cycles.denoiser = "OPTIX"
            scene.denoising_optix_input_passes = "RGB_ALBEDO_NORMAL"
        else:
            scene.cycles.denoiser = "OPENIMAGEDENOISE"
            scene.denoising_openimagedenoise_input_passes = "RGB_ALBEDO_NORMAL"
    else:
        scene.cycles.use_denoising = False


def render(filepath : str) -> None:
    """Renders the image and saves it to the given filepath.

    Params:
        filepath: The path to save the rendered image to.
    Return:
        None.
    """

    bpy.context.scene.render.filepath = filepath
    bpy.ops.scene.light_cache_bake()
    bpy.ops.render.render(write_still = True)


def setupEevee(samples : int = 64) -> None:
    """Sets up the all the settings the Eevee render engine. (for the active scene only)

    Params:
        samples: The number of samples for each pixel while rendering.
    Returns:
        None.
    """

    #select the Eevee render engine
    scene = bpy.context.scene
    scene.render.engine  = "BLENDER_EEVEE"

    #render settings
    scene.eevee.taa_render_samples = samples
    
    #ambient occlusion settings
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 50.0
    scene.eevee.gtao_factor = 0.4
    
    #screen space reflections settings
    scene.eevee.use_ssr = True
    scene.eevee.ssr_quality = 1.0
    scene.eevee.ssr_max_roughness = 1.0
    scene.eevee.ssr_thickness = 0.1
    scene.eevee.ssr_border_fade = 0.1
    
    #shadow settings
    scene.eevee.shadow_cube_size = "4096"
    scene.eevee.shadow_cascade_size = "256"
    scene.eevee.use_shadow_high_bitdepth = True
    scene.eevee.use_soft_shadows = True
    scene.eevee.light_threshold = 0.01
    
    #indirect lighting settings
    scene.eevee.gi_diffuse_bounces = 8
    scene.eevee.gi_cubemap_resolution = "1024"
    scene.eevee.gi_visibility_resolution = "32"
    bpy.ops.scene.light_cache_bake()