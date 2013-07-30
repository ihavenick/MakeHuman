"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         GPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
Vertex and face numbers

"""

import bpy
import os

#
#    printVertNums(context):
#    class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
#

class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_vnums"
    bl_label = "Print vnums"

    def execute(self, context):
        ob = context.object
        print("Verts in ", ob)
        for v in ob.data.vertices:
            if v.select:
                print("  ", v.index)
        print("End")
        return{'FINISHED'}


class VIEW3D_OT_PrintVnumsToFileButton(bpy.types.Operator):
    bl_idname = "mhw.print_vnums_to_file"
    bl_label = "Print Vnums To File"

    def execute(self, context):
        ob = context.object
        scn = context.scene
        path = os.path.expanduser(scn.MhxVertexGroupFile)
        fp = open(path, "w")
        fp.write("  [")
        for v in ob.data.vertices:
            if v.select:
                fp.write("%d, " % v.index)
        fp.write("]\n")
        fp.close()
        print(path, "written")
        return{'FINISHED'}


class VIEW3D_OT_ReadVNumsButton(bpy.types.Operator):
    bl_idname = "mhw.read_vnums_from_file"
    bl_label = "Read Vnums from file"
    bl_options = {'UNDO'}

    filepath = bpy.props.StringProperty(
        name="File Path",
        description="File path used for target file",
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return context.object

    def execute(self, context):
        ob = context.object
        fp = open(self.filepath, "rU")
        for line in fp:
            try:
                vn = int(line)
            except:
                vn = -1
            if vn >= 0:
                ob.data.vertices[vn].select = True
        fp.close()
        print("Vnums loaded")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



def printFirstVertNum(context):
    ob = context.object
    print("First vert in ", ob)
    for v in ob.data.vertices:
        if v.select:
            print("  ", v.index)
            return
    print("None found")

class VIEW3D_OT_PrintFirstVnumButton(bpy.types.Operator):
    bl_idname = "mhw.print_first_vnum"
    bl_label = "Print first vnum"

    def execute(self, context):
        printFirstVertNum(context)
        return{'FINISHED'}


#
#    selectVertNum8m(context):
#    class VIEW3D_OT_SelectVnumButton(bpy.types.Operator):
#

def selectVertNum(context):
    n = context.scene.MhxVertNum
    ob = context.object
    bpy.ops.object.mode_set(mode='OBJECT')
    for v in ob.data.vertices:
        v.select = False
    v = ob.data.vertices[n]
    v.select = True
    bpy.ops.object.mode_set(mode='EDIT')

class VIEW3D_OT_SelectVnumButton(bpy.types.Operator):
    bl_idname = "mhw.select_vnum"
    bl_label = "Select vnum"
    bl_options = {'UNDO'}

    def execute(self, context):
        selectVertNum(context)
        return{'FINISHED'}

#
#    printEdgeNums(context):
#    class VIEW3D_OT_PrintEnumsButton(bpy.types.Operator):
#

def printEdgeNums(context):
    ob = context.object
    print("Edges in ", ob)
    for e in ob.data.edges:
        if e.select:
            print(e.index)
    print("End")

class VIEW3D_OT_PrintEnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_enums"
    bl_label = "Print enums"

    def execute(self, context):
        printEdgeNums(context)
        return{'FINISHED'}
#
#    printFaceNums(context):
#    class VIEW3D_OT_PrintFnumsButton(bpy.types.Operator):
#

def printFaceNums(context):
    ob = context.object
    print("Faces in ", ob)
    for f in ob.data.polygons:
        if f.select:
            print(f.index)
    print("End")

class VIEW3D_OT_PrintFnumsButton(bpy.types.Operator):
    bl_idname = "mhw.print_fnums"
    bl_label = "Print fnums"

    def execute(self, context):
        printFaceNums(context)
        return{'FINISHED'}


class VIEW3D_OT_PrintFnumsToFileButton(bpy.types.Operator):
    bl_idname = "mhw.print_fnums_to_file"
    bl_label = "Print Fnums To File"

    def execute(self, context):
        ob = context.object
        scn = context.scene
        polys = []
        for f in ob.data.polygons:
            if f.select:
                polys.append(f.index)
        polys.sort()

        path = os.path.expanduser(scn.MhxVertexGroupFile)
        fp = open(path, "w")
        fp.write("  [")
        for fn in polys:
            fp.write("%d, " % fn)
        fp.write("]\n")
        fp.close()
        print(path, "written")
        return{'FINISHED'}

#
#    selectQuads():
#    class VIEW3D_OT_SelectQuadsButton(bpy.types.Operator):
#

def selectQuads(context):
    ob = context.object
    for f in ob.data.polygons:
        if len(f.vertices) == 4:
            f.select = True
        else:
            f.select = False
    return

class VIEW3D_OT_SelectQuadsButton(bpy.types.Operator):
    bl_idname = "mhw.select_quads"
    bl_label = "Select quads"
    bl_options = {'UNDO'}

    def execute(self, context):
        import bpy
        selectQuads(context)
        print("Quads selected")
        return{'FINISHED'}
