import os, sys
import glob
import pandas as pd
import matplotlib.pyplot as plt
import nmea

path = os.path.dirname(os.path.abspath(__file__))
fnames = [os.path.basename(r) for r in glob.glob('./*')]
print(fnames)

words = ['GPGGA', 'GPRMC', 'GPVTG', 'GPZDA', 'GPGSA', 'GLGSA', 'PSAT']
gsv_names = ['GLGSV', 'GPGSV']

filename = os.path.basename(sys.argv[1])
read_file, ext  = os.path.splitext(filename)
del_cs = nmea.delete_checksum(path, filename, read_file)

for word in words:
    nmea.log_filter(path, read_file, word)
for gsv_name in gsv_names:
    nmea.gsv_filter(path, read_file, gsv_name)

fnames = [os.path.basename(r) for r in glob.glob('./*')]
print(fnames)

for fname in fnames:
    if os.path.getsize(path + '/' +  fname) == 0:
        try:
            os.remove(path + '/' + fname)
        except PermissionError :
            pass


read_log = nmea.read_log()
nmea_parse = nmea.nmea_parse(read_log)
nmea_dict = nmea.nmea_to_dict(read_log)

print(nmea_dict['gpgga'])
from collections import Counter
count = Counter(nmea_dict['gpgga']['Fix_quality'])
fix_count = count.most_common()

print(read_file)
print("Fix quality", fix_count)
fix_report = open(str(read_file) + '_describe.txt', 'w')
fix_report.write(str(read_file) + '\n')
for i in range(len(fix_count)):
    fix_status = fix_count[i][0]
    fix_countup = fix_count[i][1]
    percent = fix_count[i][1] / nmea_dict['gpgga']['Fix_quality'].count()
    line = str(fix_status) + ','+ str(fix_countup) + ',' + str(percent)
    print(line)
    fix_report.write(str(line) + '\n')

try:
    df_age = nmea_dict['psat']['AGE']
except KeyError:
    df_age = nmea_dict['gpgga']['Time_since_last_DGPS_update']
print('********** AGE Describe **********')
age_describe = df_age.describe()
print(age_describe)
print('**********************************')

print('********** corr **********')
corr_report = open(str(read_file) + '_corr.txt', 'w')
for nmea in sorted(nmea_dict.keys()):
    print(nmea_dict[nmea].corr())
    corr_report.write(str(nmea_dict[nmea].corr()) + '\n')
print('**************************')
describe_report = open(str(read_file) + '_describe.txt', 'a')
describe_report.write(str(fix_count) + '\n')
describe_report.write(str(age_describe) + '\n')
describe_report.close()

#print(nmea_dict['gpgga'].columns)
#x = nmea_dict['gpgga']['Fix_quality']
#for column in nmea_dict['gpgga'].columns:
#    print(column)
#    try:
#        plt.scatter(x, nmea_dict['gpgga'][column])
#        plt.savefig(str(read_file) + '_gpgga_' + str(nmea) + '_scatter.png')
#        plt.show()
#    except ValueError:
#        print('NG:ValueError')
#        pass
gpgga = nmea_dict['gpgga']
nmea.describe_report(gpgga, read_file)
try:
    psat = nmea_dict['psat']
    nmea.describe_report(psat, read_file)
except KeyError:
    pass

print(nmea_dict.keys())
nmea_dict_sorted = sorted(nmea_dict.keys()) 
print(nmea_dict_sorted)
nmea.sample_plot(nmea_dict, read_file)
nmea.scatter_gpgga_by_fixmode(nmea_dict, read_file)
try:
    nmea.scatter_psat_by_fixmode(nmea_dict, read_file)
except KeyError:
    pass
nmea.lon_lat_plot(nmea_dict, read_file)
