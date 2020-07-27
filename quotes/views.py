from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

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

def del_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("股票已刪除"))
    return redirect(modi_stock)

def modi_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'modi_stock.html', {'ticker': ticker})