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

import bpy, os
from mathutils import Quaternion
from .utils import MocapError
from .io_json import *

def createTPose(context):
    rig = context.object
    scn = context.scene
    if rig.McpHasTPose:
        setTPose(context)
        return

    filepath = os.path.join(os.path.dirname(__file__), "t_pose.json")
    struct = loadJson(filepath)

    for name,value in struct:
        pb = rig.pose.bones[name]
        quat = Quaternion(value)
        pb.matrix_basis = quat.to_matrix().to_4x4()
        rest = quat.inverted()
        pb["McpRestW"] = rest.w
        pb["McpRestX"] = rest.x
        pb["McpRestY"] = rest.y
        pb["McpRestZ"] = rest.z

    children = []
    for ob in scn.objects:
        if ob.type != 'MESH':
            continue
        for mod in ob.modifiers:
            if (mod.type == 'ARMATURE' and
                mod.object == rig):
                children.append((ob, mod.name))
                scn.objects.active = ob
                bpy.ops.object.modifier_apply(apply_as='SHAPE', modifier=mod.name)
                ob.data.shape_keys.key_blocks[mod.name].value = 1

    scn.objects.active = rig
    bpy.ops.pose.armature_apply()
    for ob,name in children:
        scn.objects.active = ob
        mod = ob.modifiers.new(name, 'ARMATURE')
        mod.object = rig
        mod.use_vertex_groups = True
        bpy.ops.object.modifier_move_up(modifier=name)
        setShapeKey(ob, name, 1.0)

    scn.objects.active = rig
    rig.McpHasTPose = True
    print("Created T-pose")


def setShapeKey(ob, name, value):
    if not ob.data.shape_keys:
        return
    skey = ob.data.shape_keys.key_blocks[name]
    skey.value = value


def clearTPose(context):
    rig = context.object
    scn = context.scene
    if not rig.McpHasTPose:
        print(("%s has no defined T-pose" % rig))

    for pb in rig.pose.bones:
        try:
            qw = pb["McpRestW"]
            qx = pb["McpRestX"]
            qy = pb["McpRestY"]
            qz = pb["McpRestZ"]
        except KeyError:
            continue
        quat = Quaternion((qw,qx,qy,qz))
        pb.matrix_basis = quat.to_matrix().to_4x4()
    print("Cleared T-pose")


def setTPose(context):
    rig = context.object
    scn = context.scene
    if not rig.McpHasTPose:
        print(("%s has no defined T-pose" % rig))

    quat = Quaternion((1,0,0,0))
    mat = quat.to_matrix().to_4x4()
    for pb in rig.pose.bones:
        try:
            qw = pb["McpRestW"]
        except KeyError:
            continue
        pb.matrix_basis = mat
    print("Set T-pose")


class VIEW3D_OT_McpCreateTPoseButton(bpy.types.Operator):
    bl_idname = "mcp.create_t_pose"
    bl_label = "Create T-pose"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            createTPose(context)
        except MocapError:
            bpy.ops.mcp.error('INVOKE_DEFAULT')
        return{'FINISHED'}


class VIEW3D_OT_McpSetTPoseButton(bpy.types.Operator):
    bl_idname = "mcp.set_t_pose"
    bl_label = "Set T-pose"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            setTPose(context)
        except MocapError:
            bpy.ops.mcp.error('INVOKE_DEFAULT')
        return{'FINISHED'}


class VIEW3D_OT_McpClearTPoseButton(bpy.types.Operator):
    bl_idname = "mcp.clear_t_pose"
    bl_label = "Clear T-pose"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            clearTPose(context)
        except MocapError:
            bpy.ops.mcp.error('INVOKE_DEFAULT')
        return{'FINISHED'}


def saveTPose(context):
    rig = context.object
    struct = []
    for pb in rig.pose.bones:
        bmat = pb.matrix
        rmat = pb.bone.matrix_local
        if pb.parent:
            bmat = pb.parent.matrix.inverted() * bmat
            rmat = pb.parent.bone.matrix_local.inverted() * rmat
        mat = rmat.inverted() * bmat
        struct.append((pb.name, tuple(mat.to_quaternion())))
    filepath = os.path.join(os.path.dirname(__file__), "t_pose.json")
    saveJson(struct, filepath)


class VIEW3D_OT_McpSaveTPoseButton(bpy.types.Operator):
    bl_idname = "mcp.save_t_pose"
    bl_label = "Save T-pose"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            saveTPose(context)
        except MocapError:
            bpy.ops.mcp.error('INVOKE_DEFAULT')
        print("Saved T-pose")
        return{'FINISHED'}

