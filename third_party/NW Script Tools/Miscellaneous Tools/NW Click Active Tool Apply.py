import c4d # reference Cinema4D's existing library of code, called a "module"
from c4d import plugins # from the main C4D module, also reference the Plugins module

def main(): # Define the main function of the script
    
    tool = plugins.FindPlugin(doc.GetAction(), c4d.PLUGINTYPE_TOOL) # Define tool to find what the currently selected tool
    if tool is not None: # If there is a tool:
        doc.StartUndo() # Marks the beginning of a range of code that should be reversible
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, tool) # Make the following button click reversible
        c4d.CallButton(tool, c4d.MDATA_APPLY) # Make the "Apply" button click
        c4d.EventAdd() # Refresh the scene to update the change
        doc.EndUndo() # Marks the end of a range of code that should be reversible
    c4d.EventAdd() # Refresh the scene to update the change


if __name__=='__main__': # These two lines close out the main function.  This is usually what will be used to end your script.
    main()
