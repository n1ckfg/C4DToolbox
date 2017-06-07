import c4d # reference Cinema4D's existing library of code, called a "module"

def main(): # Define the main function of the script
    
    # - - - - - - - COPY THE FOLLOWING INTO YOUR SCRIPT, ABOVE THE MAIN FUNCTION - - - - - - - 
    
    def key(Parameter): # Define a function called "key", which will act as a container for the script to be implemented in other scripts.
        CurrentTime = doc.GetTime() # Define CurrentTime to look for the current time in the project
        CurrentFrame = CurrentTime.GetFrame(doc.GetFps()) # Define CurrentFrame to calculate what the current frame is based on the frame rate of the project
        Active = doc.GetActiveObject() # Define Active to look for the currently selected object in the manager
        if Active == None: return # If there is no active object, quit
        Track = Active.FindCTrack(Parameter) # Define Track to look for whether there is an animation track for the parameter in question
        if not Track: # If there is no animation track...
            doc.StartUndo() # Marks the beginning of a range of code that should be reversible
            Track = c4d.CTrack(Active, Parameter) # Define Track to create a new animation track instead
            doc.AddUndo(c4d.UNDOTYPE_CHANGE,Active) # Make the following placement of the new animation track reversible
            Active.InsertTrackSorted(Track) # Place the new animation track in the timeline
        Curve = Track.GetCurve() # Define Curve to look for the new animation track's curve
        Key = Curve.AddKey(c4d.BaseTime(CurrentFrame, doc.GetFps())) # Define Key to add a keyframe to the new animation track at the current frame
        doc.AddUndo(c4d.UNDOTYPE_CHANGE,Track) # Make the following filling of the keyframe reversible
        Track.FillKey(doc,Active,Key["key"]) # Fill the keyframe (make it red)
        doc.EndUndo() # Marks the end of a range of code that should be reversible
        c4d.EventAdd() # Refresh the scene to update the change
        
    #  - - - - - - - COPY THE ABOVE INTO YOUR SCRIPT, ABOVE THE MAIN FUNCTION - - - - - - - -
    
# Once you have this copied into your script, you can simply call up the function and insert your value in the parentheses.

# Example: key([c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X]) will set a key for the parameter you drag in if the above is in place.  You don't have to copy/paste the whole thing each time you want to use it that way.
    

if __name__=='__main__': # These two lines close out the main function.  This is usually what will be used to end your script.
    main()
