#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import gui3d
import gui
import log
import shader
import numpy as np
import material
import mh

class ShaderTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Material Editor')

        self.human = gui3d.app.selectedHuman

        shaderBox = self.addLeftWidget(gui.GroupBox('Shader'))
        self.shaderList = shaderBox.addWidget(gui.ListView())
        self.shaderList.setSizePolicy(gui.SizePolicy.Ignored, gui.SizePolicy.Preferred)

        self.shaderConfBox = self.addLeftWidget(gui.GroupBox('Shader config'))
        shaderConfig = self.human.material.shaderConfig
        for name in shaderConfig:
            chkBox = gui.CheckBox(name, shaderConfig[name])
            self.shaderConfBox.addWidget(chkBox)
            @chkBox.mhEvent
            def onClicked(event):
                shaderConfig = dict()
                for child in self.shaderConfBox.children:
                    shaderConfig[str(child.text())] = child.isChecked()
                self.human.mesh.configureShading(**shaderConfig)

        if not shader.Shader.supported():
            log.notice('Shaders not supported')
            self.shaderList.setEnabled(False)

        self.paramBox = self.addRightWidget(gui.GroupBox('Shader parameters'))

        self.materialBox = self.addRightWidget(gui.GroupBox('Material settings'))

        @self.shaderList.mhEvent
        def onClicked(item):
            self.setShader(unicode(item.getUserData()))

        self.loadSaveBox = self.addRightWidget(gui.GroupBox("Material file"))
        self.loadMaterialBtn = self.loadSaveBox.addWidget(gui.BrowseButton(), 0, 0)
        self.loadMaterialBtn.setFilter("MakeHuman Material (*.mhmat)")
        self.loadMaterialBtn.setText('Load')
        self.loadMaterialBtn._path = mh.getSysDataPath('')
        @self.loadMaterialBtn.mhEvent
        def onClicked(path):
            if path:
                self.loadMaterial(path)
        self.saveMaterialBtn = self.loadSaveBox.addWidget(gui.BrowseButton('save'), 0, 1)
        self.saveMaterialBtn.setFilter("MakeHuman Material (*.mhmat)")
        self.saveMaterialBtn.setText('Save')
        self.saveMaterialBtn._path = os.path.join(mh.getPath(''), 'data')
        @self.saveMaterialBtn.mhEvent
        def onClicked(path):
            if path:
                if not os.path.splitext(path)[1]:
                    path = path + ".mhmat"
                self.saveMaterial(path)

    def loadMaterial(self, path):
        self.human.material = material.fromFile(path)
        self.listMaterialSettings(self.human.material)

    def saveMaterial(self, path):
        self.human.material.toFile(path)

    def listMaterialSettings(self, mat):
        for child in self.materialBox.children[:]:
            self.materialBox.removeWidget(child)

        w1 = self.materialBox.addWidget(ColorValue("Diffuse", mat.diffuseColor))
        @w1.mhEvent
        def onActivate(event):
            self.human.material.diffuseColor = w1.value

        w2 = self.materialBox.addWidget(ScalarValue("Diffuse intensity", mat.diffuseIntensity))
        @w2.mhEvent
        def onActivate(event):
            self.human.material.diffuseIntensity = w2.value

        w3 = self.materialBox.addWidget(ImageValue("Diffuse texture", mat.diffuseTexture, mh.getSysDataPath('textures')))
        @w3.mhEvent
        def onActivate(event):
            self.human.material.diffuseTexture = w3.value
            self.updateShaderConfig()

        w4 = self.materialBox.addWidget(ColorValue("Ambient", mat.ambientColor))
        @w4.mhEvent
        def onActivate(event):
            self.human.material.ambientColor = w4.value

        w5 = self.materialBox.addWidget(ColorValue("Specular", mat.specularColor))
        @w5.mhEvent
        def onActivate(event):
            self.human.material.specularColor = w5.value

        w6 = self.materialBox.addWidget(ScalarValue("Specular intensity", mat.specularIntensity))
        @w6.mhEvent
        def onActivate(event):
            self.human.material.specularIntensity = w6.value

        w7 = self.materialBox.addWidget(ScalarValue("Specular hardness", mat.specularHardness))
        @w7.mhEvent
        def onActivate(event):
            self.human.material.specularHardness = w7.value

        w8 = self.materialBox.addWidget(ColorValue("Emissive", mat.emissiveColor))
        @w8.mhEvent
        def onActivate(event):
            self.human.material.emissiveColor = w8.value

        w9 = self.materialBox.addWidget(ScalarValue("Opacity", mat.opacity))
        @w9.mhEvent
        def onActivate(event):
            self.human.material.opacity = w9.value

        w10 = self.materialBox.addWidget(ScalarValue("Translucency", mat.translucency))
        @w10.mhEvent
        def onActivate(event):
            self.human.material.translucency = w10.value

        w11 = self.materialBox.addWidget(ImageValue("Transparency map texture", mat.transparencyMapTexture, mh.getSysDataPath('textures')))
        @w11.mhEvent
        def onActivate(event):
            self.human.material.transparencyMapTexture = w11.value
            self.updateShaderConfig()

        w12 = self.materialBox.addWidget(ScalarValue("Transparency (map) intensity", mat.transparencyIntensity))
        @w12.mhEvent
        def onActivate(event):
            self.human.material.transparencyIntensity = w12.value

        w13 = self.materialBox.addWidget(ImageValue("Bump map texture", mat.bumpMapTexture, mh.getSysDataPath('textures')))
        @w13.mhEvent
        def onActivate(event):
            self.human.material.bumpMapTexture = w13.value
            self.updateShaderConfig()

        w14 = self.materialBox.addWidget(ScalarValue("Bump map intensity", mat.bumpMapIntensity))
        @w14.mhEvent
        def onActivate(event):
            self.human.material.bumpMapIntensity = w14.value

        w15 = self.materialBox.addWidget(ImageValue("Normal map texture", mat.normalMapTexture, mh.getSysDataPath('textures')))
        @w15.mhEvent
        def onActivate(event):
            self.human.material.normalMapTexture = w15.value
            self.updateShaderConfig()

        w16 = self.materialBox.addWidget(ScalarValue("Normal map intensity", mat.normalMapIntensity))
        @w16.mhEvent
        def onActivate(event):
            self.human.material.normalMapIntensity = w16.value

        w17 = self.materialBox.addWidget(ImageValue("Displacement map texture", mat.displacementMapTexture, mh.getSysDataPath('textures')))
        @w17.mhEvent
        def onActivate(event):
            self.human.material.displacementMapTexture = w17.value
            self.updateShaderConfig()

        w18 = self.materialBox.addWidget(ScalarValue("Displacement map intensity", mat.displacementMapIntensity))
        @w18.mhEvent
        def onActivate(event):
            self.human.material.displacementMapIntensity = w18.value

        w19 = self.materialBox.addWidget(ImageValue("Specular map texture", mat.specularMapTexture, mh.getSysDataPath('textures')))
        @w19.mhEvent
        def onActivate(event):
            self.human.material.specularMapTexture = w19.value
            self.updateShaderConfig()

        w20 = self.materialBox.addWidget(ScalarValue("Specular map intensity", mat.specularMapIntensity))
        @w20.mhEvent
        def onActivate(event):
            self.human.material.specularMapIntensity = w20.value

        w21 = self.materialBox.addWidget(FileValue("UV map", self.human.material.uvMap, mh.getSysDataPath('uvs')))
        w21.browseBtn.setFilter("UV Set (*.obj)")
        @w21.mhEvent
        def onActivate(event):
            if os.path.basename(w21.value) == "default.obj":
                w21.value = None
                self.human.setUVMap(None)
            else: 
                self.human.setUVMap(w21.value)


    def listShaders(self, dir = mh.getSysDataPath('shaders/glsl')):
        shaders = set()
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if not os.path.isfile(path):
                continue
            if not name.endswith('_shader.txt'):
                continue
            # TODO clean up
            name, type = name[:-11].rsplit('_',1)
            if type not in ['vertex', 'geometry', 'fragment']:
                continue
            shaders.add(name)

        self.shaderList.clear()
        firstItem = self.shaderList.addItem('[None]', data = '')
        if self.human.mesh.shader:
            shaderName = os.path.basename(self.human.mesh.shader)
        else:
            shaderName = None
            firstItem.setChecked(True)

        for name in sorted(shaders):
            item = self.shaderList.addItem(name, data = os.path.join(dir, name))
            if shaderName and unicode(shaderName) == item.text:
                item.setChecked(True) # TODO does not have the desired effect
                path = unicode(item.getUserData())
                self.listUniforms(path, self.human.mesh.material)

    def updateShaderConfig(self):
        shaderConfig = self.human.material.shaderConfig

        for child in self.shaderConfBox.children:
            name = str(child.text())
            child.setChecked( shaderConfig[name] )
            if name == 'diffuse':
                child.setEnabled(self.human.material.supportsDiffuse())
            if name == 'bump':
                # TODO disable bump if normal enabled
                child.setEnabled(self.human.material.supportsBump())
            if name == 'normal':
                child.setEnabled(self.human.material.supportsNormal())
            if name == 'displacement':
                child.setEnabled(self.human.material.supportsDisplacement())
            if name == 'spec':
                child.setEnabled(self.human.material.supportsSpecular())

    def setShader(self, path):
        self.human.mesh.setShader(path)
        self.listUniforms(path, self.human.mesh.material)

    def listUniforms(self, path, material):
        for child in self.paramBox.children[:]:
            self.paramBox.removeWidget(child)

        if not path:
            return

        sh = shader.getShader(path)
        uniforms = sh.getUniforms()
        for index, uniform in enumerate(uniforms):
            if uniform.name.startswith('gl_'):
                continue
            self.paramBox.addWidget(UniformValue(uniform, material), index)

    def onShow(self, arg):
        super(ShaderTaskView, self).onShow(arg)
        self.listShaders()
        if self.human.material.shader:
            self.human.material.shader
        if not shader.Shader.supported():
            gui3d.app.statusPersist('Shaders not supported by OpenGL')

        self.updateShaderConfig()

        self.listMaterialSettings(self.human.material)

    def onHide(self, arg):
        gui3d.app.statusPersist('')
        super(ShaderTaskView, self).onHide(arg)

