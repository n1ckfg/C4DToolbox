import c4d, math
import socket, time, threading
from random import uniform as rnd

#~~~~~~~~~~~~~   init  ~~~~~~~~~~~~~~~~~
global doc, target, fps

def getDoc():
    return c4d.documents.GetActiveDocument()

def getFps():
    return doc.GetFps()

def getTarget():
    return doc.GetActiveObjects(0)

def initDoc():
    doc = getDoc()
    target = getTarget()
    fps = getFps()

def main():
    initDoc()
    
#~~~~~~~~~~~~~   utilities  ~~~~~~~~~~~~~~~~~

def getFrame():
    curTime = doc.GetTime()
    curFrame = curTime.GetFrame(fps)
    return curFrame

def setFrame(_frame):
    doc.SetTime(c4d.BaseTime(_frame, fps))

def refresh():
    c4d.EventAdd()
    c4d.DrawViews(c4d.DRAWFLAGS_FORCEFULLREDRAW) #Update screen

def rndVec(_x1=0,_x2=1,_y1=0,_y2=1,_z1=0,_z2=1):
    return c4d.Vector(rnd(_x1,_x2),rnd(_y1,_y2),rnd(_z1,_z2))

def keyframe(_obj):
    track = _obj.GetFirstCTrack() #Get it's first animation track (position X) 
    curve = track.GetCurve() #Get the curve for the track found(position x)
    added = curve.AddKey(0) #Moves the first key on the Position .X track to where the scrubber is
    added.SetValue(11)    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
for i in range(1,10):
    cube = c4d.BaseObject(c4d.Ocube)     # Allocate a new cube object at (0, 0, 0)
    doc.InsertObject(cube)
    cube.SetAbsPos(c4d.Vector(rnd(-1000,1000),rnd(-1000,1000),rnd(-1000,1000)))
    cube.SetAbsScale(c4d.Vector(1,5,1))
    #keyframe(cube)
'''
# setFrame(22)
# print frame()
# refresh()
# print target

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#
# Misc
#

def frame(doc):
    """Get current frame number."""
    return doc.GetTime().GetFrame(doc.GetFps())

#
# Keying
#

def getVec(id):
    """Get IDs for X, Y, Z components of a vector id. For example, XYZ of c4d.ID_BASEOBJECT_GLOBAL_POSITION"""
    x = c4d.DescID(c4d.DescLevel(id, c4d.DTYPE_VECTOR, 0), c4d.DescLevel(c4d.VECTOR_X, c4d.DTYPE_REAL, 0))
    y = c4d.DescID(c4d.DescLevel(id, c4d.DTYPE_VECTOR, 0), c4d.DescLevel(c4d.VECTOR_Y, c4d.DTYPE_REAL, 0))
    z = c4d.DescID(c4d.DescLevel(id, c4d.DTYPE_VECTOR, 0), c4d.DescLevel(c4d.VECTOR_Z, c4d.DTYPE_REAL, 0))

    return (x, y, z)

def createKey(op, id, value, forFrame = None):
    doc = op.GetDocument()
    if not doc: raise Exception, "object must be in a document"

    if forFrame == None:
        forFrame = frame(doc)

    # First check if the track type already exists, otherwise create it...
    track=op.FindCTrack(id)
    if not track:
        track=c4d.CTrack(op,id)
        op.InsertTrackSorted(track)

    curve=track.GetCurve()
    key=curve.AddKey(c4d.BaseTime(forFrame, doc.GetFps()))

    if type(value)==int or type(value)==float:
        key["key"].SetValue(curve,value)
    else:
        key["key"].SetGeData(curve,value)

def addFloatKey(op, id):
    createKey(op, id, op[id])

def addVectorKey(op, id):
    ids = getVec(id)
    v = op[id]

    createKey(op, ids[0], v.x)
    createKey(op, ids[1], v.y)
    createKey(op, ids[2], v.z)

def addKey(op, id):
    t = type(op[id])
    if t == int or t == float:
        addFloatKey(op, id)
    else:
        addVectorKey(op, id)
