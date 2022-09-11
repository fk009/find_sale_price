import csv
import datetime
import os

# コンフィグのファイルパス
ini_folder_path = "./Yahoo_DATA/"

# フォルダを作成する処理
def create_folder_f():
    """
    フォルダを作成する処理
    """
    is_yahoofolder = os.path.exists(ini_folder_path)
    if not is_yahoofolder:
        os.mkdir(ini_folder_path)


# webスクレイピングの結果をCSVとして保存する処理
def data_save_CSV_f(godos_list, goodsName):
    """
    webスクレイピングの結果をCSVとして保存する処理
    """
    # 現在の年月日_時間
    date_nowtime = datetime.datetime.now()
    now = date_nowtime.strftime('%Y-%m-%d_%H-%M-%S')
    global ini_folder_path
    data_csv_path = ini_folder_path + now + "_" + goodsName  + ".csv"

    print("CSV出力")
    with open(data_csv_path, 'w') as f:
        header = ["title", "price", "when"]
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(godos_list)
    print("CSV完了")