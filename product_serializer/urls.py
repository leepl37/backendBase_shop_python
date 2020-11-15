from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from product_serializer import views


router = DefaultRouter()
router.register('posts', views.PostViewSet, basename="PostView")
router.register('decending_orders', views.OrderViewSet, basename="OrderView")
router.register('users_info', views.UserViewSet, basename="UserView")
router.register('recent_posts', views.RecentViewSet, basename="RecentView")
router.register('search_posts', views.SearchViewSet, basename="SearchView")
router.register('buying_list', views.BuyingViewSet, basename = 'TestView')
router.register('best_product', views.BestProductViewSet, basename = 'BestProductView')
# router.register('posts_search', views.PostListCreateView.as_view(), basename='PostListCreate')
# router.register(r"posts/(?P<post_id>\d+)/comment", views.CommentViewSet)
# <post_id> view단에서 활용 ..// <post_id>\d -> 뒤에 숫자가 온다는 의미

app_name = 'product_serializer'
urlpatterns = [
    path('api/', include(router.urls)),
]

# http http://localhost:8000/product_serializer/api/posts 상품조회
# http http://localhost:8000/product_serializer/api/posts/5/ 상품조회
