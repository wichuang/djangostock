from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    # return ticker
    def __str__(self):
        return self.ticker

# Youtube
class Youtube(models.Model):
    PublishedAt = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnailurl = models.URLField(blank=True)
    def __str__(self):
        return self.title

# 發佈會表
class Event(models.Model):
    name = models.CharField(max_length=100) # 發佈會標題
    limit = models.IntegerField() # 參加人數
    status = models.BooleanField() # 狀態
    address = models.CharField(max_length=200) # 地址
    start_time = models.DateTimeField('events time') # 發佈會時間
    create_time = models.DateTimeField(auto_now=True) # 建立時間（自動獲取
    # 目前時間）
    def __str__(self):
        return self.name

# 嘉賓表
class Guest(models.Model):
    # 要加入 on_delete=models.CASCADE 才正確
    event = models.ForeignKey(Event, on_delete=models.CASCADE) # 關聯發佈會id
    realname = models.CharField(max_length=64) # 姓名
    phone = models.CharField(max_length=16) # 手機號
    email = models.EmailField() # 電子郵件
    sign = models.BooleanField() # 簽到狀態
    create_time = models.DateTimeField(auto_now=True) # 建立時間（自動獲取目前時間）

    #對於一場發佈會來說，因為手機號具有很強的唯一性，因此一般會
    #選擇手機號作為一位元嘉賓的唯一驗證資訊。在嘉賓表中，除了嘉賓id 為
    #主鍵外，這裡透過發佈會id + 手機號來作為聯合主鍵。Meta 是Django 模
    #型類別的一個內部類別，它用於定義一些Django 模型類別的行為特性。
    #unique_together 用於設定兩個欄位為聯合主鍵。
    class Meta:
        unique_together = ("event", "phone")

    #__str__() 方法告訴Python 如何將物件以str 的方式顯示出來。所以，為每
    #個模型類別新增了__str__() 方法。
    def __str__(self):
        return self.realname
