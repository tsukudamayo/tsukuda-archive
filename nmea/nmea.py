import os, sys
import re
from collections import Counter
import glob
import codecs
import pandas as pd
import matplotlib.pyplot as plt

def delete_checksum(path, filename, read_file):
    with codecs.open(str(path) + '/' + str(filename), 'r', 'Shift-JIS', 'ignore') as ld:
        lines = ld.readlines()
    ld.close()

    f = open(str(path) + '/' + str(read_file) + '_del_cs.log', 'w')
    for line in lines:
        if line.find('*') >= 0:
            reg = re.compile("(.*)(\*)(.*)")
            m = reg.match(line)
            f.write(m.group(1))
            f.write('\n')


def log_filter(path, read_file , m):
    with codecs.open(str(path) + '/' + str(read_file) + '_del_cs.log', 'r', 'Shift-JIS', 'ignore') as ld:
        lines = ld.readlines()
    ld.close()

    f = open(str(path) + '/' + str(read_file) + '_' +  str(m.lower()) + '.log', 'w')
    for line in lines:
        if line.find(str(m)) == 1:
            f.write(line[:-1])
            f.write('\n')


def gsv_filter(path, read_file, nmea):
    fnames = ['_1.log', '_2.log', '_3.log', '_4.log']
    regexes = [str(nmea) + ",[0-9],1", str(nmea) + ",[0-9],2",
               str(nmea) + ",[0-9],3", str(nmea) + ",[0-9],4"]

    with codecs.open(str(path) + '/' + str(read_file) + '_del_cs.log', 'r', 'Shift-JIS', 'ignore') as ld:
        lines = ld.readlines()
    ld.close()

    for fname, regex in zip(fnames, regexes):
        f = open(str(path) + '/' + str(read_file) + '_' + str(nmea.lower()) + str(fname), 'w')
        for line in lines:
            reg = re.compile(regex)
            s = reg.search(line)
            if s != None:
                f.write(line[:-1])
                f.write('\n')


##need to fix
#def zero_padding():
#    files = glob.glob('/*_[0-9]_g*')
#    for f in files:
#        f.replace("_[0-9]","_0[0-9]")
def read_log():

    exist_files = []

    file_glob = [os.path.basename(r) for r in glob.glob('./*')]
    #print(file_glob)

    for read_file in file_glob:
        #print(read_file)
        for target_file in nmea_logs:
            if read_file.find(str(target_file)) >= 0:
                exist_files.append(read_file)
                #print('OK')
            else:
                pass

    return exist_files
    #print(exist_files)

def nmea_parse(exist_files):

    comma_counts_dict = {}
    comma_counts_out = []
    for exist_file in exist_files:
        with open(exist_file, 'r') as f:
            lines = f.readlines()
            comma_counts_in = [line.count(',') for line in lines if line.count(',')]
            print(exist_file)
            #print(comma_counts_in)
            count_comma = Counter(comma_counts_in)
            print(count_comma.most_common()[0][0])
            comma_counts_dict[exist_file] = count_comma.most_common()[0][0]
            comma_counts_out.append(comma_counts_in)
    print(comma_counts_dict.keys())
    #print(comma_counts_out)

    for logfile, comma in comma_counts_dict.items():
        print(logfile, comma)
        with open(logfile, 'r') as f:
            lines = f.readlines()
            f.close()

        w = open(logfile, 'w')
        for line in lines:
            if line.count(',') == comma:
                w.write(line[:-1])
                w.write('\n')


def nmea_to_dataframe(exist_file):

    try:
        to_dataframe = pd.read_csv(exist_file)
    except UnicodeDecodeError:
        to_dataframe = pd.read_csv(exist_file,
                                     encoding='Shift_JISx0213')

    return to_dataframe


