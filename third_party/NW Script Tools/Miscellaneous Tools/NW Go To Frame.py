import c4d # reference Cinema4D's existing library of code, called a "module"

def main(): # Define the main function of the script
    
    # - - - - - - COPY THE FOLLOWING INTO YOUR SCRIPT, ABOVE THE MAIN FUNCTION - - - - - - - 
    
    def gotoframe(GoToFrame): # Define a function called "gotoframe", which will act as a container for the script to be implemented in other scripts.
        FPS = doc[c4d.DOCUMENT_FPS] # Define FPS to look at the current document's fps setting
        Time = c4d.BaseTime(GoToFrame,FPS) # Define Time to find the new frame location based on the combination of the current frame, the number of frames to advance, and the fps setting of the document
        doc.SetTime(Time) # Move the playhead to the newly referenced location in the timeline
        c4d.EventAdd() # Refresh the scene to update the change
    
    # - - - - - - COPY THE ABOVE INTO YOUR SCRIPT, ABOVE THE MAIN FUNCTION - - - - - - - -
    
# Once you have this copied into your script, you can simply call up the function and insert your value in the parentheses.

# Example: gotoframe(20) will move your playhead to frame 20 if the above is in place.  You don't have to copy/paste the whole thing each time you want to use it that way.
       
if __name__=='__main__': # These two lines close out the main function.  This is usually what will be used to end your script.
    main()