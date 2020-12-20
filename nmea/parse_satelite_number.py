"""
search snr ratio by each satelite number
input: nmea file ex 20170821_gnss.log -> parse_satelite_number.py 20170821
output: 011111.00,01,28,060,50(time(UTC),satelite_number,arg1,arg2,snr)
"""
import os,sys
import codecs, re
import glob

# read nmea file
with codecs.open(str(sys.argv[1]), 'r', 'Shift-JIS', 'ignore') as ld:
    lines = ld.readlines()
ld.close()

# read file header
filename = os.path.basename(sys.argv[1])
file_header, ext = os.path.splitext(filename)

# grep srn ratio each satelite number
for i in range(100):
    # regex pattern 
    second = '\\d{6}.\\d{2},'
    number = '{0:02d}'.format(i)
    string = ',\\d{2},\\d{3},\\d{0,2}'
    regex_pattern = str(number) + str(string)
    # make logfile
    with open(str(file_header) + '_' + 'satelite_number_' + str(i) + '.log', 'w') as w:
        for line in lines:
            # snr pattern compile
            pattern = re.compile(regex_pattern)
            regex = re.search(pattern, line)
            # time patten compile
            timelog = re.compile(second)
            timereg = re.search(timelog, line)
            # get time
            if timereg != None:
                sec = timereg.group()
            else:
                pass
            # get snr log and output
            if regex != None:
                log = regex.group()
                print(str(sec) + str(log))
                w.write(str(sec) + str(log))
                w.write('\n')
            else:
                pass


# delete 0 size file(no log)

path = os.path.dirname(os.path.abspath(__file__))
fnames = [os.path.basename(r) for r in glob.glob('./*')]

for fname in fnames:
    if os.path.getsize(path + '/' + fname) == 0:
        try:
            os.remove(path + '/' + fname)
        except PermissionError:
            pass