def nmea_to_dict(exist_files):

    nmea_dict = {}

    for exist_file in exist_files:
        #print(exist_file)
        idx_file = exist_files.index(exist_file)
        if exist_file.find('glgsv') >= 0:
            idx_col_names = unique_col_names.index(col_glgsv)
            #print(idx_col_names)
            if exist_file.find('_1.log') >= 0:
                glgsv_1 = nmea_to_dataframe(exist_file)
                glgsv_1.columns = unique_col_names[idx_col_names]
                nmea_dict['glgsv_1'] = glgsv_1
            elif exist_file.find('_2.log') >= 0:
                glgsv_2 = nmea_to_dataframe(exist_file)
                glgsv_2.columns = unique_col_names[idx_col_names]
                nmea_dict['glgsv_2'] = glgsv_2
            elif exist_file.find('_3.log') >= 0:
                glgsv_3 = nmea_to_dataframe(exist_file)
                glgsv_3.columns = unique_col_names[idx_col_names]
                nmea_dict['glgsv_3'] = glgsv_3
            elif exist_file.find('_4.log') >= 0:
                glgsv_4 = nmea_to_dataframe(exist_file)
                glgsv_4.columns = unique_col_names[idx_col_names]
                nmea_dict['glgsv_4'] = glgsv_4
            else:
                pass
            #print('glgsv:OK')
        elif exist_file.find('gpgga') >= 0:
            idx_col_names = unique_col_names.index(col_gpgga)
            #print(idx_col_names)
            gpgga = nmea_to_dataframe(exist_file)
            gpgga.columns = unique_col_names[idx_col_names]
            nmea_dict['gpgga'] = gpgga
            #print('gpgga:OK')
        elif exist_file.find('gpgsv') >= 0:
            idx_col_names = unique_col_names.index(col_gpgsv)
            idx_col_names2 = unique_col_names.index(col_gpgsv2)
            #print(idx_col_names)
            if exist_file.find('_1.log') >= 0:
                gpgsv_1 = nmea_to_dataframe(exist_file)
                try:
                    gpgsv_1.columns = unique_col_names[idx_col_names]
                except ValueError:
                    gpgsv_1.columns = unique_col_names[idx_col_names2]
                nmea_dict['gpgsv_1'] = gpgsv_1
            elif exist_file.find('_2.log') >= 0:
                gpgsv_2 = nmea_to_dataframe(exist_file)
                try:
                    gpgsv_2.columns = unique_col_names[idx_col_names]
                except ValueError:
                    gpgsv_2.columns = unique_col_names[idx_col_names2]
                nmea_dict['gpgsv_2'] = gpgsv_2
            elif exist_file.find('_3.log') >= 0:
                gpgsv_3 = nmea_to_dataframe(exist_file)
                try:
                    gpgsv_3.columns = unique_col_names[idx_col_names]
                except ValueError:
                    gpgsv_3.columns = unique_col_names[idx_col_names2]
                nmea_dict['gpgsv_3'] = gpgsv_3
            elif exist_file.find('_4.log') >= 0:
                gpgsv_4 = nmea_to_dataframe(exist_file)
                try:
                    gpgsv_4.columns = unique_col_names[idx_col_names]
                except ValueError:
                    gpgsv_4.columns = unique_col_names[idx_col_names2]
                nmea_dict['gpgsv_4'] = gpgsv_4
            else:
                pass
            #print('gpgsv:OK')
        elif exist_file.find('gpzda') >= 0:
            idx_col_names = unique_col_names.index(col_gpzda)
            #print(idx_col_names)
            gpzda = nmea_to_dataframe(exist_file)
            gpzda.columns = unique_col_names[idx_col_names]
            nmea_dict['gpzda'] = gpzda
            #print('gpzda:OK')
        elif exist_file.find('psat') >= 0:
            psat = nmea_to_dataframe(exist_file)
            if len(psat.columns) == len(col_psat):
                idx_col_names = unique_col_names.index(col_psat)
            #print(idx_col_names)
            elif len(psat.columns) == len(col_psat_baido):
                idx_col_names = unique_col_names.index(col_psat_baido)
            psat.columns = unique_col_names[idx_col_names]
            nmea_dict['psat'] = psat
            #print('psat:OK')
        else:
            pass

    #print(nmea_dict.keys())
    #print(nmea_dict.items())
    #df_nmea_dict = pd.DataFrame.from_nmea_dictt(nmea_dict)
    #print(nmea_dict)
    #pf = pd.Panel(nmea_dict)
    return nmea_dict#, \
           #pf, \
           #glgsv_1, glgsv_2, glgsv_3, \
           #gpgga, \
           #gpgsv_1, gpgsv_2, gpgsv_3, gpgsv_4, \
           #gpzda, \
           #psat
    #return nmea_dict
    #pf = pd.Panel(nmea_dict)
    #return nmea_dict
    #return pd.Panel.from_nmea_dictt(nmea_dict, orient='minor')

    #glgsv_1, glgsv_2, glgsv_3, \
    #gpgga, \
    #gpgsv_1, gpgsv_2, gpgsv_3, gpgsv_4, \
    #gpzda, \
    #psat = nmea_parse()

   # print(glgsv_1.tail(10))
   # #print(glgsv_1.describe())
   # ## what do you want to visualize in glgsv1
   # #print(glgsv_2.tail(10))
   # #print(glgsv_2.describe())
   # ## what do you want to visualize in glgsv2
   # #print(glgsv_3.tail(10))
   # #print(glgsv_3.describe())
   # ## what do you want to visualize in glgsv3
   # print(gpgga.tail(10))
   # #print(gpgga.describe())
   # # what do you want to visualize in gpgga
   # print(gpgsv_1.tail(10))
   # #print(gpgsv_1.describe())
   # print('iloc:',len(gpgsv_1.iloc[0]))
   # print(len(col_gpgsv))
   # ## what do you want to visualize in gpgsv1
   # #print(gpgsv_2.tail(10))
   # #print(gpgsv_2.describe())
   # ## what do you want to visualize in gpgsv2
   # #print(gpgsv_3.tail(10))
   # #print(gpgsv_3.describe())
   # ## what do you want to visualize in gpgsv3
   # #print(gpgsv_4.tail(10))
   # #print(gpgsv_4.describe())
   # ## what do you want to visualize in gpgsv4
   # print(gpzda.tail(10))
   # #print(gpzda.describe())
   # ## what do you want to visualize in gpzda
   # print(psat.tail(10))
   # #print(psat.describe())
   # ## what do you want to visualize in psat
   # print('glgsv_iloc:',len(glgsv_1.iloc[0]))
   # print('col_glgsv:', len(col_glgsv))
   # print('gpgga_iloc:',len(gpgga.iloc[0]))
   # print('col_gpgga:', len(col_gpgga))
   # print('gpgsv_iloc:',len(gpgsv_1.iloc[0]))
   # print('col_gpgsv:', len(col_gpgsv))
   # print('gpzda_iloc:',len(gpzda.iloc[0]))
   # print('col_gpzda:', len(col_gpzda))
   # print('psat_iloc:',len(psat.iloc[0]))
   # print('col_psat:', len(col_psat))
   # print(gpgga.tail(10))
   # print(nmea_dict['gpgga'].tail(10))


