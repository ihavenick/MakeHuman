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

import bpy
import os
from bpy.props import *
from .utils import getMyDocuments

#----------------------------------------------------------
#   Settings
#----------------------------------------------------------

def drawDirectories(layout, scn, outdir):
    layout.operator("mh.factory_settings")
    layout.operator("mh.read_settings")
    layout.operator("mh.save_settings")
    #layout.label("MakeHuman Program Directory")
    #layout.prop(scn, "MhProgramPath", text="")
    layout.label("Output Directory")
    layout.prop(scn, outdir, text="")
    layout.separator()


def settingsFile(name):
    outdir = os.path.join(getMyDocuments(), "makehuman/settings/")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    return os.path.join(outdir, "make_target.%s" % name)


def readDefaultSettings(context):
    fname = settingsFile("settings")
    try:
        fp = open(fname, "rU")
    except:
        print(("Did not find %s. Using default settings" % fname))
        return

    scn = context.scene
    for line in fp:
        words = line.split()
        prop = words[0]
        value = words[1].replace("\%20", " ")
        scn[prop] = value
    fp.close()
    return


def saveDefaultSettings(context):
    fname = settingsFile("settings")
    fp = open(fname, "w", encoding="utf-8", newline="\n")
    scn = context.scene
    for (key, value) in [
        ("MhProgramPath", scn.MhProgramPath),
        ("MhUserPath", scn.MhUserPath),
        ("MhTargetPath", scn.MhTargetPath),
        ("MhClothesDir", scn.MhClothesDir),
        ("MhUvsDir", scn.MhUvsDir),
        ]:
        fp.write("%s %s\n" % (key, value.replace(" ", "\%20")))
    fp.close()
    return


def restoreFactorySettings(context):
    scn = context.scene
    scn.MhProgramPath = os.path.join(getMyDocuments(), "makehuman")
    scn.MhUserPath = os.path.join(getMyDocuments(), "makehuman")
    scn.MhTargetPath = "/program/makehuman/data/correctives"
    scn.MhClothesDir = os.path.join(getMyDocuments(), "makehuman/data/clothes")
    scn.MhUvsDir = os.path.join(getMyDocuments(), "makehuman/data/uvs")

#----------------------------------------------------------
#   Settings buttons
#----------------------------------------------------------

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mh.factory_settings"
    bl_label = "Restore Factory Settings"

    def execute(self, context):
        restoreFactorySettings(context)
        return{'FINISHED'}


class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mh.save_settings"
    bl_label = "Save Settings"

    def execute(self, context):
        saveDefaultSettings(context)
        return{'FINISHED'}


class OBJECT_OT_ReadSettingsButton(bpy.types.Operator):
    bl_idname = "mh.read_settings"
    bl_label = "Read Settings"

    def execute(self, context):
        readDefaultSettings(context)
        return{'FINISHED'}

#----------------------------------------------------------
#  Init
#----------------------------------------------------------

def init():
    bpy.types.Scene.MhProgramPath = StringProperty(
        name="MakeHuman Program Directory",
        description="Path to the MakeHuman program",
        maxlen=1024,
        default=os.path.join(getMyDocuments(), "makehuman")
    )
    bpy.types.Scene.MhUserPath = StringProperty(
        name = "User Path",
        maxlen=1024,
        default=os.path.join(getMyDocuments(), "makehuman")
    )
    bpy.types.Scene.MhTargetPath = StringProperty(
        name = "Target Path",
        default = "/program/makehuman/data/correctives"
    )
    bpy.types.Scene.MhClothesDir = StringProperty(
        name="Directory",
        description="Path to the directory where clothes are stored",
        maxlen=1024,
        default=os.path.join(getMyDocuments(), "makehuman/data/clothes")
    )
    bpy.types.Scene.MhUvsDir = StringProperty(
        name="Directory",
        description="Path to the directory where UV sets are stored",
        maxlen=1024,
        default=os.path.join(getMyDocuments(), "makehuman/data/uvs")
    )

