## Yahoo_scraping_py



<br>

![pinterest_profile_image](https://user-images.githubusercontent.com/103634835/189520017-4690e695-ea0a-4e32-906a-84a834d46ddb.png)


[![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio%20Code&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://open.vscode.dev/｛fk009｝/{Yahoo_scraping_py})

<br>
<br>



# 【Yahoo! スクレイピングツール】
## 説明動画
https://youtu.be/BeG9H_YouWQ

<br>

# 【概要】
最近では、中古店がネットを使って商品を売ったりしています。
自分でも過去にプレイした後のゲームをネットで売ったことがあるのですが、
適正価格がわからず、いろんな人が過去にどれぐらいの値段で売っていたのか調べるのが大変でした。

そこで、Webスクレイピングの技術を使うことで、手軽に売買価格を調べることができるシステムを開発することにしました。
このシステムを使えば、簡単に中古商品の販売価格に関する情報が手に入ります。

また、スクレイピングの応用性がく高く、学んでおけば仕事の幅が広がると考えたため、こうしたシステムを開発することにしました。
  
  
  
<br>
<br>
  
# 【設計】

テキストボックスに商品名を入力し、検索ボタンを押すと、その商品がいつ売れたかと言った情報をウェブから取得します。

検索した内容の商品の売上情報を収集します。
・件数　・平均　・中央値　・売れた日などなど

・また、収集したデータを使ってグラフを作成します。

スクレイピングが政府もやっていることで、明確な犯罪行為ではない。
ただし、サイトに負荷をかけるような行為は問題となるため、数秒以上の処理のストップをかける。

<br>
<br>



# 【機能説明】

![2022-09-05 21_48_34-Window](https://user-images.githubusercontent.com/103634835/189520137-208e3643-6e30-4393-acb9-442bb74b9577.png)


<br>
1．『.URLジャンプボタン』
検索したサイトへジャンプして、内容を確認できます。
<br>
2．『テキストボックス』
商品名を検索する（例）　”ゼルダの伝説ブレスオブザワイルド”
<br>
3．『検索ボタン』
テキストボックスに入力したワードでの検索を実行します。
<br>
4．『ラベル』
取得した件数　商品を取得した数を表示します。
<br>
5．『ソートボタン』４つ
商品の　①最大値段　②最小値段　③平均　④中央値でソートするボタン
<br>
6．『商品一覧』
画面中央　直近で売れた商品の名前　値段　落札日を表示します。
<br>
7．『グラフボタン』
商品の日付順に、値段でのグラフを作成します。
<br>
8．『設定ボタン』
取得したい商品の状態(新品か中古か)
商品を取得する件数
画面の一覧に表示させたい商品の数
これらを設定した後に検索ボタンを押すと、設定した項目の通りになります。
<br>
9．『保存ボタン』
（スクレイピングの結果をCSVファイルとして保存）


<br>
<br>

# 【使用サードパーティ】
bs4,matplotlib, pandas, requests, 

<br>
<br>

# 【モジュールインストール】
```
pip install -r requirements.txt
```
このコマンドでパッケージのインストールができます。

<br>
<br>

# 【ファイル・フォルダ説明】


### **『main.py』**
起動ファイルになります。MainScreenView.py を呼びます。

<br>

## 【Controller　フォルダ】
<br>

### **『main_screen.py』**
メイン画面に関する処理が書かれています。
メイン画面のボタンを押した時などの処理が書かれています。

<br>

### 『set_propety.py』
設定画面に関する処理が書かれています。
設定画面のボタンを押した時などの処理が書かれています。

<br>
<br>

## 【View　フォルダ】

<br>

### 『MainScreenView.py』

メイン画面のデザインや、ウィジェットの配置に関するコードが記述されています。
設定画面のデザインや、ウィジェットの配置に関するコードが記述されています。
ウェブスクレイピング中に表示させるローディング画面に関するコードが記述されています。

<br>
<br>

## 【Model　フォルダ】

### 『data_save.py』

iniファイルやcsvファイルを保存するためのフォルダを作成します。
ウェブスクレイピングしたデータをcsvファイルとして保存します。

<br>

### 『web_Scraping.py』

ウェブスクレイピングに関するコードが記述されています。
ビューティフルソープを使って、検索したサイトのタグなどを読み取ります。

商品名、金額、売れた日を取得します。


<br>
<br>


# 【参考サイト】

[tslearn.clustringを用いた時系列データのクラスタリング](https://yoshi-cow.github.io/statistics.github.io/dtw.html)

[ヤフオクのデータをwebスクレイピングで取得して分析してみた。](https://note.com/rkhs_cemcl/n/nb1ca2380cfe2)

[【Python】requestsを使うときは必ずtimeoutを設定するべき](https://blog.cosnomi.com/posts/1259/)

[【Python】メッセージボックスを表示する(tkinter.messagebox)](https://pg-chain.com/python-messagebox)

[Pythonのmaster=Noneとかについて](https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q12206588077)

[Tkinter　TopLevelを使ってmodaldialog(モーダルなダイアログ)を実装する](https://suzutaka-programming.com/tkinter-modaldialog/)

[セッティングファイルの処理](https://kaibutsusyain.com/how-to-create-and-operate-a-configuration-file-in-python/)

