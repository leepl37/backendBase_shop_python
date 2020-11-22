from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from product.models import Product


"""
Profile Model 
서비스 회원정보 모델. 회원의 프로필 사진을 포함하고 Django User 와 연동되는 프로필 모델이다
                """
class Profile(AbstractUser):
    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    addr = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=13,
                                    validators=[RegexValidator(r"^010-?[0-9]\d{3}-?\d{4}$")], blank = True)
    user_photo = models.ImageField(
        blank=True, null=True, upload_to='accounts/%y%m')
    gender = models.CharField(max_length=80, choices=GENDER_CHOICE, null=True)
    buying_order = models.ManyToManyField(Product, blank = True)
    # buying_order = models.ForeignKey(Product, on_delete=models.CASCADE)
    
