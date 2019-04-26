import adsk.core, adsk.fusion, traceback

# This is based on a sample from the Autodesk knowledgebase which is under
# an unknown license. Trivial portions of it have been kept, and my contributions
# are licensed under the MIT license of the parent project.

# The sample is available at https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-d2b85a7e-fd08-11e4-9e07-3417ebd3d5be
# which is titled "Write user interface to a file API sample"

def reprCmdDef(cmdDef):
    return """
    id = {o.id}
    name = {o.name!r}
    """.format(o=cmdDef)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        fileDialog = ui.createFileDialog()
        fileDialog.isMultiSelectEnabled = False
        fileDialog.title = "Specify result filename"
        fileDialog.filter = 'Text files (*.txt)'
        fileDialog.filterIndex = 0
        dialogResult = fileDialog.showSave()
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filename = fileDialog.filename
        else:
            return

        result = 'Command defs:'
        for cmdDef in ui.commandDefinitions:
            result += reprCmdDef(cmdDef) + '\n'

        output = open(filename, 'w')
        output.writelines(result)
        output.close()

        ui.messageBox('File written to "' + filename + '"')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
