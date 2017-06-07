import c4d # reference Cinema4D's existing library of code, called a "module"

def main(): # Define the main function of the script

    ActiveObject = doc.GetActiveObject() # Look for the currently selected object
    if ActiveObject == None: return # if there is no object selected, quit 
    NextObject = ActiveObject.GetNext() # Look for the object following the current object in the manager
    if NextObject == None: return # if there is no following object, quit
    doc.StartUndo() # Make the following section of code reversible
    doc.AddUndo(c4d.UNDOTYPE_DELETE, ActiveObject) # Make the following removal of the object reversible
    ActiveObject.Remove() # Remove the current object
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,ActiveObject) # Make the following insertion of the object reversible
    ActiveObject.InsertAfter(NextObject) # Put the removed object after the following object in the manager
    doc.EndUndo() # Marks the end of a range of code that should be reversible
    c4d.EventAdd() # Refresh the scene to update the change
     
if __name__=='__main__': # These two lines close out the main function.  This is usually what will be used to end your script.
    main()
