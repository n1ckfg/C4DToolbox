import c4d, math, sys
import socket, time, threading
from random import uniform as rnd
#~~
from math import *
from xml.dom.minidom import *
import xml.dom.minidom as xd
import os
import re
#~~
#~~~~~~~~~~~~~~~~~~
from c4dtoolbox import *
#~~~~~~~~~~~~~~~~~~

def writeSampleXml():
    filePath = "/Users/nick/Desktop/"
    fileName = "test.xml"

    doc = Document()

    root_node = doc.createElement("MotionCapture")
    doc.appendChild(root_node)
    root_node.setAttribute("width", "640")
    root_node.setAttribute("height", "480")
    root_node.setAttribute("depth", "200")
    root_node.setAttribute("dialogueFile", "none")
    root_node.setAttribute("fps", "24")
    root_node.setAttribute("numFrames", "0")

    frame_node = doc.createElement("MocapFrame")
    root_node.appendChild(frame_node)
    frame_node.setAttribute("index","0")

    skel_node = doc.createElement("Skeleton")
    frame_node.appendChild(skel_node)
    skel_node.setAttribute("id","0")

    joint_node = doc.createElement("Joints")
    skel_node.appendChild(joint_node)

    xml_file = open(filePath + fileName, "w")
    xml_file.write(doc.toprettyxml())
    xml_file.close()

    print doc.toprettyxml()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def readSampleXml():
    counterMin = 0;
    counter=int(counterMin);
    counterMax = 200;

    filePath = "/Users/nick/Desktop/"
    fileName = "mocapData1.xml"

    #trackPoint = ["l_foot","l_knee","l_hip","r_foot","r_knee","r_hip","l_hand","l_elbow","l_shoulder","r_hand","r_elbow","r_shoulder","torso","neck","head"]
    trackPoint = ["head"]
    scaler = 1000

    xmlFile = xd.parse(filePath + "/" + fileName)
    print("loaded: " + fileName)

    for t in trackPoint:   
        polyCube()
        scale(0.1,0.1,0.1)

        joint = xmlFile.getElementsByTagName(t)
        for j in joint:

            x = scaler * float(j.getAttribute("x"))
            y = scaler * float(j.getAttribute("y"))
            z = scaler * float(j.getAttribute("z"))
            
            #if(x!=0 and y!=0 and z!=0):
            setFrame(counter)
            counter+=1
            move(x, y, z)
            rotate(rnd(-1 * scaler, scaler),rnd(-1 * scaler, scaler),rnd(-1 * scaler, scaler))
            keyframe()
        
    print("...script complete.")


