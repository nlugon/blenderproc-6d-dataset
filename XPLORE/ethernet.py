import blenderproc as bproc # make sure this comes first in order to do "python3 cli.py debug ethernet.py"

import bpy
import os
import numpy as np
import json


write_hdf5_file = False
write_bop_pose = True
num_of_poses = 10



# Initialize BlenderProc
bproc.init()

# Path to the STL file
blend_file_path = "/home/noah/BlenderProc/XPLORE/ethernet35.blend"
output_dir = "/home/noah/BlenderProc/XPLORE/output"

# Import the STL file
# bpy.ops.import_mesh.stl(filepath=stl_file_path) # WARNING Avoid using bpy (regular blender) stuff, use bproc (Blenderproc) instead

# Load the STL file as a mesh object thru Blenderproc instead of bpy (bpy->regular blender)
obj = bproc.loader.load_blend(blend_file_path)[0] # obj is the ethernet 
objs = bproc.loader.load_blend(blend_file_path) # obj is the ethernet



# Scale 3D model (WARNING : for realistic depth estimation, scale should be set to 0.001)(here set to )
# ethernet35.blend : was previously scaled down from m to dm -> need to scale down again by 0.001 for mm
obj.set_scale([0.03, 0.03, 0.03])
# Set category id which will be used in the BopWriter
obj.set_cp("category_id", 1)

# LIGHTING ========================================================================================

# Create a point light next to it
light = bproc.types.Light()
light.set_type("POINT")
light.set_location([0.0, 0.0, 4])
light.set_energy(1000)


# CAMERE =========================================================================================
# Set intrinsics via K matrix
bproc.camera.set_intrinsics_from_K_matrix(
    [[537.4799, 0.0, 318.8965],
     [0.0, 536.1447, 238.3781],
     [0.0, 0.0, 1.0]], 640, 480
)
# Set the camera to be in front of the object
cam_pose = bproc.math.build_transformation_mat([0, -2, 0], [np.pi / 2, 0, 0])
bproc.camera.add_camera_pose(cam_pose)


# DEBUG : SAVE PICTURE (WRITE HDF5 FILE)

if(write_hdf5_file): # Do this to vizualize single view
    # Render the scene
    data = bproc.renderer.render()
    # Write the rendering into a hdf5 file
    bproc.writer.write_hdf5("output/", data)


# ADD MULTIPLE CAMERA POSITIONS AROUND THE ETHERNET CABLE WHILE KEEPING ETHERNET CENTERED
# later : add "distractor bop" objects, so that avg of all objects centered, but ethernet no longer exactly in center

# Find point of interest, all cam poses should look towards it
poi = bproc.object.compute_poi(objs)
# Sample five camera poses
for i in range(num_of_poses):
    # Sample random camera location above objects
    location = np.random.uniform([-2, -2, -2], [2, 2, 2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(-0.7854, 0.7854))
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)


# GENERATE DATASET IN BOP FORMAT

if(write_bop_pose):
    # activate normal and depth rendering
    bproc.renderer.enable_normals_output()
    bproc.renderer.enable_depth_output(activate_antialiasing=False)
    # Enable transparency so the background becomes transparent (need this to add random background afterwards)
    bproc.renderer.set_output_format(enable_transparency=True)
    # render the whole pipeline
    data = bproc.renderer.render()
    # Write object poses, color and depth in bop format
    bproc.writer.write_bop(output_dir, [obj], data["depth"], data["colors"], m2mm=True, append_to_existing_output=True)





# Add backgrounds : python3 paste_images_on_backgrounds.py --images output/train_pbr/000000/rgb/ --backgrounds background_images