def sample_plot(nmea_dict, date):

    for i in sorted(nmea_dict.keys()):
        print('**********' + str(i) + '**********')
        if i.find(str(i)) >= 0:
            df = nmea_dict[str(i)]
            for j in df.columns:
                print(j)
                # Refacotring to shorten the cord(not yet implemented)
                # Since it nessesary to associate column names and logfiles in a dictionary
                try:
                    plt.plot(nmea_dict[str(i)][j])
                    plt.savefig(str(date) + '_' + str(i) + '_' + str(j) + '_plot.png')
                    #plt.show()
                    plt.clf()
                    plt.hist(nmea_dict[str(i)][j].dropna())
                    plt.savefig(str(date) + '_' + str(i) + '_' + str(j) + '_hist.png')
                    #plt.show()
                    plt.clf()
                except ValueError:
                    print('NG:ValueError')
                    pass
        else:
            pass


def scatter_gpgga_by_fixmode(nmea_dict, date):

    x = nmea_dict['gpgga']['Fix_quality']

    print('Time')
    plt.scatter(x, nmea_dict['gpgga']['Time'])
    plt.savefig(str(date) + '_gpgga_Time_scatter.png')
    plt.show()
    plt.clf()
    print('Lat')
    plt.scatter(x, nmea_dict['gpgga']['Lat'])
    plt.savefig(str(date) + '_gpgga_Lat_scatter.png')
    plt.show()
    plt.clf()
    print('Lon')
    plt.scatter(x, nmea_dict['gpgga']['Lon'])
    plt.savefig(str(date) + '_gpgga_Lon_scatter.png')
    plt.show()
    plt.clf()
    print('Number_of_satelites')
    plt.scatter(x, nmea_dict['gpgga']['Number_of_satelites'])
    plt.savefig(str(date) + '_gpgga_Number_of_satelites_scatter.png')
    plt.show()
    plt.clf()
    print('HDOP')
    plt.scatter(x, nmea_dict['gpgga']['HDOP'])
    plt.savefig(str(date) + '_gpgga_HDOP_scatter.png')
    plt.show()
    plt.clf()
    print('Altitude')
    plt.scatter(x, nmea_dict['gpgga']['Altitude'])
    plt.savefig(str(date) + '_gpgga_Altitude_scatter.png')
    plt.show()
    plt.clf()
    print('H-geoid')
    plt.scatter(x, nmea_dict['gpgga']['H-geoid'])
    plt.savefig(str(date) + '_gpgga_H-geoid_scatter.png')
    plt.show()
    plt.clf()
    print('Time_since_last_DGPS_update')
    plt.scatter(x, nmea_dict['gpgga']['Time_since_last_DGPS_update'])
    plt.savefig(str(date) + '_gpgga_Time_since_last_DGPS_update_scatter.png')
    plt.show()
    plt.clf()


