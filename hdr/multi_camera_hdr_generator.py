import bpy
from mathutils import Vector

bl_info = {
    "name": "augmero - multi_camera_hdr_generator.py",
    "description": "automates hdr generation",
    "author": "augmero",
    "version": (0, 3),
    "blender": (3, 5, 1),
    "tracker_url": "https://twitter.com/augmero_nsfw",
    "doc_url": "https://github.com/augmero/augmero-blender-script-dump",
    "support": "TESTING",
    "category": "Render",
}


def get_cameras():
    # get all cameras in the scene
    cameras = [obj for obj in bpy.context.scene.objects if obj.type == 'CAMERA']
    # only render an hdr for the cameras in this list
    camera_list = [
        "Camera.006",
    ]
    cameras = [cam for cam in cameras if cam.name in camera_list]
    return cameras


def generate_hdr_locations(cameras):
    # generate hdr rendering locations
    hdr_locations = bpy.data.collections.get('hdr_locations')
    if not hdr_locations:
        print('hdr_locations collection required')
        return

    # iterate through each camera and generate the hdr render location
    for cam in cameras:
        actual_camera = cam.data
        if not actual_camera:
            print(f'{cam.name}: no actual camera')
            continue

        empty_name = cam.name + "_hdr_loc"
        print(empty_name)
        empty = bpy.data.objects.get(empty_name)
        print(empty)
        if not empty:
            print('making new empty')
            empty = bpy.data.objects.new(empty_name, None)  # Create new empty object
            hdr_locations.objects.link(empty)
        empty.location = cam.location
        empty.rotation_euler = cam.rotation_euler
        empty.empty_display_type = 'SPHERE'
        empty.empty_display_size = .1

        focal_length = actual_camera.lens
        print(f'focal length - {focal_length}')

        sensor_width = actual_camera.sensor_width
        
        # 35mm with default 36mm sensor is approx .97m distance
        # 100mm with default 36mm is approx 2.78m distance
        distance = focal_length/sensor_width
        distance = distance - 0.9722222222222222
        if distance < 0:
            distance = 0
        print(distance)

        orientation = cam.rotation_euler.to_matrix()

        # calculate the direction the camera is facing
        direction = orientation @ Vector((0, 0, -1))

        # move the empty in the direction the camera is facing
        new_location = cam.location + direction * distance
        empty.location = new_location


def render_all(cameras, main_camera):
    original_filepath = bpy.context.scene.render.filepath

    # iterate through each camera and render and save an image
    for cam in cameras:
        # get the Copy Location constraint
        constraint = main_camera.constraints['Copy Location']

        empty_name = cam.name + "_hdr_loc"
        empty = bpy.data.objects.get(empty_name)
        if not empty:
            print(f'{cam.name} hdr location not found')
            continue

        # set the target of the constraint
        constraint.target = empty

        # set the filename based on the camera's name
        filename = f"{cam.name}.png"
        filepath = original_filepath+filename
        bpy.context.scene.render.filepath = filepath

        # render the image
        bpy.ops.render.render(write_still=True)

        print(f"Rendered and saved {filename}")

    bpy.context.scene.render.filepath = original_filepath


def multi_camera_hdr_generator():
    main_camera_name = "main camera"
    main_camera = bpy.data.objects.get(main_camera_name)
    if not main_camera:
        print('no main camera, exiting')
        return
    cameras = get_cameras()
    generate_hdr_locations(cameras)
    render_all(cameras, main_camera)


multi_camera_hdr_generator()

