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

MHX materials
"""

import os
import log

from . import mhx_drivers

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def writeTexture(fp, filepath, prefix, channel, env):
    texname = prefix+"_"+channel
    imgname = os.path.basename(filepath)
    newpath = env.config.copyTextureToNewLocation(filepath)
    newpath = newpath.replace("\\","/")
    fp.write(
        "Image %s\n" % imgname +
        "  Filename %s ;\n" % newpath +
        "  use_premultiply True ;\n" +
        "end Image\n\n"+
        "Texture %s IMAGE\n" % texname +
        "  Image %s ;\n" % imgname)
    if channel == "normal":
        fp.write("    use_normal_map True ;\n")
    fp.write(
        "end Texture\n\n")
    return texname


def writeTextures(fp, mat, prefix, env):
    prefix = prefix.replace(" ", "_")
    diffuse,spec,bump,normal,disp = None,None,None,None,None
    if mat.diffuseTexture:
        diffuse = writeTexture(fp, mat.diffuseTexture, prefix, "diffuse", env)
    if mat.specularMapTexture:
        spec = writeTexture(fp, mat.specularMapTexture, prefix, "spec", env)
    if mat.bumpMapTexture:
        bump = writeTexture(fp, mat.bumpMapTexture, prefix, "bump", env)
    if mat.normalMapTexture:
        normal = writeTexture(fp, mat.normalMapTexture, prefix, "normal", env)
    if mat.displacementMapTexture:
        disp = writeTexture(fp, mat.displacementMapTexture, prefix, "disp", env)
    return diffuse,spec,bump,normal,disp


def writeMTexes(fp, texnames, mat, slot, env):
    diffuse,spec,bump,normal,disp = texnames
    scale = env.config.scale

    if diffuse:
        fp.write(
            "  MTex %d %s UV COLOR\n" % (slot, diffuse) +
            "    texture Refer Texture %s ;" % diffuse +
"""
    use_map_color_diffuse True ;
    use_map_translucency True ;
    use_map_alpha True ;
    alpha_factor 1 ;
    diffuse_color_factor 1.0 ;
    translucency_factor 1.0 ;
  end MTex

""")
        slot += 1

    if spec:
        fp.write(
            "  MTex %d %s UV SPECULAR_COLOR\n" % (slot, spec) +
            "    texture Refer Texture %s ;\n" % spec +
            "    specular_factor %.4g ;" % (0.1*mat.specularIntensity) +
"""
    use_map_color_diffuse False ;
    use_map_specular True ;
    use_map_reflect True ;
    reflection_factor 1 ;
  end MTex

""")
        slot += 1

    if bump:
        fp.write(
            "  MTex %d %s UV NORMAL\n" % (slot, bump) +
            "    texture Refer Texture %s ;\n" % bump +
            "    normal_factor %.4g*theScale ;" % (0.1*scale*mat.bumpMapIntensity) +
"""
    use_map_color_diffuse False ;
    use_map_normal True ;
    use_rgb_to_intensity True ;
    end MTex
""")
        slot += 1

    if normal:
        fp.write(
            "  MTex %d %s UV NORMAL\n" % (slot, normal) +
            "    texture Refer Texture %s ;\n" % normal +
            "    normal_factor %.4g*theScale ;" % (0.1*scale*mat.normalMapIntensity) +
"""
    use_map_color_diffuse False ;
    use_map_normal True ;
    use_rgb_to_intensity True ;
    end MTex
""")
        slot += 1

    if disp:
        fp.write(
            "  MTex %d %s UV DISPLACEMENT\n" % (slot, disp) +
            "    texture Refer Texture %s ;\n" % disp +
            "    displacement_factor %.4g*theScale ;" % (0.1*scale*mat.displacementMapIntensity) +
"""
    use_map_color_diffuse False ;
    use_map_normal True ;
    use_rgb_to_intensity True ;
    end MTex
""")
        slot += 1


def writeMaterialSettings(fp, mat, alpha, env):
    log.debug("%s %s %s" % (mat.specularColor, mat.specularIntensity, mat.specularHardness))
    fp.write(
        "  diffuse_color Array %.4g %.4g %.4g  ;\n" % mat.diffuseColor.asTuple() +
        "  diffuse_shader 'LAMBERT' ;\n" +
        "  diffuse_intensity %.4g ;\n" % mat.diffuseIntensity +
        "  specular_color Array %.4g %.4g %.4g ;\n" % mat.specularColor.asTuple() +
        "  specular_shader 'PHONG' ;\n" +
        "  specular_intensity %.4g ;\n" % (0.1*mat.specularIntensity) +
        "  specular_hardness %.4g ;\n" % mat.specularHardness)

    if alpha < 0.99:
        fp.write(
            "  use_transparency True ;\n" +
            "  transparency_method 'Z_TRANSPARENCY' ;\n" +
            "  alpha %3.f ;\n" % alpha +
            "  specular_alpha %.3f ;\n" % alpha)

    fp.write(
"""
  use_cast_approximate True ;
  use_cast_buffer_shadows True ;
  use_cast_shadows_only False ;
  use_ray_shadow_bias True ;
  use_shadows True ;
  use_transparent_shadows True ;
  use_raytrace True ;
