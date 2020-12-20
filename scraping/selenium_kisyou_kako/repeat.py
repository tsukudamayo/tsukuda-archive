import argparse

#パーサーのインスタンスを作成
parser = argparse.ArgumentParser(description='Example command')

#文字列を受け取る-sオプションを定義
parser.add_argument('-s', '--string', type=str, help='string to display', required=True)

#数値を受け取る-nオプションを定義
parser.add_argument('-n','--num',type=int, help='number of times repeatedly display the string', default=2 )

#引数をパースし、得られた値を変数に格納する
args = parser.parse_args()

#パースによって得られた値を扱う
print(args.string * args.num)  

