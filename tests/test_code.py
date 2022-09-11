# pytest

import os
import sys

# 上の階層でもimprotできるようにする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# フォルダの存在チェック
def test_1():
    import os
    # コンフィグのファイルパス
    ini_folder_path = "./YAhoo_scraping/"
    is_yahoofolder = os.path.exists(ini_folder_path)

    assert is_yahoofolder == True

# コンフィグの値チェック
def test_2():
    try:
        import configparser
        CONFIG = configparser.ConfigParser()
        CONFIG_FILEPATH = "./YAhoo_scraping/Y_config.ini"
        CONFIG.read(CONFIG_FILEPATH, "UTF-8")
        config_treenum = CONFIG["DEFAULT"]["TREE_NUM"]
        config_state = CONFIG["DEFAULT"]["STATE"]
        config_goodsnum = CONFIG["DEFAULT"]["GOODS_PAGE_NUM"]

        is_test = ""

        if 10 <= int(config_treenum)  <= 100 and  \
            0 <= int(config_state)    <= 2   and  \
            1 <= int(config_goodsnum) <= 10:
            is_test = True
        else:
            is_test = False
    except:
        is_test = False

    assert is_test == True


