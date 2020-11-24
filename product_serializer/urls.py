from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from product_serializer import views


router = DefaultRouter()
router.register('users_info', views.UserViewSet, basename="UserView")
router.register('posts', views.PostViewSet, basename="PostView")
router.register(r"posts/(?P<product_id>\d+)/basket/(?P<product_quantity>\d+)",
                views.Product_to_BasketViewSet, basename="Product_to_Basket")

router.register('search_posts', views.SearchViewSet, basename="SearchView")
router.register('decending_orders', views.OrderViewSet, basename="OrderView")
router.register(r"decending_orders/(?P<order_pk>\d+)",
                views.BuyingViewSet, basename="BuyingAddView")
router.register('recent_posts', views.RecentViewSet, basename="RecentView")
router.register('customer_buying_list',
                views.BuyingViewSet, basename='TestView')
router.register('best_product', views.BestProductViewSet,
                basename='BestProductView')
# router.register('test', views.test.as_view(), basename='test')
app_name = 'product_serializer'
urlpatterns = [
    path('api/', include(router.urls)),
    path('test/', views.test.as_view())
]

# http http://localhost:8000/product_serializer/api/posts 상품조회
# http http://localhost:8000/product_serializer/api/posts/5/ 상품조회
