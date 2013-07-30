
// Create the skin material.
// This texture implements a SubSurface Scattering method
// using premade lightmaps.  
#ifndef (%%name%%_Material)                            

#declare TexMultiply_2x =
texture { // 2x multiplier layer.
        pigment { rgbf <2,2,2,1> }
        finish {
            specular 0
            phong 0
            ambient 0
            diffuse 0
        }
    }

#declare %%name%%_Texture =
    texture { // Red diffusion remover.
         pigment {image_map {png "%%name%%_sss_redlmap.png" interpolate 2}}
         finish {
            specular 0
            phong 0
            ambient -2
            diffuse 2
         }
    }
    texture { // Green diffusion remover.
         pigment {image_map {png "%%name%%_sss_greenlmap.png" interpolate 2 transmit all 1/2}}
         finish {
            specular 0
            phong 0
            ambient -2
            diffuse 2
         }
    }
    texture {TexMultiply_2x}    
    texture { // Blue diffusion remover.
         pigment {image_map {png "%%name%%_sss_bluelmap.png" interpolate 2 transmit all 1/2}}
         finish {
            specular 0
            phong 0
            ambient -2
            diffuse 2
         }
    }    
    texture { // Inverter.
        pigment { rgbf <-1,-1,-1,1> }
        finish {
            specular 0
            phong 0
            ambient 0
            diffuse 0
        }
    }
    texture {TexMultiply_2x} 
    texture { // Red SSS channel. High blur.
        pigment { image_map {png "%%name%%_sss_redlmap.png" interpolate 2 transmit all 1/2} }
        normal  {%%rednormal%%}
        finish { 
            specular 0
            roughness 0.01
            phong 0 phong_size 0
            ambient 0
            diffuse 2
            reflection {0}
            conserve_energy
        }
    }
    texture {TexMultiply_2x}
    texture { // Green SSS channel. Medium blur.
        pigment { image_map {png "%%name%%_sss_greenlmap.png" interpolate 2 transmit all 1/2} }
        normal  {%%greennormal%%}
        finish { 
            specular 6*%%edss%%  // EpiDermal Specularity Scattering.
            roughness 2*%%rough%%
            phong 0 phong_size 0
            ambient 0
            diffuse 2
            reflection {0}
            conserve_energy
        }
    }
    texture {TexMultiply_2x}
    texture { // Blue SSS channel. No blur.
        pigment { image_map {png "%%name%%_sss_bluelmap.png" interpolate 2 transmit all 1/2} }
        normal  {%%bluenormal%%}
        finish { 
            specular 0
            roughness 0.01
            phong 0 phong_size 0
            ambient 0
            diffuse 2
            reflection {0}
            conserve_energy
        }
    }
    texture {TexMultiply_2x}
    texture { // Ambience.
        pigment {rgbt <1, 1, 1, 1/2>}
        finish {
            specular 0
            roughness 0.01
            phong 0 phong_size 0
            ambient rgb 2*%%ambience%%
            diffuse 0
            reflection {0}
            conserve_energy
        }
    }
    texture {
        pigment {image_map {png "%%name%%_texture.png" filter all 1} }
        normal  {%%normal%%}
        finish { 
            specular %%spec%%
            roughness %%rough%%
            phong 0 phong_size 0
            ambient 0
            diffuse 0
            reflection {0}
            conserve_energy
        }
    }

#declare %%name%%_DiffuseTex =
    texture {
        pigment {image_map {png "%%name%%_texture.png"} }
        normal  {%%normal%%}
        finish { 
            specular %%spec%%
            roughness %%rough%%
            phong 0 phong_size 0
            ambient rgb %%ambience%%
            diffuse 1
            reflection {0}
            conserve_energy
        }
    }

#declare %%name%%_Material = material {
    texture {
        uv_mapping
        pigment_pattern {image_map {png "%%name%%_alpha.png" interpolate 2}}
        texture_map {
            [0 pigment {color transmit 1.0}]
            [1
                pigment_pattern {image_map {png "%%name%%_sss_alpha.png" interpolate 2}}
                texture_map {
                [0 %%name%%_DiffuseTex]
                [1 %%name%%_Texture]
                }
            ]
        }
    }
}

#end

                                                                            