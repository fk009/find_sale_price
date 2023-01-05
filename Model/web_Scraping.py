"""Webスクレイピングに関連する処理のモジュール

①中央値の計算処理
②webから情報を取ってきて、リストを作成する処理

Todo:
    yahoo意外でも取得できるように、改良する？

"""

import time

# サードパーティ
import bs4  # HTMLからデータを抽出
import pandas as pd # データ解析を容易にする機能を提供
import requests # URLで指定したサイトのデータを取得
import numpy # 計算など

# 中央値などの計算処理
def yahoo_calculation_f(scraping_list):
    """画面のラベル　総数・金額平均・金額中央値を計算する処理

    Args:
        scraping_list(list): webスクレイピングで取得したリスト。 タイトル、金額、タイムスタンプが入っている。
    
    Returns:
        goods_count(str): 取得した商品の総数
        mean(numpy.float64): 商品の金額の平均
        Median(numpy.float64): 商品の金額の中央値

    """

    # リストから金額だけを取得したリストを作成し、平均、中央値をそれぞれのラベルに入れる
    price_list = [scraping_list[x][1] for x in range(len(scraping_list))]
    price_numpylist = numpy.array(price_list)

    mean = round(numpy.mean(price_numpylist), 1) # 小数点以下２まで切り捨て、金額の平均を入れる
    Median = round(numpy.median(price_numpylist), 1) # 小数点以下２まで切り捨て、金額の中央値を入れる

    goods_count = str(len(scraping_list)) # 総数

    return goods_count, mean, Median


# webから情報を取ってきて、リストを作成する。 １．タイトル　２．値段　３．timestamp
def yahoo_scraping_f(goods_name, state_num, godpage_num):
    """ヤフオクのwebから情報を取ってきてリストを作成

    Args:
        goods_name(str): 検索した商品名
        state_num(int): 商品の状態（新品か中古か両方か）
        godpage_num(int): 取得する商品数（１P = 100）

    Returns:
        Pand_data(pandas.core.frame.DataFrame): タイトル　２．値段　３．timestampが入ったリスト
        JUMP_URL(str): スクレイピングに使用したサイトのURL

    """
    #-----------------------------------------
    goods_name_word = goods_name    # 商品の検索名
    quality_status = str(state_num)     # istatus=0がすべて、istatus=1が未使用、istatus=2が中古を表す
    goods_count = godpage_num * 100  # 商品の件数　1ページ = 100

    # サイト確認用URL
    JUMP_URL = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=" + goods_name_word + "&istatus=" + quality_status + "&b=1&n=100"

    # スクレイピングしてきたデータを入れるリスト
    scraping_list = {"title":[], "price":[], "when":[]}
    #-----------------------------------------


    # 過去に売れた商品がのってあるページを、指定した分だけ繰り返して取得する。
    for page in range(1, goods_count, 100):
        yahoo_URL = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=" + goods_name_word + "&istatus=" + quality_status + "&b=" + str(page) + "&n=100"
        r = requests.get(yahoo_URL, timeout=(3,3))  # rの中にURL先で取得したサイトのデータを格納する
        soup = bs4.BeautifulSoup(r.text, "html.parser") # 「html.parser」… HTMLの開始タグ、終了タグを発見したり、属性を抽出したりできる。 （HTMLデータ）
        products =soup.find_all("li",{"class":"Product"}) # li product タグを探し出して取り出す
        print("取得データ ", len(products))

        if len(products) <= 0:
            print(str(page) + " 商品がないため処理のストップ")
            break

        time.sleep(2)   # サイトへの負荷を逃すため

        # 取得したデータをリストへ格納していく。
        for product in products:
            goods_Title = product.find("a",{"class":"Product__titleLink"}).text
            price = product.find("span",{"class":"Product__priceValue"}).text
            when = product.find("span",{"class":"Product__time"}).text
            price = price.replace("円","")
            price = price.replace(",","")

            # データを入れる
            scraping_list["title"].append(goods_Title)
            scraping_list["price"].append(int(price))
            scraping_list["when"].append(when)

    Pand_data = pd.DataFrame(scraping_list)
    print("収集完了")

    return Pand_data, JUMP_URL


# import datetime
# データセットの成形 現在の年を取ってきてくっつける処理
# def set_yrar_in_tree_f(DATA):
#     """
#     Treeの行を年表記に変える処理
#     """

#     # 今の年度取得
#     DateTime = datetime.datetime.now()
#     date = DateTime.date()
#     NEN = date.strftime("%Y")
#     print(DATA)

#     DATA[NEN] = NEN
#     DATA['timestamp'] = DATA[NEN] + DATA['when']
#     stamp = DATA['timestamp']
#     nentukihi = [pd.to_datetime(date,format = '%Y%m/%d %H:%M') for date in stamp]
#     DATA['timestamp'] = nentukihi
#     df_sample = DATA.drop(['when',NEN], axis = 1)


#     return df_sample














