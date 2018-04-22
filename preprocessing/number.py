import numpy as np

from preprocess.load_data.data_loader import load_hotel_reserve
customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

# calculate logarithm ################
print(reserve_tb['total_price'])
reserve_tb['total_price_log'] = \
        reserve_tb['total_price'].apply(lambda x: np.log(x / 1000 + 1))
print('calculate logarithm \n', reserve_tb['total_price_log'])

# calculate categorize ################
print(customer_tb['age'])
customer_tb['age_rank'] = \
  (np.floor(customer_tb['age']/10) * 10).astype('category')
print('caluculate categorize', customer_tb['age_rank'])

# calculate normalization ################
from sklearn.preprocessing import StandardScaler

reserve_tb['people_num'] = reserve_tb['people_num'].astype(float)
ss = StandardScaler()

result = ss.fit_transform(reserve_tb[['people_num', 'total_price']])

reserve_tb['people_num_normalized'] = [x[0] for x in result]
reserve_tb['total_price_normalized'] = [x[1] for x in result]

print('people_num_normalized \n', reserve_tb['people_num_normalized'])
print('total_price_normalized \n', reserve_tb['total_price_normalized'])


# complete missing data ################
from preprocess.load_data.data_loader import load_production_missing_num
production_miss_num = load_production_missing_num()

print(len(production_miss_num))
# complete by NaN
replace_none = production_miss_num.replace('None', np.nan,)
print('raplace_none \n', replace_none)
replace_dropna = production_miss_num.dropna(subset=['thickness'],)
print('replace_dropna \n', replace_dropna)
# coplete by constants
production_miss_num = load_production_missing_num()
production_miss_num = production_miss_num.replace('None', np.nan)
print(production_miss_num)
fillna_1 = production_miss_num['thickness'].fillna(1)
print('fillna \n', fillna_1)
# complete by mean
production_miss_num = load_production_missing_num()
production_miss_num = production_miss_num.replace('None', np.nan)
production_miss_num['thickness'] = \
  production_miss_num['thickness'].astype('float64')
thickness_mean = production_miss_num['thickness'].mean()
print('thickness mean', thickness_mean)
print('complete by mean', production_miss_num['thickness'].fillna(thickness_mean))
