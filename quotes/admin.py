from django.contrib import admin

# Register your models here.
from .models import Stock, Youtube, Event, Guest

# 方式一，未加入ModelAdmin類別
# admin.site.register(Stock)
# admin.site.register(Youtube)
# admin.site.register(Event)
# admin.site.register(Guest)

# 方式二: 加入ModelAdmin類別，定義顯示藍為、過濾資料、搜尋&排序
class StockAdmin(admin.ModelAdmin):
    list_display = ['ticker']
    # search_fields = ['ticker']
    # list_filter = ['ticker]
admin.site.register(Stock, StockAdmin)

class YoutubeAdmin(admin.ModelAdmin):
    list_display = ['PublishedAt', 'title', 'description', 'thumbnailurl']
    # search_fields = ['title']
    # list_filter = []
admin.site.register(Youtube, YoutubeAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'limit', 'status', 'address', 'start_time', 'create_time']
    search_fields = ['name'] #搜尋方塊
    list_filter = ['status'] #篩檢程式
admin.site.register(Event, EventAdmin)

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone','email','sign','create_time','event']
    search_fields = ['realname','phone'] #搜尋方塊
    list_filter = ['sign'] #篩檢程式
admin.site.register(Guest, GuestAdmin)
