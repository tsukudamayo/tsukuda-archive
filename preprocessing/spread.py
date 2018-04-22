import pandas as pd
from preprocess.load_data.data_loader import load_hotel_reserve

# load dataset
customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()
# print('customer_tb \n', customer_tb)
# print('hotel_tb \n', hotel_tb)
print('reserve_tb \n', reserve_tb)

# convert held horizontally data to held verically data using pivot table #####
pivot_sample = pd.pivot_table(reserve_tb,
                              index='customer_id',
                              columns='people_num',
                              values='reserve_id',
                              aggfunc=lambda x: len(x), fill_value=0)
print('convert held horizontally data to held verically data using pivot table',
      pivot_sample)


# generate sparse matrix ########################################
from scipy.sparse import csc_matrix


cnt_tb = reserve_tb\
  .groupby(['customer_id', 'people_num'])['reserve_id'].size()\
  .reset_index()
cnt_tb.columns = ['customer_id', 'people_num', 'rsv_cnt']

# convert sparse matrix to Categorical
customer_id = pd.Categorical(cnt_tb['customer_id'])
people_num = pd.Categorical(cnt_tb['people_num'])
print('convert sparse matrix to Categorical customer_id \n', customer_id)
print('convert sparse matrix to Categorical people_num \n', people_num)

# generate sparse matrix
generate_sparse_matrix = csc_matrix(
    (cnt_tb['rsv_cnt'], (customer_id.codes, people_num.codes)),
    shape=(len(customer_id.categories), len(people_num.categories))
)
print('generate sparse matrix \n', generate_sparse_matrix)


