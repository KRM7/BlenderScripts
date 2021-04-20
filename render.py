import bpy

def cyclesRender(filepath, samples = 64, bounces = 32, denoising = False):
    #renders an image using the cycles render engine

    #select cycles
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    
    #device settings
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "CUDA"
    cuda, opencl = prefs.get_devices()
    if cuda:
        scene.cycles.device = "GPU"
    for device in prefs.devices:
        device["use"] = 1
    scene.cycles.feature_set = "EXPERIMENTAL"

    #render settings
    scene.cycles.samples = samples
    scene.cycles.max_bounces = bounces
    scene.cycles.debug_use_spatial_splits = True
    scene.render.tile_x = 128
    scene.render.tile_y = 128
    scene.cycles.volume_max_steps = 32
    scene.cycles.volume_step_rate = 1.0
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.0
    
    #img settings
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    scene.render.filepath = filepath
    
    #denoiser settings
    if denoising:
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = "OPTIX"
        scene.denoising_optix_input_passes = "RGB_ALBEDO_NORMAL"
    else:
        scene.cycles.use_denoising = False

    bpy.ops.render.render(write_still = True)


def eeveeRender(filepath, samples = 64):
    #renders an image using the eevee render engine

    #select eevee
    scene = bpy.context.scene
    scene.render.engine  = "BLENDER_EEVEE"

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
    
    #img settings
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    scene.render.filepath = filepath

    bpy.ops.render.render(write_still = True)