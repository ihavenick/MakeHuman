#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Face bone definitions
"""

from .flags import *

Joints = [
    ('head-end',        'l', ((2.0, 'head'), (-1.0, 'neck'))),
    ('l-mouth',         'v', 11942),
    ('r-mouth',         'v', 5339),
]

eyeOffs = (0,0,0.3)

HeadsTails = {
    'jaw' :             ('mouth', 'jaw'),
    'tongue_base' :     ('tongue-1', 'tongue-2'),
    'tongue_mid' :      ('tongue-2', 'tongue-3'),
    'tongue_tip' :      ('tongue-3', 'tongue-4'),

    'eye.R' :           ('r-eye', ('r-eye', eyeOffs)),
    'eye_parent.R' :    ('r-eye', ('r-eye', eyeOffs)),
    'uplid.R' :         ('r-eye', 'r-upperlid'),
    'lolid.R' :         ('r-eye', 'r-lowerlid'),

    'eye.L' :           ('l-eye', ('l-eye', eyeOffs)),
    'eye_parent.L' :    ('l-eye', ('l-eye', eyeOffs)),
    'uplid.L' :         ('l-eye', 'l-upperlid'),
    'lolid.L' :         ('l-eye', 'l-lowerlid'),
}


Armature = {
    'jaw' :             (0, 'head', F_DEF, L_HEAD),
    'tongue_base' :     (0, 'jaw', F_DEF, L_HEAD),
    'tongue_mid' :      (0, 'tongue_base', F_DEF, L_HEAD),
    'tongue_tip' :      (0, 'tongue_mid', F_DEF, L_HEAD),
    'eye.R' :           (0, 'head', F_DEF, L_HEAD),
    'eye.L' :           (0, 'head', F_DEF, L_HEAD),
    'uplid.R' :         (0.279253, 'head', F_DEF, L_HEAD),
    'lolid.R' :         (0, 'head', F_DEF, L_HEAD),
    'uplid.L' :         (-0.279253, 'head', F_DEF, L_HEAD),
    'lolid.L' :         (0, 'head', F_DEF, L_HEAD),
}


CustomShapes = {
    'jaw' :     'GZM_Jaw',
    'eye.R' :   'GZM_Circle025',
    'eye.L' :   'GZM_Circle025',
}

Constraints = {}

RotationLimits = {
    'jaw' : (-5*D,45*D, 0,0, -20*D,20*D),
}


#
#    DeformDrivers(fp, amt):
#

def DeformDrivers(fp, amt):
    return []
    lidBones = [
    ('DEF_uplid.L', 'PUpLid_L', (0, 40*D)),
    ('DEF_lolid.L', 'PLoLid_L', (0, 20*D)),
    ('DEF_uplid.R', 'PUpLid_R', (0, 40*D)),
    ('DEF_lolid.R', 'PLoLid_R', (0, 20*D)),
    ]

    drivers = []
    for (driven, driver, coeff) in lidBones:
        drivers.append(    (driven, 'ROTQ', 'AVERAGE', None, 1, coeff,
         [("var", 'TRANSFORMS', [('OBJECT', amt.name, driver, 'LOC_Z', C_LOC)])]) )
    return drivers

