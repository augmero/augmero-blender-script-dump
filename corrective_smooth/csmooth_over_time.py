import bpy
import uuid

bl_info = {
    "name": "augmero - csmooth_over_time.py",
    "description": "automates corrective smoothing over time",
    "author": "augmero",
    "version": (0, 3),
    "blender": (3, 5, 1),
    "tracker_url": "https://twitter.com/augmero_nsfw",
    "doc_url": "https://github.com/augmero/augmero-blender-script-dump",
    "support": "TESTING",
    "category": "Animation",
}


# add corrective smooth modifiers for playback range +1 in interval

scene = bpy.context.scene
frame_start = scene.frame_start
frame_end = scene.frame_end

# how many frames between binding another csmooth modifier
interval = 20
# how many smoothing iterations will each csmooth modifier do maximum
smooth_iterations_peak = 10
# what vertex group to apply the csmooth modifier to
vertex_group = "manif"

active_object = bpy.context.view_layer.objects.active
bootleg_hash = str(uuid.uuid4()).split('-')[0]


def corrective_modifier(object, origin_frame, interval, vertex_group):
    corrective_modifier_name = f"ScriptCorrectiveSmooth {origin_frame} {bootleg_hash}"
    corrective = object.modifiers.new(corrective_modifier_name, "CORRECTIVE_SMOOTH")
    corrective.vertex_group = vertex_group
    corrective.rest_source = "BIND"
    corrective.iterations = smooth_iterations_peak
    bpy.ops.object.correctivesmooth_bind(modifier=corrective_modifier_name)
    corrective.keyframe_insert(data_path='iterations', frame=origin_frame)
    corrective.iterations = 0
    corrective.keyframe_insert(data_path='iterations', frame=origin_frame-interval)
    corrective.iterations = 0
    corrective.keyframe_insert(data_path='iterations', frame=origin_frame+interval)
    return True


framer = frame_start
scene.frame_set(framer)
corrective_modifier(active_object, framer, interval, vertex_group)
while framer < frame_end:
    framer = framer + interval
    scene.frame_set(framer)
    corrective_modifier(active_object, framer, interval, vertex_group)

# disable in viewport for performance
for modifier in active_object.modifiers:
    if modifier.type == 'CORRECTIVE_SMOOTH' and 'ScriptCorrectiveSmooth' in modifier.name:
        modifier.show_viewport = False
        continue
