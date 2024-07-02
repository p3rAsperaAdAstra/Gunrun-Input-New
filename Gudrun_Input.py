from glob import glob
import re
import os
import numpy as np
from datetime import datetime

'''This script automatically creates an input file for GudRunX.'''

cwd = os.path.abspath(os.getcwd()) # need the script location for some reason?
background = 'BACKGROUND.xy' # FIXED NAME FOR BACKGROUND.xy FILE! RENAME IN YOUR DIRECTORY IF IT HAS A DIFFERENT NAME!!
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%Y%m%d %H:%M:%S')
input_txt = 'Input.txt'


# Check for BACKGROUND.xy
assert os.path.exists(background), f"YOU NEED TO HAVE A BACKGROUND FILE CALLED BACKGROUND.xy! Stopping execution."

# Dict containing settings that are edited using string replace in the template file string. 
# can be extended in the future if necessary/useful.
settings = {'START':{'RUNDIR':cwd,
                     'XRAY_CROSS_SECTION_FILE':r'StartupFiles\Xray\CrossSec_XCOM.txt',
                     'XRAY_FORM_FACTOR':r'StartupFiles\Xray\f0_WaasKirf.txt',
                     'XRAY_COMPTON_SCATTERING_FILE':r'StartupFiles\Xray\CrossSec_Compton_Balyuzi.txt',
                     'BACKGROUND':background},
            'END':{'DATETIME':formatted_datetime}}

# Moving the template file to the script itself. it's not that long.
template_string_start = r''''  '  '          '  '\'

INSTRUMENT          {

XPDF                                                    Instrument name
###RUNDIR###                                            Gudrun input file directory:
###RUNDIR###                                            Data file directory
xy                                                      Data file type
####XRAY_CROSS_SECTION_FILE###                          X-ray cross sections file
###XRAY_FORM_FACTOR###                                  X-ray form factor file
###XRAY_COMPTON_SCATTERING_FILE###                      X-ray Compton scattering file
0.5  23.  0.02                                          Q-range [1/Å] for final DCS
50  0.02                                                r-max and r-step for final g(r)

}

BEAM          {

CYLINDRICAL                      Sample geometry
2                                Number of beam profile values
1.0  1.0                         Beam profile values (Maximum of 50 allowed currently)
0.0020  0.0100  100              Step size for absorption and m.s. calculation and no. of slices
5                                Step in scattering angle to calculate corrections at: [deg.]          
-0.035  0.035  -0.7  0.7         Incident beam edges relative to centre of sample [cm]
-0.035  0.035  -0.7  0.7         Scattered beam edges relative to centre of sample [cm]
*                                File containing bremsstrahlung intensity
0                                Density of target material [gm/cm^3] 
0                                Effective target penetration depth [cm] 
Na                               K-beta filter 
0                                K-beta filter density [gm/cm^3] 
0                                K-beta filter thickness [cm] 
0                                Bremsstrahlung power 
0                                Detector cutoff [keV]
0                                Cutoff width [keV] 
*                                Lowest scattering angle
*                                Highest scattering angle
*                                Scattering angle step
0.0                              Angle offset [deg.] 
*                                Anode material:
*                                Tube voltage [kV]
0.20741                          Wavelength [A]:
0                                Theta-theta scanning?
0                                Fixed slits?
0.0  0.0  -1.0                   Footprint length, sample thickness, and depression (all relative to sample dimension):
0.0  0.0  -1.0                   Position, width and power for low angle cutoff [deg]: 
*                                Tube current [mA]
*                                kAlpha1 [A] 
*                                kAlpha2 [A] 
*                                kBeta [A] 
0.0  0.00                        kAlpha2 and kBeta relative intensities:  
0.0                              Bremsstrahlung scattering amplitude
0                                No. of bremsstrahlung iterations

}

NORMALISATION          {

0.0        Azimuthal angle of detector above scattering plane:
0          Divide by <F>^2? 
2          Power for Breit-Dirac factor (2 -3) 
1          Krogh-Moe & Norman normalisation
0.0        Overlap factor

}

SAMPLE BACKGROUND          {

1                      Number of  files
###BACKGROUND###       SAMPLE BACKGROUND data files
1                      Sample background factor 
1.0                    Data factor
0                      Exclude scans

}

'''

template_string_sample = '''SAMPLE ###SAMPLENAME###          {

1                                             Number of files
###SAMPLENAME###.xy                           ###SAMPLENAME### data files
1                                             Force calculation of sample corrections?
Element  Atom  1.0  0.0  0.0                  Composition
*  0  0  0  0                                 * 0 0 0 0 to specify end of composition input
SameAsBeam                                    Geometry
0.04  0.05                                    Inner and outer radii (cm)
5                                             Sample height (cm)
1.2422                                        Density Units:  gm/cm^3?
TABLES                                        Total cross section source
2.0                                           Tweak factor
0.7                                           Top hat width (1/Å) for cleaning up Fourier Transform
0.958                                         Minimum radius for Fourier Transform [Å]
0.08                                          Width of broadening in r-space [A]
0  0                                          0   0          to finish specifying wavelength range of resonance
0.0  0.0  1.0                                 Exponential amplitude, decay [?] and stretch
1.066989e-04                                  Sample calibration factor
5                                             No. of iterations
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0           Fluorescence levels
1.0                                           Factor to modify multiple scattering (0 - 1)
-0.8                                          Incident beam polarization factor (-1 -> +1)
1.0                                           Factor for Compton scattering
0.0                                           Bremsstrahlung scattering amplitude
0                                             No. of bremsstrahlung iterations
0                                             Broadening power
0.0  0.00                                     kAlpha2 and kBeta relative intensities:  
1.0                                           Data factor
0                                             Analyse this sample? 
0                                             Exclude scans

}

GO

'''

# final part of the input file.
template_string_end = '''END          
1
Date and time last written:  ###DATETIME###          
X'''


# substitute placeholders in template_string parts 
for setting in settings['START']: # substitute settings in template_string_start 
    placeholder, value = f'###{setting}###', settings['START'][setting]
    template_string_start = template_string_start.replace(placeholder,value)

for setting in settings['END']: # substitute settings in template_string_end 
    placeholder, value = f'###{setting}###', settings['END'][setting]
    template_string_end = template_string_end.replace(placeholder,value)


# construct input file
samples = glob('*.xy') # find all input xy files
samples.remove(background) # remove background file from all .xy files.

input_file = ''
input_file += template_string_start

for sample in samples:
    sample_name = os.path.splitext(os.path.basename(sample))[0]
    new_sample_string = template_string_sample.replace('###SAMPLENAME###',sample_name)
    input_file += new_sample_string

input_file += template_string_end

# input.txt ready to be written to text file.
if not os.path.exists('runflag.stat'): # avoid overwrite the existing input file
    with open(input_txt, 'w', encoding='utf8') as outf: outf.write(input_file)


syspar_string = fr'''bin\calc_corrsx_in_out.exe;
bin\tophatsub.exe;
bin\gnuplot\binary\wgnuplot.exe;
bin\gnuplot\binary\wgnuplot.exe -persist GNUplot.plt;
{os.path.realpath(input_txt)};'''

########## Need to also write the GudrunX_windows.syspar file. Required for Java??
with open('GudrunX_windows.syspar', 'w', encoding='utf8') as outf: outf.write(syspar_string)