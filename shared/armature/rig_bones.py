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

from .flags import *
from .rig_joints import *

Joints = [
    ('spine-23',            'l', ((0.5, 'spine-2'), (0.5, 'spine-3'))),

    ('l-toe-2',             'p', ('l-foot-2', 'l-foot-1', 'l-foot-2')),
    ('r-toe-2',             'p', ('r-foot-2', 'r-foot-1', 'r-foot-2')),

    ('l-kneecap',           'vo', (11223, 0,0,1)),
    ('r-kneecap',           'vo', (4605, 0,0,-1)),

    ('l-hand-end',          'j', 'l-finger-3-1'),
    ('r-hand-end',          'j', 'r-finger-3-1'),

    ('l-palm-02',           'vl', ((0.5, 9906), (0.5, 10500))),
    ('l-palm-03',           'vl', ((0.5, 9895), (0.5, 10497))),
    ('l-palm-04',           'vl', ((0.5, 9897), (0.5, 10495))),
    ('l-palm-05',           'vl', ((0.5, 9894), (0.5, 10494))),

    ('r-palm-02',           'vl', ((0.5, 3238), (0.5, 3834))),
    ('r-palm-03',           'vl', ((0.5, 3227), (0.5, 3831))),
    ('r-palm-04',           'vl', ((0.5, 3226), (0.5, 3829))),
    ('r-palm-05',           'vl', ((0.5, 3232), (0.5, 3828))),

    ('l-plane-thumb-1',     'v', 10291),
    ('l-plane-thumb-2',     'v', 9401),
    ('l-plane-thumb-3',     'v', 9365),

    ('r-plane-thumb-1',     'v', 3623),
    ('r-plane-thumb-2',     'v', 2725),
    ('r-plane-thumb-3',     'v', 2697),

    ('l-plane-foot',        'o', ('l-ankle', (0,-1,0))),
    ('r-plane-foot',        'o', ('r-ankle', (0,-1,0))),
    ('l-plane-toe',         'o', ('l-foot-1', (0,-1,0))),
    ('r-plane-toe',         'o', ('r-foot-1', (0,-1,0))),

    ('pubis',               'vl', ((0.9, 4341), (0.1, 4250))),
]


