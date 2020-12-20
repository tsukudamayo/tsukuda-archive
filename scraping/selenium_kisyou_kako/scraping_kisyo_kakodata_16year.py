from selenium import webdriver
import pandas as pd
import datetime
import argparse

#コマンドラインにて実行時に引数を渡すための全国の気象観測地を表すURL内のパラメータ
sapporo   =    'prec_no=14&block_no=47412' 
aomori    =    'prec_no=31&block_no=47575' 
sendai    =    'prec_no=34&block_no=47590' 
nigata    =    'prec_no=54&block_no=47604' 
nagano    =    'prec_no=48&block_no=47610' 
tokyo     =    'prec_no=44&block_no=47662' 
sizuoka   =    'prec_no=50&block_no=47656' 
kanazawa  =    'prec_no=56&block_no=47605' 
nagoya    =    'prec_no=51&block_no=47636' 
osaka     =    'prec_no=62&block_no=47772' 
wakayama  =    'prec_no=65&block_no=47777' 
tottori   =    'prec_no=69&block_no=47746' 
kochi     =    'prec_no=74&block_no=47893' 
fukuoka   =    'prec_no=82&block_no=47807' 
kagoshima =    'prec_no=88&block_no=47827' 
naha      =    'prec_no=91&block_no=47936' 

#コマンドラインオプションを定義
parser = argparse.ArgumentParser(description='2000-2016 Weather data get from web')

parser.add_argument('sapporo',type=str, help='get data at sapporo')
parser.add_argument('aomori',type=str, help='get data at aomori')
parser.add_argument('sendai',type=str, help='get data at sendai')
parser.add_argument('nigata',type=str, help='get data at nigata')
parser.add_argument('nagano',type=str, help='get data at nagano')
parser.add_argument('tokyo',type=str, help='get data at tokyo')
parser.add_argument('sizuoka',type=str, help='get data at sizuoka')
parser.add_argument('kanazawa',type=str, help='get data at kanazawa')
parser.add_argument('nagoya',type=str, help='get data at nagoya')
parser.add_argument('osaka',type=str, help='get data at osaka')
parser.add_argument('wakayama',type=str, help='get data at wakayama')
parser.add_argument('tottori',type=str, help='get data at tottori')
parser.add_argument('kochi',type=str, help='get data at kochi')
parser.add_argument('fukuoka',type=str, help='get data at fukuoka')
parser.add_argument('kagoshima',type=str, help='get data at kagoshima')
parser.add_argument('naha',type=str, help='get data at naha')

args = parser.parse_args()
print(args)

#スクレイピングの開始
driver = webdriver.Firefox()

for year in range(2000,2017):
    for month in range(1,13):
        #url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=14&block_no=47412&year="+str(year)+"&month="+str(month)+"&day=&view="
        url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?"+str(argv)+"&year="+str(year)+"&month="+str(month)+"&day=&view="
        driver.get(url)
        df = pd.io.html.read_html(url)
        print(df[0])
        data = df[0]
        #日付順にファイルが作成されなかったため以下の1行をコメントアウト
        #data.to_csv("kisyou_kako_data_"+str(year)+"_"+str(month)+".csv")
        data.to_csv(datetime.date(year,month,1).strftime('%Y-%m-%d') +".csv")