""")


def writeMaterials(fp, env):
    config = env.config
    human = env.human
    mat = human.material

    if human.uvset:
        writeMultiMaterials(fp, env)
        return

    texnames = writeTextures(fp, mat, env.name, env)

    fp.write("""
Texture solid IMAGE
end Texture

""")
    if config.useMasks:
        prxList = list(env.proxies.values())
        for prx in prxList:
            if prx.mask:
                addMaskImage(fp, env, prx.mask)

    fp.write(
        "# --------------- Materials ----------------------------- #\n\n" +
        "Material %sSkin\n" % env.name)

    nMasks = writeMaskMTexs(fp, env)
    writeMTexes(fp, texnames, mat, nMasks, env)
    writeMaterialSettings(fp, mat, 0, env)

    fp.write(
"""
  SSS
    use True ;
    back 2 ;
    color Array 0.782026708126 0.717113316059 0.717113316059  ;
    color_factor 0.750324 ;
    error_threshold 0.15 ;
    front 1 ;
    ior 1.3 ;
    radius Array 4.82147502899 1.69369900227 1.08997094631  ;
""" +
"    scale %.4g*theScale ;" % (0.01*config.scale) +
"""
    texture_factor 0 ;
  end SSS
  Property MhxDriven True ;
""")

    writeMaterialAnimationData(fp, nMasks, 2, env)
    fp.write("end Material\n\n")

    fp.write("Material %sShiny\n" % env.name)
    nMasks = writeMaskMTexs(fp, env)
    shinyTexnames = texnames[0],None,None,None,None
    writeMTexes(fp, shinyTexnames, mat, nMasks, env)

    fp.write(
"""
  diffuse_color Array 1.0 1.0 1.0  ;
  diffuse_shader 'LAMBERT' ;
  diffuse_intensity 1.0 ;
  specular_color Array 1.0 1.0 1.0  ;
  specular_shader 'PHONG' ;
  specular_intensity 1.0 ;
  alpha 0 ;
  specular_alpha 0 ;
  specular_hardness 369 ;
  specular_ior 4 ;
  specular_slope 0.1 ;
  transparency_method 'Z_TRANSPARENCY' ;
  use_cast_buffer_shadows False ;
  use_cast_shadows_only False ;
  use_raytrace True ;
  use_shadows True ;
  use_transparency True ;
  use_transparent_shadows True ;
""")

    writeMaterialAnimationData(fp, nMasks, 1, env)
    fp.write("end Material\n\n")

    writeSimpleMaterial(fp, "Invisio", env, (1,1,1))
    writeSimpleMaterial(fp, "Red", env, (1,0,0))
    writeSimpleMaterial(fp, "Green", env, (0,1,0))
    writeSimpleMaterial(fp, "Blue", env, (0,0,1))
    writeSimpleMaterial(fp, "Yellow", env, (1,1,0))
    return

#-------------------------------------------------------------------------------
#   Simple materials: red, green, blue
#-------------------------------------------------------------------------------

def writeSimpleMaterial(fp, name, env, color):
    fp.write(
        "Material %s%s\n" % (env.name, name) +
        "  diffuse_color Array %s %s %s  ;" % (color[0], color[1], color[2]))

    fp.write("""
  use_shadeless True ;
  use_shadows False ;
  use_cast_buffer_shadows False ;
  use_raytrace False ;
  use_transparency True ;
  transparency_method 'Z_TRANSPARENCY' ;
  alpha 0 ;
  specular_alpha 0 ;
