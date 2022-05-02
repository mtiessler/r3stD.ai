# A simple script that uses blender to render views of a single object by rotation the camera around it.
# Also produces depth map at the same time.

import os
import json
import bpy
import mathutils
import numpy as np
         
DEBUG = False
            
VIEWS = 150
RESOLUTION = 800
RESULTS_PATH = 'images'
DEPTH_SCALE = 1.4
COLOR_DEPTH = 8
FORMAT = 'PNG'
UPPER_VIEWS = True
CIRCLE_FIXED_START = (-1.13278, 1.871, 1.1873)
CIRCLE_FIXED_END = (-0.4, 1.871, 1.1873)


fp =  bpy.path.abspath(f"//{RESULTS_PATH}")


def listify_matrix(matrix):
    matrix_list = []
    for row in matrix:
        matrix_list.append(list(row))
    return matrix_list

if not os.path.exists(fp):
    os.makedirs(fp)

# Data to store in JSON file
out_data = {
    'camera_angle_x': bpy.data.objects['Camera'].data.angle_x,
}

# Render Optimizations
bpy.context.scene.render.use_persistent_data = True


# Set up rendering of depth map.
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

# Add passes for additionally dumping albedo and normals.
bpy.context.scene.view_layers["RenderLayer"].use_pass_normal = True
bpy.context.scene.render.image_settings.file_format = str(FORMAT)
bpy.context.scene.render.image_settings.color_depth = str(COLOR_DEPTH)

# Background
bpy.context.scene.render.dither_intensity = 0.0
bpy.context.scene.render.film_transparent = True

# Create collection for objects not to render with background

    
objs = [ob for ob in bpy.context.scene.objects if ob.type in ('EMPTY') and 'Empty' in ob.name]
bpy.ops.object.delete({"selected_objects": objs})

def parent_obj_to_camera(b_camera):
    origin = CIRCLE_FIXED_START
    b_empty = bpy.data.objects.new("Empty", None)
    b_empty.location = origin
    b_camera.parent = b_empty  # setup parenting

    scn = bpy.context.scene
    scn.collection.objects.link(b_empty)
    bpy.context.view_layer.objects.active = b_empty
    # scn.objects.active = b_empty
    return b_empty


scene = bpy.context.scene
scene.render.resolution_x = RESOLUTION
scene.render.resolution_y = RESOLUTION
scene.render.resolution_percentage = 100

cam = scene.objects['Camera']
cam.location = (0, -0.7, 0.0)
cam_constraint = cam.constraints.new(type='TRACK_TO')
cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
cam_constraint.up_axis = 'UP_Y'
b_empty = parent_obj_to_camera(cam)
cam_constraint.target = b_empty

scene.render.image_settings.file_format = 'PNG'  # set output format to .png

from math import radians

stepsize = 2* 360.0 / VIEWS
vertical_diff = 0
rotation_mode = 'XYZ'


out_data['frames'] = []

for i in range(0, VIEWS):
   
    print("Rotation {}, {}".format((stepsize * i), radians(stepsize * i)))
    scene.render.filepath = fp + '/r_' + str(i)
    
    bpy.ops.render.render(write_still=True)  # render still

    frame_data = {
        'file_path': 'images/'+scene.render.filepath.split("/")[-1],
        'rotation': radians(stepsize),
        'transform_matrix': listify_matrix(cam.matrix_world)
    }
    out_data['frames'].append(frame_data)
    
    vec_size = 0.5 * (stepsize * (i+1)) / 720
    vec_x = np.sin(radians(stepsize*i)) * vec_size
    vec_y = np.cos(radians(stepsize*i)) * vec_size
    
    b_empty.location = (CIRCLE_FIXED_START[0] + vec_x, CIRCLE_FIXED_START[1], CIRCLE_FIXED_START[2] + vec_y)

    ##b_empty.rotation_euler[0] = CIRCLE_FIXED_START[0] + (np.cos(radians(stepsize*i))+1)/2 * vertical_diff
    ##b_empty.rotation_euler[2] += radians(2*stepsize)

if not DEBUG:
    with open(fp + '/' + 'transforms.json', 'w') as out_file:
        json.dump(out_data, out_file, indent=4)
