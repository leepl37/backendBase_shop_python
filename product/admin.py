from django.contrib import admin
from .models import Product, Photo, Order

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['basket_user','basket_order','quantity']


# Photo 클래스를 inline으로 나타낸다.
class PhotoInline(admin.TabularInline):
    model = Photo

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.
class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline,  ]


# 상품과 관리자등록 
admin.site.register(Product, ProductAdmin)
