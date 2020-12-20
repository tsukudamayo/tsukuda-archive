"""
output random nmea log
"""

import os, sys
import datetime
import random

# get timestamp
#start_time = datetime.now()
#logfile = open('nmea_' + str(start_time.strftime('%Y%m%d-%H%M%S') + '.log', 'a'))
# GPGGA INITIALIZE
GGA = '$GPGGA'
UTC = float(000000.00)
LON = float(3538.00000000)
NORTH = 'N'
LAT = float(13500.00000000)
EAST = 'E'
FIX_MODE = int(0)
NUMBER_OF_SATELITE = int(0)
HDOP = float(0.0)
ALTITUDE = float(0.00)
ALTITUDE_UNIT = 'M'
WGS_84 = float(0.0)
GEOID = 'M'
LAST_DGPS = int(0)
STATION_ID = int(0)
CHECKSUM_GGA = '*' + str(int(51))

# GPGSV_1 INITALIZE
GSV = '$GPGSV'
TOTAL_OF_MESSAGE = 3
NUMBER_OF_MESSAGE_1 = 1
NUMBER_OF_MESSAGE_2 = 2
NUMBER_OF_MESSAGE_3 = 3
TOTAL_SV = 9
SV_1 = format(int(3), '02d')
SV_2 = format(int(7), '02d')
SV_3 = format(int(21), '02d')
SV_4 = format(int(2), '02d')
SV_5 = format(int(17), '02d')
SV_6 = format(int(22), '02d')
SV_7 = format(int(28), '02d')
SV_8 = format(int(19), '02d')
SV_9 = format(int(42), '02d')
SV_10 = '' 
SV_11 = '' 
SV_12 = '' 
EL_1 = int(0)
EL_2 = int(0)
EL_3 = int(0)
EL_4 = int(0)
EL_5 = int(0)
EL_6 = int(0)
EL_7 = int(0)
EL_8 = int(0)
EL_9 = int(0)
EL_10 = '' 
EL_11 = '' 
EL_12 = '' 
AZ_1 = int(0)
AZ_2 = int(0)
AZ_3 = int(0)
AZ_4 = int(0)
AZ_5 = int(0)
AZ_6 = int(0)
AZ_7 = int(0)
AZ_8 = int(0)
AZ_9 = int(0)
AZ_10 = '' 
AZ_11 = '' 
AZ_12 = '' 
SNR_1 = int(0)
SNR_2 = int(0)
SNR_3 = int(0)
SNR_4 = int(0)
SNR_5 = int(0)
SNR_6 = int(0)
SNR_7 = int(0)
SNR_8 = int(0)
SNR_9 = int(0)
SNR_10 = '' 
SNR_11 = '' 
SNR_12 = '' 
CHECKSUM_GSV_1 = '1*' + str(int(62))
CHECKSUM_GSV_2 = '1*' + str(int(62))
CHECKSUM_GSV_3 = '1*' + str(int(62))



