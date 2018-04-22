import pandas as pd
from preprocess.load_data.data_loader import load_hotel_reserve
customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

# convert datetime and date ################
# convert using to_datetime function
print(pd.to_datetime(reserve_tb['reserve_datetime'], format='%Y-%m-%d %H:%M:%S'))
print(pd.to_datetime(reserve_tb['checkin_date'] + reserve_tb['checkin_time'],
               format='%Y-%m-%d%H:%M:%S'))
# get date and time
print(pd.to_datetime(reserve_tb['reserve_datetime'],
               format='%Y-%m-%d %H:%M:%S').dt.date)
print(pd.to_datetime(reserve_tb['checkin_date'], format='%Y-%m-%d').dt.date)

# convert year,month,day,hour,minutes,week ################
customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

reserve_tb['reserve_datetime'] =\
  pd.to_datetime(reserve_tb['reserve_datetime'], format='%Y-%m-%d %H:%M:%S')
# get year
print(reserve_tb['reserve_datetime'].dt.year)
# get month
print(reserve_tb['reserve_datetime'].dt.month)
# get day
print(reserve_tb['reserve_datetime'].dt.day)
# get week
print(reserve_tb['reserve_datetime'].dt.dayofweek)
# get hour
print(reserve_tb['reserve_datetime'].dt.hour)
# get minutes
print(reserve_tb['reserve_datetime'].dt.minute)
# get seconds
print(reserve_tb['reserve_datetime'].dt.second)
# convert format
print(reserve_tb['reserve_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S'))

# convert timedelta ################
reserve_tb['reserve_datetime'] = \
  pd.to_datetime(reserve_tb['reserve_datetime'], format='%Y-%m-%d %H:%M:%S')
# convert checin_datetime
reserve_tb['checkin_datetime'] = \
  pd.to_datetime(reserve_tb['checkin_date'] + reserve_tb['checkin_time'],
                 format='%Y-%m-%d%H:%M:%S')
# calculate year delta
print(reserve_tb['reserve_datetime'].dt.year - reserve_tb['checkin_datetime'].dt.year)
# calulate month delta
print((reserve_tb['reserve_datetime'].dt.year*12 + \
       reserve_tb['reserve_datetime'].dt.month) \
       - \
       (reserve_tb['checkin_datetime'].dt.year*12 + \
        reserve_tb['checkin_datetime'].dt.month))
# calculate differnce in a day
print((reserve_tb['reserve_datetime'] - reserve_tb['checkin_datetime']) \
        .astype('timedelta64[D]'))
# calculate differnce in a hour
print((reserve_tb['reserve_datetime'] - reserve_tb['checkin_datetime']) \
        .astype('timedelta64[h]'))
# calculate differnce in a minute
print((reserve_tb['reserve_datetime'] - reserve_tb['checkin_datetime']) \
        .astype('timedelta64[m]'))
# calculate differnce in a second
print((reserve_tb['reserve_datetime'] - reserve_tb['checkin_datetime']) \
        .astype('timedelta64[s]'))
        