def scatter_psat_by_fixmode(nmea_dict, date):

    x = nmea_dict['gpgga']['Fix_quality']

    print('AGE')
    plt.scatter(x[:len(nmea_dict['psat']['AGE'])], nmea_dict['psat']['AGE'])
    plt.savefig(str(date) + '_psat_AGE_scatter.png')
    plt.show()
    plt.clf()
    print('RSF')
    plt.scatter(x[:len(nmea_dict['psat']['RSF'])], nmea_dict['psat']['RSF'])
    plt.savefig(str(date) + '_psat_RSF_scatter.png')
    plt.show()
    plt.clf()
    print('BSF')
    plt.scatter(x[:len(nmea_dict['psat']['RSF'])], nmea_dict['psat']['BSF'])
    plt.savefig(str(date) + '_psat_BSF_scatter.png')
    plt.show()
    print('HAG')
    plt.scatter(x[:len(nmea_dict['psat']['HAG'])], nmea_dict['psat']['HAG'])
    plt.savefig(str(date) + '_psat_HAG_scatter.png')
    plt.show()
    plt.clf()
#    df = nmea_dict['psat']
#    for column in df.columns:
#        print(column)
#        try:
#            plt.scatter(df['Fix_quality'], df[str(column)])
#            plt.savefig(str(date) + '_gpgga_' + str(column) + '_scatter.png')
#            plt.show()
#        except ValueError:
#            print('NG:ValueError')
#            pass

def describe_report(nmea, date):
    print(date)
    report_file = open(str(date) + '_gpgga_psat_describe.txt', 'w')
    for column in nmea.columns:
        print('-----' + str(column) + '-----')
        report = nmea[column].describe()
        print(report)
        report_file.write('-----' + str(column) + '-----' + '\n')
        report_file.write(str(report) + '\n')
        try:
            report.to_csv(str(date) + '_'  + str(column) + '_describe.csv')
        except FileNotFoundError:
            pass
    report_file.close()


