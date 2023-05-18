import bpy

bl_info = {
    "name": "augmero - remove_enabled_csmooths.py",
    "description": "removes csmooths created by csmooth_over_time.py",
    "author": "augmero",
    "version": (0, 3),
    "blender": (3, 5, 1),
    "tracker_url": "https://twitter.com/augmero_nsfw",
    "doc_url": "https://github.com/augmero/augmero-blender-script-dump",
    "support": "TESTING",
    "category": "Animation",
}


# delete all enabled corrective smooth modifiers and their associated keyframes
# delete csmooth modifiers and keyframes created by csmooth_over_time.py

active_object = bpy.context.view_layer.objects.active

for modifier in active_object.modifiers:
    if modifier.type == 'CORRECTIVE_SMOOTH' and modifier.show_render == True and 'ScriptCorrectiveSmooth' in modifier.name:
        # delete modifier
        active_object.modifiers.remove(modifier)
        continue

    # remove keyframes
    for fcurve in active_object.animation_data.action.fcurves:
        if "ScriptCorrectiveSmooth" in fcurve.data_path:
            active_object.animation_data.action.fcurves.remove(fcurve)
