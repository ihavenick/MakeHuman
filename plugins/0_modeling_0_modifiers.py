#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Generic modifiers
TODO
"""

import mh
import gui
import gui3d
import humanmodifier
import log
import targets

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task

    def onClicked(self, event):
        self.task.groupBox.showWidget(self.groupBox)

class ModifierTaskView(gui3d.TaskView):
    _group = None
    _label = None

    def __init__(self, category):
        super(ModifierTaskView, self).__init__(category, self._name, label=self._label)

        def resolveOptionsDict(opts, type = 'simple'):
            # Function to analyze options passed
            # with a dictionary in the features.
            if not 'cam' in list(opts.keys()):
                opts['cam'] = 'noSetCamera'
            if not 'min' in list(opts.keys()):
                if type == 'paired':
                    opts['min'] = -1.0
                else:
                    opts['min'] = 0.0
            if not 'max' in list(opts.keys()):
                opts['max'] = 1.0
            if 'reverse' in list(opts.keys()) and opts['reverse'] == True:
                temp = opts['max']
                opts['max'] = opts['min']
                opts['min'] = temp
            if not 'label' in list(opts.keys()):
                opts['label'] = None
                
        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []
        self.modifiers = {}

        self.categoryBox = self.addRightWidget(gui.GroupBox('Category'))
        self.groupBox = self.addLeftWidget(gui.StackedBox())

        for name, base, templates in self._features:
            title = name.capitalize()

            # Create box
            box = self.groupBox.addWidget(gui.GroupBox(title))
            self.groupBoxes.append(box)

            # Create radiobutton
            radio = self.categoryBox.addWidget(GroupBoxRadioButton(self, self.radioButtons, title, box, selected = len(self.radioButtons) == 0))

            # Create sliders
            for index, template in enumerate(templates):
                macro = len(template) == 3
                if macro:
                    tname, tvar, opts = template
                    resolveOptionsDict(opts, 'macro')
                    modifier = humanmodifier.MacroModifier(base, tname, tvar)
                    self.modifiers[tvar] = modifier
                    slider = humanmodifier.MacroSlider(modifier, opts['label'], None,
                                                       opts['cam'], opts['min'], opts['max'])
                else:
                    paired = len(template) == 4
                    if paired:
                        tname, tleft, tright, opts = template
                        resolveOptionsDict(opts, 'paired')
                        left  = '-'.join([base, tname, tleft])
                        right = '-'.join([base, tname, tright])
                    else:
                        tname, opts = template
                        resolveOptionsDict(opts)                       
                        left = None
                        right = '-'.join([base, tname])

                    if opts['label'] is None:
                        tlabel = tname.split('-')
                        if len(tlabel) > 1 and tlabel[0] == base:
                            tlabel = tlabel[1:]
                        opts['label'] = ' '.join([word.capitalize() for word in tlabel])

                    modifier = humanmodifier.UniversalModifier(left, right)

                    tpath = '-'.join(template[0:-1])
                    modifierName = tpath
                    clashIndex = 0
                    while modifierName in self.modifiers:
                        log.debug('modifier clash: %s', modifierName)
                        modifierName = '%s%d' % (tpath, clashIndex)
                        clashIndex += 1

                    self.modifiers[modifierName] = modifier
                    slider = humanmodifier.UniversalSlider(modifier, opts['label'], '%s.png' % tpath,
                                                           opts['cam'], opts['min'], opts['max'])

                box.addWidget(slider)
                self.sliders.append(slider)

        self.updateMacro()

        self.groupBox.showWidget(self.groupBoxes[0])

    def getModifiers(self):
        return self.modifiers

    def getSymmetricModifierPairNames(self):
        return [dict(left = name, right = "l-" + name[2:])
                for name in self.modifiers
                if name.startswith("r-")]

    def getSingularModifierNames(self):
        return [name
                for name in self.modifiers
                if name[:2] not in ("r-", "l-")]

    def updateMacro(self):
        human = gui3d.app.selectedHuman
        for modifier in list(self.modifiers.values()):
            if isinstance(modifier, humanmodifier.MacroModifier):
                modifier.setValue(human, modifier.getValue(human))

    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)

        if gui3d.app.settings.get('cameraAutoZoom', True):
            self.setCamera()

        for slider in self.sliders:
            slider.update()

    def onHumanChanged(self, event):
        human = event.human

        for slider in self.sliders:
            slider.update()

        if event.change in ('reset', 'load', 'random'):
            self.updateMacro()

    def loadHandler(self, human, values):
        if values[0] == self._group:
            modifier = self.modifiers.get(values[1], None)
            if modifier:
                modifier.setValue(human, float(values[2]))

    def saveHandler(self, human, file):
        for name, modifier in list(self.modifiers.items()):
            if name is None:
                continue
            value = modifier.getValue(human)
            if value or isinstance(modifier, humanmodifier.MacroModifier):
                file.write('%s %s %f\n' % (self._group, name, value))

    def setCamera(self):
        pass

class FaceTaskView(ModifierTaskView):
    _name = 'Face'
    _group = 'face'
    _features = [
        ('head shape', 'head', [
            ('head-oval', {'cam' : 'frontView'}),
            ('head-round', {'cam' : 'frontView'}),
            ('head-rectangular', {'cam' : 'frontView'}),
            ('head-square', {'cam' : 'frontView'}),
            ('head-triangular', {'cam' : 'frontView'}),
            ('head-invertedtriangular', {'cam' : 'frontView'}),
            ('head-diamond', {'cam' : 'frontView'}),
            ]),
        ('head', 'head', [
            ('head-age', 'less', 'more', {'cam' : 'frontView'}),
            ('head-angle', 'in', 'out', {'cam' : 'rightView'}),
            ('head-scale-depth', 'less', 'more', {'cam' : 'rightView'}),
            ('head-scale-horiz', 'less', 'more', {'cam' : 'frontView'}),
            ('head-scale-vert', 'more', 'less', {'cam' : 'frontView'}),
            ('head-trans', 'in', 'out', {'cam' : 'frontView'}),
            ('head-trans', 'down', 'up', {'cam' : 'frontView'}),
            ('head-trans', 'forward', 'backward', {'cam' : 'rightView'}),
            ]),
        ('neck', 'neck', [
            ('neck-scale-depth', 'less', 'more', {'cam' : 'rightView'}),
            ('neck-scale-horiz', 'less', 'more', {'cam' : 'frontView'}),
            ('neck-scale-vert', 'more', 'less', {'cam' : 'frontView'}),
            ('neck-trans', 'in', 'out', {'cam' : 'frontView'}),
            ('neck-trans', 'down', 'up', {'cam' : 'frontView'}),
            ('neck-trans', 'forward', 'backward', {'cam' : 'rightView'}),
            ]),
        ('right eye', 'eyes', [
            ('r-eye-height1', 'min', 'max', {'cam' : 'frontView'}),
            ('r-eye-height2', 'min', 'max', {'cam' : 'frontView'}),
            ('r-eye-height3', 'min', 'max', {'cam' : 'frontView'}),
            ('r-eye-push1', 'in', 'out', {'cam' : 'frontView'}),
            ('r-eye-push2', 'in', 'out', {'cam' : 'frontView'}),
            ('r-eye-move', 'in', 'out', {'cam' : 'frontView'}),
            ('r-eye-move', 'up', 'down', {'cam' : 'frontView'}),
            ('r-eye', 'small', 'big', {'cam' : 'frontView'}),
            ('r-eye-corner1', 'up', 'down', {'cam' : 'frontView'}),
            ('r-eye-corner2', 'up', 'down', {'cam' : 'frontView'})
            ]),
        ('left eye', 'eyes', [
            ('l-eye-height1', 'min', 'max', {'cam' : 'frontView'}),
            ('l-eye-height2', 'min', 'max', {'cam' : 'frontView'}),
            ('l-eye-height3', 'min', 'max', {'cam' : 'frontView'}),
            ('l-eye-push1', 'in', 'out', {'cam' : 'frontView'}),
            ('l-eye-push2', 'in', 'out', {'cam' : 'frontView'}),
            ('l-eye-move', 'in', 'out', {'cam' : 'frontView'}),
            ('l-eye-move', 'up', 'down', {'cam' : 'frontView'}),
            ('l-eye', 'small', 'big', {'cam' : 'frontView'}),
            ('l-eye-corner1', 'up', 'down', {'cam' : 'frontView'}),
            ('l-eye-corner2', 'up', 'down', {'cam' : 'frontView'}),
            ]),
        ('nose features', 'nose', [
            ('nose', 'compress', 'uncompress', {'cam' : 'rightView'}),
            ('nose', 'convex', 'concave', {'cam' : 'rightView'}),
            ('nose', 'moregreek', 'lessgreek', {'cam' : 'rightView'}),
            ('nose', 'morehump', 'lesshump', {'cam' : 'rightView'}),
            ('nose', 'potato', 'point', {'cam' : 'rightView'}),
            ('nose-nostrils', 'point', 'unpoint', {'cam' : 'frontView'}),
            ('nose-nostrils', 'up', 'down', {'cam' : 'rightView'}),
            ('nose-point', 'up', 'down', {'cam' : 'rightView'}),
            ]),
        ('nose size details', 'nose', [
            ('nose-nostril-width', 'min', 'max', {'cam' : 'frontView'}),
            ('nose-height', 'min', 'max', {'cam' : 'rightView'}),
            ('nose-width1', 'min', 'max', {'cam' : 'frontView'}),
            ('nose-width2', 'min', 'max', {'cam' : 'frontView'}),
            ('nose-width3', 'min', 'max', {'cam' : 'frontView'}),
            ('nose-width', 'min', 'max', {'cam' : 'frontView'}),
            ]),
        ('nose size', 'nose', [
            ('nose-trans', 'up', 'down', {'cam' : 'frontView'}),
            ('nose-trans', 'forward', 'backward', {'cam' : 'rightView'}),
            ('nose-trans', 'in', 'out', {'cam' : 'frontView'}),
            ('nose-scale-vert', 'incr', 'decr', {'cam' : 'frontView'}),
            ('nose-scale-horiz', 'incr', 'decr', {'cam' : 'frontView'}),
            ('nose-scale-depth', 'incr', 'decr', {'cam' : 'rightView'}),
            ]),
        ('mouth size', 'mouth', [
            ('mouth-scale-horiz', 'incr', 'decr', {'cam' : 'frontView'}),
            ('mouth-scale-vert', 'incr', 'decr', {'cam' : 'frontView'}),
            ('mouth-scale-depth', 'incr', 'decr', {'cam' : 'rightView'}),
            ('mouth-trans', 'in', 'out', {'cam' : 'frontView'}),
            ('mouth-trans', 'up', 'down', {'cam' : 'frontView'}),
            ('mouth-trans', 'forward', 'backward', {'cam' : 'rightView'}),
            ]),
        ('mouth size details', 'mouth', [
            ('mouth-lowerlip-height', 'min', 'max', {'cam' : 'frontView'}),
            ('mouth-lowerlip-middle', 'up', 'down', {'cam' : 'frontView'}),
            ('mouth-lowerlip-width', 'min', 'max', {'cam' : 'frontView'}),
            ('mouth-upperlip-height', 'min', 'max', {'cam' : 'frontView'}),
            ('mouth-upperlip-width', 'min', 'max', {'cam' : 'frontView'}),
            ]),
        ('mouth features', 'mouth', [
            ('mouth-lowerlip-ext', 'up', 'down', {'cam' : 'frontView'}),
            ('mouth-angles', 'up', 'down', {'cam' : 'frontView'}),
            ('mouth-lowerlip-middle', 'up', 'down', {'cam' : 'frontView'}),
            ('mouth-lowerlip', 'deflate', 'inflate', {'cam' : 'rightView'}),
            ('mouth-philtrum', 'up', 'down', {'cam' : 'frontView'}),
            ('mouth-philtrum', 'increase', 'decrease', {'cam' : 'rightView'}),
            ('mouth-upperlip', 'deflate', 'inflate', {'cam' : 'rightView'}),
            ('mouth-upperlip-ext', 'up', 'down', {'cam' : 'frontView'}),
            ('mouth-upperlip-middle', 'up', 'down', {'cam' : 'frontView'}),
            ]),
        ('right ear', 'ears', [
            ('r-ear', 'backward', 'forward', {'cam' : 'rightView'}),
            ('r-ear', 'big', 'small', {'cam' : 'rightView'}),
            ('r-ear', 'down', 'up', {'cam' : 'rightView'}),
            ('r-ear-height', 'min', 'max', {'cam' : 'rightView'}),
            ('r-ear-lobe', 'min', 'max', {'cam' : 'rightView'}),
            ('r-ear', 'pointed', 'triangle', {'cam' : 'rightView'}),
            ('r-ear-rot', 'backward', 'forward', {'cam' : 'rightView'}),
            ('r-ear', 'square', 'round', {'cam' : 'rightView'}),
            ('r-ear-width', 'max', 'min', {'cam' : 'rightView'}),
            ('r-ear-wing', 'out', 'in', {'cam' : 'frontView'}),
            ('r-ear-flap', 'out', 'in', {'cam' : 'frontView'}),
            ]),
        ('left ear', 'ears', [
            ('l-ear', 'backward', 'forward', {'cam' : 'leftView'}),
            ('l-ear', 'big', 'small', {'cam' : 'leftView'}),
            ('l-ear', 'down', 'up', {'cam' : 'leftView'}),
            ('l-ear-height', 'min', 'max', {'cam' : 'leftView'}),
            ('l-ear-lobe', 'min', 'max', {'cam' : 'leftView'}),
            ('l-ear', 'pointed', 'triangle', {'cam' : 'leftView'}),
            ('l-ear-rot', 'backward', 'forward', {'cam' : 'leftView'}),
            ('l-ear', 'square', 'round', {'cam' : 'leftView'}),
            ('l-ear-width', 'max', 'min', {'cam' : 'leftView'}),
            ('l-ear-wing', 'out', 'in', {'cam' : 'frontView'}),
            ('l-ear-flap', 'out', 'in', {'cam' : 'frontView'}),
            ]),
        ('chin', 'chin', [
            ('chin', 'in', 'out', {'cam' : 'rightView'}),
            ('chin-width', 'min', 'max', {'cam' : 'frontView'}),
            ('chin-height', 'min', 'max', {'cam' : 'frontView'}),
            ('chin', 'squared', 'round', {'cam' : 'frontView'}),
            ('chin', 'prognathism1', 'prognathism2', {'cam' : 'rightView'}),
            ]),
        ('cheek', 'cheek', [
            ('l-cheek', 'in', 'out', {'cam' : 'frontView'}),
            ('l-cheek-bones', 'out', 'in', {'cam' : 'frontView'}),
            ('r-cheek', 'in', 'out', {'cam' : 'frontView'}),
            ('r-cheek-bones', 'out', 'in', {'cam' : 'frontView'}),
            ]),
        ]

    def setCamera(self):
        gui3d.app.setFaceCamera()

class TorsoTaskView(ModifierTaskView):
    _name = 'Torso'
    _group = 'torso'
    _features = [
        ('Torso', 'torso', [
            ('torso-scale-depth', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ('torso-scale-horiz', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ('torso-scale-vert', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ('torso-trans', 'in', 'out', {'cam' : 'setGlobalCamera'}),
            ('torso-trans', 'down', 'up', {'cam' : 'setGlobalCamera'}),
            ('torso-trans', 'forward', 'backward', {'cam' : 'setGlobalCamera'}),
            ]),
        ('Hip', 'hip', [
            ('hip-scale-depth', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ('hip-scale-horiz', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ('hip-scale-vert', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ('hip-trans', 'in', 'out', {'cam' : 'setGlobalCamera'}),
            ('hip-trans', 'down', 'up', {'cam' : 'setGlobalCamera'}),
            ('hip-trans', 'forward', 'backward', {'cam' : 'setGlobalCamera'}),
            ]),
        ('Stomach', 'stomach', [
            ('stomach-tone', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ]),
        ('Buttocks', 'buttocks', [
            ('buttocks-tone', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ]),
        ('Pelvis', 'pelvis', [
            ('pelvis-tone', 'decr', 'incr', {'cam' : 'setGlobalCamera'}),
            ])
        ]

class ArmsLegsTaskView(ModifierTaskView):
    _name = 'Arms and Legs'
    _group = 'armslegs'
    _features = [
        ('right hand', 'armslegs', [
            ('r-hand-scale-depth', 'decr', 'incr', {'cam' : 'setRightHandTopCamera'}),
            ('r-hand-scale-horiz', 'decr', 'incr', {'cam' : 'setRightHandFrontCamera'}),
            ('r-hand-scale-vert', 'decr', 'incr', {'cam' : 'setRightHandFrontCamera'}),
            ('r-hand-trans', 'in', 'out', {'cam' : 'setRightHandFrontCamera'}),
            ('r-hand-trans', 'down', 'up', {'cam' : 'setRightHandFrontCamera'}),
            ('r-hand-trans', 'forward', 'backward', {'cam' : 'setRightHandTopCamera'}),
            ]),
        ('left hand', 'armslegs', [
            ('l-hand-scale-depth', 'decr', 'incr', {'cam' : 'setLeftHandTopCamera'}),
            ('l-hand-scale-horiz', 'decr', 'incr', {'cam' : 'setLeftHandFrontCamera'}),
            ('l-hand-scale-vert', 'decr', 'incr', {'cam' : 'setLeftHandFrontCamera'}),
            ('l-hand-trans', 'in', 'out', {'cam' : 'setLeftHandFrontCamera'}),
            ('l-hand-trans', 'down', 'up', {'cam' : 'setLeftHandFrontCamera'}),
            ('l-hand-trans', 'forward', 'backward', {'cam' : 'setLeftHandTopCamera'}),
            ]),
        ('right foot', 'armslegs', [
            ('r-foot-scale-depth', 'decr', 'incr', {'cam' : 'setRightFootRightCamera'}),
            ('r-foot-scale-horiz', 'decr', 'incr', {'cam' : 'setRightFootFrontCamera'}),
            ('r-foot-scale-vert', 'decr', 'incr', {'cam' : 'setRightFootFrontCamera'}),
            ('r-foot-trans', 'in', 'out', {'cam' : 'setRightFootFrontCamera'}),
            ('r-foot-trans', 'down', 'up', {'cam' : 'setRightFootFrontCamera'}),
            ('r-foot-trans', 'forward', 'backward', {'cam' : 'setRightFootRightCamera'}),
            ]),
        ('left foot', 'armslegs', [
            ('l-foot-scale-depth', 'decr', 'incr', {'cam' : 'setLeftFootLeftCamera'}),
            ('l-foot-scale-horiz', 'decr', 'incr', {'cam' : 'setLeftFootFrontCamera'}),
            ('l-foot-scale-vert', 'decr', 'incr', {'cam' : 'setLeftFootFrontCamera'}),
            ('l-foot-trans', 'in', 'out', {'cam' : 'setLeftFootFrontCamera'}),
            ('l-foot-trans', 'down', 'up', {'cam' : 'setLeftFootFrontCamera'}),
            ('l-foot-trans', 'forward', 'backward', {'cam' : 'setLeftFootLeftCamera'}),
            ]),
        ('left arm', 'armslegs', [
            ('l-lowerarm-scale-depth', 'decr', 'incr', {'cam' : 'setLeftArmTopCamera'}),
            ('l-lowerarm-scale-horiz', 'decr', 'incr', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-lowerarm-scale-vert', 'decr', 'incr', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-lowerarm-trans', 'in', 'out', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-lowerarm-trans', 'down', 'up', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-lowerarm-trans', 'forward', 'backward', {'cam' : 'setLeftArmTopCamera'}),
            ('l-upperarm-scale-depth', 'decr', 'incr', {'cam' : 'setLeftArmTopCamera'}),
            ('l-upperarm-scale-horiz', 'decr', 'incr', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-upperarm-scale-vert', 'decr', 'incr', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-upperarm-trans', 'in', 'out', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-upperarm-trans', 'down', 'up', {'cam' : 'setLeftArmFrontCamera'}),
            ('l-upperarm-trans', 'forward', 'backward', {'cam' : 'setLeftArmTopCamera'}),
            ]),
        ('right arm', 'armslegs', [
            ('r-lowerarm-scale-depth', 'decr', 'incr', {'cam' : 'setRightArmTopCamera'}),
            ('r-lowerarm-scale-horiz', 'decr', 'incr', {'cam' : 'setRightArmFrontCamera'}),
            ('r-lowerarm-scale-vert', 'decr', 'incr', {'cam' : 'setRightArmFrontCamera'}),
            ('r-lowerarm-trans', 'in', 'out', {'cam' : 'setRightArmFrontCamera'}),
            ('r-lowerarm-trans', 'down', 'up', {'cam' : 'setRightArmFrontCamera'}),
            ('r-lowerarm-trans', 'forward', 'backward', {'cam' : 'setRightArmTopCamera'}),
            ('r-upperarm-scale-depth', 'decr', 'incr', {'cam' : 'setRightArmTopCamera'}),
            ('r-upperarm-scale-horiz', 'decr', 'incr', {'cam' : 'setRightArmFrontCamera'}),
            ('r-upperarm-scale-vert', 'decr', 'incr', {'cam' : 'setRightArmFrontCamera'}),
            ('r-upperarm-trans', 'in', 'out', {'cam' : 'setRightArmFrontCamera'}),
            ('r-upperarm-trans', 'down', 'up', {'cam' : 'setRightArmFrontCamera'}),
            ('r-upperarm-trans', 'forward', 'backward', {'cam' : 'setRightArmTopCamera'}),
            ]),
        ('left leg', 'armslegs', [
            ('l-lowerleg-scale-depth', 'decr', 'incr', {'cam' : 'setLeftLegLeftCamera'}),
            ('l-lowerleg-scale-horiz', 'decr', 'incr', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-lowerleg-scale-vert', 'decr', 'incr', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-lowerleg-trans', 'in', 'out', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-lowerleg-trans', 'down', 'up', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-lowerleg-trans', 'forward', 'backward', {'cam' : 'setLeftLegLeftCamera'}),
            ('l-upperleg-scale-depth', 'decr', 'incr', {'cam' : 'setLeftLegLeftCamera'}),
            ('l-upperleg-scale-horiz', 'decr', 'incr', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-upperleg-scale-vert', 'decr', 'incr', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-upperleg-trans', 'in', 'out', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-upperleg-trans', 'down', 'up', {'cam' : 'setLeftLegFrontCamera'}),
            ('l-upperleg-trans', 'forward', 'backward', {'cam' : 'setLeftLegLeftCamera'}),
            ]),
        ('right leg', 'armslegs', [
            ('r-lowerleg-scale-depth', 'decr', 'incr', {'cam' : 'setRightLegRightCamera'}),
            ('r-lowerleg-scale-horiz', 'decr', 'incr', {'cam' : 'setRightLegFrontCamera'}),
            ('r-lowerleg-scale-vert', 'decr', 'incr', {'cam' : 'setRightLegFrontCamera'}),
            ('r-lowerleg-trans', 'in', 'out', {'cam' : 'setRightLegFrontCamera'}),
            ('r-lowerleg-trans', 'down', 'up', {'cam' : 'setRightLegFrontCamera'}),
            ('r-lowerleg-trans', 'forward', 'backward', {'cam' : 'setRightLegRightCamera'}),
            ('r-upperleg-scale-depth', 'decr', 'incr', {'cam' : 'setRightLegRightCamera'}),
            ('r-upperleg-scale-horiz', 'decr', 'incr', {'cam' : 'setRightLegFrontCamera'}),
            ('r-upperleg-scale-vert', 'decr', 'incr', {'cam' : 'setRightLegFrontCamera'}),
            ('r-upperleg-trans', 'in', 'out', {'cam' : 'setRightLegFrontCamera'}),
            ('r-upperleg-trans', 'down', 'up', {'cam' : 'setRightLegFrontCamera'}),
            ('r-upperleg-trans', 'forward', 'backward', {'cam' : 'setRightLegRightCamera'}),
            ])
        ]

class GenderTaskView(ModifierTaskView):
    _name = 'Gender'
    _group = 'gendered'
    _features = [
        ('Genitals', 'genitals', [
            ('genitals', 'feminine', 'masculine', {}),
            ]),
        ('Breast', 'breast', [
            (None, 'BreastSize', {'label' : 'Breast size'}),
            (None, 'BreastFirmness', {'label' : 'Breast firmness', 'reverse' : True}),
            ('breast', 'down', 'up', {}),
            ('breast-dist', 'min', 'max', {}),
            ('breast-point', 'min', 'max', {}),
            ]),
        ]

class AsymmTaskView(ModifierTaskView):
    _name = 'Asymmetry'
    _group = 'asymmetry'
    _features = [
        ('brow', 'asym', [
            ('asym-brown-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-brown-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('cheek', 'asym', [
            ('asym-cheek-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-cheek-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('ear', 'asym', [
            ('asym-ear-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-ear-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-ear-3', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-ear-4', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('eye', 'asym', [
            ('asym-eye-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-eye-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-eye-3', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-eye-4', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-eye-5', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-eye-6', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-eye-7', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-eye-8', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('jaw', 'asym', [
            ('asym-jaw-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-jaw-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-jaw-3', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('mouth', 'asym', [
            ('asym-mouth-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-mouth-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('nose', 'asym', [
            ('asym-nose-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-nose-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-nose-3', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-nose-4', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('temple', 'asym', [
            ('asym-temple-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-temple-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('top', 'asym', [
            ('asym-top-1', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ('asym-top-2', 'l', 'r', {'cam' : 'setFaceCamera'}),
            ]),
        ('body', 'asym', [
            ('asymm-breast-1', 'l', 'r', {'cam' : 'setGlobalCamera'}),
            ('asymm-trunk-1', 'l', 'r', {'cam' : 'setGlobalCamera'}),
            ]),
        ]

class MacroTaskView(ModifierTaskView):
    _name = 'Macro modelling'
    _group = 'macro'
    _label = 'Macro'

    _features = [
        ('Macro', 'macrodetails', [
            (None, 'Gender', {'label' : 'Gender'}),
            (None, 'Age', {'label' : 'Age'}),
            ('universal', 'Muscle', {'label' : 'Muscle'}),
            ('universal', 'Weight', {'label' : 'Weight'}),
            ('universal-stature', 'Height', {'label' : 'Height'}),
            (None, 'African', {'label' : 'African'}),
            (None, 'Asian', {'label' : 'Asian'}),
            (None, 'Caucasian', {'label' : 'Caucasian'}),
            ]),
        ]

    def __init__(self, category):
        super(MacroTaskView, self).__init__(category)
        for race, modifier, slider in self.raceSliders():
            slider.setValue(1.0/3)

    def raceSliders(self):
        for slider in self.sliders:
            modifier = slider.modifier
            if not isinstance(modifier, humanmodifier.MacroModifier):
                continue
            variable = modifier.variable
            if variable in ('African', 'Asian', 'Caucasian'):
                yield (variable, modifier, slider)

    def syncStatus(self):
        human = gui3d.app.selectedHuman
        
        if human.getGender() == 0.0:
            gender = gui3d.app.getLanguageString('female')
        elif human.getGender() == 1.0:
            gender = gui3d.app.getLanguageString('male')
        elif abs(human.getGender() - 0.5) < 0.01:
            gender = gui3d.app.getLanguageString('neutral')
        else:
            gender = gui3d.app.getLanguageString('%.2f%% female, %.2f%% male') % ((1.0 - human.getGender()) * 100, human.getGender() * 100)
        
        age = human.getAgeYears()
        muscle = (human.getMuscle() * 100.0)
        weight = (50 + (150 - 50) * human.getWeight())
        coords = human.meshData.getCoords([8223,12361,13155])
        height = human.getHeightCm()
        if gui3d.app.settings['units'] == 'metric':
            units = 'cm'
        else:
            units = 'in'
            height *= 0.393700787

        self.setStatus('Gender: %s, Age: %d, Muscle: %.2f%%, Weight: %.2f%%, Height: %.2f %s', gender, age, muscle, weight, height, units)

    def syncRaceSliders(self, event):
        human = event.human
        for race, modifier, slider in self.raceSliders():
            slider.setValue(1.0/3)
            value = modifier.getValue(human)
            modifier.setValue(human, value)
            slider.setValue(value)

    def setStatus(self, format, *args):
        gui3d.app.statusPersist(format, *args)

    def onShow(self, event):
        self.syncStatus()
        super(MacroTaskView, self).onShow(event)

    def onHide(self, event):
        self.setStatus('')
        super(MacroTaskView, self).onHide(event)

    def onHumanChaging(self, event):
        super(MacroTaskView, self).onHumanChanging(event)
        if event.change in ('caucasian', 'asian', 'african'):
            self.syncRaceSliders(event)

    def onHumanChanged(self, event):
        super(MacroTaskView, self).onHumanChanged(event)
        if self.isVisible():
            self.syncStatus()
        if event.change in ('caucasian', 'asian', 'african'):
            self.syncRaceSliders(event)

def load(app):
    category = app.getCategory('Modelling')

    gui3d.app.noSetCamera = (lambda: None)

    for type in [MacroTaskView, GenderTaskView, FaceTaskView, TorsoTaskView, ArmsLegsTaskView, AsymmTaskView]:
        taskview = category.addTask(type(category))
        if taskview._group is not None:
            app.addLoadHandler(taskview._group, taskview.loadHandler)
            app.addSaveHandler(taskview.saveHandler)

def unload(app):
    pass
