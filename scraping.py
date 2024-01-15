from bs4 import BeautifulSoup
import requests
import bs4
import pandas as pd


# 12月の最高気温データを取得
res = requests.get('https://tenki.jp/amp/past/2023/12/weather/3/15/47682/')
soup = BeautifulSoup(res.text, 'html.parser')

# 'past-calender-box' クラスを持つdivを取得
div_tag = soup.find('div', class_='past-calender-box')

# 'past-calender-item' クラスを持つ全てのdivタグを取得
calenders_month_12 = div_tag.find_all('div', class_='past-calender-item')

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

# 'past-calender-item' クラスを持つ全てのdivタグを取得
calenders_month_1 = div_tag.find_all('div', class_='past-calender-item')

high_temp_month_1 = []
for item in calenders_month_1:
    # 各カレンダー要素から 'temp high-temp red' クラスを持つpタグを探す
    p_tag = item.find('p', class_='temp high-temp red')
    if p_tag:
        # タグが見つかればその文字列をリストに追加
        high_temp_month_1.append(p_tag.string)


# 12月と1月の最高気温データを結合
high_temp_lists = []

for temp in high_temp_month_12:
    joined_temp = ''.join(temp)
    high_temp_lists.append(joined_temp)

for temp in high_temp_month_1:
    joined_temp = ''.join(temp)
    high_temp_lists.append(joined_temp)

# print(high_temp_lists)


# 12月の最低気温データを取得
res = requests.get('https://tenki.jp/amp/past/2023/12/weather/3/15/47682/')
soup = BeautifulSoup(res.text, 'html.parser')

div_tag = soup.find('div', class_='past-calender-box')

# 'past-calender-item' クラスを持つ全てのdivタグを取得
calenders_month_12 = div_tag.find_all('div', class_='past-calender-item')

low_temp_month_12 = []
for item in calenders_month_12:
    # 各カレンダー要素から 'temp low-temp blue' クラスを持つpタグを探す
    p_tag = item.find('p', class_='temp low-temp blue')
    if p_tag:
        # タグが見つかればその文字列をリストに追加
        low_temp_month_12.append(p_tag.string)

# print(low_temp_month_12)


# 1月の最低気温を取得
res = requests.get('https://tenki.jp/amp/past/2024/01/weather/3/15/47682/')
soup = BeautifulSoup(res.text, 'html.parser')

# 'past-calender-box' クラスを持つdivを取得
div_tag = soup.find('div', class_='past-calender-box')

# 'past-calender-item' クラスを持つ全てのdivタグを取得
calenders_month_1 = div_tag.find_all('div', class_='past-calender-item')

low_temp_month_1 = []
for item in calenders_month_1:
    # 各カレンダー要素から 'temp high-temp red' クラスを持つpタグを探す
    p_tag = item.find('p', class_='temp low-temp blue')
    if p_tag:
        # タグが見つかればその文字列をリストに追加
        low_temp_month_1.append(p_tag.string)

# print(low_temp_month_1)


# 最低気温のデータを結合
low_temp_lists = []
for temp in low_temp_month_12:
    joined_temp = ''.join(temp)
    low_temp_lists.append(joined_temp)

for temp in low_temp_month_1:
    joined_temp = ''.join(temp)
    low_temp_lists.append(joined_temp)

# print(low_temp_lists)
