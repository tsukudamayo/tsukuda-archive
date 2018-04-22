from preprocess.load_data.data_loader import load_hotel_reserve
import pandas as pd
customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

print(customer_tb['sex'])

# convert boolean by not using astype()
customer_tb[['sex_is_man']] = (customer_tb[['sex']] == 'man').astype('bool')
print(customer_tb[['sex_is_man']])

customer_tb['sex_c'] = \
  pd.Categorical(customer_tb['sex'], categories=['man', 'woman'])
print(customer_tb['sex_c'])

customer_tb['sex_c'] = customer_tb['sex_c'].astype('category')
print(customer_tb['sex_c'])

print('index data', customer_tb['sex_c'].cat.codes)
print('master', customer_tb['sex_c'].cat.categories)


# get dummy vaiables ################
customer_tb['sex'] = pd.Categorical(customer_tb['sex'])
print(customer_tb['sex'])
dummy_vars = pd.get_dummies(customer_tb['sex'], drop_first=False)
print('dummy variables \n', dummy_vars)


# aggregate category ################
import pandas as pd
import numpy as np
from preprocess.load_data.data_loader import load_hotel_reserve
customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()

# convert category
customer_tb['age_rank'] = \
  pd.Categorical(np.floor(customer_tb['age']/10)*10)
print(customer_tb['age_rank'])
# add over60 category
customer_tb['age_rank'] = customer_tb['age_rank'].cat.add_categories(['over_60'])
print('add over60 category', customer_tb['age_rank'])
print('add over60 category', customer_tb['age_rank'].cat.categories)
# convert data aggreageted
customer_tb.loc[customer_tb['age_rank']\
                .isin([60.0, 70.0, 80.0]), 'age_rank'] = 'over_60'
print('convert data aggreageted', customer_tb)
# delete master data which not using
customer_tb['age_rank'].cat.remove_unused_categories(inplace=True)

# combine category ################
customer_tb['sex_and_age'] = pd.Categorical(
    customer_tb[['sex', 'age']]
      .apply(lambda x: '{}_{}'.format(int(np.floor(x[1]/10)*10), x[0]),
             axis=1)
)
print('combine category \n', customer_tb['sex_and_age'])


# generate numerical category ################
from preprocess.load_data.data_loader import load_production
production = load_production()
# a number of faults for each type
fault_cnt_per_type = production\
  .query('fault_flg')\
  .groupby('type')['fault_flg']\
  .count()
print('a number of fault for each type \n', fault_cnt_per_type)
# a number of products for each type
type_cnt = production.groupby('type')['fault_flg'].count()

production['type_fault_rate'] = production[['type', 'fault_flg']]\
  .apply(lambda x: (fault_cnt_per_type[x[0]] - int(x[1])) / (type_cnt[x[0]] - 1),
         axis=1)
print('a number of products for each type \n', production['type_fault_rate'])

# complete by knn ################
from sklearn.neighbors import KNeighborsClassifier
from preprocess.load_data.data_loader import load_production_missing_category
production_missc_tb = load_production_missing_category()
# conv None -> nan
production_missc_tb.replace('None', np.nan, inplace=True)
# extract not missing datan
train = production_missc_tb.dropna(subset=['type'], inplace=False)
print('not missing data \n', train)
# extract missing data
test = production_missc_tb\
  .loc[production_missc_tb.index.difference(train.index), :]
print('missing data \n', test)
# generate knn model
knn = KNeighborsClassifier(n_neighbors=3)
# train knn
knn.fit(train[['length', 'thickness']], train['type'])
# complete type by predicton of knn
test['type'] = knn.predict(test[['length', 'thickness']])
print('result \n', test['type'])


