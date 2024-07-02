from glob import glob
import re
import os
import numpy as np

'''Create the GudrunX input file'''

#get the current working directory
cwd = os.getcwd()
print(cwd)
#find all input xy files
samples = glob('*.xy')
background = 'BACKGROUND.xy'
samples.remove(background)

#open the template file
with open('TEMPLATE.txt', 'r') as inp:
    string = inp.read()
    #print(string)

instr_string = re.search(r'(?s)INSTRUMENT.*?}\n', string).group() #read in the instrument string
beam_string = re.search(r'(?s)BEAM.*?}\n', string).group() #read in the beam string
norm_string = re.search(r'(?s)NORMALISATION.*?}\n', string).group() #read in the normalization string
background_string = re.search(r'(?s)SAMPLE BACKGROUND.*?}\n', string).group() #read in the background string
sample_string = re.search(r'(?s)SAMPLE TEMPLATE.*?GO\n', string).group() #read in the sample string

sample_strings = '' #initializing the sample strings
#create string for each sample
for sample in samples:
    #print(sample)
    sample_name = sample.split('.')[0] #find sample name
    #print(sample_name)
    new_sample_string = re.sub('TEMPLATE', sample_name, sample_string) #substitute the TEMPLATE with name of sample
    #print(new_sample_string)
    sample_strings += (new_sample_string + '\n') #collect the sample strings

if bool(glob('runflag.stat')) is False: #avoid overwrite the existing input file
    #write the input txt
    with open('Input.txt', 'w', encoding='utf8') as inp:
        string = string.replace('Directory', cwd) #replace Directory with current working directory in the read in string
        new_strings = string.replace(sample_string, sample_strings) #replace sample string with collected samples strings in the read in string
        #print(new_strings)
        inp.write(new_strings) #write down with the new strings

#write the leading file for jave program of GundrunX
with open('GudrunX_windows.syspar', 'w') as inp:
    inp.write(r'bin\calc_corrsx_in_out.exe;\nbin\\tophatsub.exe;\nbin\gnuplot\\binary\wgnuplot.exe;\nbin\gnuplot\\binary\wgnuplot.exe -persist GNUplot.plt;\n' + os.path.realpath('Input.txt') + ';') #write down the directories
    print(os.listdir())

print(os.listdir())