def lon_lat_plot(nmea_dict, date):
    plt.plot(nmea_dict['gpgga']['Lon'], nmea_dict['gpgga']['Lat'])
    plt.savefig(str(date) + 'lon-lat.png')
    plt.show()


#Allocate column names for NMEA sentence
#Since the number of columnas is changed during log acquisition,
#Assign column names to each column fo sentences of NMEA

#GPGGA
col_gpgga = [
    'GPGGA', 'Time', 'Lat', 'N/S', 'Lon', 'E/W', \
    'Fix_quality', 'Number_of_satelites', 'HDOP', \
    'Altitude', 'M1', 'H-geoid', 'M2', \
    'Time_since_last_DGPS_update', 'DPGS_reference_station_ID']

#GPGSA
col_gpgsa = [
    'GPGSA', 'Mode_A/M', 'Mode_1/2/3', \
    'SV_1', 'SV_2', 'SV_3', 'SV_4', 'SV_5', \
    'SV_6', 'SV_7', 'SV_8', 'SV_9', 'SV_10', \
    'PDOP', 'HDOP', 'VDOP', 'checksum']

#GLGSA
col_glgsa = [
    'GLGSA', 'Mode_A/M', 'Mode_1/2/3', \
    'SV_1', 'SV_2', 'SV_3', 'SV_4', 'SV_5', \
    'SV_6', 'SV_7', 'SV_8', 'SV_9', 'SV_10', \
    'PDOP', 'HDOP', 'VDOP', 'checksum']

#GPRMC
col_gprmc = [
    'GPRMC', 'UTC', 'Validation_A/V', \
    'Lat', 'N/S', 'Lon', 'E/W', 'knots', 'True_course', \
    'Date', 'Magnetic_variation_degreese', 'E/W', '13', 'checksum']

#GPVTG
col_gpvtg = [
    'GPVTG', 'Track_degrees_True ', 'T', 'Magnetic_degreese', 'M', \
    'knots', 'N', 'kilometers', 'K', '10', 'checksum']

#GPZDA
col_gpzda = [
    'GPZDA', 'UTC', 'Day', 'Month', 'Year', \
    'Local zone description', 'Local zone minutes description-checksum']

#GPGSV
col_gpgsv = [
    'GPGSV', 'Number_of_messages', 'Message_number', 'SV_total',\
    '1_n', '1_ed', '1_ad', '1_snr',\
    '2_n', '2_ed', '2_ad', '2_snr', \
    '3_n', '3_ed', '3_ad', '3_snr', \
    '4_n', '4_ed', '4_ad', '4_snr', \
    '-']

col_gpgsv2 = [
    'GPGSV', 'Number_of_messages', 'Message_number', 'SV_total',\
    '1_n', '1_ed', '1_ad', '1_snr',\
    '2_n', '2_ed', '2_ad', '2_snr', \
    '3_n', '3_ed', '3_ad', '3_snr', \
    '4_n', '4_ed', '4_ad', '4_snr']


#GLGSV
col_glgsv = [
    'GLGSV', 'Number_of_messages', 'Message_number', 'SV_total',\
    '1_n', '1_ed', '1_ad', '1_snr',\
    '2_n', '2_ed', '2_ad', '2_snr', \
    '3_n', '3_ed', '3_ad', '3_snr', \
    '4_n', '4_ed', '4_ad', '4_snr', \
    '-']

#PSAT,RTKSTAT
col_psat = [
    'PSAT', 'RTKSTAT', 'MODE', 'TYP', 'AGE', \
    'SUBOPT', 'DIST', '(', 'SYS_1', 'SYS_2', \
    ')(_1', 'NUM_1', 'NUM_2', ')(_2', \
    'SNR_1', 'SNR_2', ')',\
    'RSF', 'BSF', 'HAG', '-1', '-2']

