# -*- mode: python -*-
VERSION="1.0alpha8"
import sys
import subprocess

def SvnInfo():
    import os
    import sys
    import re
    import subprocess
    import os.path

    def get_revision_svn_info():
        # Try getting svn revision by calling svn info (will only work in linux
        #  and windows where sliksvn is installed)
        output = subprocess.Popen(["svn","info","."], stdout=subprocess.PIPE, stderr=sys.stderr).communicate()[0]
        for line in output.splitlines():
            key, value = line.split(':', 1)
            if key.strip().lower() == 'revision':
                return value.strip()
        raise RuntimeError("revision not found in 'svn info .' output")

    def get_revision_entries():
        # First fallback: try to parse the entries file manually
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        svndir = os.path.join(scriptdir,'.svn')
        entriesfile = os.path.join(svndir,'entries')
        entries = open(entriesfile, 'r').read()
        result = re.search(r'dir\n(\d+)\n',entries)
        output = result.group(1)
        if not output:
            raise RuntimeError("revision not found in 'entries' file")
        return output

    def get_revision_pysvn():
        # The following only works if pysvn is installed. We'd prefer not to use this since it's very slow.
        # It was taken from this stackoverflow post:
        # http://stackoverflow.com/questions/242295/how-does-one-add-a-svn-repository-build-number-to-python-code
        import pysvn
        repo = "."
        rev = pysvn.Revision( pysvn.opt_revision_kind.working )
        client = pysvn.Client()
        info = client.info2(repo,revision=rev,recurse=False)
        output = format(str(info[0][1].rev.number))
        return output

    def get_revision_file():
        # Default fallback to use if we can't figure out SVN revision in any other
        # way: Use this file's svn revision.
        pattern = re.compile(r'[^0-9]')
        return pattern.sub("", "$Revision: 5414 $")

    def get_svn_revision_1():
        svnrev = None

        try:
            svnrev = get_revision_svn_info()
            os.environ['SVNREVISION_SOURCE'] = "svn info command"
            return svnrev
        except Exception as e:
            print >> sys.stderr,  "NOTICE: Failed to get svn version number from command line: " + format(str(e)) + " (This is just a head's up, not a critical error)"

        try:
            svnrev = get_revision_entries()
            os.environ['SVNREVISION_SOURCE'] = "entries file"
            return svnrev
        except Exception as e:
            print >> sys.stderr,  "NOTICE: Failed to get svn version from file: " + format(str(e)) + " (This is just a head's up, not a critical error)"

        try:
            svnrev = get_revision_pysvn()
            os.environ['SVNREVISION_SOURCE'] = "pysvn"
            return svnrev
        except Exception as e:
            print >> sys.stderr,  "NOTICE: Failed to get svn version number using pysvn: " + format(str(e)) + " (This is just a head's up, not a critical error)"

        print >> sys.stderr,  "NOTICE: Using SVN rev from file stamp. This is likely outdated, so the number in the title bar might be off by a few commits."
        svnrev = get_revision_file()
        os.environ['SVNREVISION_SOURCE'] = "approximated from file stamp"
        return svnrev
    
    return get_svn_revision_1()

VERSION="%s (%s)" % (VERSION,SvnInfo())
vfile = open(os.path.join("core","VERSION"),"w")
vfile.write(VERSION)
vfile.close()

###COMPILE TARGETS
try:
    subprocess.check_call(["python","compile_targets.py"])
except subprocess.CalledProcessError:
    print "check that compile_targets.py is working correctly"
    sys.exit(1)

a = Analysis(['makehuman.py'],
             pathex=['lib','core','shared','apps','apps/gui', 'plugins'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None
             )

##### include mydir in distribution #######
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
#        if mydir == 'data' and f.endswith(".target"):
#            print "skipping %s" % f
#        else:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
###########################################

# append all of our necessary subdirectories
a.datas += extra_datas('data')
a.datas += extra_datas('lib')
a.datas += extra_datas('core')
a.datas += extra_datas('shared')
a.datas += extra_datas('apps')
a.datas += extra_datas('plugins')
a.datas += extra_datas('tools')
a.datas += extra_datas('utils')
a.datas += extra_datas('icons')
#a.datas += extra_datas('qt_menu.nib')

pyz = PYZ(a.pure)
if sys.platform == 'darwin':
    exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='makehuman',
          debug=False,
          strip=None,
          upx=False,
          console=False )
    coll = COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=None,
        upx=True,
        name='makehuman')
    app = BUNDLE(coll,
        name='MakeHuman.app',
        icon='icons/makehuman.icns')
    if os.path.exists(os.path.join("dist","MakeHuman.dmg")):
        os.remove(os.path.join("dist","MakeHuman.dmg"))
    subprocess.check_call(["hdiutil","create","dist/MakeHuman.dmg","-srcfolder","dist/MakeHuman.app","-volname","'MakeHuman for Mac OS X'"])
        
elif sys.platform == 'win32':
    exe = EXE(pyz,
        a.scripts,
        exclude_binaries=True,
        name='makehuman.exe',
        debug=False,
        strip=None,
        upx=True,
        console=False )
    coll = COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=None,
        upx=True,
        name='makehuman')
        
os.remove(os.path.join("core","VERSION"))
