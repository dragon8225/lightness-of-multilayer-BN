# lightness-of-multilayer-BN
 lightness
twisted BN Second Harmonic Generation (SHG) Formula:

  E₍x,2ω₎ = iω/(cn(2ω)) · χ · E₍x,ω₎² · ∫₀ᵀ e^(–iΔk·z) cos(3θ(z)) dz
  
  E₍y,2ω₎ = iω/(cn(2ω)) · χ · E₍x,ω₎² · ∫₀ᵀ e^(–iΔk·z) sin(3θ(z)) dz

In the code calculations, the overall term iω/(cn(2ω)) · χ · E₍x,ω₎² is set to 1, Δk is fixed at 1, and the total thickness T is expressed in units of Lc (with Lc set to π). All angles θ are in radians.

Quasi-Phase Matching (QPM) Field Strength:

  E₍x,2ω₎ = iω/(cn(2ω)) · χ · E₍x,ω₎² · [2/(iΔk) · N + 1/(iΔk) · (1 – e^(–iΔk·t))]

Here, N is the integer part of the total thickness (i.e., an integer multiple of Lc) and t is the fractional part of the total thickness.

Code Structure:

global_optimized

  This module implements the method for finding the global optimum by following the approach introduced in the repository:
  
  https://github.com/ki-ljl/pso
  
  Parameters can be modified inside the main function. 
  
  If you need to fix the thickness per layer, simply set t_min = t_max to the desired fixed value.

Lightness

  This module calculates the light intensity given the layer-by-layer thickness and angle information.
  
  If you wish to output the intensity for each layer, change the return statement in the corresponding function from "return I[-1]" to "return I".

Quasi_phasematching

  This module computes the quasi-phase matching field strength for a given total thickness.

For more complex plotting or further calculations, you can create a new file. Then import the GO class from the global_optimized module and the Light class from the Lightness module as needed. Please refer to the demo file for usage examples.

