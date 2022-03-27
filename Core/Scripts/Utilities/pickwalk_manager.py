import maya.cmds as cmds

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# SINGLETON CLASS TO STORE SELECTION DATA
class PickwalkManager(object):

    class __PickwalkManager:

        def __init__(self):
            self.previous_selection = []
            self.new_selection = []

    instance = None

    def __new__(cls, *args, **kwargs):
        if not PickwalkManager.instance:
            PickwalkManager.instance = PickwalkManager.__PickwalkManager()
        return PickwalkManager.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SinglePickwalk(object):

    def __init__(self, direction):

        self.manager = PickwalkManager()
        self.direction = direction
        select = self.get_pickwalk()
        self.manager.new_selection = select
        cmds.select(select)

    def get_pickwalk(self):

        selection = cmds.ls(sl=True)
        self.manager.previous_selection = selection
        if len(selection) > 0:
            pickwalk_selection = []
            for each in selection:
                if each in self.manager.new_selection:
                    pickwalk_selection.append(each)

            if len(pickwalk_selection) > 0:
                return self.pickwalk(self.manager.new_selection)
            else:
                return self.pickwalk(selection)

        return []

    def pickwalk(self, selection):
        to_select = []
        cmds.select(clear=True)
        for each in selection:
            attrs = cmds.listAttr(each, ud=True)
            if attrs is not None:
                if self.direction in attrs:
                    connections = cmds.listConnections(each + "." + self.direction)
                    if connections is not None:
                        to_select.append(cmds.listConnections(each + "." + self.direction)[0])

        if len(to_select) == 0:
            to_select.extend(selection)
        return to_select


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class AppendPickwalk(object):

    def __init__(self, direction):
        self.manager = PickwalkManager()
        self.direction = direction

        append_selection = self.get_pickwalk()
        new_selection = []
        for each in append_selection:
            if each not in self.manager.previous_selection:
                new_selection.append(each)

        self.manager.new_selection = new_selection
        cmds.select(append_selection, add=True)

    def get_pickwalk(self):
        to_select = []
        selection = cmds.ls(sl=True)
        self.manager.previous_selection = selection
        if len(selection) > 0:
            for each in selection:
                attrs = cmds.listAttr(each, ud=True)
                if attrs is not None:
                    if self.direction in attrs:
                        connections = cmds.listConnections(each + "." + self.direction)
                        if connections is not None:
                            to_select.append(cmds.listConnections(each + "." + self.direction)[0])

        if len(to_select) == 0:
            to_select.extend(selection)
        return to_select
