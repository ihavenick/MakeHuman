# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; eimcp.r version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See mcp.
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
from bpy.props import *
import math
import os

from . import utils
from . import mcp
from .utils import MocapError

Deg2Rad = math.pi/180

#
#   getTrgBone(b):
#

def getTrgBone(b):
    try:
        return mcp.trgBone[b]
    except:
        return None


def renameBone(b):
    try:
        return mcp.renames[b]
    except:
        return b

#
#   getTargetArmature(rig, scn):
#

def getTargetArmature(rig, scn):
    bones = rig.data.bones.keys()
    if scn.McpGuessTargetRig:
        name = guessArmature(rig, bones, scn)
        scn.McpTargetRig = name
    else:
        try:
            name = scn.McpTargetRig
        except:
            raise MocapError("Initialize Target Panel first")
    mcp.target = name
    (boneAssoc, mcp.renames, mcp.ikBones) = mcp.targetInfo[name]
    if not testTargetRig(name, bones, boneAssoc):
        print("Bones", bones)
        raise MocapError("Target armature %s does not match armature %s" % (rig.name, name))
    print("Target armature %s" % name)
    parAssoc = assocParents(rig, boneAssoc, mcp.renames)
    return (boneAssoc, parAssoc, None)


def guessArmature(rig, bones, scn):
    ensureTargetInited(scn)
    print("Guessing")
    if 'KneePT_L' in bones:
        return 'MHX'
    else:
        for (name, info) in mcp.targetInfo.items():
            (boneAssoc, mcp.renames, mcp.ikBones) = info
            if testTargetRig(name, bones, boneAssoc):
                return name
    print("Bones", bones)
    raise MocapError("Did not recognize target armature %s" % rig.name)


def assocParents(rig, boneAssoc, names):
    parAssoc = {}
    mcp.trgBone = {}
    taken = [ None ]
    for (name, mhx) in boneAssoc:
        name = getName(name, names)
        mcp.trgBone[mhx] = name
        pb = rig.pose.bones[name]
        taken.append(name)
        parAssoc[name] = None
        parent = pb.parent
        while parent:
            pname = getName(parent.name, names)
            if pname in taken:
                parAssoc[name] = pname
                break
            else:
                parent = rig.pose.bones[pname].parent
    return parAssoc


def getName(name, names):
    try:
        return names[name]
    except:
        return name


def testTargetRig(name, bones, rigBones):
    #print("Testing %s" % name)
    for (b, mb) in rigBones:
        if b not in bones:
            #print("Failed to find", b, mb)
            return False
    return True

#
#   findTargetKey(mhx, list):
#

def findTargetKey(mhx, list):
    for (bone, mhx1) in list:
        if mhx1 == mhx:
            return bone
    return None

###############################################################################
#
#    Target armatures
#
###############################################################################

#    (mhx bone, text)

TargetBoneNames = [
    ('hips',        'Root bone'),
    ('spine',        'Lower spine'),
    ('spine-1',        'Middle spine'),
    ('Spine3',        'Upper spine'),
    ('chest',        'Neck'),
    ('head',        'Head'),
    None,
    ('shoulder.L',    'L clavicle'),
    ('upper_arm.L',        'L upper arm'),
    ('forearm.L',        'L forearm'),
    ('hand.L',        'L hand'),
    None,
    ('shoulder.R',    'R clavicle'),
    ('upper_arm.R',        'R upper arm'),
    ('forearm.R',        'R forearm'),
    ('hand.R',        'R hand'),
    None,
    ('hip.L',        'L hip'),
    ('thigh.L',        'L thigh'),
    ('shin.L',        'L shin'),
    ('foot.L',        'L foot'),
    ('toe.L',        'L toes'),
    None,
    ('hip.R',        'R hip'),
    ('thigh.R',        'R thigh'),
    ('shin.R',        'R shin'),
    ('foot.R',        'R foot'),
    ('toe.R',        'R toes'),
]

###############################################################################
#
#    Target initialization
#
###############################################################################


def loadTargets():
    mcp.targetInfo = {}

def isTargetInited(scn):
    try:
        scn.McpTargetRig
        return True
    except:
        return False


def initTargets(scn):
    mcp.targetInfo = {}
    path = os.path.join(os.path.dirname(__file__), "target_rigs")
    for fname in os.listdir(path):
        file = os.path.join(path, fname)
        (name, ext) = os.path.splitext(fname)
        if ext == ".trg" and os.path.isfile(file):
            (name, stuff) = readTrgArmature(file, name)
            mcp.targetInfo[name] = stuff

    mcp.trgArmatureEnums = []
    keys = list(mcp.targetInfo.keys())
    keys.sort()
    for key in keys:
        mcp.trgArmatureEnums.append((key,key,key))

    bpy.types.Scene.McpTargetRig = EnumProperty(
        items = mcp.trgArmatureEnums,
        name = "Target rig",
        default = 'Xonotic')
    scn.McpTargetRig = 'Xonotic'
    print("Defined McpTargetRig")
    return


def readTrgArmature(file, name):
    print("Read target file", file)
    fp = open(file, "r")
    status = 0
    bones = []
    renames = {}
    ikbones = []
    for line in fp:
        words = line.split()
        if len(words) > 0:
            key = words[0].lower()
            if key[0] == "#":
                continue
            elif key == "name:":
                name = words[1]
            elif key == "bones:":
                status = 1
            elif key == "ikbones:":
                status = 2
            elif key == "renames:":
                status = 3
            elif len(words) != 2:
                print("Ignored illegal line", line)
            elif status == 1:
                bones.append( (words[0], utils.nameOrNone(words[1])) )
            elif status == 2:
                ikbones.append( (words[0], utils.nameOrNone(words[1])) )
            elif status == 3:
                renames[words[0]] = utils.nameOrNone(words[1])
    fp.close()
    return (name, (bones,renames,ikbones))


def ensureTargetInited(scn):
    if not isTargetInited(scn):
        initTargets(scn)


class VIEW3D_OT_McpInitTargetsButton(bpy.types.Operator):
    bl_idname = "mcp.init_targets"
    bl_label = "Init Target Panel"
    bl_options = {'UNDO'}


    def execute(self, context):
        initTargets(context.scene)
        return{'FINISHED'}
