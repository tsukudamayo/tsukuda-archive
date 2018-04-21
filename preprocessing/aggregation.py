
# _*_ coding: utf-8 _*_
from preprocess.load_data.data_loader import load_hotel_reserve

import numpy as np
import pandas as pd

customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

def main():
    # aggregation using agg ################################
    print('**************** aggregation using agg ****************')
    result = reserve_tb\
      .groupby('hotel_id')\
      .agg({
          'reserve_id': 'count',
          'customer_id': 'nunique'
      })
    result.reset_index(inplace=True)
    result.columns = ['hotel_id', 'rsv_cnt', 'cus_cnt']
    aggregation_01 = result
    print('aggregation_01', aggregation_01)

    # sum and aggregation #################################
    print('**************** sum and aggregation ****************')
    result = reserve_tb\
      .groupby(['hotel_id', 'people_num'])['total_price']\
      .sum().reset_index()
    result.rename(columns={'total_price': 'price_sum'}, inplace=True)
    aggregation_02 = result
    print('aggregation_02', aggregation_02)

    # lambda and aggregation #############################
    print('**************** lambda and aggregation ****************')
    result = reserve_tb\
      .groupby('hotel_id')\
      .agg({
          'total_price': ['max', 'min', 'mean', 'median',
                              lambda x: np.percentile(x, q=20)]
      }).reset_index()
    result.columns = ['hotel_id', 'price_max', 'price_min',
                      'price_mean', 'price_median', 'price_20per']
    aggregation_03 = result
    print('aggeregation_03', aggregation_03)

    # variance and std using aggregation ##################
    print('**************** variance and std using aggregation ****************')
    result = reserve_tb\
      .groupby('hotel_id')\
      .agg({
          'total_price': ['var', 'std']
      }).reset_index()
    result.columns = {'hotel_id', 'price_var', 'price_std'}
    # if data count = 1
    result.fillna(0, inplace=True)

    aggregation_04 = result
    print('aggregation_04', aggregation_04)

    # using mode ##########################################
    print('**************** using mode ****************')
    result = reserve_tb['total_price'].round(-3).mode()

    aggregation_05 = result
    print('aggregation_05', aggregation_05)

    # using rank #########################################
    reserve_tb['reserve_datetime'] = pd.to_datetime(
        reserve_tb['reserve_datetime'], format='%Y-%m-%d %H:%M:%S'
    )

    reserve_tb['log_no'] = reserve_tb\
      .groupby('customer_id')['reserve_datetime']\
      .rank(ascending=True, method='first')

    print(reserve_tb['log_no'])


if __name__ == '__main__':
    main()
