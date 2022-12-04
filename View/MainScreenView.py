
import math
import os
from PIL import Image, ImageTk
import sys
import tkinter
import threading
import time
from tkinter import ttk
from tkinter import Toplevel


# 上の階層でもimprotできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 自作モジュール
from Controller.main_screen import MainScreenProcessingClass
from Controller.set_propety import SettingProcessingClass
from Model import data_save

# メイン画面　デザイン・配置
class MainScreenViewClass(tkinter.Frame):
    """
    メイン画面　デザイン・配置 クラス
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

    # メイン画面　ウィジェットの作成　デザイン
    def create_widgets_main(self):
        """
        ウィジェットの配置　デザイン
        """

        # ロード画面用キャンパス
        self.anime_canvas = tkinter.Canvas(self, width=600, height=600, bg="white")

        # ---------すべての親　フレーム
        self.Yahoo_ALL_frame = tkinter.Frame(self)

        # -----------上部フレーム
        self.Yahoo_frame_upper = tkinter.Frame(self.Yahoo_ALL_frame)

        # タイトル　ラベル
        Yahoo_goods_count_label = tkinter.Label(self.Yahoo_frame_upper, text = "Yahoo！", font=("MSゴシック", "20", "bold")) #ラベルWidgetを生成
        Yahoo_goods_count_label.pack(pady=4)

        # ジャンプURL　ラベル
        Yahoo_URL_label = tkinter.Button(self.Yahoo_frame_upper, text = "サイトへジャンプ", relief="raised", bg="lightblue", font=("MSゴシック", "10")) #ラベルWidgetを生成
        Yahoo_URL_label["command"] =  lambda: self.funcMain.Yahoo_jumpURL_btn_f()
        Yahoo_URL_label.pack()

        # 商品名　テキストボックス
        Yahoo_goods_name_txt = tkinter.Entry(self.Yahoo_frame_upper, width = 70)
        Yahoo_goods_name_txt.insert(0, "")
        Yahoo_goods_name_txt.pack(side="left", padx=20)


        # 検索ボタン押したときの処理
        def yahoo_goods_chenge_f(Yahoo_tree, Yahoo_goods_name_txt):
            goods_count, Yahoo_mean, Yahoo_Median = self.funcMain.Yahoo_goods_search_btn_f(Yahoo_tree, Yahoo_goods_name_txt)
            # ラベルの書き換え処理
            Yahoo_goods_count_label["text"] = goods_count# 総数
            Yahoo_mean_label["text"] = Yahoo_mean # 小数点以下２まで切り捨て、金額の平均を入れる
            Yahoo_Median_label["text"] = Yahoo_Median # 小数点以下２まで切り捨て、金額の中央値を入れる

        # 商品検索　ボタン
        Yahoo_goods_Search_btn = tkinter.Button(self.Yahoo_frame_upper, text='検索', width=6, height=1)
        # ウェブスクレイピング中はローディング画面を表示させる。
        self.scraping_function = lambda: yahoo_goods_chenge_f(Yahoo_tree, Yahoo_goods_name_txt)
        Loading_C = LoadingViewClass(self.Yahoo_ALL_frame, self.anime_canvas, self.scraping_function)
        Yahoo_goods_Search_btn["command"] = lambda: Loading_C.start_loading_f()
        Yahoo_goods_Search_btn.pack(side="left")
        self.Yahoo_frame_upper.pack(ipady = 10)
        # -----------上部フレーム




        # -----------上部件数フレーム
        # 画面調整用フレーム
        self.Yahoo_frame_upper_2 = tkinter.Frame(self.Yahoo_ALL_frame)

        # 件数　ラベル
        Yahoo_goods_count_label = tkinter.Label(self.Yahoo_frame_upper_2, text = u"0", font = (14),fg = "#4169e1") #ラベルWidgetを生成
        Yahoo_goods_count_label.pack(side="left", padx=10)
        Yahoo_goods_count_label_2 = tkinter.Label(self.Yahoo_frame_upper_2, text = "件") #ラベルWidgetを生成
        Yahoo_goods_count_label_2.pack(side="left")

        self.Yahoo_frame_upper_2.pack()
        # -----------上部件数フレーム



        # -----------項目フレーム
        self.Yahoo_Koumoku_frame = tkinter.Frame(self.Yahoo_ALL_frame)

            # -----------（左）項目フレーム
        self.Yahoo_Koumoku_frame_left = tkinter.Frame(self.Yahoo_Koumoku_frame)

        # 平均：　ラベル
        Yahoo_mean_label = tkinter.Label(self.Yahoo_Koumoku_frame_left, text = u"0", font = (12),fg = "#4169e1") #ラベルWidgetを生成
        Yahoo_mean_label.pack(padx=5, side="left")
        Yahoo_mean_label_2 = tkinter.Label(self.Yahoo_Koumoku_frame_left, text = "平均値", font = (12),fg = "#4169e1") #ラベルWidgetを生成
        Yahoo_mean_label_2.pack(padx=5, side="left")

        self.Yahoo_Koumoku_frame_left.pack(side="left", padx=110)
            # -----------（左）項目フレーム


            # -----------（右）項目フレーム
        self.Yahoo_Koumoku_frame_Right = tkinter.Frame(self.Yahoo_Koumoku_frame)

        # 中央値：　ラベル
        Yahoo_Median_label = tkinter.Label(self.Yahoo_Koumoku_frame, text = "0", font = (12),fg = "#4169e1") #ラベルWidgetを生成
        Yahoo_Median_label.pack(padx=5, side="left")
        Yahoo_Median_label_2 = tkinter.Label(self.Yahoo_Koumoku_frame, text = "中央値", font = (12),fg = "#4169e1") #ラベルWidgetを生成
        Yahoo_Median_label_2.pack(padx=5, side="left")

        self.Yahoo_Koumoku_frame_Right.pack(side="left", padx=90)
            # -----------（右）項目フレーム

        self.Yahoo_Koumoku_frame.pack()

        # -----------項目フレーム



        # ------------直近Treeテーブル　フレーム
        self.Yahoo_Table_frame = tkinter.Frame(self.Yahoo_ALL_frame)
        # 列の識別名を指定
        Yahoo_column = ('ID', 'name', 'price', 'timestamp')

        # ツリーの文字の大きさを変更する
        Treestyle = ttk.Style()
        Treestyle.configure("Treeview.Heading", font=(4))

        # self.Yahoo_treeviewの生成
        Yahoo_tree = ttk.Treeview(self.Yahoo_Table_frame, columns = Yahoo_column)
        Yahoo_tree.bind("<<TreeviewSelect>>", self.funcMain.select_tree_record_f)

        # 列の設定
        Yahoo_tree.column('#0',width=0, stretch='no')
        Yahoo_tree.column('ID', anchor='center', width=40)
        Yahoo_tree.column('name',anchor='w', width=300)
        Yahoo_tree.column('price',anchor='w', width=70)
        Yahoo_tree.column('timestamp', anchor='center', width=130)

        # 列の見出し設定
        Yahoo_tree.heading('#0',text='')
        Yahoo_tree.heading('ID', text='ID',anchor='center')
        Yahoo_tree.heading('name',text='商品名', anchor='w')
        Yahoo_tree.heading('price', text='値段（円）', anchor='w')
        Yahoo_tree.heading('timestamp',text='売れた日', anchor='center')

        # Treeにスクロールバーの追加
        Yahoo_scrollbar = ttk.Scrollbar(self.Yahoo_Table_frame, orient=tkinter.VERTICAL, command=Yahoo_tree.yview)
        Yahoo_tree.configure(yscroll=Yahoo_scrollbar.set)
        Yahoo_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # ウィジェットの配置
        Yahoo_tree.pack(pady=10)

        self.Yahoo_Table_frame.pack()
        # ------------直近テーブル　フレーム



        # ----------ソート　フレーム
        self.Yahoo_Sort_frame = tkinter.Frame(self.Yahoo_ALL_frame)

        # 値段（安い）ソート　ボタン
        Yahoo_LowPriceSort_btn = tkinter.Button(self.Yahoo_Sort_frame, text='値段（安い）ソート', width=14, height=1, bg="mediumseagreen")
        Yahoo_LowPriceSort_btn["command"] =lambda: self.funcMain.Yahoo_sort_f(0, Yahoo_tree)
        Yahoo_LowPriceSort_btn.pack(side="left", padx=15)

        # 値段（高い）ソート　ボタン
        Yahoo_HighPriceSort_btn = tkinter.Button(self.Yahoo_Sort_frame, text='値段（高い）ソート', width=14, height=1, bg="mediumseagreen")
        Yahoo_HighPriceSort_btn["command"] = lambda: self.funcMain.Yahoo_sort_f(1, Yahoo_tree)
        Yahoo_HighPriceSort_btn.pack(side="left", padx=15)

        # 日付（古い）ソート　ボタン
        Yahoo_OldTimeSort_btn = tkinter.Button(self.Yahoo_Sort_frame, text='日付（古い）ソート', width=16, height=1, bg="mediumseagreen")
        Yahoo_OldTimeSort_btn["command"] = lambda: self.funcMain.Yahoo_sort_f(2, Yahoo_tree)
        Yahoo_OldTimeSort_btn.pack(side="left", padx=15)

        # 日付（新しい）ソートボタン
        Yahoo_NewTimeSort_btn = tkinter.Button(self.Yahoo_Sort_frame, text='日付（新しい）ソート', width=16, height=1, bg="mediumseagreen")
        Yahoo_NewTimeSort_btn["command"] = lambda: self.funcMain.Yahoo_sort_f(3, Yahoo_tree)
        Yahoo_NewTimeSort_btn.pack(side="left", padx=15)

        self.Yahoo_Sort_frame.pack(pady=10)
        # ----------ソート　フレーム


        # ----------グラフ　フレーム
        self.Yahoo_graph_frame = tkinter.Frame(self.Yahoo_ALL_frame)

        # グラフボタン
        Yahoo_graph_btn = tkinter.Button(self.Yahoo_graph_frame, text='グラフ', width=50, height=2, bg="wheat", font=("", "12","bold"))
        Yahoo_graph_btn["command"] = lambda: self.funcMain.Yahoo_graph_btn_f(Yahoo_tree)
        Yahoo_graph_btn.pack(pady=10)

        self.Yahoo_graph_frame.pack(pady=10)
        # ----------グラフ　フレーム

        # ----------設定　フレーム
        self.Yahoo_setting_frame = tkinter.Frame(self.Yahoo_ALL_frame)

        # 設定ボタン
        Yahoo_setting_btn = tkinter.Button(self.Yahoo_setting_frame, text='設定', width=15, height=3, bg="gainsboro")
        Yahoo_setting_btn["command"] = lambda: self.create_widgets_property()
        Yahoo_setting_btn.pack(side="left", padx=50)

        # 保存ボタン
        Yahoo_save_btn = tkinter.Button(self.Yahoo_setting_frame, text='保存', width=15, height=3, bg="gainsboro")
        Yahoo_save_btn["command"] = lambda: self.funcMain.Yahoo_save_btn_f()
        Yahoo_save_btn.pack(side="left", padx=50)


        self.Yahoo_setting_frame.pack(pady=10)
        # ----------設定　フレーム

        self.Yahoo_ALL_frame.pack()
       # ---------すべての親　フレーム


    # 設定画面　ウィジェットの作成　デザイン
    def create_widgets_property(self):
        """
        ウィジェットの配置　デザイン
        """

        # ツリーの行数　状態数値　ページ数を取得する
        self.tree_num, self.state, self.goods_page_num = self.funcPrpty.read_configfile_f()
        self.tree_num = int(self.tree_num)
        self.goods_page_num = int(self.goods_page_num)

        # 設定画面の設定
        self.dialog = Toplevel(self)
        self.dialog.title("modal dialog")
        self.dialog.minsize(width=480, height=550)# 画面サイズの設定
        self.dialog.maxsize(width=480, height=550)

        # モーダルダイアログ（元画面を操作不可として表示）
        self.dialog.grab_set()


        # 空フレーム
        self.setting_frame_Nothing = tkinter.Frame(self.dialog)
        self.setting_frame_Nothing.pack(ipady = 20)

        # -----------上部フレーム
        self.setting_frame_upper = tkinter.Frame(self.dialog)

        # 説明ラベル
        setting_Tree_description_label = tkinter.Label(self.setting_frame_upper, font = (14),fg = "#4169e1") #ラベルWidgetを生成
        setting_Tree_description_label["text"] = "画面に表示させる商品の数を設定します"
        setting_Tree_description_label.pack()


        #Scaleの生成
        setting_tree_scale = tkinter.Scale(self.setting_frame_upper, orient="horizontal", from_ = 10, to = 100, width = 20, length = 400)
        setting_tree_scale.set(self.tree_num)
        setting_tree_scale.pack()


        #Scale値を取得して表示するボタン
        setting_tree_Scale_btn = tkinter.Button(self.setting_frame_upper, widt=20)
        setting_tree_Scale_btn["text"] = "デフォルトに戻す（30行）"
        setting_tree_Scale_btn["command"] = lambda : self.funcPrpty.tree_set_value(setting_tree_scale)
        setting_tree_Scale_btn.pack()

        self.setting_frame_upper.pack(ipady = 20)
        # -----------上部フレーム


        # -----------中間フレーム
        self.setting_frame_middle = tkinter.Frame(self.dialog)

        # 説明ラベル
        setting_status_description_label = tkinter.Label(self.setting_frame_middle, font = (14),fg = "#4169e1") #ラベルWidgetを生成
        setting_status_description_label["text"] = "商品の状態を設定できます"
        setting_status_description_label.pack()

        setting_status_description_sub_label = tkinter.Label(self.setting_frame_middle, font = (9)) #ラベルWidgetを生成
        setting_status_description_sub_label["text"] = "0 がすべて、1 が未使用、2 が中古を表す"
        setting_status_description_sub_label.pack()

        # ドロップダウンボックス
        setting_status_comb = ttk.Combobox(self.setting_frame_middle, state = 'readonly')
        setting_status_comb["values"] = ("0","1","2")
        setting_status_comb.current(self.state)
        setting_status_comb.pack()


        self.setting_frame_middle.pack(ipady = 20)
        # -----------中間フレーム


        # -----------下部フレーム
        self.setting_frame_bottom = tkinter.Frame(self.dialog)

        # 説明ラベル
        setting_scale_description_label = tkinter.Label(self.setting_frame_bottom, font = (14),fg = "#4169e1") #ラベルWidgetを生成
        setting_scale_description_label["text"] = "スクレイピングで取得するページ数を設定できます"
        setting_scale_description_label.pack()

        setting_scale_description_sub_label = tkinter.Label(self.setting_frame_bottom, font = (9)) #ラベルWidgetを生成
        setting_scale_description_sub_label["text"] = "ページが多いと、その分時間がかかります"
        setting_scale_description_sub_label.pack()

        #Scaleの生成
        setting_page_scale = tkinter.Scale(self.setting_frame_bottom, orient="horizontal", from_ = 1, to = 10, width = 20, length = 230)
        setting_page_scale.set(self.goods_page_num)
        setting_page_scale.pack()

        #Scale値を取得して表示するボタン
        setting_page_Scale_btn = tkinter.Button(self.setting_frame_bottom, widt=20)
        setting_page_Scale_btn["text"] = "デフォルトに戻す（2ページ）"
        setting_page_Scale_btn["command"] = lambda :  self.funcPrpty.page_set_value(setting_page_scale)
        setting_page_Scale_btn.pack()


        self.setting_frame_bottom.pack(ipady = 20)
        # -----------下部フレーム


        # 設定保存ボタン
        setting_save_btn = tkinter.Button(self.dialog, widt = 20, height=1, text = "設定保存", bg = "lightyellow")
        setting_save_btn["command"] = lambda :  self.funcPrpty.setting_save_btn_f(setting_tree_scale.get(), setting_status_comb.get(), setting_page_scale.get(), self.dialog)
        setting_save_btn.pack(ipady = 30)


# ローディング画像の処理クラス
class LoadingViewClass():
    """
    ローディング画像の処理クラス

    Webscraping中はロード画面を表示させる。
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

        # 処理中かどうかを判定
        if self.is_processing:

            # 次の描画時に角度が変わるように値を変える
            if self.load_img_num > 26:
                self.load_img_num = 0
            else:
                self.load_img_num += 1

            # ローディングアニメーションの画像を読み込み
            load_jpeg = "./img/zjpeg_ghost/Ghost-{}.jpg".format(str(self.load_img_num))

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
                image=self.loading_img,  # 描画する画像
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
            app.after(50, self.draw_anime)

        else:
            # 処理が終わっているならCanvasを非表示に
            self.anime_canvas.pack_forget()


    # アニメーション表示中に実際に処理を行う関数
    def process_f(self):
        self.is_processing = True

        # time.sleep(4)
        self.WEB_scraping_F() # ウェブスクレイピング処理が終わるまでローディング画面のまま
        self.main_frame.pack() # 上の処理が終われば、もう一度メイン画面を表示

        # 待ち合わせ用関数をFalseにすることによってアニメーションが止まる
        self.is_processing = False


    # ローディング画面表示 マルチプロセス処理
    def start_loading_f(self):
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



