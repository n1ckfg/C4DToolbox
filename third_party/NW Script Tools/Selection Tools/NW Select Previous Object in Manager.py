import c4d # reference Cinema4D's existing library of code, called a "module"

def main(): # Define the main function of the script
    
    ActiveObject = doc.GetActiveObject() # Define ActiveObject to look for the currently selected object in the manager
    if ActiveObject == None: return # If there is no object selected, call it quits here
    PrevObject = ActiveObject.GetPred() # Look for the previous object in the manager relative to the currently selected object
    if PrevObject == None: return # If there is no previous object, call it quits here
    doc.StartUndo() # Marks the beginning of a range of code that should be reversible
    doc.AddUndo(c4d.UNDOTYPE_BITS, ActiveObject) # Make the following deselection of the active object reversible
    ActiveObject.DelBit(c4d.BIT_ACTIVE) # Deselect the active object
    doc.AddUndo(c4d.UNDOTYPE_BITS, PrevObject) # Make the following selection of the previous object reversible
    PrevObject.SetBit(c4d.BIT_ACTIVE) # Make the previous object an active selection
    doc.EndUndo() # Marks the end of a range of code that should be reversible
    c4d.EventAdd() # Refresh the scene to update the change
    
if __name__=='__main__': # These two lines close out the main function.  This is usually what will be used to end your script.
    main()
