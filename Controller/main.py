import os
import sys

# 上の階層でもimprotできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 自作モジュール
from View import MainScreenView

# メイン画面起動
MainScreenView
