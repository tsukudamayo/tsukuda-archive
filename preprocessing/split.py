from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from preprocess.load_data.data_loader import load_production


# load dataset
production_tb = load_production()
print('load dataset \n', production_tb)

# to split holdout validation
train_data, test_data, train_target, test_target = train_test_split(
    production_tb.drop('fault_flg', axis=1),
    production_tb[['fault_flg']],
    test_size=0.2
)
print('train data \n', train_data)
print('test_data \n', test_data)
print('train target \n', train_target)
print('test target \n', test_target)

# reset_index
train_data.reset_index(inplace=True, drop=True)
test_data.reset_index(inplace=True, drop=True)
train_target.reset_index(inplace=True, drop=True)
test_target.reset_index(inplace=True, drop=True)

# generate list of number of lines
row_no_list = list(range(len(train_target)))

# to split cross validation
k_fold = KFold(n_splits=4, shuffle=True)
print('k_fold \n', k_fold)

# loop n_splits times
for train_cv_no, test_cv_no in k_fold.split(row_no_list):
    train_cv = train_data.iloc[test_cv_no, :]
    test_cv = train_data.iloc[test_cv_no, :]
    print('loop n_splits times train_cv \n', train_cv)
    print('loop n_splits times test_cv \n', test_cv)

    
# data in chronological order ##################################
from preprocess.load_data.data_loader import load_monthly_index
monthly_index_tb = load_monthly_index()

train_window_start = 1
train_window_end = 24
horizon = 12
skip = 12

monthly_index_tb.sort_values(by='year_month')

while True:
    print('train_window_start', train_window_start)
    print('train_window_end', train_window_end)
    test_window_end = train_window_end + horizon
    train = monthly_index_tb[train_window_start:train_window_end]
    test = monthly_index_tb[(train_window_end + 1):test_window_end]
    print('train \n', train)
    print('test \n', test)
    if test_window_end >= len(monthly_index_tb.index):
        break
    train_window_start += skip
    train_window_end += skip
