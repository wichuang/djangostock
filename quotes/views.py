from django.shortcuts import render, redirect, get_object_or_404
from quotes.models import Stock
from .forms import StockForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from quotes.models import Event, Guest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import tempfile
from tkinter import *
from tkinter import filedialog
from datetime import datetime

logger = logging.getLogger(__name__)

#發佈會管理(登入後default頁面)
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('username', '')
    return render(request, "event_manage.html", {"user": username,"events":event_list})

# 發佈會名稱搜尋
@login_required
def search_name(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name_bytes)
    return render(request, "event_manage.html", {"user": username,"events": event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts, "phone":search_phone})

# Create your views here.
def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        # pk_c2c72b94a6a84bc8b51dd6721b642438
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_c2c72b94a6a84bc8b51dd6721b642438")
        # api_request = requests.get("https://cloud.iexapis.com/stable/stock/XOM/quote?token=pk_c2c72b94a6a84bc8b51dd6721b642438")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error ... "
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "請輸入公司代碼查詢股票資料..."})

def moi(request):
    import requests
    import json

    # api_request = requests.get("http://od.moi.gov.tw/od/data/api/EA28418E-8956-4790-BAF4-C2D3988266CC?$format=json")
    api_request = requests.get("https://bsb.kh.edu.tw/afterschool/opendata/afterschool_json.jsp?city=24")

    try:
        output = json.loads(api_request.content)
    except Exception as e:
        output = "Error ... "

    return render(request, 'moi.html', {'output': output})

def moi_quick(request):
    import requests
    import json

    # api_request = requests.get("http://od.moi.gov.tw/od/data/api/EA28418E-8956-4790-BAF4-C2D3988266CC?$format=json")
    api_request = requests.get("https://bsb.kh.edu.tw/afterschool/opendata/afterschool_json.jsp?city=24")

    try:
        output = json.loads(api_request.content)
    except Exception as e:
        output = "Error ... "

    return render(request, 'moi_quick.html', {'output': output})

def youtube(request):
    import requests
    import json

    youtube_key = "AIzaSyBwH2w2LzOGBNXDUjI5dW4C50ZBQWlndDQ"
    # channel_id = "UC-0CzRZeML8zw4pFTVDq65Q" #Sarah Beth
    channel_id = "UCltlhGpksn0HjNW1VGO1e8w" #William
    output=[]
    # https://www.googleapis.com/youtube/v3/search?channelId=UC-0CzRZeML8zw4pFTVDq65Q&part=snippet&key=AIzaSyBwH2w2LzOGBNXDUjI5dW4C50ZBQWlndDQ
    api_request = requests.get("https://www.googleapis.com/youtube/v3/search?channelId=" + channel_id + "&part=snippet&key=" + youtube_key)
    try:
        ticker = json.loads(api_request.text)
        if ticker.get("items") is not None:
            print( "Found...")
            output = []
            for video in ticker.get("items"):
                pubDate = video["snippet"]["publishedAt"]
                title = video["snippet"]["title"]
                desc = video["snippet"]["description"]
                url = video["snippet"]["thumbnails"]["default"]["url"]
                output.append({
                   "publishedAt": pubDate,
                   "title": title,
                   "description": desc,
                   "thumbnailurl": url
                })

    except Exception as e:
        ticker = "Error ... "
    return render(request, 'youtube.html', {'ticker': ticker, 'output': output})

def facebook(request):
    from bs4 import BeautifulSoup

    output = []
    foldername = "../facebook-WilliamChuang1957"
    # print("%s/ads_and_businesses/advertisers_you've_interacted_with.html" %foldername)
    with open("%s/ads_and_businesses/advertisers_you've_interacted_with.html" %foldername, "r", encoding="utf-8") as page:
        ticker = BeautifulSoup(page, "html.parser")
        contents = ticker.find("div", class_="_4t5n")
        ad_list = contents.find_all("div", class_="uiBoxWhite")
        for item in ad_list:
            advert = item.find("div", class_="_2let").get_text()
            timeaccess = item.find("div", class_="_2lem").get_text()
            output.append({
                "advert": advert,
                "timeaccess": timeaccess,
            })
    
    return render(request, 'facebook.html', {'ticker': ticker, 'output': output})

def wiki(request):
    import urllib.request
    from bs4 import BeautifulSoup
    import pandas as pd

    ticker = 'error'
    output = list()
    # unicode error!!
    # with urllib.request.urlopen("https://zh.wikipedia.org/wiki/台灣大專院校列表") as page:
    with urllib.request.urlopen("https://zh.wikipedia.org/wiki/%E5%8F%B0%E7%81%A3%E5%A4%A7%E5%B0%88%E9%99%A2%E6%A0%A1%E5%88%97%E8%A1%A8") as page:
        ticker = BeautifulSoup(page, 'html.parser') # parsing as string
        table = ticker.find('table', {'class': 'wikitable + sortable'}) #Grab the table
        new_table = [1,2,3,4,5,6,7] # I know the size
        
        output = list()
        row_marker = 0
        for row in table.find_all('tr'):
            if row_marker == 0: # skip the column header row
                row_marker += 1
                continue
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                if column_marker == 6: #only 網址需要用href
                    anchortag = column.find("a", href=True)
                    new_table[column_marker] = anchortag["href"]
                else:
                    new_table[column_marker] = column.get_text().replace('\n', '').replace('\xa0', '')
                column_marker += 1

            new_row = {"序號": new_table[0],
                "學校名稱": new_table[1],
                "英文簡稱": new_table[2],
                "年份": new_table[3],
                "地址": new_table[4],
                "校地": new_table[5],
                "網址": new_table[6]}
            output.append(new_row)
            row_marker += 1

    return render(request, 'wiki.html', {'ticker': ticker, 'output': output})

