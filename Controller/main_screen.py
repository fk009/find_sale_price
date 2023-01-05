"""メイン画面の処理をまとめたもの

Todo:
"""



import copy
from tkinter import messagebox
import webbrowser # ウェブブラウザコントローラー

# サードパーティ
from matplotlib import pyplot as PLT # グラフなど作成
import numpy # 計算など

# 自作モジュール
from controller import set_propety
from model import data_save
from model import web_Scraping

# iniファイルをロードする
ini_road = set_propety.SettingProcessingClass()
# from view import ToolTip


# メイン画面　メソッドのクラス
class MainScreenProcessingClass():
    """メイン画面のメソッドのクラス

    1.treeを再構築する
    2.検索したページを開く
    3.検索ボタンの処理
    4.グラフボタンの処理
    5.保存ボタンの処理
    6.ソートボタンの処理
    7.treeの行を選択したときにMSGボックスで確認できる処理

    Attributes:
        self.scraping_list(list): スクレイピングした結果を入れるリスト
        self.jumpURL(str): ジャンプできるようにURLを入れるための変数
        self.TREE_ROWS(int): ツリーに表示させる行数を決める変数
        self.serch_goods_name(str): 検索した商品名を入れるための変数
    """
    def __init__(self):
        self.scraping_list = []
        self.jumpURL = ""
        # Treeの行数
        self.TREE_ROWS = 30 # 仮初期値代入

        self.serch_goods_name = ""

    # Treeの再構築 リストを入れなおす関数
    def tree_rebuild_f(self, tree):
        """Treeの再構築 リストを入れなおす関数

        メイン画面のリストに値を入れなおす処理。行を削除したり、検索したりした場合に実行される。

        Args:
            tree(.!mainscreenviewclass.!frame.!frame4.!treeview): tkinterのツリー属性
        """

        try:
            # ツリーに値が存在する場合削除
            if len(tree.get_children()) >= 0:
                tree.delete(*tree.get_children())
            # ツリーに値を入れていく
            temp_tree_list = copy.deepcopy(self.scraping_list) # スクレイピングで取得したLIST
            for A in range(self.TREE_ROWS):
                # treeに入れる予定よりListが少ない場合は終了させる。
                if A <= len(temp_tree_list)-1:
                    temp_tree_list[A].insert(0,A+1)
                    tree.insert(parent = '', index = 'end', iid = A, values = temp_tree_list[A])
                else:
                    break
        except:
            print("Treeが存在しない:あるいは原因不明のエラー発生")
            exit()

    # 検索したYahooのページを開く
    def jumpURL_btn_f(self):
        """検索したYahooのページを開くボタン
        """

        print("ジャンプURLボタン")
        if len(self.jumpURL) != 0:
            webbrowser.open(self.jumpURL, new=0, autoraise=True)

    # 『検索』ボタンを押したときの処理
    def goods_search_btn_f(self, tree, goods_name_txt):
        """１．『検索』ボタンを押したときの処理　webスクレイピングを行い、Treeに値を入れる。　２，中央値などの計算。

        Args:
            tree(.!mainscreenviewclass.!frame.!frame4.!treeview): tkinterのツリー属性
            goods_name_txt(.!mainscreenviewclass.!frame.!frame.!entry): tkinterの入力テキストボックスの属性

        Returns:
            web_Scraping.yahoo_calculation_f: model/web_Scrapingの関数を呼び出し、その結果を返す。金額の平均、中央値の計算処理をする関数。
            ｛
                goods_count(str): 取得した商品の総数
                mean(numpy.float64): 商品の金額の平均
                Median(numpy.float64): 商品の金額の中央値
            ｝
        """


        # 検索したグッズの名前を変数に記録
        self.serch_goods_name = goods_name_txt.get()

        # セッティングファイルの値を入れる
        self.TREE_ROWS , state, godpagenum = map(int, ini_road.read_configfile_f())

        print("商品検索ボタン")
        gettext = goods_name_txt.get()

        if len(gettext) == 0:
            return

        self.TreeView = tree # tree.bindのeventではウィジェットを渡せないため

        # WEBスクレイピング開始
        scraping_list, self.jumpURL =  web_Scraping.yahoo_scraping_f(gettext, state, godpagenum)

        # 一つ上のローカル変数に値を渡す
        self.scraping_list = scraping_list.values.tolist()

        # リスト入れ直し
        self.tree_rebuild_f(tree)

        # 中央値などの計算した結果を返す。
        return web_Scraping.yahoo_calculation_f(self.scraping_list)


    # 『グラフボタン』を押したとき Treeのデータから棒グラフを作成
    def graph_btn_f(self, tree):
        """『グラフボタン』を押したとき Treeのデータから棒グラフを作成

        Args:
            tree(.!mainscreenviewclass.!frame.!frame4.!treeview): tkinterのツリー属性

        """

        print("グラフボタン")
        x = tree.get_children()
        # 現在のデータを配列に入れる
        tree_list = []
        for item in x:
                tree_list.append(tree.item(item, 'values'))
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
    def save_btn_f(self):
        """スクレイピングしたリストをCSVとして保存する処理

        リストに何もなければ保存しない。保存する場合は確認メッセージを表示する。
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
            data_save.data_save_CSV_f(self.scraping_list, self.serch_goods_name)

    # 『ソートボタン』を押したときの処理
    def sort_f(self,btnid, tree):
        """『ソートボタン』を押したときの処理

        それぞれのボタンを押すことで、その内容でソートを行う。
        0 値段ソート（安い） 1 値段ソート（高い） 2 日付（古い） 3 日付（新しい）

        Args:
            tree(.!mainscreenviewclass.!frame.!frame4.!treeview): tkinterのツリー属性

        """

        print("ソートボタン")
        x = tree.get_children()
        # 現在のデータを配列に入れる
        tree_list = []
        for item in x:
                tree_list.append(tree.item(item, 'values'))
                # ツリーのデータを削除
                tree.delete(item)

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
            tree.insert(parent = '', index = 'end', iid = A, values = tree_list[A])

    # Treeの行を選択すると、その行をMSGボックスで確認できる処理
    def select_tree_record_f(self, event):
        """選択したTree行をMSGで確認・削除もできる

        1.id 2.商品名 3.値段 4.売れた日
        """
        tree = self.TreeView

        # 選択行の判別
        record_id = tree.focus()
        # 選択行のレコードを取得
        record_values = tree.item(record_id, 'values')
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
                self.scraping_list.pop(int(record_values[0]) - 1) # リストから削除
                self.tree_rebuild_f(tree) # Tree再構築









