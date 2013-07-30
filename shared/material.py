#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MakeHuman Material format with parser and serializer.
"""

import log
import os
import meshstat


class Color(object):
    def __init__(self, r=0.00, g=0.00, b=0.00):
        self.setValues(r,g,b)

    def setValues(self, r, g, b):
        self.setR(r)
        self.setG(g)
        self.setB(b)

    def getValues(self):
        return [self.r, self.g, self.b]

    values = property(getValues, setValues)

    def setR(self, r):
        self.r = max(0.0, min(1.0, float(r)))

    def setG(self, g):
        self.g = max(0.0, min(1.0, float(g)))

    def setB(self, b):
        self.b = max(0.0, min(1.0, float(b)))

    def __repr__(self):
        return "Color(%s %s %s)" % (self.r,self.g,self.b)

    def copyFrom(self, color):
        if isinstance(color, Color):
            self.setValues(color.r, color.g, color.b)
        else:
            r = color[0]
            g = color[1]
            b = color[2]
            self.setValues(r, g, b)

        return self

    def asTuple(self):
        return (self.r, self.g, self.b)

    def asStr(self):
        return "%d %d %d" % self.asTuple()

# Protected shaderDefine parameters that are set exclusively by means of shaderConfig options (configureShading())
_shaderConfigDefines = ['DIFFUSE', 'BUMPMAP', 'NORMALMAP', 'DISPLACEMENT', 'SPECULARMAP', 'VERTEX_COLOR']

# Protected shader parameters that are set exclusively by means of material properties (configureShading())
_materialShaderParams = ['diffuse', 'ambient', 'specular', 'emissive', 'diffuseTexture', 'bumpmapTexture', 'bumpmapIntensity', 'normalmapTexture', 'normalmapIntensity', 'displacementmapTexture', 'displacementmapTexture', 'specularmapTexture', 'specularmapIntensity']

class Material(object):
    """
    Material definition.
    Defines the visual appearance of an object when it is rendered (when it is
    set to solid).

    NOTE: Use one material per object! You can use copyFrom() to duplicate
    materials.
    """

    def __init__(self, name="UnnamedMaterial", performConfig=True):
        self.name = name

        self.filename = None
        self.filepath = None

        self._ambientColor = Color(1.0, 1.0, 1.0)
        self._diffuseColor = Color(1.0, 1.0, 1.0)
        self._diffuseIntensity = 0.8    # TODO is this useful?
        self._specularColor = Color(1.0, 1.0, 1.0)
        self._specularIntensity = 0.5   # TODO is this useful?
        self._transparencyIntensity = 0.0
        self._specularHardness = 0.2
        self._emissiveColor = Color()

        self._opacity = 1.0
        self._translucency = 0.0

        self._diffuseTexture = None
        self._bumpMapTexture = None
        self._bumpMapIntensity = 1.0
        self._normalMapTexture = None
        self._normalMapIntensity = 1.0
        self._displacementMapTexture = None
        self._displacementMapIntensity = 1.0
        self._specularMapTexture = None
        self._specularMapIntensity = 1.0 # TODO do we need this AND specularIntensity?
        self._transparencyMapTexture = None
        self._transparencyMapIntensity = 1.0

        self._shader = None
        self._shaderConfig = {
            'diffuse'      : True,
            'bump'         : True,
            'normal'       : True,
            'displacement' : True,
            'spec'         : True,
            'vertexColors' : True
        }
        self._shaderParameters = {}
        self._shaderDefines = []
        self.shaderChanged = True   # Determines whether shader should be recompiled

        if performConfig:
            self._updateShaderConfig()

        self._uvMap = None

    def copyFrom(self, material):
        self.name = material.name

        self.filename = material.filename
        self.filepath = material.filepath

        self._ambientColor.copyFrom(material.ambientColor)
        self._diffuseColor.copyFrom(material.diffuseColor)
        self._diffuseIntensity = material.diffuseIntensity
        self._specularColor.copyFrom(material.specularColor)
        self._specularIntensity = material.specularIntensity
        self._specularHardness = material.specularHardness
        self._emissiveColor.copyFrom(material.emissiveColor)

        self._opacity = material.opacity
        self._translucency = material.translucency

        self._diffuseTexture = material.diffuseTexture
        self._bumpMapTexture = material.bumpMapTexture
        self._bumpMapIntensity = material.bumpMapIntensity
        self._normalMapTexture = material.normalMapTexture
        self._normalMapIntensity = material.normalMapIntensity
        self._displacementMapTexture = material.displacementMapTexture
        self._displacementMapIntensity = material.displacementMapIntensity
        self._specularMapTexture = material.specularMapTexture
        self._specularMapIntensity = material.specularMapIntensity
        self._transparencyMapTexture = material.transparencyMapTexture
        self._transparencyMapIntensity = material.transparencyMapIntensity

        self._shader = material.shader
        self._shaderConfig = dict(material._shaderConfig)
        self._shaderParameters = dict(material.shaderParameters)
        self._shaderDefines = list(material.shaderDefines)
        self.shaderChanged = True

        self._uvMap = material.uvMap

        return self

    def fromFile(self, filename):
        """
        Parse .mhmat file and set as the properties of this material.
        """
        try:
            f = open(filename, "rU")
        except:
            f = None
        if f == None:
            log.error("Failed to load material from file %s.", filename)
            return

        self.filename = filename
        self.filepath = os.path.dirname(filename)

        shaderConfig_diffuse = None
        shaderConfig_bump = None
        shaderConfig_normal = None
        shaderConfig_displacement = None
        shaderConfig_spec = None
        shaderConfig_vertexColors = None

        for line in f:
            words = line.split()
            if len(words) == 0:
                continue
            if words[0] in ["#", "//"]:
                continue

            if words[0] == "name":
                self.name = words[1]
            if words[0] == "ambientColor":
                self._ambientColor.copyFrom([float(w) for w in words[1:4]])
            if words[0] == "diffuseColor":
                self._diffuseColor.copyFrom([float(w) for w in words[1:4]])
            if words[0] == "diffuseIntensity":
                self._diffuseIntensity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "specularColor":
                self._specularColor.copyFrom([float(w) for w in words[1:4]])
            if words[0] == "specularIntensity":
                self._specularIntensity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "specularHardness":
                self._specularHardness = max(0.0, min(1.0, float(words[1])))
            if words[0] == "emissiveColor":
                self._emissiveColor.copyFrom([float(w) for w in words[1:4]])
            if words[0] == "opacity":
                self._opacity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "translucency":
                self._translucency = max(0.0, min(1.0, float(words[1])))
            if words[0] == "diffuseTexture":
                self._diffuseTexture = getFilePath(words[1], self.filepath)
            if words[0] == "bumpmapTexture":
                self._bumpMapTexture = getFilePath(words[1], self.filepath)
            if words[0] == "bumpmapIntensity":
                self._bumpMapIntensity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "normalmapTexture":
                self._normalMapTexture = getFilePath(words[1], self.filepath)
            if words[0] == "normalmapIntensity":
                self._normalMapIntensity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "displacementmapTexture":
                self._displacementMapTexture = getFilePath(words[1], self.filepath)
            if words[0] == "displacementmapIntensity":
                self._displacementMapIntensity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "specularmapTexture":
                self._specularMapTexture = getFilePath(words[1], self.filepath)
            if words[0] == "specularmapIntensity":
                self._specularMapIntensity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "transparencymapTexture":
                self._transparencyMapTexture = getFilePath(words[1], self.filepath)
            if words[0] == "transparencymapIntensity":
                self._transparencyMapIntensity = max(0.0, min(1.0, float(words[1])))
            if words[0] == "shader":
                self._shader = getFilePath(words[1], self.filepath)
            if words[0] == "uvMap":
                self._uvMap = getFilePath(words[1], self.filepath)
            if words[0] == "shaderParam":
                if len(words) > 3:
                    self.setShaderParameter(words[1], words[2:])
                else:
                    self.setShaderParameter(words[1], words[2])
            if words[0] == "shaderDefine":
                self.addShaderDefine(words[1])
            if words[0] == "shaderConfig":
                if words[1] == "diffuse":
                    shaderConfig_diffuse = words[2].lower() in ["yes", "enabled", "true"]
                if words[1] == "bump":
                    shaderConfig_bump = words[2].lower() in ["yes", "enabled", "true"]
                if words[1] == "normal":
                    shaderConfig_normal = words[2].lower() in ["yes", "enabled", "true"]
                if words[1] == "displacement":
                    shaderConfig_displacement = words[2].lower() in ["yes", "enabled", "true"]
                if words[1] == "spec":
                    shaderConfig_spec = words[2].lower() in ["yes", "enabled", "true"]
                if words[1] == "vertexColors":
                    shaderConfig_vertexColors = words[2].lower() in ["yes", "enabled", "true"]

        f.close()
        self.configureShading(diffuse=shaderConfig_diffuse, bump=shaderConfig_bump, normal=shaderConfig_normal, displacement=shaderConfig_displacement, spec=shaderConfig_spec, vertexColors=shaderConfig_vertexColors)

    def _texPath(self, filename, materialPath = None):
        if materialPath:
            return os.path.relpath(filename, materialPath)
        elif self.filepath:
            return os.path.relpath(filename, self.filepath)
        else:
            return filename

    def toFile(self, filename, comments = []):
        import codecs

        try:
            f = codecs.open(filename, 'w', encoding='utf-8')
        except:
            f = None
        if f == None:
            log.error("Failed to open material file %s for writing.", filename)
            return

        f.write('# Material definition for %s\n' % self.name)
        for comment in comments:
            if not (comment.strip().startswith('//') or comment.strip().startswith('#')):
                comment = "# " + comment
            f.write(comment+"\n")
        f.write("\n")

        f.write("name %s\n" % self.name)
        f.write("ambientColor %s\n" % self.ambientColor.asStr())
        f.write("diffuseColor %s\n" % self.diffuseColor.asStr())
        f.write("diffuseIntensity %s\n" % self.diffuseIntensity)
        f.write("specularColor %s\n" % self.specularColor.asStr())
        f.write("specularIntensity %s\n" % self.specularIntensity)
        f.write("specularHardness %s\n" % self.specularHardness)
        f.write("emissiveColor %s\n" % self.emissiveColor.asStr())
        f.write("opacity %s\n" % self.opacity)
        f.write("translucency %s\n\n" % self.translucency)

        hasTexture = False
        filedir = os.path.dirname(filename)
        if self.diffuseTexture:
            f.write("diffuseTexture %s\n" % self._texPath(self.diffuseTexture, filedir) )
            hasTexture = True
        if self.bumpMapTexture:
            f.write("bumpmapTexture %s\n" % self._texPath(self.bumpMapTexture, filedir) )
            f.write("bumpmapIntensity %s\n" % self.bumpMapIntensity)
            hasTexture = True
        if self.normalMapTexture:
            f.write("normalmapTexture %s\n" % self._texPath(self.normalMapTexture, filedir) )
            f.write("normalmapIntensity %s\n" % self.normalMapIntensity)
            hasTexture = True
        if self.displacementMapTexture:
            f.write("displacementmapTexture %s\n" % self._texPath(self.displacementMapTexture, filedir) )
            f.write("displacementmapIntensity %s\n" % self.displacementMapIntensity)
            hasTexture = True
        if self.specularMapTexture:
            f.write("specularmapTexture %s\n" % self._texPath(self.specularMapTexture, filedir) )
            f.write("specularmapIntensity %s\n" % self.specularMapIntensity)
            hasTexture = True
        if self.transparencyMapTexture:
            f.write("transparencymapTexture %s\n" % self._texPath(self.transparencyMapTexture, filedir) )
            f.write("transparencymapIntensity %s\n" % self.transparencyMapIntensity)
            hasTexture = True
        if hasTexture: f.write('\n')

        if self.uvMap:
            f.write("uvMap %s\n\n" % self._texPath(self.uvMap, filedir) )

        if self.shader:
            f.write("shader %s\n\n" % self.shader)

        hasShaderParam = False
        global _materialShaderParams
        for name, param in list(self.shaderParameters.items()):
            if name not in _materialShaderParams:
                hasShaderParam = True
                import image
                if isinstance(param, list):
                    f.write("shaderParam %s %s\n" % (name, " ".join([str(p) for p in param])) )
                elif isinstance(param, image.Image):
                    if hasattr(param, "sourcePath"):
                        f.write("shaderParam %s %s\n" % (name, self._texPath(param.sourcePath, filedir)) )
                elif isinstance(param, str) and not isNumeric(param):
                    # Assume param is a path
                    f.write("shaderParam %s %s\n" % (name, self._texPath(param, filedir)) )
                else:
                    f.write("shaderParam %s %s\n" % (name, param) )
        if hasShaderParam: f.write('\n')

        hasShaderDefine = False
        global _shaderConfigDefines
        for define in self.shaderDefines:
            if define not in _shaderConfigDefines:
                hasShaderDefine = True
                f.write("shaderDefine %s\n" % define)
        if hasShaderDefine: f.write('\n')

        for name, value in list(self.shaderConfig.items()):
            f.write("shaderConfig %s %s\n" % (name, value) )

        f.close()

    def getUVMap(self):
        return self._uvMap

    def setUVMap(self, uvMap):
        self._uvMap = getFilePath(uvMap, self.filepath)

    uvMap = property(getUVMap, setUVMap)

    def getAmbientColor(self):
        #return self._ambientColor.values
        return self._ambientColor

    def setAmbientColor(self, color):
        self._ambientColor.copyFrom(color)

    ambientColor = property(getAmbientColor, setAmbientColor)


    def getDiffuseColor(self):
        #return self._diffuseColor.values
        # return self._diffuseColor * self._diffuseIntensity
        return self._diffuseColor

    def setDiffuseColor(self, color):
        self._diffuseColor.copyFrom(color)

    diffuseColor = property(getDiffuseColor, setDiffuseColor)


    def getDiffuseIntensity(self):
        return self._diffuseIntensity

    def setDiffuseIntensity(self, intensity):
        self._diffuseIntensity = min(1.0, max(0.0, intensity))

    diffuseIntensity = property(getDiffuseIntensity, setDiffuseIntensity)


    def getSpecularColor(self):
        #return self._specularColor.values
        return self._specularColor

    def setSpecularColor(self, color):
        self._specularColor.copyFrom(color)

    specularColor = property(getSpecularColor, setSpecularColor)


    def getSpecularIntensity(self):
        return self._specularIntensity

    def setSpecularIntensity(self, intensity):
        self._specularIntensity = min(1.0, max(0.0, intensity))

    specularIntensity = property(getSpecularIntensity, setSpecularIntensity)


    def getSpecularHardness(self):
        """
        The specular hardness or shinyness.
        """
        return self._specularHardness

    def setSpecularHardness(self, hardness):
        """
        Sets the specular hardness or shinyness.
        """
        self._specularHardness = max(0.0, hardness)

    specularHardness = property(getSpecularHardness, setSpecularHardness)


    def getTransparencyColor(self):
        #return self._transparencyColor.values
        return self._transparencyColor

    def setTransparencyColor(self, color):
        self._transparencyColor.copyFrom(color)

    transparencyColor = property(getTransparencyColor, setTransparencyColor)


    def getTransparencyIntensity(self):
        return self._transparencyIntensity

    def setTransparencyIntensity(self, intensity):
        self._transparencyIntensity = min(1.0, max(0.0, intensity))

    transparencyIntensity = property(getTransparencyIntensity, setTransparencyIntensity)


    def getEmissiveColor(self):
        #return self._emissiveColor.values
        return self._emissiveColor

    def setEmissiveColor(self, color):
        self._emissiveColor.copyFrom(color)

    emissiveColor = property(getEmissiveColor, setEmissiveColor)


    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = min(1.0, max(0.0, opacity))

    opacity = property(getOpacity, setOpacity)


    def getTranslucency(self):
        return self._translucency

    def setTranslucency(self, translucency):
        self._translucency = min(1.0, max(0.0, translucency))

    translucency = property(getTranslucency, setTranslucency)


    def supportsDiffuse(self):
        return self.diffuseTexture != None

    def supportsBump(self):
        return self.bumpMapTexture != None

    def supportsDisplacement(self):
        return self.displacementMapTexture != None

    def supportsNormal(self):
        return self.normalMapTexture != None

    def supportsSpecular(self):
        return self.specularMapTexture != None

    def supportsTransparency(self):
        return self.transparencyMapTexture != None

    def configureShading(self, diffuse=None, bump = None, normal=None, displacement=None, spec = None, vertexColors = None):
        """
        Configure shading options and set the necessary properties based on
        the material configuration of this object. This configuration applies
        for shaders only (depending on whether the selected shader supports the
        chosen options), so only has effect when a shader is set.
        This method can be invoked even when no shader is set, the chosen
        options will remain effective when another shader is set.
        A value of None leaves configuration options unchanged.
        """
        if diffuse != None: self._shaderConfig['diffuse'] = diffuse
        if bump != None: self._shaderConfig['bump'] = bump
        if normal != None: self._shaderConfig['normal'] = normal
        if displacement != None: self._shaderConfig['displacement'] = displacement
        if spec != None: self._shaderConfig['spec'] = spec
        if vertexColors != None: self._shaderConfig['vertexColors'] = vertexColors

        self._updateShaderConfig()

    @property
    def shaderConfig(self):
        """
        The shader parameters as set by configureShading().
        """
        return dict(self._shaderConfig)

    def _updateShaderConfig(self):
        global _shaderConfigDefines
        global _materialShaderParams

        import numpy as np

        if not self.shader:
            return

        self._shaderParameters['ambient']  = self.ambientColor.values
        self._shaderParameters['diffuse'] = list(np.asarray(self.diffuseColor.values, dtype=np.float32) * self.diffuseIntensity) + [self.opacity]
        self._shaderParameters['specular'] = list(np.asarray(self.specularColor.values, dtype=np.float32) * self.specularIntensity) + [self.specularHardness]
        self._shaderParameters['emissive'] = self.emissiveColor

        # Remove (non-custom) shader config defines (those set by shader config)
        for shaderDefine in _shaderConfigDefines:
            try:
                self._shaderDefines.remove(shaderDefine)
            except:
                pass

        # Reset (non-custom) shader parameters controlled by material properties
        for shaderParam in _materialShaderParams:
            try:
                del self._shaderParameters[shaderParam]
            except:
                pass

        if self._shaderConfig['vertexColors']:
            log.debug("Enabling vertex colors.")
            self._shaderDefines.append('VERTEX_COLOR')
        if self._shaderConfig['diffuse'] and self.supportsDiffuse():
            log.debug("Enabling diffuse texturing.")
            self._shaderDefines.append('DIFFUSE')
            self._shaderParameters['diffuseTexture'] = self.diffuseTexture
        bump = self._shaderConfig['bump'] and self.supportsBump()
        normal = self._shaderConfig['normal'] and self.supportsNormal()
        if bump and not normal:
            log.debug("Enabling bump mapping.")
            self._shaderDefines.append('BUMPMAP')
            self._shaderParameters['bumpmapTexture'] = self.bumpMapTexture
            self._shaderParameters['bumpmapIntensity'] = self.bumpMapIntensity
        if normal:
            log.debug("Enabling normal mapping.")
            self._shaderDefines.append('NORMALMAP')
            self._shaderParameters['normalmapTexture'] = self.normalMapTexture
            self._shaderParameters['normalmapIntensity'] = self.normalMapIntensity
        if self._shaderConfig['displacement'] and self.supportsDisplacement():
            log.debug("Enabling displacement mapping.")
            self._shaderDefines.append('DISPLACEMENT')
            self._shaderParameters['displacementmapTexture'] = self.displacementMapTexture
            self._shaderParameters['displacementmapIntensity'] = self.displacementMapIntensity
        if self._shaderConfig['spec'] and self.supportsSpecular():
            log.debug("Enabling specular mapping.")
            self._shaderDefines.append('SPECULARMAP')
            self._shaderParameters['specularmapTexture'] = self.specularMapTexture
            self._shaderParameters['specularmapIntensity'] = self._specularMapIntensity

        self._shaderDefines.sort()   # This is important for shader caching
        self.shaderChanged = True

    def setShader(self, shader):
        self._shader = shader
        self._updateShaderConfig()
        self.shaderChanged = True

    def getShader(self):
        return self._shader

    shader = property(getShader, setShader)


    @property
    def shaderParameters(self):
        """
        All shader parameters. Both those set by material properties as well as
        custom shader parameters set by setShaderParameter().
        """
        return dict(self._shaderParameters)

    def setShaderParameter(self, name, value):
        """
        Set a custom shader parameter. Shader parameters are uniform parameters
        passed to the shader programme, their type should match that declared in
        the shader code.
        """
        global _materialShaderParams

        if name in _materialShaderParams:
            raise RuntimeError('The shader parameter "%s" is protected and should be set by means of material properties.' % name)

        if isinstance(value, list):
            value = [float(v) for v in value]
        elif isinstance(value, str):
            if isNumeric(value):
                value = float(value)
            else:
                # Assume value is a path
                value = getFilePath(value, self.filepath)

        self._shaderParameters[name] = value

    def removeShaderParameter(self, name):
        global _materialShaderParams

        if name in _materialShaderParams:
            raise RuntimeError('The shader parameter "%s" is protected and should be set by means of material properties.' % name)
        try:
            del self._shaderParameters[name]
        except:
            pass

    def clearShaderParameters(self):
        """
        Remove all custom set shader parameters.
        """
        global _materialShaderParams

        for shaderParam in self.shaderParameters:
            if shaderParam not in _materialShaderParams:
                self.removeShaderParameter(shaderParam)


    @property
    def shaderDefines(self):
        """
        All shader defines. Both those set by configureShading() as well as
        custom shader defines set by addShaderDefine().
        """
        return list(self._shaderDefines)

    def addShaderDefine(self, defineStr):
        global _shaderConfigDefines

        if defineStr in _shaderConfigDefines:
            raise RuntimeError('The shader define "%s" is protected and should be set by means of configureShading().' % defineStr)
        if defineStr in self.shaderDefines:
            return
        self._shaderDefines.append(defineStr)
        self._shaderDefines.sort()   # This is important for shader caching

        self.shaderChanged = True

    def removeShaderDefine(self, defineStr):
        global _shaderConfigDefines

        if defineStr in _shaderConfigDefines:
            raise RuntimeError('The shader define %s is protected and should be set by means of configureShading().' % defineStr)
        try:
            self._shaderDefines.remove(defineStr)
        except:
            pass

        self.shaderChanged = True

    def clearShaderDefines(self):
        """
        Remove all custom set shader defines.
        """
        global _shaderConfigDefines

        for shaderDefine in self._shaderDefines:
            if shaderDefine not in _shaderConfigDefines:
                self.removeShaderDefine(shaderDefine)
        self.shaderChanged = True


    def _getTexture(self, texture):
        if isinstance(texture, str):
            return getFilePath(texture, self.filepath)
        else:
            return texture


    def getDiffuseTexture(self):
        return self._diffuseTexture

    def setDiffuseTexture(self, texture):
        self._diffuseTexture = self._getTexture(texture)
        self._updateShaderConfig()

    diffuseTexture = property(getDiffuseTexture, setDiffuseTexture)


    def getBumpMapTexture(self):
        return self._bumpMapTexture

    def setBumpMapTexture(self, texture):
        self._bumpMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    bumpMapTexture = property(getBumpMapTexture, setBumpMapTexture)


    def getBumpMapIntensity(self):
        return self._bumpMapIntensity

    def setBumpMapIntensity(self, intensity):
        self._bumpMapIntensity = intensity
        self._updateShaderConfig()

    bumpMapIntensity = property(getBumpMapIntensity, setBumpMapIntensity)


    def getNormalMapTexture(self):
        return self._normalMapTexture

    def setNormalMapTexture(self, texture):
        self._normalMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    normalMapTexture = property(getNormalMapTexture, setNormalMapTexture)


    def getNormalMapIntensity(self):
        return self._normalMapIntensity

    def setNormalMapIntensity(self, intensity):
        self._normalMapIntensity = intensity
        self._updateShaderConfig()

    normalMapIntensity = property(getNormalMapIntensity, setNormalMapIntensity)


    def getDisplacementMapTexture(self):
        return self._displacementMapTexture

    def setDisplacementMapTexture(self, texture):
        self._displacementMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    displacementMapTexture = property(getDisplacementMapTexture, setDisplacementMapTexture)


    def getDisplacementMapIntensity(self):
        return self._displacementMapIntensity

    def setDisplacementMapIntensity(self, intensity):
        self._displacementMapIntensity = intensity
        self._updateShaderConfig()

    displacementMapIntensity = property(getDisplacementMapIntensity, setDisplacementMapIntensity)


    def getSpecularMapTexture(self):
        """
        The specular or reflectivity map texture.
        """
        return self._specularMapTexture

    def setSpecularMapTexture(self, texture):
        """
        Set the specular or reflectivity map texture.
        """
        self._specularMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    specularMapTexture = property(getSpecularMapTexture, setSpecularMapTexture)


    def getSpecularMapIntensity(self):
        return self._specularMapIntensity

    def setSpecularMapIntensity(self, intensity):
        self._specularMapIntensity = intensity
        self._updateShaderConfig()

    specularMapIntensity = property(getSpecularMapIntensity, setSpecularMapIntensity)


    def getTransparencyMapTexture(self):
        """
        The transparency or reflectivity map texture.
        """
        return self._transparencyMapTexture

    def setTransparencyMapTexture(self, texture):
        """
        Set the transparency or reflectivity map texture.
        """
        self._transparencyMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    transparencyMapTexture = property(getTransparencyMapTexture, setTransparencyMapTexture)


    def getTransparencyMapIntensity(self):
        return self._transparencyMapIntensity

    def setTransparencyMapIntensity(self, intensity):
        self._transparencyMapIntensity = intensity
        self._updateShaderConfig()

    transparencyMapIntensity = property(getTransparencyMapIntensity, setTransparencyMapIntensity)


def fromFile(filename):
    """
    Create a material from a .mhmat file.
    """
    mat = Material(performConfig=False)
    mat.fromFile(filename)
    return mat

def getFilePath(filename, folder = None):
    if not filename:
        return filename

    # Search within current folder
    if folder:
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            return os.path.abspath(path)
    # Treat as absolute path or search relative to application path
    if os.path.isfile(filename):
        return os.path.abspath(filename)
    # Search in user data folder
    import mh
    userPath = os.path.join(mh.getPath(''), filename)
    if os.path.isfile(userPath):
        return os.path.abspath(userPath)
    # Search in system data path
    sysPath = mh.getSysDataPath(filename)
    if os.path.isfile(sysPath):
        return os.path.abspath(sysPath)

    # Nothing found
    return filename

def isNumeric(string):
    try:
        return str(string).isnumeric()
    except:
        # On decoding errors
        return False

class UVMap:
    def __init__(self, name):
        self.name = name
        self.type = "UvSet"
        self.filepath = None
        self.materialName = "Default"
        self.uvs = None
        self.fuvs = None


    def read(self, mesh, filepath):
        import numpy as np

        filename,ext = os.path.splitext(filepath)
        if ext == ".mhuv":
            raise NameError("ERROR: .mhuv files are obsolete. Change to .obj: %s" % filepath)

        uvs,fuvs = loadUvObjFile(filepath)
        self.filepath = filepath
        self.uvs = np.array(uvs)
        self.fuvs = np.array(fuvs)

        if len(self.fuvs) != meshstat.numberOfFaces:
            raise NameError("The file %s is corrupt. Number of faces %d != %d" %
                (filepath, len(self.fuvs), meshstat.numberOfFaces))


def loadUvObjFile(filepath):
    fp = open(filepath, "rU")
    uvs = []
    fuvs = []
    for line in fp:
        words = line.split()
        if len(words) == 0:
            continue
        elif words[0] == "vt":
            uvs.append((float(words[1]), float(words[2])))
        elif words[0] == "f":
            fuvs.append( [(int(word.split("/")[1]) - 1) for word in words[1:]] )
    fp.close()
    return uvs,fuvs
