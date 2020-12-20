from selenium import webdriver
import pandas as pd

driver = webdriver.Firefox()

for i in range(1,13):
    url = "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=14&block_no=47412&year=2015&month="+str(i)+"&day=&view="
    driver.get(url)
    df = pd.io.html.read_html(url)
    print(df[0])
    data = df[0]
    data.to_csv("kisyou_kako_data_pandas"+str(i)+".csv")
