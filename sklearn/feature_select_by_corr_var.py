import sys
import pandas as pd

from sklearn.datasets import load_iris


def select_feature_by_corr_var(df, n_components=3):
    """ 
    input:
        df : pandas dataframe
        n_components: the number of feature columns which you want to select

    output:
        df: pandas dataframe which selected feature
    """

    print('**************** correration ****************')
    print(df.corr())
    
    corr_dicts = {}
    for i in df.corr().__iter__():
        print(i)
        for j, row in df.corr().iterrows():
            print(j)
            corr_x_y = (i, j)
            current_df = df.corr()[i][j]
            corr_dict = {corr_x_y: current_df}
            corr_dicts.update(corr_dict)

    for k, v in sorted(corr_dicts.items(), key=lambda x: -x[1]):
        print(str(k) + ' : ' + str(v))

    print('**************** variance ****************')
    columns_list = list(df.columns)
    print(columns_list)
    
    print(df.var())
    df_var = df.var()
    for k, v in sorted(corr_dicts.items(), key=lambda x: -x[1]):
        if v == 1.0:
            pass
        else:            
            print(k)
            print(k[0], df_var[k[0]])
            print(k[1], df_var[k[1]])
            
            if df_var[k[0]] > df_var[k[1]]:
                try:
                    columns_list.remove(k[1])
                except ValueError:
                    pass
            elif df_var[k[0]] < df_var[k[1]]:
                try:
                    columns_list.remove(k[0])
                except ValueError:
                    pass
            else:
                pass
            print(columns_list)
            
        if len(columns_list) == n_components:
            break
        elif len(columns_list) < 1:
            print('n_components=0 is invalid value')
            sys.exit(1)
            
    df = df[columns_list]

    return df


def main():
    data_set = load_iris()
    df = pd.DataFrame(data_set.data, columns=data_set.feature_names)
    print(df.head())
    select_df = select_feature_by_corr_var(df)
    print(select_df)
    print(select_df.shape)
    


if __name__ == '__main__':
    main()
