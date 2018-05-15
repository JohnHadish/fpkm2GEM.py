import os
import pandas as pd
import re

#Test names_file
# names_file = './Trial_Names'

#modify this parameter to your working dir
start_dir = '/scidas/arabidopsis/ath_PRJNA412447/sra2gev/'

#Test start_dir
# start_dir = './'

# Names file should be 2 column tab deliminated file with Run number in column
# one and run name in column 2
names_file = '/scidas/arabidopsis/ath_PRJNA412447/sra2gev/PRJNA412447_Names.csv'


# This is what you want your ematrix to be called at the end. You can select
# file path as well if you so desire.
ematrix_name = "GEM.txt"


os.chdir(start_dir)

#Finds all .fpkm files within the directory
fpkm_files = []
for root, dirs, files in os.walk(start_dir):
    #This causes our program to ignore the 'work' folder, so that we do not get
    #duplicates of each file.
    dirs[:] = [d for d in dirs if d not in 'work']
    for file in files:
        if file.endswith(".fpkm"):
            fpkm_files.append(os.path.join(root, file))

#This makes the actual ematrix (minus the names of each column)
ematrix = pd.DataFrame({'gene':[]})
for fpkm in fpkm_files:
    file_basename = os.path.basename(fpkm)
    run_name = file_basename.split('_vs_')[0]
    df = pd.read_csv(fpkm
                    , header=None
                    , sep='\t'
                    , names=["gene", run_name]
                    )
    df.drop_duplicates(['gene'], inplace=True)

    ematrix = ematrix.merge(df.iloc[:,[0,1]], on='gene', how='outer')

print(ematrix.head())


#Sets gene as the names of each row
ematrix = ematrix.set_index('gene')
#Rename the ematrix:
names_file = pd.read_csv(names_file
               , header=None
               , sep='\t')
names_dict = names_file.set_index(0).to_dict()
print(names_dict)
#I did this command becasue the column remap was not working with dictionary for some reason
#pandas glitch or something
ematrix.columns = ematrix.columns.to_series().map(names_dict[1])
ematrix = ematrix.reindex(sorted(ematrix.columns), axis=1)
#This exports our ematrix
ematrix.to_csv(ematrix_name, sep = '\t', na_rep="NA")
