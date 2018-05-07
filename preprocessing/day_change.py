# _*_ coding: utf-8 _*
import gc
import pandas as pd


def day_change_fn(df, date,  date_time_column):
    """ countup date when time is 00:00:00 """
    new_date = []
    date = int(date)
    for idx, row in df.iterrows():
        print(row)
        if sum([int(y) for y in row['_time'].split(':')]) == 0:
            date += 1
        else:
            pass
        new_date.append(date)
        
    df['_date'] = pd.DataFrame(new_date)

    df[date_time_column] = df[['_date', '_time']]\
      .apply(lambda x: '{} {}'.format(str(x[0]), str(x[1])), axis=1)

    df = df.drop(columns=['_date', '_time'])
    gc.collect()

    return df


def main():
    fname = '20180507.csv'
    date = fname[0:8]
    df = pd.read_csv(fname, header=None)
    df.columns = ['_time']
    conv_df = day_change_fn(df, date, 'Time')
    print(conv_df)


if __name__ == '__main__':
    # main
    main()
