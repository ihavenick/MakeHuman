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

TODO
"""

import os
import mh
import log
import shutil

#
#   class Config
#

class Config:

    def __init__(self):
        self.useTexFolder       = True
        self.eyebrows           = True
        self.lashes             = True
        self.helpers            = False
        self.useTPose           = False
        self.scale              = 1.0
        self.unit               = "dm"

        self.rigOptions         = None
        self.useNormals         = False
        self.useRelPaths        = True
        self.cage               = False
        self.texFolder          = None
        self.customPrefix       = ""
        self.human              = None


    def selectedOptions(self, exporter):
        self.useTexFolder       = exporter.useTexFolder.selected
        self.eyebrows           = exporter.eyebrows.selected
        self.lashes             = exporter.lashes.selected
        self.helpers            = exporter.helpers.selected
        self.useTPose           = False # exporter.useTPose.selected
        self.scale,self.unit    = exporter.taskview.getScale()
        return self


    @property
    def subdivide(self):
        if not self.human:
            log.warning('No human set in config, disabled subdivision for export.')
            return False
        else:
            return self.human.isSubdivided()


    def setHuman(self, human):
        """
        Set the human object for this config.
        """
        self.human = human


    def getProxies(self):
        """
        Get the proxy list from the current state of the set human object.
        Proxy list will contain all proxy items such as proxy mesh and clothes,
        hair, eyes and cages.
        """
        if not self.human:
            return {}

        proxies = {}
        if self.human.hairProxy:
            proxy = self.human.hairProxy
            proxy.layer = 2
            name = self.goodName(proxy.name)
            proxies[name] = proxy

        if self.human.eyesProxy:
            proxy = self.human.eyesProxy
            proxy.layer = 2
            name = self.goodName(proxy.name)
            proxies[name] = proxy

        for (key,clo) in list(self.human.clothesObjs.items()):
            if clo:
                proxy = self.human.clothesProxies[key]
                proxy.layer = 3
                name = self.goodName(key)
                proxies[name] = proxy

        if self.human.proxy:
            proxy = self.human.proxy
            proxy.layer = 4
            name = self.goodName(proxy.name)
            proxies[name] = proxy

        if self.cage:
            obj = gui3d.app.selectedHuman
            filepath = mh.getSysDataPath("cages/cage/cage.mhclo")
            proxy = mh2proxy.readProxyFile(obj, filepath, type="Cage", layer=4)
            proxy.update(obj)
            proxies[name] = proxy

        return proxies


    def setupTexFolder(self, filepath):
        (fname, ext) = os.path.splitext(filepath)
        fname = self.goodName(os.path.basename(fname))
        self.outFolder = os.path.realpath(os.path.dirname(filepath))
        self.filename = os.path.basename(filepath)
        if self.useTexFolder:
            self.texFolder = self.getSubFolder(self.outFolder, "textures")
            self._copiedFiles = {}


    def getSubFolder(self, path, name):
        folder = os.path.join(path, name)
        print("Using folder", folder)
        if not os.path.exists(folder):
            log.message("Creating folder %s", folder)
            try:
                os.mkdir(folder)
            except:
                log.error("Unable to create separate folder:", exc_info=True)
                return None
        return folder


    def copyTextureToNewLocation(self, filepath):
        srcDir = os.path.abspath(os.path.expanduser(os.path.dirname(filepath)))
        filename = os.path.basename(filepath)

        print("CopyTex", srcDir)
        print("  ", filename)
        print("  ", self.useTexFolder, self.texFolder, end=' ')
        print("  ", self.outFolder)

        if self.useTexFolder:
            newpath = os.path.abspath( os.path.join(self.texFolder, filename) )
            print("New", newpath)
            try:
                self._copiedFiles[filepath]
                done = True
            except:
                done = False
            if not done:
                try:
                    shutil.copyfile(filepath, newpath)
                except:
                    log.message("Unable to copy \"%s\" -> \"%s\"" % (filepath, newpath))
                self._copiedFiles[filepath] = True
        else:
            newpath = filepath

        if not self.useRelPaths:
            return newpath
        else:
            relpath = os.path.relpath(newpath, self.outFolder)
            print("  Rel", relpath)
            return str(os.path.normpath(relpath))


    def goodName(self, name):
        string = name.replace(" ", "_").replace("-","_").lower()
        return string

#
#
#

def getExistingProxyFile(path, uuid, category):
    if not uuid:
        if not os.path.exists(os.path.realpath(path)):
            return None
        log.message("Found %s", path)
        return path
    else:
        file = os.path.basename(path)
        paths = []
        folder = os.path.join(mh.getPath(''), 'data', category)
        addProxyFiles(file, folder, paths, 6)
        folder = mh.getSysDataPath(category)
        addProxyFiles(file, folder, paths, 6)
        for path in paths:
            uuid1 = scanFileForUuid(path)
            if uuid1 == uuid:
                log.message("Found %s %s", path, uuid)
                return path
        return None


def addProxyFiles(file, folder, paths, depth):
    if depth < 0:
        return None
    try:
        files = os.listdir(folder)
    except OSError:
        return None
    for pname in files:
        path = os.path.join(folder, pname)
        if pname == file:
            paths.append(path)
        elif os.path.isdir(path):
            addProxyFiles(file, path, paths, depth-1)
    return


def scanFileForUuid(path):
    fp = open(path)
    for line in fp:
        words = line.split()
        if len(words) == 0:
            pass
        elif words[0] == 'uuid':
            fp.close()
            return words[1]
        elif words[0] == 'verts':
            break
    fp.close()
    return None

def scanFileForTags(path):
    tags = set()
    fp = open(path)
    for line in fp:
        words = line.split()
        if len(words) == 0:
            continue
        elif words[0] == 'tag':
            tags.add(words[1])
        else:
            break
    fp.close()
    return tags