HeadsTails = {
    'hips' :               ('pelvis', 'spine-3'),
    'spine' :              ('spine-3', 'spine-23'),
    'spine-1' :            ('spine-23', 'spine-2'),
    'chest' :              ('spine-2', 'spine-1'),
    'chest-1' :            ('spine-1', 'neck'),
    'neck' :               ('neck', 'head'),
    'head' :               ('head', 'head-2'),

    'shoulder.L' :         ('l-clavicle', 'l-scapula'),
    'deltoid.L' :          ('l-scapula', 'l-shoulder'),
    'upper_arm.L' :        ('l-shoulder', 'l-elbow'),
    'forearm.L' :          ('l-elbow', 'l-hand'),
    'hand.L' :             ('l-hand', 'l-hand-end'),

    'shoulder.R' :         ('r-clavicle', 'r-scapula'),
    'deltoid.R' :          ('r-scapula', 'r-shoulder'),
    'upper_arm.R' :        ('r-shoulder', 'r-elbow'),
    'forearm.R' :          ('r-elbow', 'r-hand'),
    'hand.R' :             ('r-hand', 'r-hand-end'),

    'thumb.01.L' :         ('l-finger-1-1', 'l-finger-1-2'),
    'thumb.02.L' :         ('l-finger-1-2', 'l-finger-1-3'),
    'thumb.03.L' :         ('l-finger-1-3', 'l-finger-1-4'),

    'thumb.01.R' :         ('r-finger-1-1', 'r-finger-1-2'),
    'thumb.02.R' :         ('r-finger-1-2', 'r-finger-1-3'),
    'thumb.03.R' :         ('r-finger-1-3', 'r-finger-1-4'),

    'palm_index.L' :       ('l-palm-02', 'l-finger-2-1'),
    'f_index.01.L' :       ('l-finger-2-1', 'l-finger-2-2'),
    'f_index.02.L' :       ('l-finger-2-2', 'l-finger-2-3'),
    'f_index.03.L' :       ('l-finger-2-3', 'l-finger-2-4'),

    'palm_index.R' :       ('r-palm-02', 'r-finger-2-1'),
    'f_index.01.R' :       ('r-finger-2-1', 'r-finger-2-2'),
    'f_index.02.R' :       ('r-finger-2-2', 'r-finger-2-3'),
    'f_index.03.R' :       ('r-finger-2-3', 'r-finger-2-4'),

    'palm_middle.L' :      ('l-palm-03', 'l-finger-3-1'),
    'f_middle.01.L' :      ('l-finger-3-1', 'l-finger-3-2'),
    'f_middle.02.L' :      ('l-finger-3-2', 'l-finger-3-3'),
    'f_middle.03.L' :      ('l-finger-3-3', 'l-finger-3-4'),

    'palm_middle.R' :      ('r-palm-03', 'r-finger-3-1'),
    'f_middle.01.R' :      ('r-finger-3-1', 'r-finger-3-2'),
    'f_middle.02.R' :      ('r-finger-3-2', 'r-finger-3-3'),
    'f_middle.03.R' :      ('r-finger-3-3', 'r-finger-3-4'),

    'palm_ring.L' :        ('l-palm-04', 'l-finger-4-1'),
    'f_ring.01.L' :        ('l-finger-4-1', 'l-finger-4-2'),
    'f_ring.02.L' :        ('l-finger-4-2', 'l-finger-4-3'),
    'f_ring.03.L' :        ('l-finger-4-3', 'l-finger-4-4'),

    'palm_ring.R' :        ('r-palm-04', 'r-finger-4-1'),
    'f_ring.01.R' :        ('r-finger-4-1', 'r-finger-4-2'),
    'f_ring.02.R' :        ('r-finger-4-2', 'r-finger-4-3'),
    'f_ring.03.R' :        ('r-finger-4-3', 'r-finger-4-4'),

    'palm_pinky.L' :       ('l-palm-05', 'l-finger-5-1'),
    'f_pinky.01.L' :       ('l-finger-5-1', 'l-finger-5-2'),
    'f_pinky.02.L' :       ('l-finger-5-2', 'l-finger-5-3'),
    'f_pinky.03.L' :       ('l-finger-5-3', 'l-finger-5-4'),

    'palm_pinky.R' :       ('r-palm-05', 'r-finger-5-1'),
    'f_pinky.01.R' :       ('r-finger-5-1', 'r-finger-5-2'),
    'f_pinky.02.R' :       ('r-finger-5-2', 'r-finger-5-3'),
    'f_pinky.03.R' :       ('r-finger-5-3', 'r-finger-5-4'),

    'thigh.L' :            ('l-upper-leg', 'l-knee'),
    'shin.L' :             ('l-knee', 'l-ankle'),
    'foot.L' :             ('l-ankle', 'l-foot-1'),
    'toe.L' :              ('l-foot-1', 'l-toe-2'),

    'thigh.R' :            ('r-upper-leg', 'r-knee'),
    'shin.R' :             ('r-knee', 'r-ankle'),
    'foot.R' :             ('r-ankle', 'r-foot-1'),
    'toe.R' :              ('r-foot-1', 'r-toe-2'),
}

Planes = {
    "PlaneArm.L" :         ('l-shoulder', 'l-elbow', 'l-hand'),
    "PlaneLeg.L" :         ('l-upper-leg', 'l-kneecap', 'l-ankle'),
    "PlaneFoot.L" :        ('l-plane-foot', 'l-ankle', 'l-foot-1'),
    "PlaneToe.L" :         ('l-plane-toe', 'l-foot-1', 'l-toe-2'),

    "PlaneThumb.L" :       ('l-plane-thumb-1', 'l-plane-thumb-2', 'l-plane-thumb-3'),
    "PlaneIndex.L" :       ('l-finger-2-1', 'l-finger-2-2', 'l-finger-2-4'),
    "PlaneMiddle.L" :      ('l-finger-3-1', 'l-finger-3-2', 'l-finger-3-4'),
    "PlaneRing.L" :        ('l-finger-4-1', 'l-finger-4-2', 'l-finger-4-4'),
    "PlanePinky.L" :       ('l-finger-5-1', 'l-finger-5-2', 'l-finger-5-4'),

    "PlaneArm.R" :         ('r-shoulder', 'r-elbow', 'r-hand'),
    "PlaneLeg.R" :         ('r-upper-leg', 'r-kneecap', 'r-ankle'),
    "PlaneFoot.R" :        ('r-plane-foot', 'r-ankle', 'r-foot-1'),
    "PlaneToe.R" :         ('r-plane-toe', 'r-foot-1', 'r-toe-2'),

    "PlaneThumb.R" :       ('r-plane-thumb-1', 'r-plane-thumb-2', 'r-plane-thumb-3'),
    "PlaneIndex.R" :       ('r-finger-2-1', 'r-finger-2-2', 'r-finger-2-4'),
    "PlaneMiddle.R" :      ('r-finger-3-1', 'r-finger-3-2', 'r-finger-3-4'),
    "PlaneRing.R" :        ('r-finger-4-1', 'r-finger-4-2', 'r-finger-4-4'),
    "PlanePinky.R" :       ('r-finger-5-1', 'r-finger-5-2', 'r-finger-5-4'),
}