class ColorValue(gui.GroupBox):
    def __init__(self, name, value):
        super(ColorValue, self).__init__(name)
        self.name = name

        self.widgets = []
        for col in xrange(3):
            child = FloatValue(self, 0)
            self.addWidget(child, 0, col)
            self.widgets.append(child)
        self.pickBtn = self.addWidget(gui.ColorPickButton(value))
        @self.pickBtn.mhEvent
        def onClicked(color):
            self.value = color

        self.value = value

    def getValue(self):
        return material.Color().copyFrom([widget.value for widget in self.widgets])

    def setValue(self, value):
        if isinstance(value, material.Color):
            value = value.asTuple()
        else:
            value = tuple(value)

        for idx, widget in enumerate(self.widgets):
            widget.setText(str(value[idx]))

    value = property(getValue, setValue)

class ScalarValue(gui.GroupBox):
    def __init__(self, name, value):
        super(ScalarValue, self).__init__(name)
        self.name = name

        self.widget = FloatValue(self, 0)
        self.addWidget(self.widget, 0, 0)
        self.value = value

    def getValue(self):
        return self.widget.value

    def setValue(self, value):
        self.widget.setText(str(value))

    value = property(getValue, setValue)

class ImageValue(gui.GroupBox):
    def __init__(self, name, value, defaultPath = None):
        super(ImageValue, self).__init__(name)
        self.name = name

        self.widget = TextureValue(self, 0, defaultPath)
        self.addWidget(self.widget, 0, 0)
        self.value = value

    def getValue(self):
        return self.widget.value

    def setValue(self, value):
        self.widget.value = value

    value = property(getValue, setValue)

