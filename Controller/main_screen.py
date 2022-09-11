import copy
from tkinter import messagebox
import webbrowser # ウェブブラウザコントローラー

# サードパーティ
from matplotlib import pyplot as PLT # グラフなど作成
import numpy # 計算など

# 自作モジュール
from Controller import set_propety
from Model import data_save
from Model import web_Scraping as WS

# iniファイルをロードする
ini_road = set_propety.SettingProcessingClass()
# from View import ToolTip


# メイン画面　メソッドのクラス
class MainScreenProcessingClass():
    """
    メイン画面　メソッドのクラス
    """
    def __init__(self):
        self.Yahoo_scraping_list = []
        self.jumpURL = ""
        # Treeの行数
        self.TREE_ROWS = 30 # 仮初期値代入

        self.serch_goods_name = ""

    # Treeの再構築 リストを入れなおす関数
    def tree_rebuild_f(self, Yahoo_tree):
        """
        Treeの再構築 リストを入れなおす関数
        """

        try:
            # ツリーに値が存在する場合削除
            if len(Yahoo_tree.get_children()) >= 0:
                Yahoo_tree.delete(*Yahoo_tree.get_children())
            # ツリーに値を入れていく
            temp_tree_list = copy.deepcopy(self.Yahoo_scraping_list) # スクレイピングで取得したLIST
            for A in range(self.TREE_ROWS):
                # treeに入れる予定よりListが少ない場合は終了させる。
                if A <= len(temp_tree_list)-1:
                    temp_tree_list[A].insert(0,A+1)
                    Yahoo_tree.insert(parent = '', index = 'end', iid = A, values = temp_tree_list[A])
                else:
                    break
        except:
            print("Treeが存在しない:あるいは原因不明のエラー発生")
            exit()

    # 画面のラベル　総数・金額平均・金額中央値を計算して表示する処理
    def total_scraping_list_count_f(self, Yahoo_goods_count_label, Yahoo_mean_label, Yahoo_Median_label):
        """
        画面のラベル　総数・金額平均・金額中央値を表示する処理
        """

        Yahoo_goods_count_label["text"] = str(len(self.Yahoo_scraping_list)) # 総数

        # リストから金額だけを取得したリストを作成し、平均、中央値をそれぞれのラベルに入れる
        price_list = [self.Yahoo_scraping_list[x][1] for x in range(len(self.Yahoo_scraping_list))]
        price_numpylist = numpy.array(price_list)

        Yahoo_mean_label["text"] = round(numpy.mean(price_numpylist), 1) # 小数点以下２まで切り捨て、金額の平均を入れる
        Yahoo_Median_label["text"] = round(numpy.median(price_numpylist), 1) # 小数点以下２まで切り捨て、金額の中央値を入れる

    # 検索したYahooのページを開く
    def Yahoo_jumpURL_btn_f(self):
        """
        検索したYahooのページを開くボタン
        """

        print("ジャンプURLボタン")
        if len(self.jumpURL) != 0:
            webbrowser.open(self.jumpURL, new=0, autoraise=True)

    # 『検索』ボタンを押したときの処理
    def Yahoo_goods_search_btn_f(self, Yahoo_tree, Yahoo_goods_name_txt, Yahoo_goods_count_label, Yahoo_mean_label, Yahoo_Median_label):
        """
        『検索』ボタンを押したときの処理　webスクレイピングを行い、Treeに値を入れる。
        """
        # 検索したグッズの名前を変数に記録
        self.serch_goods_name = Yahoo_goods_name_txt.get()

        # セッティングファイルの値を入れる
        self.TREE_ROWS , state, godpagenum = map(int, ini_road.read_configfile_f())

        print("商品検索ボタン")
        gettext = Yahoo_goods_name_txt.get()

        if len(gettext) == 0:
            return

        self.TreeView = Yahoo_tree # tree.bindのeventではウィジェットを渡せないため

        # WEBスクレイピング開始
        scraping_list, self.jumpURL =  WS.yahoo_scraping_f(gettext, state, godpagenum)

        # 一つ上のローカル変数に値を渡す
        self.Yahoo_scraping_list = scraping_list.values.tolist()

        self.tree_rebuild_f(Yahoo_tree)
        self.total_scraping_list_count_f(Yahoo_goods_count_label, Yahoo_mean_label, Yahoo_Median_label)

    # 『グラフボタン』を押したとき Treeのデータから棒グラフを作成
    def Yahoo_graph_btn_f(self, Yahoo_tree):
        """
        『グラフボタン』を押したとき Treeのデータから棒グラフを作成
        """

        print("グラフボタン")
        x = Yahoo_tree.get_children()
        # 現在のデータを配列に入れる
        tree_list = []
        for item in x:
                tree_list.append(Yahoo_tree.item(item, 'values'))
        tree_list.sort(key=lambda x: x[3]) # 日付古い順
        # ('番号', '商品名', '値段', '日付')　'2022-07-23 23:08:00'

        # x軸とy軸用のデータを入れていく。
        plt_x, plt_y = [], []
        for A in tree_list[:]:
            plt_x.append(A[3]) # '2022-02-23', '2022-03-23',
            plt_y.append(int(A[2]))

        # データをグラフにする
        PLT.plot(plt_x, plt_y)
        PLT.xticks(rotation=45) # X軸の名称を斜めにする
        PLT.tight_layout()
        PLT.rcParams["font.size"] = 7
        PLT.show()

    # 『保存ボタン』を押したとき
    def Yahoo_save_btn_f(self):
        """
        スクレイピングしたリストをCSVとして保存する処理
        """
        print("保存ボタン")
        # リストに何もなければ、処理しない。
        if self.serch_goods_name == "":
            return

        # メッセージで保存するかどうかを確認
        ret = messagebox.askyesno(title="保存確認",
                                message="スクレイピングで取得したデータを保存しますか？"
                                )
        if ret:
            data_save.data_save_CSV_f(self.Yahoo_scraping_list, self.serch_goods_name)

    # 『ソートボタン』を押したときの処理
    def Yahoo_sort_f(self,btnid, Yahoo_tree):
        """
        『ソートボタン』を押したときの処理

        Treeをソートする
        0 値段ソート（安い） 1 値段ソート（高い） 2 日付（古い） 3 日付（新しい）
        """

        print("ソートボタン")
        x = Yahoo_tree.get_children()
        # 現在のデータを配列に入れる
        tree_list = []
        for item in x:
                tree_list.append(Yahoo_tree.item(item, 'values'))
                # ツリーのデータを削除
                Yahoo_tree.delete(item)

       # 値によって処理を変える。
        #0 値段ソート（安い）　ボタン
        if btnid == 0:
            tree_list.sort(key=lambda x: int(x[2]))

        #1 値段ソート（高い）　ボタン
        if btnid == 1:
            tree_list.sort(key=lambda x: int(x[2]), reverse=True)

        #2 日付（古い）ソート　ボタン
        elif btnid == 2:
            tree_list.sort(key=lambda x: x[3])

        #3 日付（新しい）ソートボタン
        elif btnid == 3:
            tree_list.sort(key=lambda x: x[3], reverse=True)

        # ツリーに値を入れていく
        for A in range(len(tree_list)):
            Yahoo_tree.insert(parent = '', index = 'end', iid = A, values = tree_list[A])

    # Treeの行を選択すると、その行をMSGボックスで確認できる処理
    def select_tree_record_f(self, event):
        """
        選択したTree行をMSGで確認・削除もできる

        1.id 2.商品名 3.値段 4.売れた日
        """
        Yahoo_tree = self.TreeView

        # 選択行の判別
        record_id = Yahoo_tree.focus()
        # 選択行のレコードを取得
        record_values = Yahoo_tree.item(record_id, 'values')
        ret = messagebox.askyesno(title="この行を削除しますか？",
                                message="id： "+ record_values[0]
                                + "\n\n商品名： " + record_values[1]
                                + "\n\n値段： " + record_values[2]
                                + "\n\n売れた日： " + record_values[3]
                                )
        if ret:
            # 再確認MSGボックス
            ret_2 = messagebox.askyesno(title="再確認",
                                                message="本当にこの行を削除しますか？"
                                                + "\n\n商品名： " + record_values[1])
            if ret_2:
                self.Yahoo_scraping_list.pop(int(record_values[0]) - 1) # リストから削除
                self.tree_rebuild_f(Yahoo_tree) # Tree再構築