Armature = {
    'hips' :               (0, None, F_DEF, L_UPSPNFK),
    'spine' :              (0, 'hips', F_DEF|F_CON, L_UPSPNFK),
    'spine-1' :            (0, 'spine', F_DEF|F_CON, L_UPSPNFK),
    'chest' :              (0, 'spine-1', F_DEF|F_CON, L_UPSPNFK),
    'chest-1' :            (0, 'chest', F_DEF|F_CON, L_UPSPNFK),
    'neck' :               (0, 'chest-1', F_DEF|F_CON, L_UPSPNFK),
    'head' :               (0, 'neck', F_DEF|F_CON, L_UPSPNFK),

    'shoulder.L' :         (0, 'chest-1', F_DEF, L_UPSPNFK|L_LARMFK|L_LARMIK),
    'deltoid.L' :          (0, 'shoulder.L', F_DEF|F_CON, L_UPSPNFK|L_LARMFK|L_LARMIK),
    'upper_arm.L' :        ("PlaneArm.L", 'deltoid.L', F_DEF|F_CON, L_LARMFK),
    'forearm.L' :          ("PlaneArm.L", 'upper_arm.L', F_DEF|F_CON, L_LARMFK),
    'hand.L' :             ("PlaneArm.L", 'forearm.L', F_DEF|F_CON, L_LARMFK),

    'shoulder.R' :         (0, 'chest-1', F_DEF, L_UPSPNFK|L_RARMFK|L_RARMIK),
    'deltoid.R' :          (0, 'shoulder.R', F_DEF|F_CON, L_UPSPNFK|L_RARMFK|L_RARMIK),
    'upper_arm.R' :        ("PlaneArm.R", 'deltoid.R', F_DEF|F_CON, L_RARMFK),
    'forearm.R' :          ("PlaneArm.R", 'upper_arm.R', F_DEF|F_CON, L_RARMFK),
    'hand.R' :             ("PlaneArm.R", 'forearm.R', F_DEF|F_CON, L_RARMFK),

    'thumb.01.L' :         ("PlaneThumb.L", 'hand.L', F_DEF, L_LPALM),
    'thumb.02.L' :         ("PlaneThumb.L", 'thumb.01.L', F_DEF|F_CON, L_LHANDFK),
    'thumb.03.L' :         ("PlaneThumb.L", 'thumb.02.L', F_DEF|F_CON, L_LHANDFK),

    'thumb.01.R' :         ("PlaneThumb.R", 'hand.R', F_DEF, L_RPALM),
    'thumb.02.R' :         ("PlaneThumb.R", 'thumb.01.R', F_DEF|F_CON, L_RHANDFK),
    'thumb.03.R' :         ("PlaneThumb.R", 'thumb.02.R', F_DEF|F_CON, L_RHANDFK),

    'palm_index.L' :       ("PlaneIndex.L", 'hand.L', F_DEF, L_LPALM),
    'f_index.01.L' :       ("PlaneIndex.L", 'palm_index.L', F_DEF|F_CON, L_LHANDFK),
    'f_index.02.L' :       ("PlaneIndex.L", 'f_index.01.L', F_DEF|F_CON, L_LHANDFK),
    'f_index.03.L' :       ("PlaneIndex.L", 'f_index.02.L', F_DEF|F_CON, L_LHANDFK),

    'palm_index.R' :       ("PlaneIndex.R", 'hand.R', F_DEF, L_RPALM),
    'f_index.01.R' :       ("PlaneIndex.R", 'palm_index.R', F_DEF|F_CON, L_RHANDFK),
    'f_index.02.R' :       ("PlaneIndex.R", 'f_index.01.R', F_DEF|F_CON, L_RHANDFK),
    'f_index.03.R' :       ("PlaneIndex.R", 'f_index.02.R', F_DEF|F_CON, L_RHANDFK),

    'palm_middle.L' :      ("PlaneMiddle.L", 'hand.L', F_DEF, L_LPALM),
    'f_middle.01.L' :      ("PlaneMiddle.L", 'palm_middle.L', F_DEF|F_CON, L_LHANDFK),
    'f_middle.02.L' :      ("PlaneMiddle.L", 'f_middle.01.L', F_DEF|F_CON, L_LHANDFK),
    'f_middle.03.L' :      ("PlaneMiddle.L", 'f_middle.02.L', F_DEF|F_CON, L_LHANDFK),

    'palm_middle.R' :      ("PlaneMiddle.R", 'hand.R', F_DEF, L_RPALM),
    'f_middle.01.R' :      ("PlaneMiddle.R", 'palm_middle.R', F_DEF|F_CON, L_RHANDFK),
    'f_middle.02.R' :      ("PlaneMiddle.R", 'f_middle.01.R', F_DEF|F_CON, L_RHANDFK),
    'f_middle.03.R' :      ("PlaneMiddle.R", 'f_middle.02.R', F_DEF|F_CON, L_RHANDFK),

    'palm_ring.L' :        ("PlaneRing.L", 'hand.L', F_DEF, L_LPALM),
    'f_ring.01.L' :        ("PlaneRing.L", 'palm_ring.L', F_DEF|F_CON, L_LHANDFK),
    'f_ring.02.L' :        ("PlaneRing.L", 'f_ring.01.L', F_DEF|F_CON, L_LHANDFK),
    'f_ring.03.L' :        ("PlaneRing.L", 'f_ring.02.L', F_DEF|F_CON, L_LHANDFK),

    'palm_ring.R' :        ("PlaneRing.R", 'hand.R', F_DEF, L_RPALM),
    'f_ring.01.R' :        ("PlaneRing.R", 'palm_ring.R', F_DEF|F_CON, L_RHANDFK),
    'f_ring.02.R' :        ("PlaneRing.R", 'f_ring.01.R', F_DEF|F_CON, L_RHANDFK),
    'f_ring.03.R' :        ("PlaneRing.R", 'f_ring.02.R', F_DEF|F_CON, L_RHANDFK),

    'palm_pinky.L' :       ("PlanePinky.L", 'hand.L', F_DEF, L_LPALM),
    'f_pinky.01.L' :       ("PlanePinky.L", 'palm_pinky.L', F_DEF|F_CON, L_LHANDFK),
    'f_pinky.02.L' :       ("PlanePinky.L", 'f_pinky.01.L', F_DEF|F_CON, L_LHANDFK),
    'f_pinky.03.L' :       ("PlanePinky.L", 'f_pinky.02.L', F_DEF|F_CON, L_LHANDFK),

    'palm_pinky.R' :       ("PlanePinky.R", 'hand.R', F_DEF, L_RPALM),
    'f_pinky.01.R' :       ("PlanePinky.R", 'palm_pinky.R', F_DEF|F_CON, L_RHANDFK),
    'f_pinky.02.R' :       ("PlanePinky.R", 'f_pinky.01.R', F_DEF|F_CON, L_RHANDFK),
    'f_pinky.03.R' :       ("PlanePinky.R", 'f_pinky.02.R', F_DEF|F_CON, L_RHANDFK),

    'thigh.L' :            ("PlaneLeg.L", 'hips', F_DEF, L_LLEGFK),
    'shin.L' :             ("PlaneLeg.L", 'thigh.L', F_DEF|F_CON, L_LLEGFK),
    'foot.L' :             ("PlaneFoot.L", 'shin.L', F_DEF|F_CON, L_LLEGFK),
    'toe.L' :              ("PlaneToe.L", 'foot.L', F_DEF|F_CON, L_LLEGFK),

    'thigh.R' :            ("PlaneLeg.R", 'hips', F_DEF, L_RLEGFK),
    'shin.R' :             ("PlaneLeg.R", 'thigh.R', F_DEF|F_CON, L_RLEGFK),
    'foot.R' :             ("PlaneFoot.R", 'shin.R', F_DEF|F_CON, L_RLEGFK),
    'toe.R' :              ("PlaneToe.R", 'foot.R', F_DEF|F_CON, L_RLEGFK),
}

