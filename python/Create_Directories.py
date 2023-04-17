import pathlib

#Define Main Directory
maindir = r'F:\raw-data\AIRS\V7_DAILY'

#Name strings of categories (e.g., catchment_names, variables, years) desrired for each path
catchment_names = ['Modi','Myagdi']
variables = ['Precip','Temp_max','Temp_min']
years = range(2002,2023)
sources = ['CHELSA','CHIRPS','GPM_IMERG']


[pathlib.Path(maindir+'/{}'.format(year)).mkdir(parents=True,exist_ok=True) for year in years]

#Use list comprehension for each category
[[[[pathlib.Path(maindir+'/{}/{}/{}/{}'.format(catchment,variable,year,source)).mkdir(parents=True,exist_ok=True)
for catchment in catchment_names] 
for variable in variables] 
for year in years]
for source in sources]

#Remove folder paths
[[[pathlib.Path(maindir+'/{}/{}/{}/CHRIPS'.format(catchment,variable,year)).rmdir()
for catchment in catchment_names] 
for variable in variables] 
for year in years]


#Formatting leading zeroes refresh
num=3
leading0_2 = '{:02}'.format(num)
leading0_3 = '{:03}'.format(num)
leading0_4 = '{:04}'.format(num)
