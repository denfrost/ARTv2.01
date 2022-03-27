import sys
import maya.standalone as std
std.initialize(name='python')
import maya.cmds as cmds
import maya.mel as mel
filename = sys.argv[1]

cmds.loadPlugin("fbxmaya.mll")
sys.stdout.write(filename)
sys.stdout.write("\n\n")


def stripNamespace(filename):

    try:
        # open the file
        string = "FBXImportMode -v \"add\";"
        string += "FBXImport -file \"" + filename + "\";"
        string += "FBXImportFillTimeline -v true;"
        mel.eval(string)

        # remove the namespace
        cmds.namespace(setNamespace="::")
        currentNamespaces = cmds.namespaceInfo(listOnlyNamespaces=True)

        restricted = ['UI', 'shared']

        for namespace in currentNamespaces:
            if namespace not in restricted:
                cmds.namespace(mv=(':' + namespace, ':'), force=True)
                cmds.namespace(removeNamespace=namespace)

        # re-export the file
        mel.eval("FBXExport -f \"" + filename + "\";")

        # exit
        std.uninitialize()

    except Exception, e:
        sys.stderr.write(str(e))
        sys.exit(-1)


stripNamespace(filename)
