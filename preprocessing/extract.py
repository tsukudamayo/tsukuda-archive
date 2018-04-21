# _*_ coding: utf-8 _*_
from preprocess.load_data.data_loader import load_hotel_reserve

import pandas as pd


def main():
    customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()
    print(customer_tb)
    print(hotel_tb)
    print(reserve_tb)

    # extract columns ################################
    print('**************** specify by strings not index ****************')
    extract_01 = reserve_tb[['reserve_id', 'hotel_id', 'customer_id',
                             'reserve_datetime', 'checkin_date', 'checkin_time',
                             'checkout_date']]
    print('extract_01', extract_01)

    # extract columns using iloc ####################
    print('**************** using iloc ****************')
    extract_02 = reserve_tb.loc[:, ['reserve_id', 'hotel_id', 'customer_id',
                                     'reserve_datetime', 'checkin_date',
                                     'checkin_time', 'checkout_date']]
    print('extract_02', extract_02)

    # drop columns using drop #######################
    print('**************** using drop ****************')
    extract_03 = reserve_tb.drop(['people_num', 'total_price'], axis=1)
    print('extract_03', extract_03)

    # drop return None ##############################
    print('************* using drop inplace=True, return None *************')
    extract_04 = reserve_tb.drop(['people_num', 'total_price'], axis=1, inplace=True)
    print('extract_04', extract_04)

    # extract using query ###########################
    print('**************** using query ****************')
    extract_05 = reserve_tb.query('"2016-10-13" <= checkout_date <= "2016-10-14"')
    print('extract_05', extract_05)

    # extract random 50% sampling ####################
    print('**************** random 50% sampling ****************')
    extract_06 = reserve_tb.sample(frac=0.5)
    print('extract_06', extract_06)

    # extract group by ID sampling ##################
    print('**************** group by ID sampling ****************')
    target = pd.Series(reserve_tb['customer_id'].unique()).sample(frac=0.5)
    extract_07 = reserve_tb[reserve_tb['customer_id'].isin(target)]
    print('extract_07', extract_07)


if __name__ == '__main__':
    main()
