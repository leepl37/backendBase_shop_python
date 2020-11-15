from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import get_object_or_404
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from product_serializer.serializers import PostSerializer, OrderSerializer, UserSerializer, BuyingSerializer, BestProductSerializer
from product.models import Product, Order
from accounts.models import Profile
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import CreateAPIView
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework import generics




#회원기능 1-3 회원정보 제공


class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    # serializer_class = UserSerializer
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            Q(username=self.request.user)
        )
        return qs



#상품관리기능 2-1 \\ name 필드 검색을 통한 n개 상품을 조회 기능 페이지네이션 구현
class SearchViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['p_name']
    ordering_fileds = ['pk']
    ordering = ['-pk']

    def get_queryset(self):
        q = self.request.query_params.get('q', '')
        qs = super().get_queryset()
        if q:
            qs = qs.filter(p_name__icontains=q)
        return qs

# http http://127.0.0.1:8000/product_serializer/api/searchposts/?search="공"


#상품관리기능 2-2 \\ 상품별 주문수 내림차순으로 페이지네이션 후 조회 기능 구현
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            Q(basket_user=self.request.user)
        )
        return qs
#상품관리기능 2-3 \\ 최근 일주일간 등록된 제품을 최신순으로 조회 기능 페이지네이션 구현
class RecentViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    ordering_fileds = ['pk']
    ordering = ['-pk']

    def get_queryset(self):
        qs = super().get_queryset()
        timesince = timezone.now() - timedelta(days=7)
        qs = qs.filter(created_at__gte=timesince)
        return qs



#상품관리기능 2-4 \\ 로그인한 회원의 구매리스트 조회 기능 구현(중복된 구매상품은 최근 주문만)

class BuyingViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = BuyingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(
            Q(username=self.request.user)
        )
        return qs


#상품관리기능 2-5 \\ 가장 많은 사용자가 구매한 상품 리스트 조회(단순 주문 수 X
class BestProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = BestProductSerializer


class PostViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = PostSerializer

    

