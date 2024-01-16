from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

res = requests.get('https://tenki.jp/amp/past/2023/12/weather/3/15/47682/')
soup = BeautifulSoup(res.text, 'html.parser')

# 'past-calender-box' クラスを持つdivを取得
div_tag = soup.find('div', class_='past-calender-box')

# 'past-calender-item' クラスを持つ全てのdivタグを取得
calenders_month_12 = div_tag.select('div.past-calender-item:not(.past)')

high_temp_month_12 = []
for item in calenders_month_12:
    # 各カレンダー要素から 'temp high-temp red' クラスを持つpタグを探す
    p_tag = item.find('p', class_='temp high-temp red')
    if p_tag:
        # タグが見つかればその文字列をリストに追加
        high_temp_month_12.append(p_tag.string)

# 1月の最高気温を取得
res = requests.get('https://tenki.jp/amp/past/2024/01/weather/3/15/47682/')
soup = BeautifulSoup(res.text, 'html.parser')

# 'past-calender-box' クラスを持つdivを取得
div_tag = soup.find('div', class_='past-calender-box')

# CSSセレクタを使用して 'past-calender-item' クラスのみを持つdivタグを取得
calenders_month_1 = div_tag.select('div.past-calender-item:not(.past)')

high_temp_month_1 = []
for item in calenders_month_1:
    # 各カレンダー要素から 'temp high-temp red' クラスを持つpタグを探す
    p_tag = item.find('p', class_='temp high-temp red')
    if p_tag:
        # タグが見つかればその文字列をリストに追加
        high_temp_month_1.append(p_tag.get_text())


# 12月と1月の最高気温データを結合
high_temp_list = []

for temp in high_temp_month_12:
    joined_temp = ''.join(temp)
    high_temp_list.append(joined_temp)

for temp in high_temp_month_1:
    joined_temp = ''.join(temp)
    high_temp_list.append(joined_temp)
    
high_temp_list = high_temp_list[12:45]


# 12月の最低気温データを取得
res = requests.get('https://tenki.jp/amp/past/2023/12/weather/3/15/47682/')
soup = BeautifulSoup(res.text, 'html.parser')

div_tag = soup.find('div', class_='past-calender-box')

# 'past-calender-item' クラスを持つ全てのdivタグを取得
calenders_month_12 = div_tag.select('div.past-calender-item:not(.past)')

low_temp_month_12 = []
for item in calenders_month_12:
    # 各カレンダー要素から 'temp low-temp blue' クラスを持つpタグを探す
    p_tag = item.find('p', class_='temp low-temp blue')
    if p_tag:
        # タグが見つかればその文字列をリストに追加
        low_temp_month_12.append(p_tag.string)


# 1月の最低気温を取得
res = requests.get('https://tenki.jp/amp/past/2024/01/weather/3/15/47682/')
soup = BeautifulSoup(res.text, 'html.parser')

# 'past-calender-box' クラスを持つdivを取得
div_tag = soup.find('div', class_='past-calender-box')

# 'past-calender-item' クラスを持つ全てのdivタグを取得
calenders_month_1 = div_tag.select('div.past-calender-item:not(.past)')

low_temp_month_1 = []
for item in calenders_month_1:
    # 各カレンダー要素から 'temp high-temp red' クラスを持つpタグを探す
    p_tag = item.find('p', class_='temp low-temp blue')
    if p_tag:
        # タグが見つかればその文字列をリストに追加
        low_temp_month_1.append(p_tag.string)


# 最低気温のデータを結合
low_temp_list = []
for temp in low_temp_month_12:
    joined_temp = ''.join(temp)
    low_temp_list.append(joined_temp)

for temp in low_temp_month_1:
    joined_temp = ''.join(temp)
    low_temp_list.append(joined_temp)
    
# 不要なデータを削除
low_temp_list = low_temp_list[12:45]

# pandas を使用して sleep_time データをリストに変換
df = pd.read_csv('./dspro_last_assignment_local_data.csv')
date_list = df['日付']
sleep_time_list = df['睡眠時間']

# データベースへの接続
path = './'
db_name = 'database.sqlite'
con = sqlite3.connect(path + db_name, detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()

# テーブルの作成
sql_create_table_database = '''
CREATE TABLE IF NOT EXISTS database (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME,
    high_temp REAL,
    low_temp REAL,
    sleep_time REAL
);
'''
cur.execute(sql_create_table_database)

# データを挿入するSQL
sql_insert = "INSERT INTO database (date, high_temp, low_temp, sleep_time) VALUES (?, ?, ?, ?)"

# 各リストからデータを組み合わせて挿入
for i in range(len(sleep_time_list)):
    # 各リストからデータを取得    
    date = date_list[i]
    # date = datetime.datetime.strptime('2023/12/13', '%Y/%m/%d')
    high_temp = float(high_temp_list[i].replace('℃', '')) if i < len(high_temp_list) else None
    low_temp = float(low_temp_list[i].replace('℃', '')) if i < len(low_temp_list) else None
    sleep_time = sleep_time_list[i]

    # データを挿入
    cur.execute(sql_insert, (date, high_temp, low_temp, sleep_time))

# コミット処理
con.commit()

# DB接続を閉じる
con.close()