end Material
""")

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def writeMaterialAnimationData(fp, nMasks, nTextures, env):
    fp.write("  use_textures Array")
    for n in range(nMasks):
        fp.write(" 1")
    for n in range(nTextures):
        fp.write(" 1")
    fp.write(" ;\n")
    fp.write("  AnimationData %sMesh True\n" % env.name)
    #mhx_drivers.writeTextureDrivers(fp, rig_panel.BodyLanguageTextureDrivers)
    writeMaskDrivers(fp, env)
    fp.write("  end AnimationData\n")


def writeMaskMTexs(fp, env):
    nMasks = 0
    if env.config.useMasks:
        prxList = list(env.proxies.values())
        for prx in prxList:
            if prx.mask:
                nMasks = addMaskMTex(fp, prx.mask, None, 'MULTIPLY', nMasks)
    return nMasks


def writeMaskDrivers(fp, env):
    if not env.config.useMasks:
        return
    fp.write("#if toggle&T_Clothes\n")
    n = 0
    for prx in env.proxies.values():
        if prx.type == 'Clothes' and prx.mask:
            (dir, file) = prx.mask
            mhx_drivers.writePropDriver(fp, env, ["Mhh%s" % prx.name], "1-x1", 'use_textures', n)
            n += 1
    fp.write("#endif\n")
    return

#-------------------------------------------------------------------------------
#   Multi materials
#-------------------------------------------------------------------------------

TX_SCALE = 1
TX_BW = 2

TexInfo = {
    "diffuse" :     ("COLOR", "use_map_color_diffuse", "diffuse_color_factor", 0),
    "specular" :    ("SPECULAR", "use_map_specular", "specular_factor", TX_BW),
    "alpha" :       ("ALPHA", "use_map_alpha", "alpha_factor", TX_BW),
    "translucency": ("TRANSLUCENCY", "use_map_translucency", "translucency_factor", TX_BW),
    "bump" :        ("NORMAL", "use_map_normal", "normal_factor", TX_SCALE|TX_BW),
    "displacement": ("DISPLACEMENT", "use_map_displacement", "displacement_factor", TX_SCALE|TX_BW),
}

def writeMultiMaterials(fp, env):
    config = env.config
    uvset = env.human.uvset

    for mat in uvset.materials:
        for tex in mat.textures:
            name = os.path.basename(tex.file)
            fp.write("Image %s\n" % name)
            newpath = config.copyTextureToNewLocation(tex)
            fp.write(
                "  Filename %s ;\n" % newpath +
#                "  alpha_mode 'PREMUL' ;\n" +
                "end Image\n\n" +
                "Texture %s IMAGE\n" % name +
                "  Image %s ;\n" % name +
                "end Texture\n\n")

        fp.write("Material %s_%s\n" % (env.name, mat.name))
        alpha = False
        for (key, value) in mat.settings:
            if key == "alpha":
                alpha = True
                fp.write(
                "  use_transparency True ;\n" +
                "  use_raytrace False ;\n" +
                "  use_shadows False ;\n" +
                "  use_transparent_shadows False ;\n" +
                "  alpha %s ;\n" % value)
            elif key in ["diffuse_color", "specular_color"]:
                fp.write("  %s Array %s %s %s ;\n" % (key, value[0], value[1], value[2]))
            elif key in ["diffuse_intensity", "specular_intensity"]:
                fp.write("  %s %s ;\n" % (key, value))
        if not alpha:
            fp.write("  use_transparent_shadows True ;\n")

        n = 0
        for tex in mat.textures:
            name = os.path.basename(tex.file)
            if len(tex.types) > 0:
                (key, value) = tex.types[0]
            else:
                (key, value) = ("diffuse", "1")
            (type, use, factor, flags) = TexInfo[key]
            diffuse = False
            fp.write(
                "  MTex %d %s UV %s\n" % (n, name, type) +
                "    texture Refer Texture %s ;\n" % name)
            for (key, value) in tex.types:
                (type, use, factor, flags) = TexInfo[key]
                if flags & TX_SCALE:
                    scale = "*theScale"
                else:
                    scale = ""
                fp.write(
                "    %s True ;\n" % use +
                "    %s %s%s ;\n" % (factor, value, scale))
                if flags & TX_BW:
                    fp.write("    use_rgb_to_intensity True ;\n")
                if key == "diffuse":
                    diffuse = True
            if not diffuse:
                fp.write("    use_map_color_diffuse False ;\n")
            fp.write("  end MTex\n")
            n += 1
        fp.write("end Material\n\n")

#-------------------------------------------------------------------------------
#   Masking
#-------------------------------------------------------------------------------

def addMaskImage(fp, env, filepath):
    newpath = env.config.copyTextureToNewLocation(filepath)
    filename = os.path.basename(filepath)
    fp.write(
        "Image %s\n" % filename +
        "  Filename %s ;\n" % newpath +
        #"  alpha_mode 'PREMUL' ;\n" +
        "end Image\n\n" +
        "Texture %s IMAGE\n" % filename  +
        "  Image %s ;\n" % filename +
        "end Texture\n\n"
    )


def addMaskMTex(fp, filepath, proxy, blendtype, n):
    if proxy:
        try:
            uvLayer = proxy.uvtexLayerName[proxy.maskLayer]
        except KeyError:
            return n

    filename = os.path.basename(filepath)
    fp.write(
"  MTex %d %s UV ALPHA\n" % (n, filename) +
"    texture Refer Texture %s ;\n" % filename +
"    use_map_alpha True ;\n" +
"    use_map_color_diffuse False ;\n" +
"    alpha_factor 1 ;\n" +
"    blend_type '%s' ;\n" % blendtype +
"    mapping 'FLAT' ;\n" +
"    invert True ;\n" +
"    use_stencil True ;\n" +
"    use_rgb_to_intensity True ;\n")
    if proxy:
        fp.write("    uv_layer '%s' ;\n" %  uvLayer)
    fp.write("  end MTex\n")
    return n+1

