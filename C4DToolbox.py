import c4d, math
from random import uniform as rnd

target = doc.GetActiveObjects(0)
fps = doc.GetFps()

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

def randomVec(_x1,_x2,_y1,_y2,_z1,_z2):
    return Vector(rnd(_x1,_x2),rnd(_y1,_y2),rnd(_z1,_z2))

def keyframe(_obj):
    track = _obj.GetFirstCTrack() #Get it's first animation track (position X) 
    curve = track.GetCurve() #Get the curve for the track found(position x)
    added = curve.AddKey(0) #Moves the first key on the Position .X track to where the scrubber is
    added.SetValue(11)    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for i in range(1,10):
    cube = c4d.BaseObject(c4d.Ocube)     # Allocate a new cube object at (0, 0, 0)
    doc.InsertObject(cube)
    cube.SetAbsPos(c4d.Vector(rnd(-1000,1000),rnd(-1000,1000),rnd(-1000,1000)))
    cube.SetAbsScale(c4d.Vector(1,5,1))
    #keyframe(cube)

setFrame(22)
print frame()
refresh()
