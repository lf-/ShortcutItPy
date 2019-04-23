#Author-lf
#Description-Add a bunch of commands to a toolbar panel in Tools so they can be shortcut

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        ws = ui.workspaces.itemById('FusionSolidEnvironment')
        panels = ws.toolbarPanels
        myPanel = panels.itemById('ShortcutItPanel')
        if myPanel:
            myPanel.deleteMe()

        myPanel = panels.add('ShortcutItPanel', 'Shortcut It', '')
        needCmdDefs = (
            ('IsolateCmd', './isolate'),
            ('UnisolateCmd', './unisolate'),
            ('UnisolateAllCmd', './unisolate'),
            ('FindInBrowser', './findinbrowser'),
        )
        for cmdName, resDir in needCmdDefs:
            cmd = ui.commandDefinitions.itemById(cmdName)
            if not cmd:
                ui.messageBox('Cannot find {}'.format(cmdName))
                continue
            if resDir is not None:
                cmd.resourceFolder = resDir
            cmd.controlDefinition.isVisible = True
            cmd.controlDefinition.isEnabled = True
            myPanel.controls.addCommand(cmd)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ws = ui.workspaces.itemById('FusionSolidEnvironment')
        panels = ws.toolbarPanels
        myPanel = panels.itemById('ShortcutItPanel')
        if myPanel:
            myPanel.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
