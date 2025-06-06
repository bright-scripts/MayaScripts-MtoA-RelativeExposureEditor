#Importing Maya commands 
import pymel.core as pymel


def main():
    getUserInput()


# Defining classes #
class UInputs:
    def __init__(self, ffV, cbA, cbSO, cbIH):
        self.ffV = ffV
        self.cbA = cbA
        self.cbSO = cbSO
        self.cbIH = cbIH
# End of defining classes #


# Functions:

def getLights(includeHidden=False, onlySelected=False):
    '''
        Returns a list with two elements:
        [0]: all Maya lights in the scene
        [1]: all Arnold lights in the scene
        Args: 
        - includeHidden (boolean) -> return hidden lights as well? (false by default)
        - onlySelected (boolean) -> return only seleceted lights? (false by default)

    '''

    mayaLightTypes = ["areaLight","spotLight","ambientLight","directionalLight","pointLight","volumeLight"]
    arnoldLightTypes = ["aiSkyDomeLight","aiAreaLight","aiLightPortal","aiPhotometricLight",]

    mayaLights = pymel.ls(type= mayaLightTypes, visible= not includeHidden)
    arnoldLights = pymel.ls(type= arnoldLightTypes, visible= not includeHidden)
    
    #### Filter allLights down to only selected lights: ####
    if onlySelected:
        temp = [[],[]] # An array of the transform names of all lights in the scene
        for x in mayaLights:
            temp[0].append(x.name()[0: x.name().rfind("Shape")]+x.name()[x.name().rfind("Shape")+5:]) # strip "Shape" from the end (but not the nuber if there's one) of the ligth type object's name, then append the result to temp[0]

        for x in arnoldLights:
            temp[1].append(x.name()[0: x.name().rfind("Shape")]+x.name()[x.name().rfind("Shape")+5:])

        selectedObjects = pymel.ls(selection= True, type= "transform", sn= True)

        for i in range(len(temp[0])-1, -1, -1):
            if temp[0][i] not in selectedObjects:
                mayaLights.pop(i)

        for i in range(len(temp[1])-1, -1, -1):
            if temp[1][i] not in selectedObjects:
                arnoldLights.pop(i)

    #### End of Filter allLights down to only selected lights: ####

    return [mayaLights, arnoldLights]
### end of getLights() ###

def getUserInput():
    '''
        Asks for user input through a UI form and returns it as an array
    '''
    #### Building UI form ####
    win = pymel.window(title="Batch Light Editor")
    layout = pymel.columnLayout()
    ffValue = pymel.floatFieldGrp(label="Change value by/to:", parent=layout) # ff stands for "Float Field"
    cbAbsolute = pymel.checkBox(label="Override: Absolute change", value=False, parent=layout)
    cbSelectedOnly = pymel.checkBox(label="Selected lights only", value=False, parent=layout)
    cbIncludeHidden = pymel.checkBox(label="Include hidden lights", value=False, parent=layout)
    btnAccept = pymel.button(label="Accept", parent=layout)
    #### End of Building UI form ####

    #### Store User Input ####
    def storeUserInput(*args):
        userInputs = UInputs(ffV = ffValue.getValue1(), cbA = cbAbsolute.getValue(), cbSO = cbSelectedOnly.getValue(), cbIH= cbIncludeHidden.getValue() )

        ##### Processing user inputs #####
        processUserInput(userInputs)
        ##### End of processing user inputs #####

        pymel.deleteUI(win, window=True) # Closing user input window
    #### End of Store User Input ####

    btnAccept.setCommand(storeUserInput) # Set function to execute on button push
    win.show() # Open the built window
    return
### end of getUserInput() ###

### ProcessUserInput() ###
def processUserInput(userInputs):
    allLights = getLights(userInputs.cbIH, userInputs.cbSO)

    #### Setting the exposure based on all previous criteria ####
    for x in allLights[0]: # Set Maya light exposures
        print(f"Old value of '{x.name()}': {x.attr('aiExposure').get()}")
        if userInputs.cbA:
            newValue = userInputs.ffV
        else:
            newValue = x.attr("aiExposure").get() + userInputs.ffV

        x.attr("aiExposure").set(newValue)
        print(f'New= {x.attr("aiExposure").get()}')

    for x in allLights[1]: # Set Arnold light exposures
        print(f"Old value of '{x.name()}': {x.attr('exposure').get()}")
        if userInputs.cbA:
            newValue = userInputs.ffV
        else:
            newValue = x.attr("exposure").get() + userInputs.ffV

        x.attr("exposure").set(newValue)
        print(f'New= {x.attr("exposure").get()}')
    #### End of Setting the exposure based on all previous criteria ####

### End of processUserInput() ###

# dev helper functions:
def helpPrintallLights(allLights, message):
    print("### " + message + " ###")
    for x in allLights[0]: # Set Maya light exposures
      print(x.name())

    for x in allLights[1]: # Set Arnold light exposures
      print(x.name())
    print("###======================###")

##########################
if __name__ == "__main__":
    main()
