"""webスクレイピングの結果をCSVとして保存する処理

Attributes:
    CONFIG_FOLDER_PATH(str): セッティングフォルダのパス

Todo:

"""

import csv
import datetime
import os

# コンフィグのフォルダのパス
CONFIG_FOLDER_PATH = os.path.dirname(__file__).rstrip("model")
CONFIG_FOLDER_PATH = os.path.join(CONFIG_FOLDER_PATH, "DATA\\")


# フォルダを作成する処理
def create_folder_f():
    """フォルダを作成する処理

    Attributes:
        is_yahoofolder(bool):フォルダが存在するかを確認 Trueならそのまま　Falseなら新たに作成

    """
    is_yahoofolder = os.path.exists(CONFIG_FOLDER_PATH)
    if not is_yahoofolder:
        os.mkdir(CONFIG_FOLDER_PATH)


# webスクレイピングの結果をCSVとして保存する処理
def data_save_CSV_f(godos_list, goodsName):
    """webスクレイピングの結果をCSVとして保存する処理
    
    Attributes:
        CONFIG_FOLDER_PATH(str): 設定フォルダのパス
        data_csv_path(str): CSVを出力する場所

    """
    # 現在の年月日_時間
    date_nowtime = datetime.datetime.now()
    now = date_nowtime.strftime('%Y-%m-%d_%H-%M-%S')
    global CONFIG_FOLDER_PATH
    data_csv_path = CONFIG_FOLDER_PATH + now + "_" + goodsName  + ".csv"

    print("CSV出力")
    with open(data_csv_path, 'w') as f:
        header = ["title", "price", "when"]
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(godos_list)
    print("CSV完了")