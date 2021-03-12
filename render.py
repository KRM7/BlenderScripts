import bpy

def cyclesRender(filepath, samples = 22, bounces = 16, denoising = False):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "GPU"
    scene.cycles.feature_set = "EXPERIMENTAL"
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
    #denoising
    if denoising:
        #TODO denoiser settings
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = "OPTIX"
    else:
        scene.cycles.use_denoising = False

    bpy.ops.render.render(write_still = True)

def eeveeRender(filepath, samples = 64):
    scene = bpy.context.scene
    scene.render.engine  = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = samples
    #ambient occlusion
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 50.0
    scene.eevee.gtao_factor = 0.4
    #screen space reflections
    scene.eevee.use_ssr = True
    scene.eevee.ssr_quality = 1.0
    scene.eevee.ssr_max_roughness = 1.0
    scene.eevee.ssr_thickness = 0.1
    scene.eevee.ssr_border_fade = 0.1
    #shadows
    scene.eevee.shadow_cube_size = "4096"
    scene.eevee.shadow_cascade_size = "256"
    scene.eevee.use_shadow_high_bitdepth = True
    scene.eevee.use_soft_shadows = True
    scene.eevee.light_threshold = 0.01
    #indirect lighting
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