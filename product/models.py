from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

"""
Product Model
    상품정보를 저장하는 모델. 각 상품은 다수의 상품 사진을 포함한다. 아래 첨부한 상품 데이터를 적절히 활용합니다. (날짜의 형식
    은 중요하지 않습니다.) 특히 상품 데이터는 주문자와 연결되어야 합니다.
                        """
class Product(models.Model):

    p_name = models.CharField(max_length=200)
    quantity = models.PositiveSmallIntegerField(null=True, default=1, validators=[
                                                MinValueValidator(1), MaxValueValidator(100)])
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.p_name
    
    def plus_count(self, product):
        product.count+=1
        product.save()
        

    def sum(self):
        return self.quantity * self.price

# 사진 여러장 첨부
class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        upload_to='product/%Y/%M/%D', blank=True, null=True)


"""
 Order Model
 상품의 주문정보를 저장하는 모델. 본 모델은 구매자의 구매관리 에 활용한다. (날짜의 형식은 중요하지 않습니다.)
            """
class Order(models.Model):

    basket_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    basket_order = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[RegexValidator(r"^[0-9]?\d{1}$")])

    class Meta:
        ordering = ['-quantity']

    def __str__(self):
        return f'{self.basket_user}\'shop_basket'


