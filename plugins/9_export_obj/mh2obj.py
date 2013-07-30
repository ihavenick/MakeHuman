#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------
Exports proxy mesh to obj

"""

import wavefront
import os
import exportutils

#
#    exportObj(human, filepath, config):
#

def exportObj(human, filepath, config=None):
    if config is None:
        config = exportutils.config.Config()
    obj = human.meshData
    config.setHuman(human)
    config.setupTexFolder(filepath)
    filename = os.path.basename(filepath)
    name = config.goodName(os.path.splitext(filename)[0])

    rmeshes,_amt = exportutils.collect.setupObjects(
        name,
        human,
        config=config,
        helpers=config.helpers,
        eyebrows=config.eyebrows,
        lashes=config.lashes,
        subdivide=config.subdivide)

    objects = [rmesh.richMesh.object for rmesh in rmeshes]
    wavefront.writeObjFile(filepath, objects, True, config)

    return

