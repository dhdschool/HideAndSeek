import distutils.util

import subprocess
import os
import webbrowser
import mujoco

import mediapy as media
import matplotlib.pyplot as plt

# if subprocess.run('nvidia-smi').returncode:
#     raise RuntimeError(
#         'Cannot communicate with GPU. '
#         'Make sure you are using a GPU Colab runtime. '
#         'Go to the Runtime menu and select Choose runtime type.')



#os.environ['MUJOCO_GL'] = 'egl'

# try:
#   print('Checking that the installation succeeded:')
#   import mujoco
#   from mujoco import viewer
#   mujoco.MjModel.from_xml_string('<mujoco/>')



# except Exception as e:
#   raise e from RuntimeError(
#       'Something went wrong during installation. Check the shell output above '
#       'for more information.\n'
#       'If using a hosted Colab runtime, make sure you enable GPU acceleration '
#       'by going to the Runtime menu and selecting "Choose runtime type".')



xml = """
<mujoco>
    <option integrator="RK4"/>

    <asset>
        <texture name="grid" type="2d" builtin="checker" rgb1=".1 .2 .3"
         rgb2=".2 .3 .4" width="300" height="300"/>
        <material name="grid" texture="grid" texrepeat="8 8" reflectance=".2"/>
    </asset>

    <worldbody>
        <geom name="floor" pos="0 0 -10" size="100 100 .05" type="plane" material="grid"/>
        
        <geom name="wall1" pos="20 0 0" size=".05 20 20" type="box" rgba="1 0 0 1"/>
        <geom name="wall2" pos="-20 0 0" size=".05 20 20" type="box" rgba="1 0 0 1"/>
        <geom name="wall3" pos="0 20 0" size="20 .05 20" type="box" rgba="1 0 0 1"/>
        <geom name="wall4" pos="0 -20 0" size="20 .05 20" type="box" rgba="1 0 0 1"/>
        <light name="top" pos="0 0 2"/>
        <body name="man">
            <geom type="capsule" pos="0 0 0" size="1 1" rgba="0 0 1 1" mass = "1"/>
            <site name="lidarSite" zaxis="1 0 0"/>
            <joint type="slide" axis="1 0 0"/>
            <joint type="slide" axis="0 1 0"/>
            <joint type="slide" axis="0 0 1"/>
            <joint type="hinge" axis="0 0 1"/>
            
        </body>
        <camera name="closeup" mode="targetbody" target="man" pos="0 -5 10"/>

    </worldbody>
    
    <sensor>
        <rangefinder name="lidar" site="lidarSite"/>
    </sensor>
    
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model)

options = mujoco.MjvOption()
mujoco.mjv_defaultOption(options)
options.flags[mujoco.mjtVisFlag.mjVIS_RANGEFINDER] = True
options.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = True


#Render a video
mujoco.mj_resetData(model, data)  # Reset state and time.
data.body("man").xfrc_applied[0:3] = [5, 0, 5]
duration = 20  # s
framerate = 60  # Hz
n_frames = int(duration * framerate)

frames = []
for current_frame in range(n_frames):
    while data.time < current_frame / framerate:
        mujoco.mj_step(model, data)


    renderer.update_scene(data, "closeup")
    frames.append(renderer.render())

#Make and open an html file to take advantage of the IDE compared to a notebook
htmlString = media.show_video(frames, height=650, width=1450, fps=framerate, return_html=True)
with open("data.html", "w") as file:
    file.write(htmlString)
webbrowser.open_new_tab("data.html")