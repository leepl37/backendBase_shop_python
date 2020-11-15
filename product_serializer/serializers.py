from django.forms.models import model_to_dict
from django.http import JsonResponse
from accounts.models import Profile
from rest_framework import serializers
from product.models import Product, Order
from django.conf import settings
from django.contrib.auth import get_user_model


# 상품 조회 페이지
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # fields = ['p_user', 'p_name','price','created_at']
        fields = "__all__"


# 상품별 주문수 내림차순 조회
class OrderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('name_p')
    price = serializers.SerializerMethodField('price_p')

    def name_p(self, order):
        return order.basket_order.p_name

    def price_p(self, order):
        return order.basket_order.price

    class Meta:
        model = Order
        # 내림차순
        ordering = ['-quantity']
        fields = ['name', 'basket_user', 'price', 'quantity']


# http http://localhost:8000/product_serializer/api/orders/ "Authorization: JWT %token%"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','last_login','username','last_name','first_name','email','addr','phone_number','gender','user_photo']

class BuyingSerializer(serializers.ModelSerializer):
    구매물품 = serializers.SerializerMethodField('find_name')

    def find_name(self, user):
        name_p = user.buying_order.all()
        test = [ n.p_name for n in name_p]
        return str(test)
        # test=name_p[0]

        # return str(test)

    class Meta:
        
        model = Profile
        fields = ['username','구매물품']



class BestProductSerializer(serializers.ModelSerializer):
    # product = serializers.SerializerMethodField('find_best_product')
    
    class Meta:
        model = Product
        fields = "__all__"

    # def find_best_product(self, product):
    #     li=[n.count for n in product.objects.all()]
    #     index=li.index(max(li))
    #     best_product=product.objects.all()[index]
    #     return best_product
   