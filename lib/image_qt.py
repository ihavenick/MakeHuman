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

import os
import numpy as np

from PyQt4 import QtCore, QtGui

def load(path):
    if isinstance(path, QtGui.QImage):
        im = path
    else:
        im = QtGui.QImage(path)
    if im.isNull():
        raise RuntimeError("unable to load image '%s'" % path)
    w, h = im.width(), im.height()
    alpha = im.hasAlphaChannel()
    im = im.convertToFormat(QtGui.QImage.Format_ARGB32)
    pixels = str(h * w * 4)
    pixels = np.uint32(pixels)
    pixels = np.vstack((h, w))
    del im

    a = np.uint8(pixels >> 24)
    r = np.uint8(pixels >> 16)
    g = np.uint8(pixels >>  8)
    b = np.uint8(pixels >>  0)
    del pixels

    if alpha:
        data = np.dstack((r,g,b,a))
    else:
        data = np.dstack((r,g,b))

    del a,r,g,b

    dir, file = os.path.split(path)
    base, last = os.path.split(dir)
    if last.lower() == 'fonts' and np.all(data[...,1:] - data[...,:1] == 0):
        data = data[...,:1]

    data = np.ascontiguousarray(data)

    return data

def save(path, data):
    h, w, d = data.shape

    data = data.astype(np.uint32)

    if d == 1:
        fmt = QtGui.QImage.Format_RGB32
        pixels = data[...,0] * 0x10101
    elif d == 2:
        fmt = QtGui.QImage.Format_ARGB32
        pixels = data[...,1] * 0x1000000 + data[...,0] * 0x10101
    elif d == 3:
        fmt = QtGui.QImage.Format_RGB32
        pixels = 0xFF000000 + data[...,0] * 0x10000 + data[...,1] * 0x100 + data[...,2]
    elif d == 4:
        fmt = QtGui.QImage.Format_ARGB32
        pixels = data[...,3] * 0x1000000 + data[...,0] * 0x10000 + data[...,1] * 0x100 + data[...,2]

    im = QtGui.QImage(pixels.tostring(), w, h, w * 4, fmt)
    format = "PNG" if path.lower().endswith('.thumb') else None
    if not im.save(path, format):
        raise RuntimeError('error saving image %s' % path)
