#!/usr/bin/env python
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

import sys
sys.path = ["./core", "./lib"] + sys.path
import algos3d
import os
import zipfile
import fnmatch

def getAllFiles(rootPath, filterStrArr):
    result = [ None ]*len(filterStrArr)
    for root, dirnames, filenames in os.walk(rootPath):
        for i, filterStr in enumerate(filterStrArr):
            if not result[i]:
                result[i] = []
            result[i].extend(getFiles(root, filenames, filterStr))
    return result

def getFiles(root, filenames, filterStr):
    foundFiles = []
    for filename in fnmatch.filter(filenames, filterStr):
        foundFiles.append(os.path.join(root, filename))
    return foundFiles


if __name__ == '__main__':
    obj = algos3d.Target(None, None)
    allFiles = getAllFiles('data', ['*.target', '*.png'])
    with zipfile.ZipFile('data/targets.npz', mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        allTargets = allFiles[0]
        print((len(allFiles)))
        for (i, path) in enumerate(allTargets):
            try:
                obj._load_text(path)
                iname, vname = obj._save_binary(path)
                zip.write(iname)
                zip.write(vname)
                os.remove(iname)
                os.remove(vname)
                print(("[%.0f%% done] converted target %s" % (100*(float(i)/float(len(allTargets))), path)))
            except Exception as e:
                print(('error converting target %s' % path))

    print("Writing images list")
    with open('data/images.list', 'w') as f:
        allImages = allFiles[1]
        for path in allImages:
            path = path.replace('\\','/')
            f.write(path + '\n')
    print("All done.")
