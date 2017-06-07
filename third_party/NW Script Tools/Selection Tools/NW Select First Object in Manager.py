import c4d # reference Cinema4D's existing library of code, called a "module"

def main(): # Define the main function of the script
    
    ActiveObject = doc.GetActiveObject() # Define ActiveObject to look for the currently selected object
    if ActiveObject == None: pass # If there is no object selected, skip the next step and pick up again where the indentation stops
    else: # This defines what happens if there IS a currently selected object
        doc.StartUndo() # Marks the beginning of a range of code that should be reversible
        doc.AddUndo(c4d.UNDOTYPE_BITS, ActiveObject) # Make the following deselection of the current object reversible
        ActiveObject.DelBit(c4d.BIT_ACTIVE) # Deselect the currently selected object
        doc.EndUndo() # Marks the end of a range of code that should be reversible
    doc.StartUndo() # Marks the beginning of a range of code that should be reversible
    FirstObject = doc.GetFirstObject() # Define FirstObject to look for the first object listed in the manager
    if FirstObject == None: return # If there is no object listed, call it quits here
    doc.AddUndo(c4d.UNDOTYPE_BITS, FirstObject) # Make the following selection of the returned object reversible
    FirstObject.SetBit(c4d.BIT_ACTIVE) # Make that returned object an active selection
    doc.EndUndo() # Marks the end of a range of code that should be reversible
    c4d.EventAdd() # Refresh the scene to update the change

if __name__=='__main__': # These two lines close out the main function.  This is usually what will be used to end your script.
    main()