now = datetime.datetime.now()
now = now - datetime.timedelta(hours=9)
for i in range(500):
    UTC = now.strftime('%H%M%S') + '.00'
    LON = format(random.uniform(float(3400.00000000), float(3500.00000000)), '.8f')
    LAT = format(random.uniform(float(13000.00000000), float(14000.00000000)), '.8f')
    HDOP = random.uniform(float(0.0), float(1.0))
    FIX_MODE = random.randint(int(0), int(2))
    NUMBER_OF_SATELITE = random.randint(int(6), int(21))
    ALTITUDE = format(random.uniform(float(-1000.000), float(1000.000)), '.3f')
    WGS_84 = format(random.uniform(float(0.0), float(1000.0)), '.1f')
    LAST_DGPS = format(random.randint(int(0), int(10)), '.1f')
    TOTAL_SV = NUMBER_OF_SATELITE
    EL_1 = random.randint(int(0), int(90))
    EL_2 = random.randint(int(0), int(90))
    EL_3 = random.randint(int(0), int(90))
    EL_4 = random.randint(int(0), int(90))
    EL_5 = random.randint(int(0), int(90))
    EL_6 = random.randint(int(0), int(90))
    EL_7 = random.randint(int(0), int(90))
    EL_8 = random.randint(int(0), int(90))
    EL_9 = random.randint(int(0), int(90))
    AZ_1 = random.randint(int(0), int(360))
    AZ_2 = random.randint(int(0), int(360))
    AZ_3 = random.randint(int(0), int(360))
    AZ_4 = random.randint(int(0), int(360))
    AZ_5 = random.randint(int(0), int(360))
    AZ_6 = random.randint(int(0), int(360))
    AZ_7 = random.randint(int(0), int(360))
    AZ_8 = random.randint(int(0), int(360))
    AZ_9 = random.randint(int(0), int(360))
    SNR_1 = random.randint(int(0), int(70))
    SNR_2 = random.randint(int(0), int(70))
    SNR_3 = random.randint(int(0), int(70))
    SNR_4 = random.randint(int(0), int(70))
    SNR_5 = random.randint(int(0), int(70))
    SNR_6 = random.randint(int(0), int(70))
    SNR_7 = random.randint(int(0), int(70))
    SNR_8 = random.randint(int(0), int(70))
    SNR_9 = random.randint(int(0), int(70))

    gga_log = str(GGA) + ',' + str(UTC) + ',' +  str(LON) + ',' + \
              str(NORTH) + ',' + str(LAT) + ',' + str(EAST) + ',' + \
              str(FIX_MODE) + ',' + str(NUMBER_OF_SATELITE) + ',' + \
              str(HDOP) + ',' + str(ALTITUDE) + ',' + \
              str(ALTITUDE_UNIT) + ',' + str(WGS_84) + ',' + \
              str(GEOID) + ',' + str(LAST_DGPS) + ',' + \
              str(STATION_ID) + str(CHECKSUM_GGA)

    gsv1_log = str(GSV) + ',' + str(TOTAL_OF_MESSAGE) + ',' + \
               str(NUMBER_OF_MESSAGE_1) + ',' + str(TOTAL_SV) + ',' + \
               str(SV_1) + ',' + str(EL_1) + ',' + str(AZ_1) + ',' + str(SNR_1) + ',' + \
               str(SV_2) + ',' + str(EL_2) + ',' + str(AZ_2) + ',' + str(SNR_2) + ',' + \
               str(SV_3) + ',' + str(EL_3) + ',' + str(AZ_3) + ',' + str(SNR_3) + ',' + \
               str(SV_4) + ',' + str(EL_4) + ',' + str(AZ_4) + ',' + str(SNR_4) + ',' + \
               str(CHECKSUM_GSV_1)

    gsv2_log = str(GSV) + ',' + str(TOTAL_OF_MESSAGE) + ',' + \
               str(NUMBER_OF_MESSAGE_2) + ',' + str(TOTAL_SV) + ',' + \
               str(SV_5) + ',' + str(EL_5) + ',' + str(AZ_5) + ',' + str(SNR_5) + ',' + \
               str(SV_6) + ',' + str(EL_6) + ',' + str(AZ_6) + ',' + str(SNR_6) + ',' + \
               str(SV_7) + ',' + str(EL_7) + ',' + str(AZ_7) + ',' + str(SNR_7) + ',' + \
               str(SV_8) + ',' + str(EL_8) + ',' + str(AZ_8) + ',' + str(SNR_8) + ',' + \
               str(CHECKSUM_GSV_2)

    gsv3_log = str(GSV) + ',' + str(TOTAL_OF_MESSAGE) + ',' + \
               str(NUMBER_OF_MESSAGE_3) + ',' + str(TOTAL_SV) + ',' + \
               str(SV_9) + ',' + str(EL_9) + ',' + str(AZ_9) + ',' + str(SNR_9) + ',' + \
               str(SV_10) + ',' + str(EL_10) + ',' + str(AZ_10) + ',' + str(SNR_10) + ',' + \
               str(SV_11) + ',' + str(EL_11) + ',' + str(AZ_11) + ',' + str(SNR_11) + ',' + \
               str(SV_12) + ',' + str(EL_12) + ',' + str(AZ_12) + ',' + str(SNR_12) + ',' + \
               str(CHECKSUM_GSV_3)

    print(gga_log)
    print(gsv1_log)
    print(gsv2_log)
    print(gsv3_log)

    now = now + datetime.timedelta(seconds=1)

