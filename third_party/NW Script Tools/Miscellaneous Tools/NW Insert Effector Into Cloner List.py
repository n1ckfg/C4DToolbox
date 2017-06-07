import c4d # reference Cinema4D's existing library of code, called a "module"
from c4d import gui, documents # from the c4d module, reference the gui and documents modules

def main(): # Define the main function of the script
    
    # - - - - - - - COPY THE FOLLOWING INTO YOUR SCRIPT, ABOVE THE MAIN FUNCTION - - - - - - - 

    def InsertEffector(Effector):
        Active = doc.GetActiveObject() # Define Active to look for the currently selected object in the manager
        if Active == None: return  # if there is no object selected, quit
        CloneList = Active[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] # Define CloneList to look for an Effectors List in the active object
        if CloneList == None: return # if there is no Effectors List, quit
        doc.StartUndo() # Marks the beginning of a range of code that should be reversible
        Effector.InsertUnder(Active) # Insert the Effector (Random Effector object) under the active object (the Cloner)
        doc.AddUndo(c4d.UNDOTYPE_NEW, Effector) # Make the previous insertion of the Random Effector reversible
        Child = Active.GetDown() # Look for the child object (the Random Effector) in the manager relative to the currently selected object (the Cloner)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, Child) # Make the following change to the name of the Random Effector reversible
        Child[c4d.ID_BASELIST_NAME]="MyRandom" # Change the name of the Random Effector to "MyRandom"
        doc.AddUndo(c4d.UNDOTYPE_DELETE, Child) # Make the following removal of the Random Effector reversible
        Child.Remove() # Remove the Random Effector from the heirarchy (same as cutting to the clipboard)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, Child) # Make the following insertion of the Random Effector reversible
        Child.InsertAfter(Active) # Insert the Random Effector after the Cloner in the Heirarchy
        Target = doc.SearchObject("MyRandom") # Define Target to look for an object in the heirarchy called "MyRandom" (the Random Effector)
        if Target == None: return # If there is no object called "MyRandom", quit
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, Target) # Make the following insertion of the Random Effector into the Cloner's Effectors List reversible
        CloneList.InsertObject(Target,1) # Insert the Random Effector into a Cloner's Effector List and make it appear as active using type 1
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, Active) # Make the following update to the active object reversible
        Active[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]=CloneList # Make sure the active object's Effector List is the same as that of the CloneList variable
        Next = Active.GetNext() # Define Next to look for the next object (the Random Effector) in the heirarchy relative to the currently selected object (The Cloner)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, Next) # Make the following change to the Random Effector's name reversible
        Next[c4d.ID_BASELIST_NAME]="Random" # change the Random Effector's name back to "Random"
        doc.EndUndo() # Marks the end of a range of code that should be reversible
        c4d.EventAdd() # Refresh the scene to update the change

     #  - - - - - - - COPY THE ABOVE INTO YOUR SCRIPT, ABOVE THE MAIN FUNCTION - - - - - - - -

if __name__=='__main__': # These two lines close out the main function.  This is usually what will be used to end your script.
    main()
