import bpy


bl_info = {
    "name": "augmero - camera_switch_handler.py",
    "description": "switches hdr and collection visibility relevant to active camera",
    "author": "augmero",
    "version": (0, 3),
    "blender": (3, 5, 1),
    "tracker_url": "https://twitter.com/augmero_nsfw",
    "doc_url": "https://github.com/augmero/augmero-blender-script-dump",
    "support": "TESTING",
    "category": "Render",
}


hdr_folder = "F:\\Blender stuff\\Projects\\ProjectA\\scene hdr"

csh_stored_camera = None


def set_collection_visibility(name, visibile):
    collection = bpy.data.collections.get(name)
    if collection:
        collection.hide_render = not visibile
        collection.hide_viewport = not visibile


def hide_other_cameras(active_camera):
    cameras = [obj for obj in bpy.context.scene.objects if obj.type == 'CAMERA']
    for cam in cameras:
        set_collection_visibility(cam.name, False)
    set_collection_visibility(active_camera.name, True)


def update_world_texture(scene):
    active_camera = bpy.context.scene.camera

    if active_camera:
        # get the image texture node in the world shader
        world = bpy.context.scene.world
        image_node = world.node_tree.nodes.get('world_hdr')
        if not image_node:
            print('world hdr not found, cannot set active camera world hdr')
            return
        filepath = hdr_folder + active_camera.name + '.hdr'
        print(filepath)
        image_name = f"{active_camera.name}.hdr"
        image = bpy.data.images.get(image_name)
        if not image:
            image = bpy.data.images.load(f"{hdr_folder}\\{active_camera.name}.hdr")
        # set the file name to the name of the active camera

        image_node.image = image


def observe_camera_change(scene):
    global csh_stored_camera
    active_camera = bpy.context.scene.camera
    if not active_camera:
        print('No active camera')
        return
    if csh_stored_camera == active_camera:
        print('Camera did not change')
        return

    print(f'Camera changed from {csh_stored_camera} to {active_camera}')
    csh_stored_camera = active_camera
    update_world_texture(scene)
    hide_other_cameras(active_camera)


def force_camera_change(scene):
    global csh_stored_camera
    csh_stored_camera = None
    observe_camera_change(scene)


# register the update function to be called when the active camera changes
bpy.app.handlers.depsgraph_update_post.append(observe_camera_change)
bpy.app.handlers.render_pre.append(observe_camera_change)
