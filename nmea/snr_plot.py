import os, sys
import glob
import pandas as pd
import matplotlib.pyplot as plt

# get file in current directory
file_glob = [os.path.basename(r) for r in glob.glob('./*')]

# get satelinte_number_file 1~100
for i in range(1, 100):
    plot_dict = {}
    print(i)
    grep = '_' + str(i) + '.log'
    for read_file in file_glob:
    # search satelite number log
        if(read_file.find(str(grep))) >= 0:
        # search date
            if(read_file.find('20170821')) >= 0:
                df_21 = pd.read_csv(read_file, header=None)
                plot_dict['821'] = df_21
                plt.plot(df_21[0], df_21[4], label='821 3m', color='blue', alpha=0.7)
            elif(read_file.find('20170822')) >= 0:
                df_22 = pd.read_csv(read_file, header=None)
                plot_dict['822'] = df_22
                plt.plot(df_22[0], df_22[4], label='822 3m', color='green', alpha=0.7)
            elif(read_file.find('20170823')) >= 0:
                df_23 = pd.read_csv(read_file, header=None)
                plot_dict['823'] = df_23
                plt.plot(df_23[0], df_23[4], label='823 5m', color='red', alpha=0.7)
            elif(read_file.find('20170901')) >= 0:
                df_1 = pd.read_csv(read_file, header=None)
                plt.plot(df_1[0], df_1[4], label='901 3m', color='cyan', alpha=0.7)
                plot_dict['901'] = df_1
        else:
            pass
    # plot if directory is not empty( no data )
    if( len(plot_dict) != 0 ): 
        plt.legend()
        plt.savefig(str(i) + '.png')
        plt.show()
    else:
        print('No data')
        pass
