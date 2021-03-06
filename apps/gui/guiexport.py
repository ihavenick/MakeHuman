#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This module implements the 'Files > Export' tab
"""

import os

import mh
import gui
import gui3d
import posemode
import log

class ExportTaskView(gui3d.TaskView):
    def __init__(self, category):

        gui3d.TaskView.__init__(self, category, 'Export')

        self.formats = []
        self.recentlyShown = None

        exportPath = mh.getPath('exports')

        self.fileentry = self.addTopWidget(gui.FileEntryView('Export', mode='save'))
        self.fileentry.setDirectory(exportPath)
        self.fileentry.setFilter('All Files (*.*)')

        self.exportBodyGroup = []
        self.exportHairGroup = []

        self.posefile = None

        # Mesh Formats
        self.formatBox = self.addLeftWidget(gui.GroupBox('Mesh Format'))

        # Rig formats
        self.rigBox = self.addLeftWidget(gui.GroupBox('Rig format'))

        # Map formats
        self.mapsBox = self.addLeftWidget(gui.GroupBox('Maps'))

        self.empty = True

        self.optionsBox = self.addRightWidget(gui.StackedBox())
        self.optionsBox.setAutoResize(True)

        # Scales
        self.scaleBox = self.addRightWidget(gui.GroupBox('Scale units'))
        self.scaleButtons = self.addScales(self.scaleBox)

        self.boxes = {
            'mesh': self.formatBox,
            'rig': self.rigBox,
            'map': self.mapsBox,
            'scale': self.scaleBox
            }

        self.updateGui()

        @self.fileentry.mhEvent
        def onFileSelected(filename):
            path = os.path.normpath(os.path.join(exportPath, filename))
            dir, name = os.path.split(path)
            name, ext = os.path.splitext(name)

            if not os.path.exists(dir):
                os.makedirs(dir)

            def filename(targetExt, different = False):
                if not different and ext != '' and ('.' + targetExt.lower()) != ext.lower():
                    log.warning("expected extension '.%s' but got '%s'", targetExt, ext)
                return os.path.join(dir, name + '.' + targetExt)

            found = False
            for exporter, radio, options in self.formats:
                if radio.selected:
                    exporter.export(gui3d.app.selectedHuman, filename)
                    found = True
                    break

            if not found:
                log.error("Unknown export format selected!")
                return

            gui3d.app.prompt('Info', 'The mesh has been exported to %s.' % dir, 'OK', helpId='exportHelp')

            mh.changeCategory('Modelling')


    _scales = {
        "decimeter": 1.0,
        "meter": 0.1,
        "inch": 1.0/0.254,
        "centimeter": 10.0
        }

    def addScales(self, scaleBox):
        check = True
        buttons = []
        scales = []
        for name in ["decimeter", "meter", "inch", "centimeter"]:
            button = scaleBox.addWidget(gui.RadioButton(scales, name, check))
            check = False
            buttons.append((button,name))
        return buttons

    def getScale(self):
        for (button, name) in self.scaleButtons:
            if button.selected and name in self._scales:
                return (self._scales[name], name)
        return (1, "decimeter")

    def addExporter(self, exporter):
        checked = self.empty and exporter.group == "mesh"
        radio = self.boxes[exporter.group].addWidget(gui.RadioButton(self.exportBodyGroup, exporter.name, checked))
        options = self.optionsBox.addWidget(gui.GroupBox('Options'))
        exporter.build(options, self)
        if exporter.group == "mesh":
            self.empty = False
        self.formats.append((exporter, radio, options))
        if checked:
            self.updateGui()

        @radio.mhEvent
        def onClicked(event):
            self.updateGui()

    def setFileExtension(self, extension, filter='All Files (*.*)'):
        self.fileentry.setFilter(filter)
        path,ext = os.path.splitext(str(self.fileentry.edit.text()))
        if ext:
            if extension:
                self.fileentry.edit.setText("%s.%s" % (path, extension.lstrip('.')))
            else:
                self.fileentry.edit.setText(path)

    def updateGui(self):
        for exporter, radio, options in self.formats:
            if radio.selected:
                if self.recentlyShown: self.recentlyShown.onHide(self)
                self.optionsBox.showWidget(options)
                self.setFileExtension(exporter.fileExtension, exporter.filter)
                exporter.onShow(self)
                self.recentlyShown = exporter
                break

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)

        self.fileentry.setFocus()

        human = gui3d.app.selectedHuman
        camera = mh.cameras[0]

        self.pan = human.getPosition()
        self.eye = camera.eye
        self.focus = camera.focus
        self.rotation = human.getRotation()
        human.setPosition([0, -1, 0])
        gui3d.app.setGlobalCamera();
        camera.eyeZ = 70
        human.setRotation([0.0, 0.0, 0.0])

        self.enterPoseMode()


    def onHide(self, event):

        gui3d.TaskView.onHide(self, event)

        human = gui3d.app.selectedHuman
        camera = mh.cameras[0]

        human.setPosition(self.pan)
        camera.eye = self.eye
        camera.focus = self.focus
        human.setRotation(self.rotation)

        self.exitPoseMode()

        for exporter, radio, _ in self.formats:
            if radio.selected:
                exporter.onHide(self)
                break
        self.recentlyShown = None


    def enterPoseMode(self):
        self.posefile = posemode.enterPoseMode()
        if self.posefile:
            posemode.loadMhpFile(self.posefile)


    def exitPoseMode(self):
        posemode.exitPoseMode(self.posefile)
