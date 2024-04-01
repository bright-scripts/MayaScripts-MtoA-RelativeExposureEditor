#Importing Maya commands 
import pymel.core as pymel
#Importing RegEx, so that we can sort out possible name differences between the original and this file's lights' names


def main():
    getUserInput()


# Defining classes #
class UInputs:
    def __init__(self, ffV, cbR, cbSO, cbVO):
        self.ffV = ffV
        self.cbR = cbR
        self.cbSO = cbSO
        self.cbVO = cbVO
# End of defining classes #


# Functions:

def getLights(onlyVisible=True):
    '''
        Returns a list with two elements:
        [0]: all Maya lights in the scene
        [1]: all Arnold lights in the scene
        Args: onlyVisible (boolean) -> only return visible lights? (True by default)
    '''

    mayaLightTypes = ["areaLight","spotLight","ambientLight","directionalLight","pointLight","volumeLight"]
    arnoldLightTypes = ["aiSkyDomeLight","aiAreaLight","aiLightPortal","aiPhotometricLight",]

    mayaLights = pymel.ls(type= mayaLightTypes, visible= onlyVisible)
    arnoldLights = pymel.ls(type= arnoldLightTypes, visible= onlyVisible)
    
    return [mayaLights, arnoldLights]
### end of getLights() ###

def getUserInput():
    '''
        Asks for user input through a UI form and returns it as an array
    '''
    #### Building UI form ####
    win = pymel.window(title="Batch Light Editor")
    layout = pymel.columnLayout()
    ffValue = pymel.floatFieldGrp(label="Change value by/to:", value1=0, parent=layout) # ff stands for "Float Field"
    cbRelative = pymel.checkBox(label="Override: Absolute change", value=False, parent=layout)
    cbSelectedOnly = pymel.checkBox(label="Effect selected lights only", value=False, parent=layout)
    cbVisibleOnly = pymel.checkBox(label="Effect visible lights only", value=False, parent=layout)
    btnAccept = pymel.button(label="Accept", parent=layout)
    #### End of Building UI form ####

    #### Processing User Input ####
    def storeUserInput(*args):
        pymel.deleteUI(win, window=True) # Closing user input window
        userInputs = UInputs(ffV = ffValue.getValue1(), cbR = cbRelative.getValue(), cbSO = cbSelectedOnly.getValue(), cbVO= cbVisibleOnly.getValue() )
        return userInputs

    
    #### End of Processing User Input ####

    userInputs = UInputs
    btnAccept.setCommand(processUserInput) #NOTE: How could I store the return value from `processUserInput` in the variable `userInputs` w/o calling the function elsewhere?
    win.show()
    return 
### end of getUserInput() ###

def processUserInput():
    userInput = 1
    # print(repr(getLights()))
    allLights = getLights()

    for x in allLights[0]: # Set Maya light exposures
       # print(x.attr("aiExposure").get())
        newValue = x.attr("aiExposure").get() + userInput
        x.attr("aiExposure").set(newValue)
       # print(f'New= {x.attr("aiExposure").get()}')

    for x in allLights[1]: # Set Arnold light exposures
       # print(x.attr("exposure").get())
        newValue = x.attr("exposure").get() + userInput
        x.attr("exposure").set(newValue)
       # print(f'New= {x.attr("exposure").get()}')

##########################
if __name__ == "__main__":
    main()
