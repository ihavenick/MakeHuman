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

import bpy
import os
import shutil
from . import mc

print("Reload materials")

def checkObjectHasDiffuseTexture(ob):
    """
    An object must either lack material, or have a diffuse texture.
    """
    if ob.data.materials:
        mat = ob.data.materials[0]
        if mat is None:
            return True
        else:
            for mtex in mat.texture_slots:
                if mtex is None:
                    continue
                if mtex.use_map_color_diffuse:
                    return True
        return False
    else:
        return True


def writeMaterial(fp, ob, folder):
    """
    Create an mhmat file and write material settings there.
    """
    if ob.data.materials:
        mat = ob.data.materials[0]
        if mat is None:
            return None
        else:
            name = mc.goodName(mat.name)
            _,filepath = mc.getFileName(ob, folder, "mhmat")
            outdir = os.path.dirname(filepath)
            print(("Create material file %s" % filepath))
            try:
                with open(filepath, "w", encoding="utf-8") as fp:
                    matfile = writeMaterialFile(fp, mat, name, outdir)
            except IOError:
                raise error.MhcloError("Cannot create material file %s" % filepath)
            print(("%s created" % filepath))
            return os.path.basename(filepath)
    return None


def writeMaterialFile(fp, mat, name, outdir):
    """
    Write a material (.mhmat) file in the output folder.
    Also copies all textures to the output folder
    """

    fp.write(
        '# Material definition for MakeHuman benchmark clothes\n' +
        '\n' +
        'name %sMaterial\n' % name +
        '\n' +
        '// Color shading attributes\n'
        'ambientColor 1.0 1.0 1.0\n' +
        'diffuseColor  %.4g %.4g %.4g\n' % tuple(mat.diffuse_color) +
        'diffuseIntensity %.4g\n' % mat.diffuse_intensity +
        'specularColor  %.4g %.4g %.4g\n' % tuple(mat.specular_color) +
        'specularIntensity %.4g\n' % mat.specular_intensity +
        'specularHardness %.4g\n' % mat.specular_hardness +
        'opacity %.4g\n' % mat.alpha +
        '\n' +
        '// Textures and properties\n')

    useDiffuse = useSpecular = useBump = useNormal = useDisplacement = "false"
    for mtex in mat.texture_slots:
        if mtex is None:
            continue
        tex = mtex.texture
        blenddir = os.path.dirname(bpy.data.filepath)
        relpath =  bpy.path.relpath(tex.image.filepath)     # starts with //
        filepath = os.path.join(blenddir, relpath[2:])
        texpath = os.path.basename(filepath)

        if mtex.use_map_color_diffuse:
            fp.write('diffuseTexture %s\n' % texpath)
            useDiffuse = "true"
        if mtex.use_map_alpha:
            useAlpha = "true"
        if mtex.use_map_specular:
            fp.write('specularTexture %s\n' % texpath)
            useSpecular = "true"
        if mtex.use_map_normal:
            if True:
                fp.write('bumpTexture %s\n' % texpath)
                useBump = "true"
            else:
                fp.write('normalTexture %s\n' % texpath)
                useNormal = "true"
        if mtex.use_map_displacement:
            fp.write('displacementTexture %s\n' % texpath)
            useDisplacement = "true"

        print(("Copy texture %s => %s" % (filepath, outdir)))
        shutil.copy(filepath, outdir)

    fp.write(
        '\n' +
        '// Shader programme\n' +
        'shader data/shaders/glsl/phong\n' +
        '\n' +
        '// Configure built-in shader defines\n' +
        'shaderConfig diffuse %s\n' % useDiffuse +
        'shaderConfig bump %s\n' % useBump +
        'shaderConfig normal  %s\n' % useNormal +
        'shaderConfig displacement  %s\n' % useDisplacement +
        'shaderConfig spec  %s\n' % useSpecular +
        'shaderConfig vertexColors true\n')

