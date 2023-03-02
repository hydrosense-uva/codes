import glob,os

txt_directory = r'F:\raw-data\AIRS'
txt_files = sorted(list(glob.glob(txt_directory+r'\*.txt')))

new_files = ['/AIRS_standard_7.0_{}.txt'.format(year) for year in range(2002,2023)]


#For New File per Group of .TXT Lines in Single File
for writefile, year in zip(new_files,range(2002,2023)):
    open(txt_directory+writefile,'w').writelines([ line for line in open(txt_files[0]) if ('.{}.'.format(year) in line)])



#For New File per Read File
for readfile,writefile in zip(txt_files,new_files):
    open(txt_directory+writefile,'w').writelines([ line for line in open(readfile) if ('.nc' in line)])

