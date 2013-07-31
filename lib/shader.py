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

TODO
"""

import os.path
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.ARB.texture_multisample import *
import texture
import log

class Uniform(object):
    def __init__(self, index, name, pytype, dims):
        self.index = index
        self.name = name
        self.pytype = pytype
        self.dims = dims
        self.values = None

    def __call__(self, index, values):
        raise NotImplementedError

    def update(self, pgm):
        pass

class VectorUniform(Uniform):
    uniformTypes = {
        GL_FLOAT:               ((1,),  np.float32,     float,  glUniform1fv,		glGetUniformfv),
        GL_FLOAT_VEC2:          ((2,),  np.float32,     float,  glUniform2fv,		glGetUniformfv),
        GL_FLOAT_VEC3:          ((3,),  np.float32,     float,  glUniform3fv,		glGetUniformfv),
        GL_FLOAT_VEC4:          ((4,),  np.float32,     float,  glUniform4fv,		glGetUniformfv),
        GL_INT:                 ((1,),  np.int32,       int,    glUniform1iv,		glGetUniformiv),
        GL_INT_VEC2:            ((2,),  np.int32,       int,    glUniform2iv,		glGetUniformiv),
        GL_INT_VEC3:            ((3,),  np.int32,       int,    glUniform3iv,		glGetUniformiv),
        GL_INT_VEC4:            ((4,),  np.int32,       int,    glUniform4iv,		glGetUniformiv),
        GL_UNSIGNED_INT:        ((1,),  np.uint32,      int,    glUniform1uiv,		glGetUniformuiv),
        GL_UNSIGNED_INT_VEC2:   ((2,),  np.uint32,      int,    glUniform2uiv,		glGetUniformuiv),
        GL_UNSIGNED_INT_VEC3:   ((3,),  np.uint32,      int,    glUniform3uiv,		glGetUniformuiv),
        GL_UNSIGNED_INT_VEC4:   ((4,),  np.uint32,      int,    glUniform4uiv,		glGetUniformuiv),
        GL_BOOL:                ((1,),  np.int32,       bool,   glUniform1iv,		glGetUniformiv),
        GL_BOOL_VEC2:           ((2,),  np.int32,       bool,   glUniform2iv,		glGetUniformiv),
        GL_BOOL_VEC3:           ((3,),  np.int32,       bool,   glUniform3iv,		glGetUniformiv),
        GL_BOOL_VEC4:           ((4,),  np.int32,       bool,   glUniform4iv,		glGetUniformiv),
        GL_FLOAT_MAT2:          ((2,2), np.float32,     float,  glUniformMatrix2fv,	glGetUniformfv),
        GL_FLOAT_MAT2x3:        ((2,3), np.float32,     float,  glUniformMatrix2x3fv,	glGetUniformfv),
        GL_FLOAT_MAT2x4:        ((2,4), np.float32,     float,  glUniformMatrix2x4fv,	glGetUniformfv),
        GL_FLOAT_MAT3x2:        ((3,2), np.float32,     float,  glUniformMatrix3x2fv,	glGetUniformfv),
        GL_FLOAT_MAT3:          ((3,3), np.float32,     float,  glUniformMatrix3fv,	glGetUniformfv),
        GL_FLOAT_MAT3x4:        ((3,4), np.float32,     float,  glUniformMatrix3x4fv,	glGetUniformfv),
        GL_FLOAT_MAT4x2:        ((4,2), np.float32,     float,  glUniformMatrix4x2fv,	glGetUniformfv),
        GL_FLOAT_MAT4x3:        ((4,3), np.float32,     float,  glUniformMatrix4x3fv,	glGetUniformfv),
        GL_FLOAT_MAT4:          ((4,4), np.float32,     float,  glUniformMatrix4fv,	glGetUniformfv),
        }

    if 'glUniform1dv' in globals():
        uniformTypes2 = {
            GL_DOUBLE:              ((1,),  np.float64,     float,  glUniform1dv,		glGetUniformdv),
            GL_DOUBLE_VEC2:         ((2,),  np.float64,     float,  glUniform2dv,		glGetUniformdv),
            GL_DOUBLE_VEC3:         ((3,),  np.float64,     float,  glUniform3dv,		glGetUniformdv),
            GL_DOUBLE_VEC4:         ((4,),  np.float64,     float,  glUniform4dv,		glGetUniformdv),
            GL_DOUBLE_MAT2:         ((2,2), np.float64,     float,  glUniformMatrix2dv,		glGetUniformdv),
            GL_DOUBLE_MAT2x3:       ((2,3), np.float64,     float,  glUniformMatrix2x3dv,	glGetUniformdv),
            GL_DOUBLE_MAT2x4:       ((2,4), np.float64,     float,  glUniformMatrix2x4dv,	glGetUniformdv),
            GL_DOUBLE_MAT3x2:       ((3,2), np.float64,     float,  glUniformMatrix3x2dv,	glGetUniformdv),
            GL_DOUBLE_MAT3:         ((3,3), np.float64,     float,  glUniformMatrix3dv,		glGetUniformdv),
            GL_DOUBLE_MAT3x4:       ((3,4), np.float64,     float,  glUniformMatrix3x4dv,	glGetUniformdv),
            GL_DOUBLE_MAT4x2:       ((4,2), np.float64,     float,  glUniformMatrix4x2dv,	glGetUniformdv),
            GL_DOUBLE_MAT4x3:       ((4,3), np.float64,     float,  glUniformMatrix4x3dv,	glGetUniformdv),
            GL_DOUBLE_MAT4:         ((4,4), np.float64,     float,  glUniformMatrix4dv,		glGetUniformdv),
            }

    @classmethod
    def check(cls, type):
        if hasattr(cls, 'uniformTypes2') and cls.uniformTypes2:
            cls.uniformTypes.update(cls.uniformTypes2)
            cls.uniformTypes2.clear()
        return type in cls.uniformTypes

    def __init__(self, index, name, type):
        dims, dtype, pytype, glfunc, glquery = self.uniformTypes[type]
        super(VectorUniform, self).__init__(index, name, pytype, dims)
        self.dtype = dtype
        self.glfunc = glfunc
        self.glquery = glquery

    def set(self, data):
        values = np.asarray(data, dtype=self.dtype).reshape(self.dims)
        if len(self.dims) > 1:
            self.glfunc(self.index, 1, GL_TRUE, values)
        else:
            self.glfunc(self.index, len(values), values)

    def update(self, pgm):
        values = np.zeros(self.dims, dtype=self.dtype)
        self.glquery(pgm, self.index, values)
        if len(self.dims) > 1:
            values = values.T
        self.values = values
        log.debug('VectorUniform(%s) = %s', self.name, self.values)
        return self.values

class SamplerUniform(Uniform):

    textureTargets = {
        GL_SAMPLER_1D:                                  GL_TEXTURE_1D,
        GL_SAMPLER_2D:                                  GL_TEXTURE_2D,
        GL_SAMPLER_3D:                                  GL_TEXTURE_3D,
        GL_SAMPLER_CUBE:                                GL_TEXTURE_CUBE_MAP,
        GL_SAMPLER_1D_SHADOW:                           GL_TEXTURE_1D,
        GL_SAMPLER_2D_SHADOW:                           GL_TEXTURE_2D,
        GL_SAMPLER_1D_ARRAY:                            GL_TEXTURE_1D_ARRAY,
        GL_SAMPLER_2D_ARRAY:                            GL_TEXTURE_2D_ARRAY,
        GL_SAMPLER_1D_ARRAY_SHADOW:                     GL_TEXTURE_1D_ARRAY,
        GL_SAMPLER_2D_ARRAY_SHADOW:                     GL_TEXTURE_2D_ARRAY,
        GL_SAMPLER_2D_MULTISAMPLE:                      GL_TEXTURE_2D_MULTISAMPLE,
        GL_SAMPLER_2D_MULTISAMPLE_ARRAY:                GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
        GL_SAMPLER_CUBE_SHADOW:                         GL_TEXTURE_CUBE_MAP,
        GL_SAMPLER_BUFFER:                              GL_TEXTURE_BUFFER,
        GL_SAMPLER_2D_RECT:                             GL_TEXTURE_RECTANGLE,
        GL_SAMPLER_2D_RECT_SHADOW:                      GL_TEXTURE_RECTANGLE,
        GL_INT_SAMPLER_1D:                              GL_TEXTURE_1D,
        GL_INT_SAMPLER_2D:                              GL_TEXTURE_2D,
        GL_INT_SAMPLER_3D:                              GL_TEXTURE_3D,
        GL_INT_SAMPLER_CUBE:                            GL_TEXTURE_CUBE_MAP,
        GL_INT_SAMPLER_1D_ARRAY:                        GL_TEXTURE_1D_ARRAY,
        GL_INT_SAMPLER_2D_ARRAY:                        GL_TEXTURE_2D_ARRAY,
        GL_INT_SAMPLER_2D_MULTISAMPLE:                  GL_TEXTURE_2D_MULTISAMPLE,
        GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:            GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
        GL_INT_SAMPLER_BUFFER:                          GL_TEXTURE_BUFFER,
        GL_INT_SAMPLER_2D_RECT:                         GL_TEXTURE_RECTANGLE,
        GL_UNSIGNED_INT_SAMPLER_1D:                     GL_TEXTURE_1D,
        GL_UNSIGNED_INT_SAMPLER_2D:                     GL_TEXTURE_2D,
        GL_UNSIGNED_INT_SAMPLER_3D:                     GL_TEXTURE_3D,
        GL_UNSIGNED_INT_SAMPLER_CUBE:                   GL_TEXTURE_CUBE_MAP,
        GL_UNSIGNED_INT_SAMPLER_1D_ARRAY:               GL_TEXTURE_1D_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_2D_ARRAY:               GL_TEXTURE_2D_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE:         GL_TEXTURE_2D_MULTISAMPLE,
        GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY:   GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
        GL_UNSIGNED_INT_SAMPLER_BUFFER:                 GL_TEXTURE_BUFFER,
        GL_UNSIGNED_INT_SAMPLER_2D_RECT:                GL_TEXTURE_RECTANGLE,
        }

    if 'GL_IMAGE_1D' in globals():    
        try:
            textureTargets2 = {
                GL_IMAGE_1D:                                    GL_TEXTURE_1D,
                GL_IMAGE_2D:                                    GL_TEXTURE_2D,
                GL_IMAGE_3D:                                    GL_TEXTURE_3D,
                GL_IMAGE_2D_RECT:                               GL_TEXTURE_2D_RECTANGLE,
                GL_IMAGE_CUBE:                                  GL_TEXTURE_CUBE_MAP,
                GL_IMAGE_BUFFER:                                GL_TEXTURE_BUFFER,
                GL_IMAGE_1D_ARRAY:                              GL_TEXTURE_1D_ARRAY,
                GL_IMAGE_2D_ARRAY:                              GL_TEXTURE_2D_ARRAY,
                GL_IMAGE_2D_MULTISAMPLE:                        GL_TEXTURE_2D_MULTISAMPLE,
                GL_IMAGE_2D_MULTISAMPLE_ARRAY:                  GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
                GL_INT_IMAGE_1D:                                GL_TEXTURE_1D,
                GL_INT_IMAGE_2D:                                GL_TEXTURE_2D,
                GL_INT_IMAGE_3D:                                GL_TEXTURE_3D,
                GL_INT_IMAGE_2D_RECT:                           GL_TEXTURE_2D_RECTANGLE,
                GL_INT_IMAGE_CUBE:                              GL_TEXTURE_CUBE_MAP,
                GL_INT_IMAGE_BUFFER:                            GL_TEXTURE_BUFFER,
                GL_INT_IMAGE_1D_ARRAY:                          GL_TEXTURE_1D_ARRAY,
                GL_INT_IMAGE_2D_ARRAY:                          GL_TEXTURE_2D_ARRAY,
                GL_INT_IMAGE_2D_MULTISAMPLE:                    GL_TEXTURE_2D_MULTISAMPLE,
                GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY:              GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
                GL_UNSIGNED_INT_IMAGE_1D:                       GL_TEXTURE_1D,
                GL_UNSIGNED_INT_IMAGE_2D:                       GL_TEXTURE_2D,
                GL_UNSIGNED_INT_IMAGE_3D:                       GL_TEXTURE_3D,
                GL_UNSIGNED_INT_IMAGE_2D_RECT:                  GL_TEXTURE_2D_RECTANGLE,
                GL_UNSIGNED_INT_IMAGE_CUBE:                     GL_TEXTURE_CUBE_MAP,
                GL_UNSIGNED_INT_IMAGE_BUFFER:                   GL_TEXTURE_BUFFER,
                GL_UNSIGNED_INT_IMAGE_1D_ARRAY:                 GL_TEXTURE_1D_ARRAY,
                GL_UNSIGNED_INT_IMAGE_2D_ARRAY:                 GL_TEXTURE_2D_ARRAY,
                GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE:           GL_TEXTURE_2D_MULTISAMPLE,
                GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY:     GL_TEXTURE_2D_MULTISAMPLE_ARRAY,
                }
        except:
            pass

    @classmethod
    def check(cls, type):
        if hasattr(cls, 'textureTargets2') and cls.textureTargets2:
            cls.textureTargets.update(cls.textureTargets2)
            cls.textureTargets2.clear()
        return type in cls.textureTargets

    def __init__(self, index, name, type):
        target = self.textureTargets[type]
        super(SamplerUniform, self).__init__(index, name, str, (1,))
        self.target = target

    def set(self, data):
        cls = type(self)
        glActiveTexture(GL_TEXTURE0 + cls.currentSampler)
        tex = texture.getTexture(data)
        if tex not in (False, None):
            glBindTexture(self.target, tex.textureId)
        glUniform1i(self.index, cls.currentSampler)
        cls.currentSampler += 1

    @classmethod
    def reset(cls):
        cls.currentSampler = 1

class Shader(object):
    _supported = None

    @classmethod
    def supported(cls):
        if cls._supported is None:
            cls._supported = bool(glCreateProgram)
        return cls._supported

    def __init__(self, path, defines = []):
        if not self.supported():
            raise RuntimeError("No shader support detected")

        super(Shader, self).__init__()

        self.path = path

        self.vertexId = None
        self.fragmentId = None
        self.shaderId = None
        self.modified = None
        self.uniforms = None
        self.defines = defines
        self.vertexTangentAttrId = None

        self.initShader()

    def __del__(self):
        try:
            self.delete()
        except Exception:
            pass

    @staticmethod
    def createShader(file, type, defines = []):
        with open(file, 'rU') as f:
            source = f.read()
        if "#version" not in source:
            log.warning("The shader source in %s does not contain an explicit GLSL version declaration. This could cause problems with some compilers.", file)
        if defines:
            # Add #define instructions for shader preprocessor to enable extra
            # shader features at compile time
            firstComments, code = Shader.splitVersionDeclaration(source)
            defineLines = "\n".join([ "#define " + define for define in defines])
            source = "\n".join([firstComments, defineLines, code])
        shader = glCreateShader(type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            logmsg = glGetShaderInfoLog(shader)
            log.error("Error compiling shader: %s", logmsg)
            return None
        return shader

    @staticmethod
    def splitVersionDeclaration(sourceStr):
        """
        Split source string in part that contains the #version declaration,
        that should occur before any instructions (only comments can preceed),
        and the rest of the shader code.
        Define statements can be inserted between the two split strings.
        This is to ensure that any #version statements remain the first
        instruction in the shader source, conform with the GLSL spec.
        If no #version statement is found, the full source will be in the second
        string, allowing #define statements to be inserted at the top of the 
        source.
        NOTE: For this to work correctly, #version effectively needs to be the
        first instruction in the shader source, but this is usually enforced by
        the GLSL compiler anyway.
        Returns a tuple of two strings.
        """
        if "#version" in sourceStr:
            lines = sourceStr.split("\n")
            for lIdx,line in enumerate(lines):
                # Determine line where #version occurs
                if line.strip().startswith("#version"):
                    return "\n".join(lines[:lIdx+1]), "\n".join(lines[lIdx+1:])
        # Else don't split source
        return "", sourceStr

    def delete(self):
        if self.vertexId:
            glDeleteShader(self.vertexId)
            self.vertexId = None
        if self.fragmentId:
            glDeleteShader(self.fragmentId)
            self.fragmentId = None
        if self.shaderId:
            glDeleteProgram(self.shaderId)
            self.shaderId = None

    def initShader(self):
        vertexSource = self.path + '_vertex_shader.txt'
        geometrySource = self.path + '_geometry_shader.txt'
        fragmentSource = self.path + '_fragment_shader.txt'

        self.shaderId = glCreateProgram()

        if os.path.isfile(vertexSource):
            self.vertexId = self.createShader(vertexSource, GL_VERTEX_SHADER, self.defines)
            glAttachShader(self.shaderId, self.vertexId)

        if os.path.isfile(geometrySource) and 'GL_GEOMETRY_SHADER' in globals():
            self.geometryId = self.createShader(geometrySource, GL_GEOMETRY_SHADER, self.defines)
            glAttachShader(self.shaderId, self.geometryId)

        if os.path.isfile(fragmentSource):
            self.fragmentId = self.createShader(fragmentSource, GL_FRAGMENT_SHADER, self.defines)
            glAttachShader(self.shaderId, self.fragmentId)

        glLinkProgram(self.shaderId)
        if not glGetProgramiv(self.shaderId, GL_LINK_STATUS):
            log.error("Error linking shader: %s", glGetProgramInfoLog(self.shaderId))
            self.delete()
            return

        self.vertexTangentAttrId = glGetAttribLocation(self.shaderId, b'tangent')

        self.uniforms = None
        self.updateUniforms()

    def getUniforms(self):
        if self.uniforms is None:
            parameterCount = glGetProgramiv(self.shaderId, GL_ACTIVE_UNIFORMS)
            self.uniforms = []
            for index in range(parameterCount):
                name, size, type = glGetActiveUniform(self.shaderId, index)
                if VectorUniform.check(type):
                    uniform = VectorUniform(index, name, type)
                elif SamplerUniform.check(type):
                    uniform = SamplerUniform(index, name, type)
                uniform.update(self.shaderId)
                self.uniforms.append(uniform)

        return self.uniforms

    def updateUniforms(self):
        for uniform in self.getUniforms():
            uniform.update(self.shaderId)

    def setUniforms(self, params):
        SamplerUniform.reset()

        for uniform in self.getUniforms():
            value = params.get(uniform.name)
            if value is not None:
                uniform.set(value)

    def requiresVertexTangent(self):
        return self.vertexTangentAttrId != -1

_shaderCache = {}

def getShader(path, defines=[], cache=None):
    shader = None
    cache = cache or _shaderCache

    path1 = path + '_vertex_shader.txt'
    path2 = path + '_fragment_shader.txt'
    path3 = path + '_geometry_shader.txt'
    paths = [p for p in [path1, path2, path3] if os.path.isfile(p)]
    if not paths:
        cache[path] = False
        return False

    mtime = max(os.path.getmtime(p) for p in paths)

    cacheName = path
    if defines:
        # It's important that the defines are sorted alfpabetically here
        cacheName = cacheName + "@" + "|".join(defines)

    if cacheName in cache:
        shader = cache[cacheName]
        if shader is False:
            return shader

        if mtime > shader.modified:
            log.message('reloading %s', cacheName)
            try:
                shader.initShader()
                shader.modified = mtime
            except RuntimeError as text:
                log.error("Error loading shader %s", cacheName, exc_info=True)
                shader = False
    else:
        try:
            shader = Shader(path, defines)
            shader.modified = mtime
        except RuntimeError as text:
            log.error("Error loading shader %s", path, exc_info=True)
            shader = False

    cache[cacheName] = shader
    return shader
    
def reloadShaders():
    log.message('Reloading shaders')
    for path in _shaderCache:
        try:
            _shaderCache[path].initShader()
        except RuntimeError as text:
            log.error("Error loading shader %s", path, exc_info=True)
            _shaderCache[path] = False
