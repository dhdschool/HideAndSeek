import mujoco
import mediapy as media
import webbrowser
from math import pi, cos, sin



class Player:
    def __init__(self, id=0):
        self.id = id
        self.name = "Player"
        self.rgba = "0 1 0 1"

    #Function to make xml text corresponding to various player components
    def make_xml(self):
        rotationLst = self.rotations(30)
        lidarSites = [f'<site name="{self.id}lidarSite{i}" zaxis="{rotationLst[i]}"/>' for i in range(30)]
        newline = '\n'
        body = f"""
                    <body name="{self.name + str(self.id)}">
                        <geom type="capsule" pos="0 0 0" size="1 1" rgba="{self.rgba}" mass = "1"/>
                        {newline.join(lidarSites)}
                        <joint type="slide" axis="1 0 0"/>
                        <joint type="slide" axis="0 1 0"/>
                        <joint type="slide" axis="0 0 1"/>
                        <joint type="hinge" axis="0 0 1"/>
                    </body>
                    """

        lidarSensors = [f'<rangefinder name="{self.id}lidar{i}" site="{self.id}lidarSite{i}"/>' for i in range(30)]
        sensor = f"""
            {newline.join(lidarSensors)}
"""
        return (body, sensor)

    def rotations(self, rotationNo: int):
        lst = []
        for i in range(rotationNo):
            string = f"{round(cos(i*2*pi/rotationNo),5)} {round(sin(i*2*pi/rotationNo),5)} 0"
            lst.append(string)
        return lst

class Hider(Player):
    def __init__(self, id=0):
        self.id = id
        self.name = "Hider"
        self.rgba = "0 0 1 1"

class Seeker(Player):
    def __init__(self, id=0):
        self.id = id
        self.name = "Seeker"
        self.rgba = "1 0 0 1"

defaultPlayer = Hider()
playerBody, playerSensors = defaultPlayer.make_xml()