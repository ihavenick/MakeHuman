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

Bone definitions for Rigify rig
"""

from collections import OrderedDict
from .flags import *
from .rig_joints import *

PlatysmaLength  = 0.9
LatDorsiLength  = 0.5
BicepsLength    = 0.25
BracLength  = 0.5
FemorisLength   = 0.5
FemorisGoal     = 0.162
SoleusLength    = 0.4

Joints = [
    ('plexus',              'vl', ((0.9, 1892), (0.1, 3960))),
    ('l-breast-2',          'v', 8458),
    ('r-breast-2',          'v', 1786),
    ('l-breast-1',          'vl', ((0.6, 8458), (0.4, 10591))),
    ('r-breast-1',          'vl', ((0.6, 1786), (0.4, 3926))),

    ('l-pect-1',            'vl', ((0.9, 8458), (0.1, 10610))),
    ('r-pect-1',            'vl', ((0.9, 1786), (0.1, 3955))),

    ('l-plat-1',            'v', 7587),
    ('r-plat-1',            'v', 885),
    ('l-plat-2',            'l', ((1-PlatysmaLength, 'l-plat-1'), (PlatysmaLength, 'l-clavicle'))),
    ('r-plat-2',            'l', ((1-PlatysmaLength, 'r-plat-1'), (PlatysmaLength, 'r-clavicle'))),

    ('l-trap-1',            'v', 7561),
    ('r-trap-1',            'v', 850),
    ('l-trap-2',            'v', 8232),
    ('r-trap-2',            'v', 1554),

    ('l-scapula-1',         'vl', ((0.25, 8070), (0.75, 8238))),
    ('r-scapula-1',         'vl', ((0.25, 1378), (0.75, 1560))),
    #('chest-mid',           'l', ((0.5, 'spine-2'), (0.5, 'neck'))),
    ('l-scapula-2',         'l', ((0.5, 'l-scapula-1'), (0.5, 'spine-1'))),
    ('r-scapula-2',         'l', ((0.5, 'r-scapula-1'), (0.5, 'spine-1'))),

    ('l-lat-2',             'l', ((1-LatDorsiLength, 'spine-3'), (LatDorsiLength, 'l-scapula'))),
    ('r-lat-2',             'l', ((1-LatDorsiLength, 'spine-3'), (LatDorsiLength, 'r-scapula'))),

    ('l-biceps-1',          'l', ((0.5, 'l-shoulder'), (0.5, 'l-elbow'))),
    ('r-biceps-1',          'l', ((0.5, 'r-shoulder'), (0.5, 'r-elbow'))),
    ('l-biceps-3',          'v', 8385),
    ('r-biceps-3',          'v', 1713),
    ('l-biceps-2',          'l', ((0.5, 'l-biceps-1'), (0.5, 'l-biceps-3'))),
    ('r-biceps-2',          'l', ((0.5, 'r-biceps-1'), (0.5, 'r-biceps-3'))),

    ('l-triceps-3',         'v', 8394),
    ('r-triceps-3',         'v', 1722),
    ('l-triceps-2',         'l', ((1-BicepsLength, 'l-biceps-1'), (BicepsLength, 'l-triceps-3'))),
    ('r-triceps-2',         'l', ((1-BicepsLength, 'r-biceps-1'), (BicepsLength, 'r-triceps-3'))),

    ('l-brac-1',            'vl', ((0.9, 10076), (0.1, 10543))),
    ('r-brac-1',            'vl', ((0.9, 3408), (0.1, 3878))),
    ('l-pron-1',            'vl', ((0.1, 10076), (0.9, 10543))),
    ('r-pron-1',            'vl', ((0.1, 3408), (0.9, 3878))),
    ('l-brac-3',            'vl', ((0.6, 10554), (0.4, 10220))),
    ('r-brac-3',            'vl', ((0.6, 3889), (0.4, 3552))),
    ('l-pron-2',            'vl', ((0.4, 10554), (0.6, 10220))),
    ('r-pron-2',            'vl', ((0.4, 3889), (0.6, 3552))),
    ('l-brac-2',            'l', ((1-BracLength, 'l-brac-1'), (BracLength, 'l-brac-3'))),
    ('r-brac-2',            'l', ((1-BracLength, 'r-brac-1'), (BracLength, 'r-brac-3'))),

    ('l-hipside',           'vl', ((0.9, 10909), (0.1, 4279))),
    ('r-hipside',           'vl', ((0.1, 10909), (0.9, 4279))),
    ('l-hip',               'vl', ((0.9, 10778), (0.1, 4135))),
    ('r-hip',               'vl', ((0.1, 10778), (0.9, 4135))),
    ('l-gluteus',           'v', 10867),
    ('r-gluteus',           'v', 4233),

    ('l-quadriceps',        'vl', ((0.75, 11135), (0.25, 11130))),
    ('r-quadriceps',        'vl', ((0.75, 4517), (0.25, 4512))),

    ('l-fem-1',             'vl', ((0.2, 11033), (0.8, 11020))),
    ('r-fem-1',             'vl', ((0.2, 4415), (0.8, 4402))),
    ('l-fem-3',             'l', ((1-FemorisGoal, 'l-knee'), (FemorisGoal, 'l-ankle'))),
    ('r-fem-3',             'l', ((1-FemorisGoal, 'r-knee'), (FemorisGoal, 'r-ankle'))),
    ('l-fem-2',             'l', ((1-FemorisLength, 'l-fem-1'), (FemorisLength, 'l-fem-3'))),
    ('r-fem-2',             'l', ((1-FemorisLength, 'r-fem-1'), (FemorisLength, 'r-fem-3'))),

    ('l-knee-1',            'vl', ((0.8, 11116), (0.2, 11111))),
    ('r-knee-1',            'vl', ((0.8, 4498), (0.2, 4493))),
    ('l-knee-2',            'vl', ((0.8, 11135), (0.2, 11130))),
    ('r-knee-2',            'vl', ((0.8, 4517), (0.2, 4512))),

    ('l-soleus-1',          'vl', ((0.5, 11293), (0.5, 11302))),
    ('r-soleus-1',          'vl', ((0.5, 4675), (0.5, 4684))),
    ('l-sole-2',            'v', 12820),
    ('r-sole-2',            'v', 6223),
    ('l-soleus-2',          'l', ((1-SoleusLength, 'l-soleus-1'), (SoleusLength, 'l-sole-2'))),
    ('r-soleus-2',          'l', ((1-SoleusLength, 'r-soleus-1'), (SoleusLength, 'r-sole-2'))),

    ('l-forearm-1',         'l', ((0.7, 'l-elbow'), (0.3, 'l-hand'))),
    ('r-forearm-1',         'l', ((0.7, 'r-elbow'), (0.3, 'r-hand'))),
    ('l-shin-1',            'l', ((0.7, 'l-knee'), (0.3, 'l-ankle'))),
    ('r-shin-1',            'l', ((0.7, 'r-knee'), (0.3, 'r-ankle'))),
]

HeadsTails = {
    'pubis' :              ('pubis', 'spine-3'),
    'ribcage.L' :          ('plexus', 'l-pect-1'),
    'ribcage.R' :          ('plexus', 'r-pect-1'),
    'stomach' :            ('plexus', 'pubis'),
    'breast.L' :           ('l-breast-1', 'l-breast-2'),
    'breast.R' :           ('r-breast-1', 'r-breast-2'),
    'pectoralis.L' :       ('l-pect-1', 'l-scapula'),
    'pectoralis.R' :       ('r-pect-1', 'r-scapula'),

    'platysma.L' :         ('l-plat-1', 'l-plat-2'),
    'platysma.R' :         ('r-plat-1', 'r-plat-2'),
    'trapezius.L' :        ('l-trap-1', 'l-trap-2'),
    'trapezius.R' :        ('r-trap-1', 'r-trap-2'),
    'trap_goal.L' :        ('l-shoulder', 'l-trap-2'),
    'trap_goal.R' :        ('r-shoulder', 'r-trap-2'),
    'scapula.L' :          ('l-scapula-1', 'l-scapula-2'),
    'scapula.R' :          ('r-scapula-1', 'r-scapula-2'),
    'lat_dorsi.L' :        ('spine-3', 'l-lat-2'),
    'lat_dorsi.R' :        ('spine-3', 'r-lat-2'),

    'biceps.L' :           ('l-biceps-1', 'l-biceps-2'),
    'biceps.R' :           ('r-biceps-1', 'r-biceps-2'),
    'triceps.L' :          ('l-elbow', 'l-triceps-2'),
    'triceps.R' :          ('r-elbow', 'r-triceps-2'),

    'trg_elbow.L' :        ('l-elbow', 'l-brac-1'),
    'trg_elbow.R' :        ('r-elbow', 'r-brac-1'),
    'pronator.L' :         ('l-brac-1', 'l-brac-2'),
    'pronator.R' :         ('r-brac-1', 'r-brac-2'),
    'brachioradialis.L' :  ('l-pron-1', 'l-pron-2'),
    'brachioradialis.R' :  ('r-pron-1', 'r-pron-2'),
    'forearmhook.L' :      ('l-brac-3', 'l-pron-2'),
    'forearmhook.R' :      ('r-brac-3', 'r-pron-2'),

    'hipside.L' :          ('pubis', 'l-hipside'),
    'hip.L' :              ('pelvis', 'l-hip'),
    'hipside.R' :          ('pubis', 'r-hipside'),
    'hip.R' :              ('pelvis', 'r-hip'),
    'gluteus.L' :          ('l-upper-leg', 'l-gluteus'),
    'gluteus.R' :          ('r-upper-leg', 'r-gluteus'),

    'quadriceps.L' :       ('l-quadriceps', 'l-hipside'),
    'quadriceps.R' :       ('r-quadriceps', 'r-hipside'),
    'femoris.L' :          ('l-fem-1', 'l-fem-2'),
    'femoris.R' :          ('r-fem-1', 'r-fem-2'),
    'trg_knee.L' :         ('l-knee-1', 'l-knee-2'),
    'trg_knee.R' :         ('r-knee-1', 'r-knee-2'),
    'soleus.L' :           ('l-soleus-1', 'l-soleus-2'),
    'soleus.R' :           ('r-soleus-1', 'r-soleus-2'),
    'sole.L' :             ('l-foot-1', 'l-sole-2'),
    'sole.R' :             ('r-foot-1', 'r-sole-2'),

    'elbow_fan.L' :        ('l-elbow', 'l-forearm-1'),
    'elbow_fan.R' :        ('r-elbow', 'r-forearm-1'),
    'knee_fan.L' :         ('l-knee', 'l-shin-1'),
    'knee_fan.R' :         ('r-knee', 'r-shin-1'),
}


Armature = {
    'breast.L' :           (0, 'chest-1', F_WIR|F_DEF, L_TWEAK),
    'breast.R' :           (0, 'chest-1', F_WIR|F_DEF, L_TWEAK),
    'pubis' :              (0, 'hips', 0, L_HELP),
    'stomach' :            (0, 'chest-1',  F_DEF, L_MSCL),

    'pectoralis.L' :       (173*D, 'chest-1', F_DEF, L_MSCL),
    'platysma.L' :         (-153*D, 'neck', F_DEF, L_MSCL),
    'trapezius.L' :        (176*D, 'chest-1', F_DEF|F_CON, L_MSCL),
    'trap_goal.L' :        (0, 'shoulder.L', F_CON, L_MSCL),
    'lat_dorsi.L' :        (74*D, 'chest-1', F_DEF, L_MSCL),
    'scapula.L' :          (-24*D, 'shoulder.L', F_DEF, L_MSCL),

    'pectoralis.R' :       (-173*D, 'chest-1', F_DEF, L_MSCL),
    'platysma.R' :         (153*D, 'neck', F_DEF, L_MSCL),
    'trapezius.R' :        (-176*D, 'chest-1', F_DEF|F_CON, L_MSCL),
    'trap_goal.R' :        (0, 'shoulder.R', F_CON, L_MSCL),
    'lat_dorsi.R' :        (-74*D, 'chest-1', F_DEF, L_MSCL),
    'scapula.R' :          (24*D, 'shoulder.R', F_DEF, L_MSCL),

    'biceps.L' :           (91*D, 'upper_arm.L', F_DEF, L_MSCL),
    'triceps.L' :          (-101*D, 'upper_arm.L', F_DEF, L_MSCL),
    #'trg_elbow.L' :        (-105*D, 'upper_arm.L', F_DEF|F_CON, L_MSCL),
    #'pronator.L' :         (10*D, 'trg_elbow.L', F_DEF|F_CON, L_MSCL),
    #'brachioradialis.L' :  (74*D, 'forearm.L', F_DEF, L_MSCL),
    #'forearmhook.L' :      (0, 'hand.L',0, L_MSCL),

    'biceps.R' :           (-91*D, 'upper_arm.R', F_DEF, L_MSCL),
    'triceps.R' :          (101*D, 'upper_arm.R', F_DEF, L_MSCL),
    #'trg_elbow.R' :        (105*D, 'upper_arm.R', F_DEF|F_CON, L_MSCL),
    #'pronator.R' :         (-10*D, 'trg_elbow.R', F_DEF|F_CON, L_MSCL),
    #'brachioradialis.R' :  (-74*D, 'forearm.R', F_DEF, L_MSCL),
    #'forearmhook.R' :      (0, 'hand.R',0, L_MSCL),

    'hipside.L' :          (0, 'hips', 0, L_HELP),
    #'hip.L' :              (0, 'pelvis', F_DEF, L_MSCL),
    #'gluteus.L' :          (0, 'root', F_DEF, L_MSCL),
    'hipside.R' :          (0, 'hips', 0, L_HELP),
    #'hip.R' :              (0, 'pelvis', F_DEF, L_MSCL),
    #'gluteus.R' :          (0, 'root', F_DEF, L_MSCL),

    'quadriceps.L' :       (-8*D, 'thigh.L', F_DEF, L_MSCL),
    'femoris.L' :          (-177*D, 'thigh.L', F_DEF, L_MSCL),
    'trg_knee.L' :         (-179*D, 'thigh.L', F_DEF, L_MSCL),
    'soleus.L' :           (168*D, 'shin.L', F_DEF, L_MSCL),
    'sole.L' :             (0, 'foot.L', 0, L_MSCL),

    'quadriceps.R' :       (8*D, 'thigh.R', F_DEF, L_MSCL),
    'femoris.R' :          (177*D, 'thigh.R', F_DEF, L_MSCL),
    'trg_knee.R' :         (179*D, 'thigh.R', F_DEF, L_MSCL),
    'soleus.R' :           (-168*D  , 'shin.R', F_DEF, L_MSCL),
    'sole.R' :             (0, 'foot.R', 0, L_MSCL),

    'elbow_fan.L' :        ('forearm.L', 'upper_arm.L', F_DEF, L_MSCL),
    'elbow_fan.R' :        ('forearm.R', 'upper_arm.R', F_DEF, L_MSCL),
    'knee_fan.L' :         ('shin.L', 'thigh.L', F_DEF, L_MSCL),
    'knee_fan.R' :         ('shin.R', 'thigh.R', F_DEF, L_MSCL),
}

CustomShapes = {
    'breast.L' :        'GZM_Breast_L',
    'breast.R' :        'GZM_Breast_R',
}

RotationLimits = {}

Constraints = {
    'pubis' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'hips', 1, 1, ('pubis', 'spine-3')])
        ],

    'stomach' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'pubis', 0, 1, ('plexus', 'pubis')])
        ],


    # Left side

    'pectoralis.L' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shoulder.L', 1, 1, ('l-pect-1', 'l-scapula')])
        ],

    'platysma.L' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shoulder.L', 0, 1, ('l-plat-1', 'l-clavicle')])
        ],

    'trapezius.L' : [
        ('StretchTo', C_VOLZ, 1,
            ['Stretch_To', 'trap_goal.L', 1, 1])
        ],

    'scapula.L' : [
        ('TrackTo', 0, 1,
            ['Chest', 'chest-1', 0, 'TRACK_Y', 'UP_Z', False])
        ],

    'lat_dorsi.L' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shoulder.L', 1, 1, ('spine-3', 'l-scapula')])
        ],

    #'deltoid.L' : [
    #    ('StretchTo', C_VOLXZ, 1,
    #        ['Stretch_To', 'upper_arm.L', 0, 1, ('l-scapula', 'l-shoulder')])
    #    ],

    'biceps.L' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'forearm.L',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'SCALE', (1,1,1), (1.3,1.4,1.3)])
        ],

    'triceps.L' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'forearm.L',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'SCALE', (1,1,1), (1.3,0.8,1.3)])
        ],

    'trg_elbow.L' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'forearm.L',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'ROTATION', (0,0,0), (29,0,0)])
        ],

    'pronator.L' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'forearmhook.L', 0, 1, ('l-brac-1', 'l-brac-3')])
        ],

    'brachioradialis.L' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'forearmhook.L', 1, 1])
        ],

    'quadriceps.L' : [
        ('StretchTo', 0, 1,
            ['Stretch_To', 'hipside.L', 1, 5, ('l-quadriceps', 'l-hipside')])
        ],

    'femoris.L' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shin.L', FemorisGoal, 1, ('l-fem-1', 'l-fem-3')])
        ],

    'trg_knee.L' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'shin.L',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'SCALE', (1,1,1), (1.3,1.4,1.3)])
        ],

    'soleus.L' : [
        ('StretchTo', C_VOLX, 1,
            ['Stretch_To', 'sole.L', 1, 1, ('l-soleus-1', 'l-sole-2')])
        ],

    # Right side

    'pectoralis.R' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shoulder.R', 1, 1, ('r-pect-1', 'r-scapula')])
        ],

    'platysma.R' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shoulder.R', 0, 1, ('r-plat-1', 'r-clavicle')])
        ],

    'trapezius.R' : [
        ('StretchTo', C_VOLZ, 1,
            ['Stretch_To', 'trap_goal.R', 1, 1])
        ],

    'scapula.R' : [
        ('TrackTo', 0, 1,
            ['Chest', 'chest-1', 0, 'TRACK_Y', 'UP_Z', False])
        ],

    'lat_dorsi.R' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shoulder.R', 1, 1, ('spine-3', 'r-scapula')])
        ],

    #'deltoid.R' : [
    #    ('StretchTo', C_VOLXZ, 1,
    #        ['Stretch_To', 'upper_arm.R', 0, 1, ('r-scapula', 'r-shoulder')])
    #    ],

    'biceps.R' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'forearm.R',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'SCALE', (1,1,1), (1.3,1.4,1.3)])
        ],

    'triceps.R' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'forearm.R',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'SCALE', (1,1,1), (1.3,0.8,1.3)])
        ],

    'trg_elbow.R' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'forearm.R',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'ROTATION', (0,0,0), (29,0,0)])
        ],

    'pronator.R' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'forearmhook.R', 0, 1, ('r-brac-1', 'r-brac-3')])
        ],

    'brachioradialis.R' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'forearmhook.R', 1, 1])
        ],

    'quadriceps.R' : [
        ('StretchTo', 0, 1,
            ['Stretch_To', 'hipside.R', 1, 5, ('r-quadriceps', 'r-hipside')])
        ],

    'femoris.R' : [
        ('StretchTo', C_VOLXZ, 1,
            ['Stretch_To', 'shin.R', FemorisGoal, 1, ('r-fem-1', 'r-fem-3')])
        ],

    'trg_knee.R' : [
        ('Transform', C_LOCAL, 1,
            ['Transform', 'shin.R',
                'ROTATION', (0,0,0), (90,0,0),
                ('X','X','X'),
                'SCALE', (1,1,1), (1.3,1.4,1.3)])
        ],

    'soleus.R' : [
        ('StretchTo', C_VOLX, 1,
            ['Stretch_To', 'sole.R', 1, 1, ('r-soleus-1', 'r-sole-2')])
        ],

    'elbow_fan.L' : [
        ('CopyRot', C_LOCAL, 0.5,
            ['forearm', 'forearm.L', (1,0,1), (0,0,0), False])
        ],

    'elbow_fan.R' : [
        ('CopyRot', C_LOCAL, 0.5,
            ['forearm', 'forearm.R', (1,0,1), (0,0,0), False])
        ],

    'knee_fan.L' : [
        ('CopyRot', C_LOCAL, 0.5,
            ['shin', 'shin.L', (1,0,1), (0,0,0), False])
        ],

    'knee_fan.R' : [
        ('CopyRot', C_LOCAL, 0.5,
            ['shin', 'shin.R', (1,0,1), (0,0,0), False])
        ],
}

