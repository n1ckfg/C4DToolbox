import c4d, math, sys
import socket, time, threading
from random import uniform as rnd

#~~~~~~~~~~~~~   init  ~~~~~~~~~~~~~~~~~

doc = c4d.documents.GetActiveDocument()
fps = doc.GetFps()
target = doc.GetActiveObjects(0)

def getDoc():
    doc = c4d.documents.GetActiveDocument()
    return c4d.documents.GetActiveDocument()

def getFps():
    fps = doc.GetFps()
    return doc.GetFps()

def getTarget():
    target = doc.GetActiveObjects(0)
    return doc.GetActiveObjects(0)

def initDoc():
    doc = getDoc()
    fps = getFps()
    target = getTarget()

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

def setPos(x,y,z):
    target = getTarget()
    p = c4d.Vector(x,y,z)
    target[0].SetAbsPos(p)
    refresh()

def setRot(x,y,z):
    target = getTarget()
    r = c4d.Vector(x,y,z)
    target[0].SetAbsRot(r)
    refresh()

def getPos(target=None):
    if not target:
        target = getTarget()
    p = target[0].GetAbsPos()
    return p

def getRot(target=None):
    if not target:
        target = getTarget()
    r = target[0].GetAbsRot()
    return r

def ident(target=None):
    if not target:
        target = getTarget()

    if len(target) > 0: # we have one or more target objects in the scene
        for ob in target:
            print "Object: " + ob.GetName() + ", type: <" + ob.GetTypeName() + ">, ID: " + str(ob.GetType())

def polyCube():
    obj = c4d.BaseObject(c4d.Ocube) # Create new cube
    obj.SetRelPos(c4d.Vector(20))   # Set position of cube
    doc.InsertObject(obj)  
    refresh()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Based on https://github.com/jusu/Cinema4D-Helpers
#
# Misc
#

def frame(doc):
    """Get current frame number."""
    return doc.GetTime().GetFrame(doc.GetFps())

#
# Keying
#

def getVecIds(id=c4d.ID_BASEOBJECT_REL_POSITION):
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
    ids = getVecIds(id)
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

def keyframe(op=getTarget()[0], id=c4d.ID_BASEOBJECT_REL_POSITION):
    initDoc()
    addKey(op,id)
    refresh()

#~~~~~~~~~~~~~   MayaToolbox shortcuts  ~~~~~~~~~~~~~~~~~

s = getTarget
move = setPos
rotate = setRot