col_psat_baido = [
    'PSAT', 'RTKSTAT', 'MODE', 'TYP', 'AGE', \
    'SUBOPT', 'DIST', '(', 'SYS_1', 'SYS_2', 'SYS_3', \
    ')(_1', 'NUM_1', 'NUM_2', 'NUM_3', ')(_2', \
    'SNR_1', 'SNR_2', 'SNR_3', ')', \
    'RSF', 'BSF', 'HAG', '-1', '-2']

nmea_logs = [
    'gpgga.log', 'gprmc.log', 'gpvtg.log', 'gpzda.log', 'psat.log', \
    'gpgsv_1.log', 'gpgsv_2.log', 'gpgsv_3.log', 'gpgsv_4.log', \
    'glgsv_1.log', 'glgsv_2.log', 'glgsv_3.log', 'glgsv_4.log']

col_names = [col_gpgga, col_gprmc, col_gpvtg, col_gpzda, col_psat, \
        col_gpgsv, col_gpgsv, col_gpgsv, col_gpgsv, \
        col_glgsv, col_glgsv, col_glgsv, col_glgsv]

unique_col_names = [col_glgsv, col_gpgga, col_gpgsv, col_gpgsv2,\
                    col_gprmc, col_gpvtg, col_gpzda, \
                    col_psat, col_psat_baido]

#path_dir = os.path.dirname(os.path.abspath(__file__))
#print(path_dir)


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    fnames = [os.path.basename(r) for r in glob.glob('./*')]
    print(fnames)

    words = ['GPGGA', 'GPRMC', 'GPVTG', 'GPZDA', 'GPGSA', 'GLGSA', 'PSAT']
    gsv_names = ['GLGSV', 'GPGSV']

    filename = os.path.basename(sys.argv[1])
    read_file, ext = os.path.splitext(filename)
    del_cs = delete_checksum(path, filename, read_file)

    for word in words:
        log_filter(path, read_file, word)
    for gsv_name in gsv_names:
        gsv_filter(path, read_file, gsv_name)

    fnames = [os.path.basename(r) for r in glob.glob('./*')]
    print(fnames)

    for fname in fnames:
        if os.path.getsize(path + '/' + fname) == 0:
            try:
                os.remove(path + '/' + fname)
            except PermissionError:
                pass

    read_log = read_log()
    nmea_parse = nmea_parse(read_log)
    nmea_dict = nmea_to_dict(read_log)

    print(nmea_dict['gpgga'])
    count = Counter(nmea_dict['gpgga']['Fix_quality'])
    fix_count = count.most_common()

    print(read_file)
    print("Fix quality", fix_count)
    fix_report = open(str(read_file) + '_describe.txt', 'w')
    for i in range(len(fix_count)):
        fix_status = fix_count[i][0]
        fix_countup = fix_count[i][1]
        percent = fix_count[i][1] / nmea_dict['gpgga']['Fix_quality'].count()
        line = str(fix_status) + ',' + str(fix_countup) + ',' + str(percent)
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
    print(nmea_dict)
    for nmea in sorted(nmea_dict.keys()):
        print(nmea_dict[nmea].corr())
        corr_report.write(str(nmea_dict[nmea].corr()) + '\n')
    print('**************************')
    age_fix_report = open(str(read_file) + '_describe.txt', 'w')
    age_fix_report.write(str(fix_count) + '\n')
    age_fix_report.write(str(age_describe) + '\n')
    age_fix_report.close()

    gpgga = nmea_dict['gpgga']
    describe_report(gpgga, read_file)
    try:
        psat = nmea_dict['psat']
        describe_report(psat, read_file)
    except KeyError:
        pass
    print(nmea_dict.keys())
    nmea_dict_sorted = sorted(nmea_dict.keys())
    print(nmea_dict_sorted)
    sample_plot(nmea_dict, read_file)
    scatter_gpgga_by_fixmode(nmea_dict, read_file)
    try:
        scatter_psat_by_fixmode(nmea_dict, read_file)
    except KeyError:
        pass
    lon_lat_plot(nmea_dict, read_file)

