#Importing Maya commands 
import pymel.core as pymel
#Importing RegEx, so that we can sort out possible name differences between the original and this file's lights' names


def main():
    getUserInput()


# Defining classes #
class UInputs:
    def __init__(self, ffV, cbR, cbSO, cbIH):
        self.ffV = ffV
        self.cbR = cbR
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

    mayaLights = pymel.ls(type= mayaLightTypes, visible= not includeHidden, selection= onlySelected)
    arnoldLights = pymel.ls(type= arnoldLightTypes, visible= not includeHidden, selection= onlySelected)
    
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
    cbRelative = pymel.checkBox(label="Override: Absolute change", value=False, parent=layout)
    cbSelectedOnly = pymel.checkBox(label="Effect selected lights only", value=False, parent=layout)
    cbIncludeHidden = pymel.checkBox(label="Include hidden lights", value=False, parent=layout)
    btnAccept = pymel.button(label="Accept", parent=layout)
    #### End of Building UI form ####

    #### Store User Input ####
    def storeUserInput(*args):
        userInputs = UInputs(ffV = ffValue.getValue1(), cbR = cbRelative.getValue(), cbSO = cbSelectedOnly.getValue(), cbIH= cbIncludeHidden.getValue() )

        processUserInput(userInputs)

        pymel.deleteUI(win, window=True) # Closing user input window
    #### End of Store User Input ####

    btnAccept.setCommand(storeUserInput)
    win.show()
    return
### end of getUserInput() ###

### ProcessUserInput() ###
def processUserInput(userInputs):
    print(repr(getLights(userInputs.cbIH, userInputs.cbSO)))
    allLights = getLights(userInputs.cbIH, userInputs.cbSO)

    for x in allLights[0]: # Set Maya light exposures
        print(x.attr("aiExposure").get())
        newValue = x.attr("aiExposure").get() + userInputs.ffV
        x.attr("aiExposure").set(newValue)
        print(f'New= {x.attr("aiExposure").get()}')

    for x in allLights[1]: # Set Arnold light exposures
        print(x.attr("exposure").get())
        newValue = x.attr("exposure").get() + userInputs.ffV
        x.attr("exposure").set(newValue)
        print(f'New= {x.attr("exposure").get()}')

### End of processUserInput() ###
##########################
if __name__ == "__main__":
    main()