class FileValue(gui.GroupBox):
    def __init__(self, name, value, defaultPath = None):
        super(FileValue, self).__init__(name)
        self.name = name

        self.fileText = self.addWidget(gui.TextView(''), 0, 0)
        self.browseBtn = self.addWidget(gui.BrowseButton(), 1, 0)

        if defaultPath:
            self.browseBtn._path = defaultPath

        @self.browseBtn.mhEvent
        def onClicked(path):
            if not path:
                return
            self.setValue(path)
            self.callEvent('onActivate', self.getValue())

        self.setValue(value)

    def getValue(self):
        return self._value

    def setValue(self, value):
        if value:
            self._value = value
            self.fileText.setText(os.path.basename(value))
        else:
            self.fileText.setText('Default')

    value = property(getValue, setValue)

class UniformValue(gui.GroupBox):
    def __init__(self, uniform, material = None):
        super(UniformValue, self).__init__(uniform.name)
        self.uniform = uniform
        self.material = material
        self.widgets = None
        self.create()

    def create(self):
        values = None
        if self.material:
            # Material params have precedence over declarations in shader code
            params = self.material.shaderParameters
            values = params.get(self.uniform.name)
        if values is None:
            values = np.atleast_2d(self.uniform.values)
        else:
            values = np.atleast_2d(values)
        rows, cols = values.shape
        self.widgets = []
        for row in xrange(rows):
            widgets = []
            for col in xrange(cols):
                child = self.createWidget(values[row,col], row)
                self.addWidget(child, row, col)
                widgets.append(child)
            self.widgets.append(widgets)

    def createWidget(self, value, row):
        type = self.uniform.pytype
        if type == int:
            return IntValue(self, value)
        if type == float:
            return FloatValue(self, value)
        if type == str:
            # TODO account for tex idx
            defaultPath = mh.getSysDataPath('litspheres') if self.uniform.name == 'litsphereTexture' else None
            return TextureValue(self, value, defaultPath)
        if type == bool:
            return BooleanValue(self, value)
        return TextView('???')

    def onActivate(self, arg=None):
        values = [[widget.value
                   for widget in widgets]
                  for widgets in self.widgets]
        if len(self.uniform.dims) == 1:
            values = values[0]
            if self.uniform.dims == (1,) and self.uniform.pytype == str:
                values = values[0]
                if not os.path.isfile(values):
                    return
        gui3d.app.selectedHuman.mesh.setShaderParameter(self.uniform.name, values)

