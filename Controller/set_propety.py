"""セッティングに関するモジュール

Attributes:
    CONFIG_FILEPATH(str): 設定ファイルのパス
    CONFIG(configparser.ConfigParser object): コンフィグファイルを利用するためのインスタンス

Todo:

"""

import configparser # 設定ファイルを扱うモジュールをインポート
import os

# コンフィグのファイルパス
CONFIG_FILEPATH = os.path.dirname(__file__).rstrip("controller")
CONFIG_FILEPATH = os.path.join(CONFIG_FILEPATH, "DATA\\Y_config.ini")

# ConfigParserのインスタンスを取得
CONFIG = configparser.ConfigParser()

# セッティング画面の処理を書いたクラス
class SettingProcessingClass():
    """セッティング画面の処理を書いたクラス

        Attributes:
            self.treenum(str): ツリーの行数
            self.state(str): 商品の状態（0=すべて, 1=未使用, 2=中古）
            self.godpagesnum(str): 取得するページ数
    """
    def __init__(self):
        # ini エラー用初期値
        self.treenum = "30"
        self.state = "2"
        self.godpagesnum = "2"

    # ツリーのスクロールバー　値
    def tree_set_value(self, widget_val):
        """ツリーのスクロールバー　値

        設定画面　スクロールバーに（デフォルトに戻すボタンを押したとき）値をセットする

        Args:
            widget_val(tkinter.Scale): 商品数のスクロールバーの値（デフォルトに戻すボタン）
        """
        widget_val.set(30)   #Scaleに30をセット

    # ページスクロールバー　値
    def page_set_value(self, widget_val):
        """ページスクロールバー　値

        設定画面　スクロールバーに（デフォルトに戻すボタンを押したとき）値をセットする

        Args:
            widget_val(tkinter.Scale): ページ数のスクロールバーの値
        """
        widget_val.set(2)   #Scaleに2をセット

    # 設定ボタンを押したとき
    def setting_save_btn_f(self, treenum, statenum, pagenum, dialog):
        """設定ボタンの処理

        Setting.ini に値を記録する処理

        Args:
            treenum(int): ツリーの行数
            statenum(str): 商品の状態（0=すべて, 1=未使用, 2=中古）
            pagenum(int): 取得するページ数
            dialog(tkinter.Toplevel): メイン画面に紐づくサブ画面
        """

        print("設定保存ボタン")
        # view のウィジェットの値を取得し、その値を上書き記録する。
        self.writ_configfile_f(treenum, statenum, pagenum)
        dialog.destroy()

    # iniファイルの新規作成
    def create_config_file_f(self):
        """iniファイルの作成

        Webスクレイピングをする際に利用する、設定に関するファイルを作成

        Attributes:
            CONFIG(configparser.ConfigParser): コンフィグファイルを利用するためのインスタンス
            is_file(bool): ファイルが存在しているかどうかをチェック。存在する（true）なら削除

        """

        print("コンフィグファイルの作成")
        CONFIG = configparser.ConfigParser() # 初期化させる
        is_file = os.path.isfile(CONFIG_FILEPATH)
        if is_file:
            os.remove(CONFIG_FILEPATH)

        # configの各項目に上書き
        CONFIG["DEFAULT"]["TREE_NUM"] = self.treenum
        CONFIG["DEFAULT"]["STATE"] = self.state
        CONFIG["DEFAULT"]["GOODS_PAGE_NUM"] = self.godpagesnum

        # config_1.iniファイルに上書き
        with open(CONFIG_FILEPATH, "w") as file:
            CONFIG.write(file)

    # configファイルがあるかどうかをチェック
    def config_existence_check_f(self):
        """configファイルがあるかどうかをチェックし、なければ作成する

        Attributes:
            is_file(bool): ファイルが存在しているかどうかをチェック。存在しない（false）なら新たに作成

        """
        is_file = os.path.isfile(CONFIG_FILEPATH)
        if is_file:
            print(f"設定ファイル {CONFIG_FILEPATH} ")
            return True
        else:
            print(f"ファイルが存在しないか、壊れているため、作成します")
            self.create_config_file_f()
            return False

    # configfileの読み取り
    def read_configfile_f(self):
        """configfileの読み取り処理

        Attributes:
            config_treenum(str):ツリーの行数
            config_state(str): 商品の状態（0=すべて, 1=未使用, 2=中古）
            config_goodsnum(str):取得するページ数

        Returns:
            (iniファイルがない・壊れている)
            self.treenum(str): ツリーの行数の初期値を返す
            self.state(str): 商品の状態（0=すべて, 1=未使用, 2=中古）の初期値を返す
            self.godpagesnum(str): 取得するページ数の初期値を返す

            (iniファイルの値を返す)
            config_treenum(str): ツリーの行数を返す
            config_state(str): 商品の状態（0=すべて, 1=未使用, 2=中古）を返す
            config_goodsnum(str): 取得するページ数を返す

        """
        # iniファイルの存在チェック
        self.config_existence_check_f()

        try:
            # コンフィグファイル読み取り
            CONFIG.read(CONFIG_FILEPATH, "UTF-8")
            config_treenum = CONFIG["DEFAULT"]["TREE_NUM"]
            config_state = CONFIG["DEFAULT"]["STATE"]
            config_goodsnum = CONFIG["DEFAULT"]["GOODS_PAGE_NUM"]
        except:
            print("コンフィグファイルに問題あり")
            self.create_config_file_f()
            return self.treenum, self.state, self.godpagesnum

        if 10 <= int(config_treenum)  <= 100 and  \
            0 <= int(config_state)    <= 2   and  \
            1 <= int(config_goodsnum) <= 10:
            pass
        else:
            print("コンフィグファイルの値に問題あり")
            self.create_config_file_f()
            return self.treenum, self.state, self.godpagesnum

        # 変数の内容を出力
        print("設定値 = " + "{},{},{}".format(config_goodsnum, config_state, config_treenum))
        return config_treenum, config_state, config_goodsnum

    # configfileの上書き
    def writ_configfile_f(self, treenum, state, godsnum):
        """configfileの書き換え処理
        """

        CONFIG = configparser.ConfigParser() # 初期化させる
        # configの各項目に上書き
        CONFIG["DEFAULT"]["TREE_NUM"] = str(treenum)
        CONFIG["DEFAULT"]["STATE"] = str(state)
        CONFIG["DEFAULT"]["GOODS_PAGE_NUM"] = str(godsnum)

        # config_1.iniファイルに上書き
        with open(CONFIG_FILEPATH, "w") as file:
            CONFIG.write(file)

