import c4d, math, sys
import socket, time, threading
from random import uniform as rnd

#~~~~~~~~~~~~~   core  ~~~~~~~~~~~~~~~~~

def getDoc():
    return c4d.documents.GetActiveDocument()

def getFps():
    doc = getDoc()
    return doc.GetFps()

def getTarget():
    doc = getDoc()
    return doc.GetActiveObjects(0)

def getMode():
    returns = ""
    if c4d.IsCommandChecked(12101): # Object Mode
        returns = "object"
    elif c4d.IsCommandChecked(12298): # Model Mode
        returns = "model"
    return returns

def setMode(s = "object"):
    returns = ""
    if s=="model":
        returns = "model"
        c4d.CallCommand(12298) # Model Mode
    elif s=="object":
        returns = "object"
        c4d.CallCommand(12101) # Object Mode
    return returns

def refresh():
    c4d.EventAdd()
    c4d.DrawViews(c4d.DRAWFLAGS_FORCEFULLREDRAW) #Update screen

#~~~~~~~~~~~~~   utilities  ~~~~~~~~~~~~~~~~~

def getFrame():
    doc = getDoc()
    fps = getFps()
    curTime = doc.GetTime()
    curFrame = curTime.GetFrame(fps)
    return curFrame

def setFrame(_frame):
    doc = getDoc()
    fps = getFps()
    doc.SetTime(c4d.BaseTime(_frame, fps))

#random 3d vector
def rnd3d(spread=5):
    return c4d.Vector(rnd(-spread,spread),rnd(-spread,spread),rnd(-spread,spread))

#move to random location
def rndMove(spread=5):
    val = rnd3d(spread)
    move(val[0],val[1],val[2])

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

def setScale(x,y,z):
    target = getTarget()
    s = c4d.Vector(x,y,z)
    target[0].SetAbsScale(s)
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

def getScale(target=None):
    if not target:
        target = getTarget()
    s = target[0].GetAbsScale()
    return s

def ident(target=None):
    if not target:
        target = getTarget()

    if len(target) > 0: # we have one or more target objects in the scene
        for ob in target:
            print "Object: " + ob.GetName() + ", type: <" + ob.GetTypeName() + ">, ID: " + str(ob.GetType())

def polyCube():
    doc = getDoc()
    target = c4d.BaseObject(c4d.Ocube) # Create new cube
    target.SetRelPos(c4d.Vector(20))   # Set position of cube
    doc.InsertObject(target)  
    refresh()


#~~~~~~~~~~~~~   keyframes  ~~~~~~~~~~~~~~~~~
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

def keyframe(target=None, id=None):
    if not target:
        target=getTarget()

    if not id:
        #origMode = getMode()
        setMode("object")

        id=c4d.ID_BASEOBJECT_REL_POSITION
        addKey(target[0],id)
        id=c4d.ID_BASEOBJECT_REL_ROTATION
        addKey(target[0],id)
        id=c4d.ID_BASEOBJECT_REL_SCALE
        addKey(target[0],id)

        #setMode(origMode)
    else:
        addKey(target[0],id)
        
    refresh()

#~~~~~~~~~~~~~   MayaToolbox shortcuts  ~~~~~~~~~~~~~~~~~

s = getTarget
move = setPos
rotate = setRot

def m(p):
    move(p[0],p[1],[2])

def t(_t=None):
    try:
        setFrame(_t)
    except:
        print "time: " + str(getFrame())
    return getFrame()