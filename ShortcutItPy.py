#Author-lf
#Description-Add a bunch of commands to a toolbar panel in Tools so they can be shortcut

import adsk.core, adsk.fusion, adsk.cam, traceback

# "leak" these things (keep them in scope)
leaks = []


class ResetSelectionFiltersCreate(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        try:    
            evtArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = evtArgs.command
            on_exec = ResetSelectionFiltersExec()
            cmd.execute.add(on_exec)
            leaks.append(on_exec)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class ResetSelectionFiltersExec(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        # evtArgs = adsk.core.CommandEventArgs.cast(args)
        app = adsk.core.Application.get()
        ui = app.userInterface
        # this unfortunately is not implemented in API
        


def add_commands_to_menu(ui, needCmdDefs, myPanel):
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
        add_commands_to_menu(ui, needCmdDefs, myPanel)
        rsf_cmd = ui.commandDefinitions.addButtonDefinition(
            'ResetSelectionFilters',
            'Reset Selection Filters',
            'Clears the selection filters and allows all selection types',
            './unisolate'
        )
        rsfc = ResetSelectionFiltersCreate()
        leaks.append(rsfc)
        rsf_cmd.commandCreated.add(rsfc)
        myPanel.controls.addCommand(rsf_cmd)

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
        cmddef = ui.commandDefinitions.itemById('ResetSelectionFilters')
        if cmddef:
            cmddef.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
