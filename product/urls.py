from django.urls import path, include, re_path
from product import views




app_name = 'product'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('list_add/<post_pk>', views.list_add, name='list_add'),
    path('list_remove/<post_pk>',
         views.list_remove, name='list_remove'),
    path('shop_basket/', views.shop_basket, name='shop_basket'),
    path('product_of_week/', views.product_of_week, name='product_of_week'),
    path('buying_product/<post_pk>', views.buying_product, name='buying_product'),
    path('buying_product_list/', views.buying_product_list, name='buying_product_list'),
    path('buying_delete/<post_pk>', views.buying_delete, name='buying_delete'),
    path('best_buying_product/', views.best_buying_product,
         name='best_buying_product'),


]

# <post_id> view단에서 활용 ..// <post_id>\d -> 뒤에 숫자가 온다는 의미