def wiki_quick(request):
    import urllib.request
    from bs4 import BeautifulSoup
    import pandas as pd

    ticker = 'error'
    output = list()
    # with urllib.request.urlopen("https://zh.wikipedia.org/wiki/台灣大專院校列表") as page:
    with urllib.request.urlopen("https://zh.wikipedia.org/wiki/%E5%8F%B0%E7%81%A3%E5%A4%A7%E5%B0%88%E9%99%A2%E6%A0%A1%E5%88%97%E8%A1%A8") as page:
        ticker = BeautifulSoup(page, 'html.parser')
        table = ticker.find('table', {'class': 'wikitable + sortable'})
        trs = table.find_all('tr')[1:]
        output = list()
        for tr in trs:
            output.append([td.text for td in tr.find_all('td')])
            # output.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])
        # output[:5]

    return render(request, 'wiki_quick.html', {'ticker': ticker, 'output': output})

def about(request):
    return render(request, 'about.html', {})

def view_pdf(request):
    # Importing required modules
    from PIL import Image,ImageTk
    from pdf2image import convert_from_path

    # Grab the filename of the pdf file
    open_file = filedialog.askopenfilename(
        initialdir='D:\\My Work\\python\\djangostock\\stocks\\',
        title = "Open PDF File",
        filetypes = (
            ("PDF Files", "*.pdf"),
            ("All Files", ("*.*"))
        )
    )

    # Check to see if there is a file
    if open_file:
        # Creating Tk container
        root = Tk()
        # Creating the frame for PDF Viewer
        pdf_frame = Frame(root).pack(fill=BOTH,expand=1)
        # Adding Scrollbar to the PDF frame
        scrol_y = Scrollbar(pdf_frame,orient=VERTICAL)
        # Adding text widget for inserting images
        pdf = Text(pdf_frame,yscrollcommand=scrol_y.set,bg="grey")
        # Setting the scrollbar to the right side
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=pdf.yview)
        # Finally packing the text widget
        pdf.pack(fill=BOTH,expand=1)

        # Here the PDF is converted to list of images
        pages = convert_from_path(open_file, poppler_path='D:\\My Work\\python\\djangostock\\venv\\Lib\\site-packages\\pdf2image\\poppler-0.68.0\\bin',size=(800,900))
        # Empty list for storing images
        photos = []
        # Storing the converted images into list
        for i in range(len(pages)):
            photos.append(ImageTk.PhotoImage(pages[i]))
        # Adding all the images to the text widget
        for photo in photos:
            pdf.image_create(END,image=photo)
        
            # For Seperating the pages
            pdf.insert(END,'\n\n')

        # Ending of mainloop, 讓pdf視窗一直顯示
        mainloop()

    now=datetime.now() #now變數將傳遞給pdf_image.html顯示現在時間
    # 下列程式碼錯誤=> Tcl_AsyncDelete: async handler deleted by the wrong thread
    # return render(request, 'pdf_image.html', locals()) #locals表示傳遞所有local變數
    # 改為只傳遞now就OK!
    return render(request, 'pdf_image.html', {"now": now})

def save_pdf(request):
    # Importing required modules
    from PIL import Image,ImageTk
    from pdf2image import convert_from_path

    # Grab the filename of the pdf file
    open_file = filedialog.askopenfilename(
        initialdir='D:\\My Work\\python\\djangostock\\stocks\\',
        title = "Open PDF File",
        filetypes = (
            ("PDF Files", "*.pdf"),
            ("All Files", ("*.*"))
        )
    )

    # Check to see if there is a file
    if open_file:
        with tempfile.TemporaryDirectory() as path:
            # 目前報錯 PermissionError: [WinError 32] 程序無法存取檔案，因為檔案正由另一個程序使用            
            images = convert_from_path(open_file, poppler_path='D:\\My Work\\python\\djangostock\\venv\\Lib\\site-packages\\pdf2image\\poppler-0.68.0\\bin', output_folder=path, fmt="jpeg")
            # 無法至下行指令
            # print('path', path)

    return render(request, 'pdf_image.html', {})

def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("股票已加入"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=pk_c2c72b94a6a84bc8b51dd6721b642438")
            print(ticker_item)
            try:
                api = json.loads(api_request.content)
                output.append(api)
            # except Exception as e:
            except:
                print( "api error" )
                api = "Error ... "
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

# 顯示要選擇股票刪除的路徑
def stock_delete(request):
    ticker = Stock.objects.all()
    return render(request, 'stock_delete.html', {'ticker': ticker})

# 執行刪除股票的路徑
def del_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("股票已刪除"))
    return redirect(stock_delete) #回到選擇股票刪除的頁面

def dj_test(request):
    return render(request, 'dj_test.html', {})

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == 'admin' and password == 'admin123':
            return HttpResponseRedirect('event_manage')
        else:
            return render(request,'dj_test.html', {'error': 'username or password error!'})
