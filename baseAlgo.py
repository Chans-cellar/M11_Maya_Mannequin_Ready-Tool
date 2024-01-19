import maya.cmds as cmds


def getRootRig():
    rootRig = None
    roots = cmds.ls(assemblies=True)
    for item in roots:
        # get the objects that endswith rig keyword and add to the dropdown
        if item.endswith('Rig'):
            rootRig = item
    return rootRig


def listLayers():
    parentGroups = cmds.listRelatives(getRootRig(), c=True, fullPath=True)
    FaceGroupName = str(getRootRig()).rsplit('Rig')[0]
    for group in parentGroups:
        meshGroups = [FaceGroupName, 'Hand_Tech_Parts', 'Shoes', 'Hand_Gloves', 'LegGuards', 'Trousers',
                      'T_Shirts', 'Beard', 'Hairs', 'Caps']
        if group.endswith(tuple(meshGroups)):
            print(group)
            print(cmds.listRelatives(group, c=True, fullPath=True))


listLayers()