RotationLimits = {
    'spine' :           (-30*D,30*D, -30*D,30*D, -30*D,30*D),
    'spine-1' :         (-30*D,30*D, -30*D,30*D, -30*D,30*D),
    'chest' :           (-20*D,20*D, 0,0, -20*D,20*D),
    'chest-1' :         (-20*D,20*D, 0,0, -20*D,20*D),
    'neck' :            (-45*D,45*D, -45*D,45*D, -60*D,60*D),

    'thigh.L' :         (-160*D,90*D, -45*D,45*D, -140*D,80*D),
    'thigh.R' :         (-160*D,90*D, -45*D,45*D, -80*D,140*D),
    'shin.L' :          (-20*D,170*D,-40*D,40*D, 0,0),
    'shin.R' :          (-20*D,170*D,-40*D,40*D, 0,0),
    'foot.L' :          (-90*D,45*D, -30*D,15*D, 0,0),
    'foot.R' :          (-90*D,45*D, -15*D,30*D, 0,0),
    'toe.L' :           (-20*D,60*D, 0,0, 0,0),
    'toe.R' :           (-20*D,60*D, 0,0, 0,0),

    'shoulder.L' :      (-16*D,50*D, -70*D,70*D,  -45*D,45*D),
    'shoulder.L' :      (-16*D,50*D,  -70*D,70*D,  -45*D,45*D),
    'upper_arm.L' :     (-45*D,135*D, -60*D,60*D, -135*D,135*D),
    'upper_arm.R' :     (-45*D,135*D, -60*D,60*D, -135*D,135*D),
    'forearm.L' :       (-70*D,130*D, -178*D,150*D, -10*D,10*D),
    'forearm.R' :       (-70*D,130*D, -150*D,178*D, -10*D,10*D),
    'hand.L' :          (-90*D,70*D, -10*D,10*D, -20*D,20*D),
    'hand.R' :          (-90*D,70*D, -10*D,10*D, -20*D,20*D),

    'thumb.03.L' :      (None,None, 0,0, 0,0),
    'f_index.02.L' :    (None,None, 0,0, 0,0),
    'f_index.03.L' :    (None,None, 0,0, 0,0),
    'f_middle.02.L' :   (None,None, 0,0, 0,0),
    'f_middle.03.L' :   (None,None, 0,0, 0,0),
    'f_ring.02.L' :     (None,None, 0,0, 0,0),
    'f_ring.03.L' :     (None,None, 0,0, 0,0),
    'f_pinky.02.L' :    (None,None, 0,0, 0,0),
    'f_pinky.03.L' :    (None,None, 0,0, 0,0),

    'thumb.03.R' :      (None,None, 0,0, 0,0),
    'f_index.02.R' :    (None,None, 0,0, 0,0),
    'f_index.03.R' :    (None,None, 0,0, 0,0),
    'f_middle.02.R' :   (None,None, 0,0, 0,0),
    'f_middle.03.R' :   (None,None, 0,0, 0,0),
    'f_ring.02.R' :     (None,None, 0,0, 0,0),
    'f_ring.03.R' :     (None,None, 0,0, 0,0),
    'f_pinky.02.R' :    (None,None, 0,0, 0,0),
    'f_pinky.03.R' :    (None,None, 0,0, 0,0),
}