class NumberValue(gui.TextEdit):
    def __init__(self, parent, value):
        super(NumberValue, self).__init__(str(value), self._validator)
        self.parent = parent

    def sizeHint(self):
        size = self.minimumSizeHint()
        size.width = size.width() * 3
        return size

    def onActivate(self, arg=None):
        self.parent.callEvent('onActivate', self.value)

class IntValue(NumberValue):
    _validator = gui.intValidator

    @property
    def value(self):
        return int(self.text)

class FloatValue(NumberValue):
    _validator = gui.floatValidator

    @property
    def value(self):
        return float(self.text)

class BooleanValue(gui.CheckBox):
    def __init__(self, parent, value):
        super(BooleanValue, self).__init__()
        self.parent = parent
        self.setSelected(value)

    def onClicked(self, arg=None):
        self.parent.callEvent('onActivate', self.value)

    @property
    def value(self):
        return self.selected

class TextureValue(gui.QtGui.QWidget, gui.Widget):
    def __init__(self, parent, value, defaultPath = None):
        super(TextureValue, self).__init__()
        self.parent = parent
        self._path = value

        self.layout = gui.QtGui.QGridLayout(self)
        self.imageView = gui.ImageView()
        self.browseBtn = gui.BrowseButton()
        self.browseBtn.setFilter("Image Files (*.png *.jpg *.bmp)")

        if defaultPath:
            self.browseBtn._path = defaultPath

        @self.browseBtn.mhEvent
        def onClicked(path):
            if not path:
                return
            self._path = path
            self.imageView.setImage(self.value)
            self.parent.callEvent('onActivate', self.value)

        self.value = value

        self.layout.addWidget(self.imageView)
        self.layout.addWidget(self.browseBtn)

    def getValue(self):
        return self._path

    def setValue(self, value):
        self._path = value
        if value:
            self.imageView.setImage(value)
        else:
            self.imageView.setImage(mh.getSysDataPath('notfound.thumb'))

    value = property(getValue, setValue)

def load(app):
    category = app.getCategory('Utilities')
    taskview = category.addTask(ShaderTaskView(category))

def unload(app):
    pass


