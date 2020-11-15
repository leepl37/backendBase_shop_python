from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from django.urls import path
from accounts import views
app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.root, name='root'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('passwordchange/', views.passwordchangeview, name='passwordchange'),
    path('profilechange/', views.profilechange, name='profilechange'),
    # API
    
    #회원기능 1-2 \\ 로그인
    path('token/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),



    path('signupAPI/', views.SignupView.as_view(), name='signupAPI'),
    # 다른 웹에서 호출을 하면(http://localhost:8000/accounts/signupAPI/ username=tony password='pass') 뷰단에서 입력된 메소드대로 회원가입이 이루어진다.
   
]
