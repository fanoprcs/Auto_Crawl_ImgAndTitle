import numpy as np
import os, cv2
import math
from PIL import Image
import flask, webbrowser
from bs4 import BeautifulSoup
import requests
app = flask.Flask(__name__)
app.secret_key = "secret key"
type = "none"
url = "none"
num = "none"
@app.route('/')
def home():
    return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type,show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num)

@app.route("/get_type", methods=["POST"])
def get_type():
    global type 
    type = flask.request.values.get('type')
    return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num)

@app.route("/get_url", methods=["POST"])
def get_url():
    global url 
    url = flask.request.values.get('url')
    return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num)

@app.route("/get_num", methods=["POST"])
def get_num():
    global num
    num = flask.request.values.get('num')
    return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_num_area = '下載數量為: ' + num, show_url_area = "選擇網址為: " + url)
@app.route("/exe", methods=["POST"])
def exe():
    try:
        response = requests.get(url)
        root = BeautifulSoup(response.text, "lxml")
    except:
        return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num, show_status_area = "網址輸入錯誤，請重新輸入。")
    try:
        a = int(num)
    except:
        return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num, show_status_area = "數量輸入錯誤，請重新輸入。")
    try:
        results = root.find_all(type, limit = 10000)
    except:
        return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num, show_status_area = "類型輸入錯誤，請確認輸入的類型為img、h1、h2、h3、h4、h5。")
    if len(results) == 0:#無法進行資料抓取
        return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num, show_status_area = "很抱歉，此網站存取該資料是用動態加載的方式，無法進行爬蟲，請換個資料或另外選擇網站。")
    if type == "img": #將圖片存到到images中，並且每次下載會創建新資料夾
        img_link = [result.get("src") for result in results]
        if not os.path.exists("images"):
            os.mkdir("images")
        new_folder = "01"
        for file_name in os.listdir("images"):
            if file_name == new_folder:
                new_folder = str(int(new_folder) + 1)
                if len(new_folder) == 1:
                    new_folder = "0" + new_folder
        os.mkdir("images/" + new_folder)
        count = 0
        k = 0
        for index, link in enumerate(img_link):
            try:
                img = requests.get(link)  # 下載圖片
            except:
                k += 1
                continue
            with open("images/" + new_folder +"/" + str(index - k + 1) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
                file.write(img.content)  # 寫入圖片的二進位碼
            count += 1
            if count == a:
                break
    else: #將標題載入到documents中，並且沒次下載會建立新的文件
        try:
            text = [result.text for result in results]
        except:
            return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num, show_status_area = "很抱歉，格式出了差錯，請另外選擇網站。")
        if not os.path.exists("documents"):
            os.mkdir("documents")
        new_txt = "01"
        for file_name in os.listdir("documents"):
            if file_name.split('.')[0] == new_txt:
                new_txt = str(int(new_txt) + 1)
                if len(new_txt) == 1:
                    new_txt = "0" + new_txt
        count = 0
        with open("documents/" + new_txt + ".txt", "a") as file:  # 開啟資料夾及命名圖片檔
            for line in text:
                try:
                    file.write( line + '\n')
                    count += 1
                except:
                    pass
    return flask.render_template('page.html', show_type_area = "抓取的類型為: " + type, show_url_area = "選擇網址為: " + url, show_num_area = '下載數量為: ' + num, show_status_area = "共找到 " + str(count) + " 筆資料，開始進行下載。")

if __name__ == "__main__":
    port = 1002
    link = "http://127.0.0.1:{0}".format(port)
    webbrowser.open(link)
    app.run(host="0.0.0.0", debug = True, port = port)
