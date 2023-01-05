"""controller起動モジュール

一番最初に読み込まれるモジュール

Todo:
    説明書きを終わらせる。（完了）



"""

# 自作モジュール
from controller import main_view_start
from model import data_save

# フォルダ作成
data_save.create_folder_f()

# メイン画面起動
main_view_start