CustomShapes = {
    'root' :            'GZM_Root',
    'hips' :            'GZM_CrownHips',
    'spine' :           'GZM_CircleSpine',
    'spine-1' :         'GZM_CircleSpine',
    'chest' :           'GZM_CircleChest',
    'chest-1' :         'GZM_CircleChest',
    'neck' :            'GZM_Neck',
    'head' :            'GZM_Head',

    'thigh.L' :         'GZM_Circle025',
    'thigh.R' :         'GZM_Circle025',
    'shin.L' :          'GZM_Circle025',
    'shin.R' :          'GZM_Circle025',
    'foot.L' :          'GZM_Foot',
    'foot.R' :          'GZM_Foot',
    'toe.L' :           'GZM_Toe',
    'toe.R' :           'GZM_Toe',

    'shoulder.L' :      'GZM_Shoulder',
    'shoulder.R' :      'GZM_Shoulder',
    'deltoid.L' :       'GZM_Shoulder',
    'deltoid.R' :       'GZM_Shoulder',
    'upper_arm.L' :     'GZM_Circle025',
    'upper_arm.R' :     'GZM_Circle025',
    'forearm.L' :       'GZM_Circle025',
    'forearm.R' :       'GZM_Circle025',
    'hand.L' :          'GZM_Hand_L',
    'hand.R' :          'GZM_Hand_R',
}

Constraints = {}

ObjectProps = [
]


ArmatureProps = [
    ('MhxScale', 1.000),
    ('MhxRig', '"Control"'),
    ('MhxVisemeSet', '"BodyLanguage"'),
]

