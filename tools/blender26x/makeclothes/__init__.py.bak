# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2013
# Coding Standards:    See http://www.makehuman.org/node/165
#
# Abstract
# Utility for making clothes to MH characters.
#

bl_info = {
    "name": "Make Clothes",
    "author": "Thomas Larsson",
    "version": "0.909",
    "blender": (2, 6, 7),
    "location": "View3D > Properties > Make MH clothes",
    "description": "Make clothes and UVs for MakeHuman characters",
    "warning": "",
    'wiki_url': "http://www.makehuman.org/node/228",
    "category": "MakeHuman"}


if "bpy" in locals():
    print("Reloading makeclothes v %s" % bl_info["version"])
    import imp
    imp.reload(maketarget)
    imp.reload(mc)
    imp.reload(materials)
    imp.reload(makeclothes)
else:
    print("Loading makeclothes v %s" % bl_info["version"])
    import bpy
    import os
    from bpy.props import *
    import maketarget
    from maketarget.error import MHError, handleMHError
    from . import mc
    from . import materials
    from . import makeclothes

#
#    class MakeClothesPanel(bpy.types.Panel):
#


def inset(layout):
    split = layout.split(0.05)
    split.label("")
    return split.column()


class MakeClothesPanel(bpy.types.Panel):
    bl_label = "Make Clothes version %s" % bl_info["version"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.prop(scn, "MCShowSettings")
        if scn.MCShowSettings:
            maketarget.settings.drawDirectories(inset(layout), scn, "MhClothesDir")

        #layout.operator("mhclo.snap_selected_verts")
        '''
        layout.prop(scn, "MCShowUtils")
        if scn.MCShowUtils:
            ins = inset(layout)
            ins.operator("mhclo.print_vnums")
            ins.operator("mhclo.copy_vert_locs")
            ins.separator()
        '''
        layout.prop(scn, "MCShowAutoVertexGroups")
        if scn.MCShowAutoVertexGroups:
            layout.prop(scn, "MCRemoveGroupType", expand=True)
            inset(layout).operator("mhclo.remove_vertex_groups")
            layout.separator()
            layout.prop(scn, "MCAutoGroupType", expand=True)
            if scn.MCAutoGroupType == 'Helpers':
                layout.prop(scn, "MCAutoHelperType", expand=True)
            ins = inset(layout)
            ins.operator("mhclo.auto_vertex_groups")
            ins.separator()
            #ins.prop(scn, "MCKeepVertsUntil", expand=False)
            #ins.operator("mhclo.delete_helpers")
            #ins.separator()

        '''
        layout.prop(scn, "MCShowMaterials")
        if scn.MCShowMaterials:
            ins = inset(layout)
            """
            ins.prop(scn, "MCMaterials")
            #ins.prop(scn, "MCBlenderMaterials")
            ins.prop(scn, "MCHairMaterial")
            """

            row = ins.row()
            col = row.column()
            col.prop(scn, "MCUseTexture")
            col.prop(scn, "MCUseMask")
            col.prop(scn, "MCUseBump")
            col.prop(scn, "MCUseNormal")
            col.prop(scn, "MCUseDisp")
            col.prop(scn, "MCUseTrans")
            col = row.column()
            col.prop(scn, "MCTextureLayer", text = "")
            col.prop(scn, "MCMaskLayer", text="")
            col.prop(scn, "MCBumpStrength", text="")
            col.prop(scn, "MCNormalStrength", text="")
            col.prop(scn, "MCDispStrength", text="")
            ins.prop(scn, "MCAllUVLayers")
            ins.separator()
        '''

        layout.separator()
        split = layout.split(0.3)
        split.label("Load")
        split.prop(scn, "MhBodyType", text="Type")
        row = layout.row()
        row.operator("mhclo.load_human", text="Nude Human").helpers = False
        row.operator("mhclo.load_human", text="Human With Helpers").helpers = True
        layout.separator()
        layout.operator("mhclo.make_clothes")
        layout.separator()

        '''
        layout.prop(scn, "MCShowAdvanced")
        if scn.MCShowAdvanced:
            ins = inset(layout)
            ins.operator("mhclo.print_clothes")
            ins.operator("mhclo.export_obj_file")
            ins.operator("mhclo.export_delete_verts")
            ins.label("Algorithm Control")
            row = ins.row()
            row.prop(scn, "MCThreshold")
            row.prop(scn, "MCListLength")
            ins.separator()
        '''

        layout.prop(scn, "MCShowExportDetails")
        if scn.MCShowExportDetails:
            ins = inset(layout)

            row = ins.row()
            row.operator("mhclo.set_human", text="Set Human").isHuman = True
            row.operator("mhclo.set_human", text="Set Clothing").isHuman = False
            ins.separator()

            '''
            ins.label("Shapekeys")
            for skey in makeclothes.theShapeKeys:
                ins.prop(scn, "MC%s" % skey)

            ins.separator()
            ins.label("Z depth")
            ins.prop(scn, "MCZDepthName")
            ins.operator("mhclo.set_zdepth")
            ins.prop(scn, "MCZDepth")
            '''

            ins.separator()
            ins.label("Boundary")
            row = ins.row()
            row.prop(scn, "MCUseBoundary")
            if scn.MCUseBoundary:
                row.prop(scn, "MCScaleUniform")
                ins.prop(scn, "MCScaleCorrect")
                ins.prop(scn, "MCBodyPart")
                vnums = makeclothes.theSettings.bodyPartVerts[scn.MCBodyPart]
                if scn.MCScaleUniform:
                    self.drawXYZ(vnums[0], "XYZ", ins)
                else:
                    self.drawXYZ(vnums[0], "X", ins)
                    self.drawXYZ(vnums[1], "Y", ins)
                    self.drawXYZ(vnums[2], "Z", ins)
                ins.operator("mhclo.examine_boundary")
            ins.separator()

        layout.prop(scn, "MCShowLicense")
        if scn.MCShowLicense:
            ins = inset(layout)
            ins.prop(scn, "MCAuthor")
            ins.prop(scn, "MCLicense")
            ins.prop(scn, "MCHomePage")
            ins.label("Tags")
            ins.prop(scn, "MCTag1")
            ins.prop(scn, "MCTag2")
            ins.prop(scn, "MCTag3")
            ins.prop(scn, "MCTag4")
            ins.prop(scn, "MCTag5")
            ins.separator()

        if not scn.MCUseInternal:
            return
        ins.separator()
        ins.label("For internal use")
        ins.prop(scn, "MCLogging")
        ins.prop(scn, "MhProgramPath")
        ins.prop(scn, "MCSelfClothed")
        ins.operator("mhclo.select_helpers")
        ins.operator("mhclo.export_base_uvs_py")

        #ins.prop(scn, "MCVertexGroups")
        #ins.operator("mhclo.offset_clothes")
        return

    def drawXYZ(self, pair, name, layout):
        m,n = pair
        row = layout.row()
        row.label("%s1:   %d" % (name,m))
        row.label("%s2:   %d" % (name,n))


#
#    class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
#

class OBJECT_OT_InitInterfaceButton(bpy.types.Operator):
    bl_idname = "mhclo.init_interface"
    bl_label = "Init"

    def execute(self, context):
        makeclothes.init()
        makeclothes.readDefaultSettings(context)
        print("Interface initialized")
        return{'FINISHED'}

#
#    class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
#

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mhclo.factory_settings"
    bl_label = "Restore factory settings"
    bl_options = {'UNDO'}

    def execute(self, context):
        makeclothes.init()
        return{'FINISHED'}

#
#    class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
#

class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mhclo.save_settings"
    bl_label = "Save settings"

    def execute(self, context):
        makeclothes.saveDefaultSettings(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_SnapSelectedVertsButton(bpy.types.Operator):
#

class OBJECT_OT_SnapSelectedVertsButton(bpy.types.Operator):
    bl_idname = "mhclo.snap_selected_verts"
    bl_label = "Snap selected"
    bl_options = {'UNDO'}

    def execute(self, context):
        makeclothes.snapSelectedVerts(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
#

class OBJECT_OT_MakeClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.make_clothes"
    bl_label = "Make clothes"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.makeClothes(context, True)
            makeclothes.exportObjFile(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

class OBJECT_OT_PrintClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.print_clothes"
    bl_label = "Print mhclo file"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.makeClothes(context, False)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#   class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
#

class OBJECT_OT_CopyVertLocsButton(bpy.types.Operator):
    bl_idname = "mhclo.copy_vert_locs"
    bl_label = "Copy vertex locations"
    bl_options = {'UNDO'}

    def execute(self, context):
        src = context.object
        for trg in context.scene.objects:
            if trg != src and trg.select and trg.type == 'MESH':
                print("Copy vertex locations from %s to %s" % (src.name, trg.name))
                for n,sv in enumerate(src.data.vertices):
                    tv = trg.data.vertices[n]
                    tv.co = sv.co
                print("Vertex locations copied")
        return{'FINISHED'}


#
#   class OBJECT_OT_ExportDeleteVertsButton(bpy.types.Operator):
#

class OBJECT_OT_ExportDeleteVertsButton(bpy.types.Operator):
    bl_idname = "mhclo.export_delete_verts"
    bl_label = "Export Delete Verts"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.exportDeleteVerts(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#   class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
#

class OBJECT_OT_ExportObjFileButton(bpy.types.Operator):
    bl_idname = "mhclo.export_obj_file"
    bl_label = "Export Obj file"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.exportObjFile(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#   class OBJECT_OT_ExportBaseUvsPyButton(bpy.types.Operator):
#   class OBJECT_OT_SplitHumanButton(bpy.types.Operator):
#

class OBJECT_OT_ExportBaseUvsPyButton(bpy.types.Operator):
    bl_idname = "mhclo.export_base_uvs_py"
    bl_label = "Export base UV py file"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.exportBaseUvsPy(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

class OBJECT_OT_SelectHelpersButton(bpy.types.Operator):
    bl_idname = "mhclo.select_helpers"
    bl_label = "Select Helpers"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.selectHelpers(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_ExportBlenderMaterialsButton(bpy.types.Operator):
#

class OBJECT_OT_ExportBlenderMaterialButton(bpy.types.Operator):
    bl_idname = "mhclo.export_blender_material"
    bl_label = "Export Blender material"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            pob = makeclothes.getClothing(context)
            (outpath, outfile) = makeclothes.getFileName(pob, context, "mhx")
            makeclothes.exportBlenderMaterial(pob.data, outpath)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
#

class OBJECT_OT_MakeHumanButton(bpy.types.Operator):
    bl_idname = "mhclo.set_human"
    bl_label = "Make human"
    bl_options = {'UNDO'}
    isHuman = BoolProperty()

    def execute(self, context):
        try:
            ob = context.object
            ob.MhHuman = self.isHuman
            print("Object %s: Human = %s" % (ob.name, ob.MhHuman))
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_LoadHumanButton(bpy.types.Operator):
#

class OBJECT_OT_LoadHumanButton(bpy.types.Operator):
    bl_idname = "mhclo.load_human"
    bl_label = "Load human"
    bl_options = {'UNDO'}
    helpers = BoolProperty()

    def execute(self, context):
        from maketarget import mt, import_obj, utils
        scn = context.scene

        print("BODY", scn.MhBodyType)
        try:
            if self.helpers:
                basepath = mt.baseMhcloFile
                import_obj.importBaseMhclo(context, basepath)
                maketarget.maketarget.afterImport(context, basepath, False, True)
                scn.MCAutoGroupType = 'Helpers'
                scn.MCAutoHelperType = 'All'
            else:
                basepath = mt.baseObjFile
                import_obj.importBaseObj(context, basepath)
                maketarget.maketarget.afterImport(context, basepath, True, False)
                scn.MCAutoGroupType = 'Body'

            if scn.MhBodyType == 'None':
                maketarget.maketarget.newTarget(context)
                found = True
            else:
                trgpath = os.path.join(os.path.dirname(__file__), "targets", scn.MhBodyType + ".target")
                try:
                    utils.loadTarget(trgpath, context)
                    found = True
                except FileNotFoundError:
                    found = False
            if not found:
                raise MHError("Target \"%s\" not found.\nPath \"%s\" does not seem to be the path to the MakeHuman program" % (trgpath, scn.MhProgramPath))
            maketarget.maketarget.applyTargets(context)
            ob = context.object
            ob.name = "Human"
            ob.MhHuman = True
            makeclothes.removeVertexGroups(context, 'All')
            makeclothes.autoVertexGroups(ob, scn)

        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_ExamineBoundaryButton(bpy.types.Operator):
#

class OBJECT_OT_ExamineBoundaryButton(bpy.types.Operator):
    bl_idname = "mhclo.examine_boundary"
    bl_label = "Examine boundary"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.examineBoundary(context.object, context.scene)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
#

class OBJECT_OT_OffsetClothesButton(bpy.types.Operator):
    bl_idname = "mhclo.offset_clothes"
    bl_label = "Offset clothes"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.offsetCloth(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
#

class OBJECT_OT_SetZDepthButton(bpy.types.Operator):
    bl_idname = "mhclo.set_zdepth"
    bl_label = "Set Z depth"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.setZDepth(context.scene)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
#

class VIEW3D_OT_PrintVnumsButton(bpy.types.Operator):
    bl_idname = "mhclo.print_vnums"
    bl_label = "Print vertex numbers"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.printVertNums(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    class VIEW3D_OT_DeleteHelpersButton(bpy.types.Operator):
#

class VIEW3D_OT_DeleteHelpersButton(bpy.types.Operator):
    bl_idname = "mhclo.delete_helpers"
    bl_label = "Delete helpers until above"
    bl_options = {'UNDO'}
    answer = StringProperty()

    def execute(self, context):
        ob = context.object
        scn = context.scene
        if makeclothes.isHuman(ob):
            makeclothes.deleteHelpers(context)
        return{'FINISHED'}

#
#    class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
#

class VIEW3D_OT_RemoveVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.remove_vertex_groups"
    bl_label = "Remove vertex groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.removeVertexGroups(context, context.scene.MCRemoveGroupType)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#   class VIEW3D_OT_AutoVertexGroupsButton(bpy.types.Operator):
#

class VIEW3D_OT_AutoVertexGroupsButton(bpy.types.Operator):
    bl_idname = "mhclo.auto_vertex_groups"
    bl_label = "Auto vertex groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            makeclothes.removeVertexGroups(context, 'All')
            makeclothes.autoVertexGroups(context.object, context.scene)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}

#
#    Init and register
#

def register():
    makeclothes.init()
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

