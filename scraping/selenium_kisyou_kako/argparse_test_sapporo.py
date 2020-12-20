#コマンドラインオプションテスト
import argparse
sapporo   =    'prec_no=14&block_no=47412' 
aomori    =    'prec_no=31&block_no=47575' 
parser = argparse.ArgumentParser(description='2000-2016 Weather data get from web')
parser.add_argument('-sapporo',type=str, help='get data at sapporo'#, action="store_true"
        )
parser.add_argument('-aomori',type=str, help='get data at aomori'#, action="store_true"
        )
args = parser.parse_args()
if (args == sapporo):
    print(args)
elif(args == aomori):
    print(args)
