"""メイン画面に関するデザインなどの処理

Todo:

"""

import math
import os
from PIL import Image, ImageTk
import sys
import threading
import time
import tkinter
from tkinter import ttk
from tkinter import Toplevel

# 上の階層でもimprotできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 自作モジュール
from controller.main_screen import MainScreenProcessingClass
from controller.set_propety import SettingProcessingClass
from model import data_save

# 画像フォルダのパスを指定する変数
JPEG_FILE_PATH = os.path.dirname(__file__).rstrip("view")
JPEG_FILE_PATH = os.path.join(JPEG_FILE_PATH, "img\\zjpeg_ghost\\")


# メイン画面　デザイン・配置
class MainScreenViewClass(tkinter.Frame):
    """メイン画面　デザイン・配置 クラス

    Attributes:
        self.master(tkinter.Tk): tkinterのフレームに関するクラス
        self.funcMain(MainScreenProcessingClass): メイン画面の処理に関する機能のクラス
        self.funcPrpty(SettingProcessingClass): 設定画面の処理に関する機能のクラス
        self.scraping_function(LoadingViewClass): ローディング処理に関する機能のクラス
    """
    def __init__(self, master=None): # master=None 自分が親
        super().__init__(master) # 基底クラスのコンストラクタをオーバーライド

        self.master.minsize(width=600, height=600)# 画面サイズの設定　min max 両方で大きさが変更されなくする。
        self.master.maxsize(width=600, height=600)
        self.master.title('メイン画面') # 画面タイトルの設定

        # クラス変数にセッティングファンクションclassを入れる
        self.funcMain = MainScreenProcessingClass()        # メイン画面の処理クラス
        self.funcPrpty = SettingProcessingClass()   # 設定画面の処理クラス
        self.pack()
        self.create_widgets_main()

        self.scraping_function = ""

    # （メイン）上部フレーム関数
    def frame_upper_f(self, frame_upper, mean_label, Median_label, tree):
        """上部ウィジェットの配置・処理　デザイン

            Args:
                frame_upper(tkinter.Frame): メイン画面上部のwidgetをまとめるフレーム
                mean_label(tkinter.Label): 金額の平均値を入れるラベル
                Median_label(tkinter.Label): 金額の中央値を入れるラベル
                tree(tkinter.ttk.Treeview): メイン画面のテーブルのこと

            Attributes:
                goods_title_label(tkinter.Label): プログラムのタイトル
                URL_label(tkinter.Label): スクレイピングしたサイトのURL
                goods_name_txt(tkinter.Entry): 検索したい商品を入力するテキストボックス
                goods_Search_btn(tkinter.Button): 商品を検索するためのボタン
        """

        # タイトル　ラベル
        goods_title_label = tkinter.Label(self.frame_upper, text = "Yahoo！", font=("MSゴシック", "20", "bold")) #ラベルWidgetを生成
        goods_title_label.pack(pady=4)
        # サイトへジャンプするボタン
        URL_label = tkinter.Button(frame_upper, text = "サイトへジャンプ", relief="raised", bg="lightblue", font=("MSゴシック", "10")) #ラベルWidgetを生成
        URL_label["command"] =  lambda: self.funcMain.jumpURL_btn_f()
        URL_label.pack()
        # 商品名　テキストボックス
        goods_name_txt = tkinter.Entry(self.frame_upper, width = 70)
        goods_name_txt.insert(0, "")
        goods_name_txt.pack(side="left", padx=20)

        # 検索ボタン押したときのラベル書き換え処理
        def yahoo_goods_chenge_f(tree, goods_name_txt):
            """ウェブスクレイピング処理 ・ ラベル書き換え処理

                Attributes:
                    goods_count_label(tkinter.Label) :商品の総数
                    mean_label(tkinter.Label) :金額の平均値を入れるラベル
                    Median_label(tkinter.Label) :金額の中央値を入れるラベル
            """
            goods_count, mean, Median = self.funcMain.goods_search_btn_f(tree, goods_name_txt)
            # ラベルの書き換え処理
            self.goods_count_label["text"] = goods_count# 総数
            mean_label["text"] = mean # 小数点以下２まで切り捨て、金額の平均を入れる
            Median_label["text"] = Median # 小数点以下２まで切り捨て、金額の中央値を入れる

        # ウェブスクレイピング中はローディング画面を表示させる。
        self.scraping_function = lambda: yahoo_goods_chenge_f(tree, goods_name_txt)
        Loading_C = LoadingViewClass(self.ALL_frame, self.anime_canvas, self.scraping_function)

        # 商品検索　ボタン
        goods_Search_btn = tkinter.Button(self.frame_upper, text='検索', width=6, height=1)
        goods_Search_btn["command"] = lambda: Loading_C.start_loading_f()
        goods_Search_btn.pack(side="left")

        self.frame_upper.pack(ipady = 10)

    # （メイン）検索結果のフレーム
    def frame_search_total_f(self):
        """検索結果に関するラベルデザイン

            Attributes:
                self.frame_search_total(tkinter.Frame) :件数のwidgetをまとめるフレーム
                self.goods_count_label(tkinter.Label) :商品数に関するラベル
                goods_count_label_subject(tkinter.Label) :（件）を表示するラベル

        """

        self.goods_count_label.pack(side="left", padx=10)
        goods_count_label_subject = tkinter.Label(self.frame_search_total, text = "件") #ラベルWidgetを生成
        goods_count_label_subject.pack(side="left")

        self.frame_search_total.pack()

    # （メイン）項目フレーム
    def Koumoku_frame_f(self, mean_label, Median_label):
        """金額に関するラベルデザイン

            Args:
                mean_label(tkinter.Label): 金額の平均値を入れるラベル
                Median_label(tkinter.Label): 金額の中央値を入れるラベル

            Attributes:
                self.Koumoku_frame_left(tkinter.Frame) :平均、中央値のラベルをまとめるフレーム
        """
            # -----------（左）項目フレーム
        # 平均：　ラベル
        mean_label.pack(padx=5, side="left")
        mean_label_subject = tkinter.Label(self.Koumoku_frame_left, text = "平均値", font = (12),fg = "#4169e1") #ラベルWidgetを生成
        mean_label_subject.pack(padx=5, side="left")
        self.Koumoku_frame_left.pack(side="left", padx=110)
            # -----------（左）項目フレーム
            # -----------（右）項目フレーム
        # 中央値：　ラベル
        Median_label.pack(padx=5, side="left")
        Median_label_subject = tkinter.Label(self.Koumoku_frame, text = "中央値", font = (12),fg = "#4169e1") #ラベルWidgetを生成
        Median_label_subject.pack(padx=5, side="left")
        self.Koumoku_frame_Right.pack(side="left", padx=90)
            # -----------（右）項目フレーム
        self.Koumoku_frame.pack()

    # （メイン）テーブルフレーム
    def Table_frame_f(self, tree):
        """テーブル(tree)に関する設定　デザイン

            Args:
                tree(tkinter.ttk.Treeview): メイン画面のテーブルのこと

            Attributes:
                self.Table_frame(tkinter.Frame) :テーブルなどをまとめるフレーム
                Treestyle(ttk.Style) :ウィジェットのスタイル設定
                scrollbar(ttk.Scrollbar) :商品が画面のテーブル内に収まらないときのためのスクロールバー
        """


        # ツリーの文字の大きさを変更する
        Treestyle = ttk.Style()
        Treestyle.configure("Treeview.Heading", font=(4))

        # self.treeviewの生成
        tree.bind("<<TreeviewSelect>>", self.funcMain.select_tree_record_f)

        # 列の設定
        tree.column('#0',width=0, stretch='no')
        tree.column('ID', anchor='center', width=40)
        tree.column('name',anchor='w', width=300)
        tree.column('price',anchor='w', width=70)
        tree.column('timestamp', anchor='center', width=130)

        # 列の見出し設定
        tree.heading('#0',text='')
        tree.heading('ID', text='ID',anchor='center')
        tree.heading('name',text='商品名', anchor='w')
        tree.heading('price', text='値段（円）', anchor='w')
        tree.heading('timestamp',text='売れた日', anchor='center')

        # Treeにスクロールバーの追加
        scrollbar = ttk.Scrollbar(self.Table_frame, orient=tkinter.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # ウィジェットの配置
        tree.pack(pady=10)

        self.Table_frame.pack()

    # （メイン）ソートフレーム
    def Sort_btn_f(self, tree):
        """ソートに関するデザイン
        
            Args:
                tree(tkinter.ttk.Treeview): メイン画面のテーブルのこと

            Attributes:
                self.Sort_frame(tkinter.frame) :ソートボタンをまとめるframe
                LowPriceSort_btn(tkinter.Button) :値段の安い順にソートするボタン
                HighPriceSort_btn(tkinter.Button) :値段の高い順にソートするボタン
                OldTimeSort_btn(tkinter.Button) :日付の古い順にソートするボタン
                NewTimeSort_btn(tkinter.Button) :日付の新しい順にソートするボタン
        """

        # 値段（安い）ソート　ボタン
        LowPriceSort_btn = tkinter.Button(self.Sort_frame, text='値段（安い）ソート', width=14, height=1, bg="mediumseagreen")
        LowPriceSort_btn["command"] =lambda: self.funcMain.sort_f(0, tree)
        LowPriceSort_btn.pack(side="left", padx=15)

        # 値段（高い）ソート　ボタン
        HighPriceSort_btn = tkinter.Button(self.Sort_frame, text='値段（高い）ソート', width=14, height=1, bg="mediumseagreen")
        HighPriceSort_btn["command"] = lambda: self.funcMain.sort_f(1, tree)
        HighPriceSort_btn.pack(side="left", padx=15)

        # 日付（古い）ソート　ボタン
        OldTimeSort_btn = tkinter.Button(self.Sort_frame, text='日付（古い）ソート', width=16, height=1, bg="mediumseagreen")
        OldTimeSort_btn["command"] = lambda: self.funcMain.sort_f(2, tree)
        OldTimeSort_btn.pack(side="left", padx=15)

        # 日付（新しい）ソートボタン
        NewTimeSort_btn = tkinter.Button(self.Sort_frame, text='日付（新しい）ソート', width=16, height=1, bg="mediumseagreen")
        NewTimeSort_btn["command"] = lambda: self.funcMain.sort_f(3, tree)
        NewTimeSort_btn.pack(side="left", padx=15)

        self.Sort_frame.pack(pady=10)

    # （メイン）グラフボタンフレーム
    def graph_btn_f(self, tree):
        """グラフに関するデザイン

            Args:
                tree(tkinter.ttk.Treeview): メイン画面のテーブルのこと

            Attributes:
                self.graph_frame(tkinter.frame) :グラフに関するフレーム
                graph_btn(tkinter.Button) :テーブルに表示されているデータをグラフ化するボタン
        """
        # グラフボタン
        graph_btn = tkinter.Button(self.graph_frame, text='グラフ', width=50, height=2, bg="wheat", font=("", "12","bold"))
        graph_btn["command"] = lambda: self.funcMain.graph_btn_f(tree)
        graph_btn.pack(pady=10)

        self.graph_frame.pack(pady=10)

    # （メイン）設定ボタンフレーム
    def settingbtn_f(self):
        """設定、保存に関するデザイン

            Attributes:
                self.setting_frame(tkinter.frame) :設定、保存ボタンをまとめるframe
                setting_btn(tkinter.Button) :スクレイピングに関する設定ができるダイアログを表示するボタン
                save_btn(tkinter.Button) :スクレイピングしてきたデータをCSVとして出力、保存するボタン
        """

        # 設定ボタン
        setting_btn = tkinter.Button(self.setting_frame, text='設定', width=15, height=3, bg="gainsboro")
        setting_btn["command"] = lambda: self.create_widgets_property()
        setting_btn.pack(side="left", padx=50)

        # 保存ボタン
        save_btn = tkinter.Button(self.setting_frame, text='保存', width=15, height=3, bg="gainsboro")
        save_btn["command"] = lambda: self.funcMain.save_btn_f()
        save_btn.pack(side="left", padx=50)

        self.setting_frame.pack(pady=10)

    # メイン画面　ウィジェットの作成　デザイン
    def create_widgets_main(self):
        """ウィジェットの配置　デザイン
        Attributes:
            self.anime_canvas(tkinter.Canvas): ロード画面用キャンパス
            self.ALL_frame(tkinter.Frame): すべてのframeの親フレーム
            self.frame_upper(tkinter.Frame): 上部フレーム
            self.frame_search_total(tkinter.Frame): 検索総数フレーム
            self.Koumoku_frame(tkinter.Frame): 項目フレーム
            self.Koumoku_frame_left(tkinter.Frame): （左）項目フレーム
            self.Koumoku_frame_Right(tkinter.Frame): （右）項目フレーム
            self.Table_frame(tkinter.Frame): 直近Treeテーブルフレーム
            self.Sort_frame(tkinter.Frame): ソート　フレーム
            self.graph_frame(tkinter.Frame): グラフ　フレーム
            self.setting_frame(tkinter.Frame): 設定　フレーム

            self.goods_count_label(tkinter.Label): 件数　ラベル
            column(tuple):列の識別名を指定するためのもの
            tree(tkinter.ttk.Treeview): self.treeviewの生成
            mean_label(tkinter.Label): 平均値を表示するラベル
            Median_label(tkinter.Label): 中央値を表示するラベル
        """

        # ---frame
        self.anime_canvas = tkinter.Canvas(self, width=600, height=600, bg="white")
        self.ALL_frame = tkinter.Frame(self)
        self.frame_upper = tkinter.Frame(self.ALL_frame)
        self.frame_search_total = tkinter.Frame(self.ALL_frame)
        self.Koumoku_frame = tkinter.Frame(self.ALL_frame)
        self.Koumoku_frame_left = tkinter.Frame(self.Koumoku_frame)
        self.Koumoku_frame_Right = tkinter.Frame(self.Koumoku_frame)
        self.Table_frame = tkinter.Frame(self.ALL_frame)
        self.Sort_frame = tkinter.Frame(self.ALL_frame)
        self.graph_frame = tkinter.Frame(self.ALL_frame)
        self.setting_frame = tkinter.Frame(self.ALL_frame)

        # ---tkinterのWidget
        self.goods_count_label = tkinter.Label(self.frame_search_total, text = u"0", font = (14),fg = "#4169e1") #ラベルWidgetを生成
        column = ('ID', 'name', 'price', 'timestamp')
        tree = ttk.Treeview(self.Table_frame, columns = column)
        mean_label = tkinter.Label(self.Koumoku_frame_left, text = u"0", font = (12),fg = "#4169e1") #ラベルWidgetを生成
        Median_label = tkinter.Label(self.Koumoku_frame, text = "0", font = (12),fg = "#4169e1") #ラベルWidgetを生成

        # ---frameごとに関数を実行---
        self.frame_upper_f(self.frame_upper, mean_label, Median_label, tree)
        self.frame_search_total_f()
        self.Koumoku_frame_f(mean_label, Median_label)
        self.Table_frame_f(tree)
        self.Sort_btn_f(tree)
        self.graph_btn_f(tree)
        self.settingbtn_f()

       # ---------すべての親　フレーム
        self.ALL_frame.pack()


    # ------------------（ ↓ 設定ダイアログに関する処理）-----------------------------


    # （設定） ダイアログのサイズなどを指定
    def dialog_set_f(self):
        """ダイアログのサイズなどを指定する

            Attributes:
                self.dialog(tkinter.Toplevel): 設定画面のダイアログ
                self.setting_frame_Nothing(tkinter.Frame) :空フレーム（Widgetのデザインを整えるための空フレーム）
        """
        self.dialog.title("modal dialog")
        self.dialog.minsize(width=480, height=550)# 画面サイズの設定
        self.dialog.maxsize(width=480, height=550)
        # モーダルダイアログ（元画面を操作不可として表示）
        self.dialog.grab_set()

        # 空フレーム（Widgetのデザインを整えるための空フレーム）
        self.setting_frame_Nothing = tkinter.Frame(self.dialog)
        self.setting_frame_Nothing.pack(ipady = 20)

    # （設定） ダイアログフレーム（画面に表示させる商品の数）
    def setting_frame_goodsnum_f(self):
        """商品の数に関するデザイン　処理
            Attributes:
                self.setting_frame_goodsnum(tkinter.Frame) :商品数に関するものをまとめたフレーム
                setting_Tree_description_label(tkinter.Lavel) :説明が書かれたラベル
                setting_tree_scale(tkinter.Scale) :商品数を指定するためのスクロールバー
                setting_tree_Scale_btn(tkinter.Button) :押すと、スクロールバーをデフォルトの値で入れなおすためのボタン

            return:
                setting_tree_scale(tkinter.Scale): 商品数が指定された状態を返却

        """
        setting_Tree_description_label = tkinter.Label(self.setting_frame_goodsnum, font = (14),fg = "#4169e1") #ラベルWidgetを生成
        setting_Tree_description_label["text"] = "画面に表示させる商品の数を設定します"
        setting_Tree_description_label.pack()


        #Scaleの生成
        setting_tree_scale = tkinter.Scale(self.setting_frame_goodsnum, orient="horizontal", from_ = 10, to = 100, width = 20, length = 400)
        setting_tree_scale.set(self.tree_num)
        setting_tree_scale.pack()


        #Scale値を取得して表示するボタン
        setting_tree_Scale_btn = tkinter.Button(self.setting_frame_goodsnum, widt=20)
        setting_tree_Scale_btn["text"] = "デフォルトに戻す（30行）"
        setting_tree_Scale_btn["command"] = lambda : self.funcPrpty.tree_set_value(setting_tree_scale)
        setting_tree_Scale_btn.pack()

        self.setting_frame_goodsnum.pack(ipady = 20)

        return setting_tree_scale

    # （設定） ダイアログフレーム（商品の状態を指定）
    def setting_frame_status_f(self):
        """商品状態に関するデザイン

            Attributes:
                self.setting_frame_status(tkinter.Frame) :商品の状態に関するものをまとめたフレーム
                setting_status_description_label(tkinter.Lavel) :説明が書かれたラベル
                setting_status_description_sub_label(tkinter.Lavel) :補足説明が書かれたラベル
                setting_status_comb(ttk.Combobox) :０～２の数字が入ったコンボボックス

            return:
                setting_tree_scale(tkinter.Scale): 商品数が指定された状態を返却

        """
        setting_status_description_label = tkinter.Label(self.setting_frame_status, font = (14),fg = "#4169e1") #ラベルWidgetを生成
        setting_status_description_label["text"] = "商品の状態を設定できます"
        setting_status_description_label.pack()

        setting_status_description_sub_label = tkinter.Label(self.setting_frame_status, font = (9)) #ラベルWidgetを生成
        setting_status_description_sub_label["text"] = "0 がすべて、1 が未使用、2 が中古を表す"
        setting_status_description_sub_label.pack()

        # ドロップダウンボックス
        setting_status_comb = ttk.Combobox(self.setting_frame_status, state = 'readonly')
        setting_status_comb["values"] = ("0","1","2")
        setting_status_comb.current(self.state)
        setting_status_comb.pack()

        self.setting_frame_status.pack(ipady = 20)

        return setting_status_comb

    # （設定） ダイアログフレーム（スクレイピングするページ数）
    def setting_frame_scrapingPage_f(self):
        """スクレイピングするページ数に関する処理　デザイン

            Attributes:
                self.setting_frame_scrapingPage(tkinter.Frame) :ページ数に関するものをまとめたフレーム
                setting_scale_description_label(tkinter.Label) :説明が書かれたラベル
                setting_scale_description_sub_label(tkinter.Label) :補足説明が書かれたラベル
                setting_page_scale(tkinter.Scale) ::ページ数を指定するためのスクロールバー
                setting_page_Scale_btn(tkinter.Button) :押すと、スクロールバーをデフォルトの値で入れなおすためのボタン

            return:
                setting_page_scale(tkinter.Scale) :ページ数が指定された状態を返却

        """
        setting_scale_description_label = tkinter.Label(self.setting_frame_scrapingPage, font = (14),fg = "#4169e1") #ラベルWidgetを生成
        setting_scale_description_label["text"] = "スクレイピングで取得するページ数を設定できます"
        setting_scale_description_label.pack()

        setting_scale_description_sub_label = tkinter.Label(self.setting_frame_scrapingPage, font = (9)) #ラベルWidgetを生成
        setting_scale_description_sub_label["text"] = "ページが多いと、その分時間がかかります"
        setting_scale_description_sub_label.pack()

        #Scaleの生成
        setting_page_scale = tkinter.Scale(self.setting_frame_scrapingPage, orient="horizontal", from_ = 1, to = 10, width = 20, length = 230)
        setting_page_scale.set(self.goods_page_num)
        setting_page_scale.pack()

        #Scale値を取得して表示するボタン
        setting_page_Scale_btn = tkinter.Button(self.setting_frame_scrapingPage, widt=20)
        setting_page_Scale_btn["text"] = "デフォルトに戻す（2ページ）"
        setting_page_Scale_btn["command"] = lambda :  self.funcPrpty.page_set_value(setting_page_scale)
        setting_page_Scale_btn.pack()

        self.setting_frame_scrapingPage.pack(ipady = 20)

        return setting_page_scale

    # （設定）ダイアログフレーム（保存ボタン）
    def setting_frame_save_f(self, setting_tree_scale, setting_status_comb, setting_page_scale):
        """保存ボタンに関する処理　デザイン

            Args:
                setting_tree_scale(tkinter.Scale) :画面に表示させる商品数が入ったスクロールバー
                setting_status_comb(ttk.Combobox) :商品の状態が入ったコンボボックス
                setting_page_scale(tkinter.Scale) :ページ数が入ったスクロールバー

            Attributes:
                self.setting_frame_save(tkinter.Frame) :保存ボタンに関するものをまとめたフレーム
                setting_save_btn(tkinter.Button) :押すと設定値を保存するボタン
        """

        # ボタンを押すと、iniファイルに数値を保存する。
        setting_save_btn = tkinter.Button(self.setting_frame_save, widt = 20, height=1, text = "設定保存", bg = "lightyellow")
        setting_save_btn["command"] = lambda :  self.funcPrpty.setting_save_btn_f(setting_tree_scale.get(), setting_status_comb.get(), setting_page_scale.get(), self.dialog)
        setting_save_btn.pack(ipady = 30)

        self.setting_frame_save.pack(ipady = 20)

    # 設定画面　ウィジェットの作成　デザイン
    def create_widgets_property(self):
        """Widgetの配置　デザイン

        Attributes:
            self.dialog(tkinter.Toplevel): 設定画面のダイアログ
            self.setting_frame_goodsnum(tkinter.Frame): 画面に表示させる商品の数に関するフレーム
            self.setting_frame_status(tkinter.Frame): 商品の状態に関するフレーム
            self.setting_frame_scrapingPage(tkinter.Frame): スクレイピングするページ数に関するフレーム
            self.setting_frame_save(tkinter.Frame): 保存ボタンに関するフレーム

            self.tree_num(int): 画面に表示させる商品の数
            self.state(str): 商品の状態（0=すべて,1=に使用 ,2=中古）
            self.goods_page_num(int): スクレイピングするページ数

            setting_tree_scale(tkinter.Scale): 商品の数のスクロールバー
            setting_status_comb(ttk.Combobox): 商品の状態のコンボボックス
            setting_page_scale(tkinter.Scale): スクレイピングするページ数のスクロールバー
        """

        # ---frame
        self.dialog = Toplevel(self)
        self.setting_frame_goodsnum = tkinter.Frame(self.dialog)
        self.setting_frame_status = tkinter.Frame(self.dialog)
        self.setting_frame_scrapingPage = tkinter.Frame(self.dialog)
        self.setting_frame_save   = tkinter.Frame(self.dialog)

        # ---tkinterのWidget
        setting_tree_scale  = tkinter.Scale()
        setting_status_comb = ttk.Combobox()
        setting_page_scale  = tkinter.Scale()

        # ツリーの行数　状態数値　ページ数をiniファイルから取得する
        self.tree_num, self.state, self.goods_page_num = self.funcPrpty.read_configfile_f()
        self.tree_num = int(self.tree_num)
        self.state = str(self.state)
        self.goods_page_num = int(self.goods_page_num)

        # ---frameごとに関数を実行---
        self.dialog_set_f()
        setting_tree_scale  = self.setting_frame_goodsnum_f()
        setting_status_comb = self.setting_frame_status_f()
        setting_page_scale  = self.setting_frame_scrapingPage_f()
        self.setting_frame_save_f(setting_tree_scale, setting_status_comb, setting_page_scale)


# ローディング画像の処理クラス
class LoadingViewClass():
    """ローディング画像の処理クラス

    Webscraping中はロード画面を表示させる。

        Args:
            main_frame(tkinter.Frame) :メイン画面のフレーム
            anime_canvas(tkinter.Canvas) :ローディング画面の描画に使うキャンパス
            WEB_scraping_F(function) :関数『yahoo_goods_chenge_f』が入っている（ウェブスクレイピング処理 ・ ラベル書き換え処理）

        Attributes:
            self.is_processing(bool) :処理中かどうかを判定するためのもの(True ならローディング処理　 False なら終了)
            self.load_img_num(int) :ローディング画面に表示させるための、画像のナンバー
            self.loading_img(PIL.ImageTk.PhotoImage) : PhotoImage クラス tkinterで画像を使うためのクラス
            self.loading_time_text(str) :ローディング画面に表示させる、経過時間
            self.time_sta(float) :処理を初めてからの経過時間(秒)

    """
    def __init__(self, main_frame, anime_canvas, WEB_scraping_F) -> None:
        self.main_frame = main_frame # 一時的にウィジェットを非表示するときに使う
        self.anime_canvas = anime_canvas # ローディング画面の描画に使う
        self.WEB_scraping_F = WEB_scraping_F # ウェブスクレイピング処理を行う

        # クラス変数
        self.is_processing = False
        self.load_img_num = 0
        self.loading_img = None
        self.loading_time_text = ""
        self.time_sta = time.time()

    # ローディングアニメーションを描画する処理
    def draw_anime(self):
        """ローディング画面の描画に関する処理

        self.is_processing が True である限り、ローディング画面を表示する処理
        """

        # 処理中かどうかを判定
        if self.is_processing:

            # 切り替える画像の最後まで来たら、また初めの画像にする。
            if self.load_img_num > 26:
                self.load_img_num = 0
            else:
                self.load_img_num += 1

            # ローディングアニメーションの画像を読み込み
            load_jpeg = JPEG_FILE_PATH + "/Ghost-{}.jpg".format(str(self.load_img_num))
            self.loading_img = Image.open(load_jpeg)
            im_resize = self.loading_img.resize(size=(140,140)) # サイズ変更
            self.loading_img = ImageTk.PhotoImage(im_resize) # Tkinter用の画像に変換

            # ローディング中に表示させる時間 text
            time_end = time.time()
            now_time = math.floor(time_end) - math.floor(self.time_sta)
            self.loading_time_text = "ロード {} 秒経過".format(str(now_time))

            # Canvasに画像を描画
            self.anime_canvas.create_image(
                600/2,  # X座標：中心に描画されるように、Cnvasの幅を2で割る
                600/2,  # Y座標も同様
                image = self.loading_img,  # 描画する画像
            )

            # ロード時間の描画
            self.anime_canvas.delete("text") # 重なりを防ぐために一度消す
            self.anime_canvas.create_text(
                600/2, 150,  # 位置
                text = self.loading_time_text,  # 文字
                tag = "text",
                font = ("Times", 20, "bold")
            )
            # ローディング文字の描画_2
            self.anime_canvas.create_text(
                600/2, 450,  # 位置
                text="スクレイピング中！",  # 文字
                font = ("Times", 20, "bold")
            )

            # 50ミリ秒後にもう一度描画
            app.after(80, self.draw_anime)

        else:
            # 処理が終わっているならCanvasを非表示に
            self.anime_canvas.pack_forget()

    # アニメーション表示中に実際に処理を行う関数
    def process_f(self):
        """アニメーション表示中に実際に処理を行う関数

        Webscrapingをする処理を行っている。処理が終わり次第、メイン画面を表示させる。
        """
        self.is_processing = True

        self.WEB_scraping_F() # ウェブスクレイピング処理（これが終わるまでローディング画面のまま）
        self.main_frame.pack() # 上の処理が終われば、もう一度メイン画面を表示

        self.is_processing = False # 待ち合わせ用関数をFalseにすることによってアニメーションが止まる

    # ローディング画面表示 マルチプロセス処理
    def start_loading_f(self):
        """ローディング画面表示 マルチプロセス処理

        検索ボタンを押すと、この処理を最初に呼び出している。
        『self.process_f』と『self.draw_anime』を並列処理
        """
        self.main_frame.pack_forget() # ウェジットを非表示にする
        self.anime_canvas.pack() # canvas　表示

        # 処理を別スレッドで開始
        threading.Thread(target = self.process_f).start()
        self.time_sta = time.time() # ロード時間を図るために時間を入れる。
        # ループ開始
        app.after(0, self.draw_anime) # afterメソッド　送らせて繰り返し処理　


# フォルダ作成処理
data_save.create_folder_f()
#(Viewからはcontrollerの呼び出し)

# メイン画面を表示する
root = tkinter.Tk()
app = MainScreenViewClass(master=root)
app.mainloop()



