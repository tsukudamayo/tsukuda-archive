from preprocess.load_data.data_loader import load_hotel_reserve

import numpy as np
import pandas as pd
import gc
import operator

import pandas.tseries.offsets as offsets


customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

def main():
    # # verify data #############################################
    # print('**************** hotel_tb ****************')
    # print(hotel_tb)
    # reduce data before join
    join_01 = pd.merge(
        reserve_tb.query('people_num == 1'),
        hotel_tb.query('is_business'),
        on='hotel_id',
        how='inner',
    )
    print('join_01 \n', join_01)
    del join_01
    gc.collect()

    # recommend same area #######################################
    # count small_area_name each small area
    small_area_mst = hotel_tb\
      .groupby(['big_area_name', 'small_area_name'], as_index=False)\
      .size().reset_index()
    small_area_mst.columns = ['big_area_name', 'small_area_name', 'hotel_cnt']
    print('small_area_mst \n', small_area_mst)

    # more than 20 -> small_area_name, less than 20 -> big_area_name
    small_area_mst['join_area_id'] = \
      np.where(small_area_mst['hotel_cnt'] -1 >= 20,
               small_area_mst['small_area_name'],
               small_area_mst['big_area_name'])
    print('join_area_id \n', small_area_mst['join_area_id'])

    # drop
    small_area_mst.drop(['hotel_cnt', 'big_area_name'], axis=1, inplace=True)

    # join recommend hotel and small_area_mst
    base_hotel_mst = pd.merge(hotel_tb, small_area_mst, on='small_area_name')\
      .loc[:, ['hotel_id', 'join_area_id']]
    print('base_hotel_mst \n', base_hotel_mst)

    # if needed
    del small_area_mst
    gc.collect()

    # recommend_hotel_mst is for candidate of recommends
    recommend_hotel_mst = pd.concat([
        hotel_tb[['small_area_name', 'hotel_id']]\
          .rename(columns={'small_area_name': 'join_area_id'}, inplace=False),
        hotel_tb[['big_area_name', 'hotel_id']]\
          .rename(columns={'big_area_name': 'join_area_id'}, inplace=False)
    ])
    print('recommend_hotel_mst \n', recommend_hotel_mst)

    # since duplicate 'hotel_id' when data was joined, rename 'hotel_id'
    recommend_hotel_mst.rename(columns={'hotel_id': 'rec_hotel_id'},
                               inplace=True)
    print('recommend_hotel_mst \n', recommend_hotel_mst)

    # drop itself by using query function
    result = pd.merge(base_hotel_mst, recommend_hotel_mst, on='join_area_id')\
               .loc[:, ['hotel_id', 'rec_hotel_id']]\
               .query('hotel_id != rec_hotel_id')
    print('result \n', result)

    # sort by reserve_datetime for each customer
    """
        sort for each group by using groupby().apply()
        sort by using sort_values() axis=0 -> row, axis=1 -> columns
    """
    result = reserve_tb\
               .groupby('customer_id')\
               .apply(lambda group:
                      group.sort_values(by='reserve_datetime',
                                        axis=0,
                                        inplace=False))
    print('sort by reserve_datetime for each customer \n', result)

    # define before price which two before each customer ################
    """ shift data down by using shift() """
    result['before_price'] = pd.Series(result['total_price'].shift(periods=2))
    print('define before price which two before each customer \n',
          result['before_price'])
    del result
    gc.collect()

    # calculate the total value up to two previous ######################
    price_total = reserve_tb['price_sum'] = pd.Series(
        reserve_tb\
          .groupby('customer_id')
          .apply(lambda x: x.sort_values(by='reserve_datetime',
                                         ascending=True))
          # implement window function
          .loc[:, 'total_price']
          .rolling(center=False, window=3, min_periods=3).sum()
          .reset_index(drop=True)
    )
    print('calculate the total value up to two previous \n', price_total)
    del price_total
    gc.collect()

    # caluclate the average value up to three previous #################
    price_avg = reserve_tb['price_avg'] = pd.Series(
        reserve_tb\
          .groupby('customer_id')
          .apply(lambda x: x.sort_values(by='reserve_datetime', ascending=True))
          ['total_price'].rolling(center=False, window=3, min_periods=1).mean()
          .reset_index(drop=True)
    )
    price_avg_each_customers = reserve_tb['price_avg'] = \
      reserve_tb.groupby('customer_id')['price_avg'].shift(periods=1)
    print('caluclate the average value up to three previous \n',
          price_avg_each_customers)
    del price_avg
    del price_avg_each_customers
    gc.collect()

    # calculate the total value up to 90 days previous ################
    reserve_tb['reserve_datetime'] = pd.to_datetime(
        reserve_tb['reserve_datetime'], format='%Y-%m-%d %H:%M:%S'
    )
    print(reserve_tb['reserve_datetime'])

    sum_table = pd.merge(
        reserve_tb[['reserve_id', 'customer_id', 'reserve_datetime']],
        reserve_tb[['customer_id', 'reserve_datetime', 'total_price']]
          .rename(columns={'reserve_datetime': 'reserve_datetime_before'}),
        on='customer_id'
    )
    print(sum_table)

    sum_table = sum_table[operator.and_(
        sum_table['reserve_datetime'] > sum_table['reserve_datetime_before'],
        sum_table['reserve_datetime'] + offsets.Day(-90)
          <= sum_table['reserve_datetime_before']
    )].groupby('reserve_id')['total_price'].sum().reset_index()
    print(sum_table)

    sum_table.columns = ['reserve_id', 'total_price_sum']
    result = pd.merge(
        reserve_tb, sum_table, on='reserve_id', how='left'
    ).fillna(0)
    print(result)
    


if __name__ == '__main__':

    main()
