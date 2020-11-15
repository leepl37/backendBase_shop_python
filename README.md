
## 검색엔진 엔지니어 과제 테스트


### [웹사이트주소](https://gwanholee.azurewebsites.net/)  : 아이디=tony 패스워드=shirth, 회원가입해도 무관.
  무료서버라 로딩타임이 2분 정도 걸립니다....


### 필수스택
* Python3.6 이상
* Django 3.1 이상
* Django REST Framework 사용
* uWSGI

### 구현 기능

##### 회원기능
* 회원가입 1-1

```py
class SignupSerializer(ModelSerializer):
  password = serializers.CharField(write_only = True)
  def create(self, validated_data):
    user = User.objects.create(username = validated_data["username"])
    user.set_password(validated_data["password"])
    user.save()
    return user         
    
  class Meta:
    model = User
    fields = ['pk','username','password']
```


* 로그인 1-2

```py
from rest_framework_jwt.views import obtain_jwt_token (토큰으로 로그인 인증)
```

* 회원정보 제공 1-3

```py
class UserViewSet(ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = UserSerializer

  def get_queryset(self):
    qs = super().get_queryset()
    qs = qs.filter(
    Q(username=self.request.user)
    )
    return qs
```


##### 상품 관리 기능 
> 상품조회 
* 2-1 name 필드 검색을 통한 n개 상품을 조회 기능 페이지네이션 구현

```py
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
```


* 2-2 상품별 주문수 내림차순으로 페이지네이션 후 조회 기능 구현

```py
class OrderViewSet(ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer

  class Meta:
    model = Order
    # 내림차순
    ordering = ['-quantity']
```


* 2-3 최근 일주일간 등록된 제품을 최신순으로 조회 기능 페이지네이션 구현
```py
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
```


> 주문조회  
*  2-4 로그인한 회원의 구매리스트 조회 기능 구현(중복된 구매상품은 최근 주문만)

```py
class BuyingViewSet(ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = BuyingSerializer

  def get_queryset(self):
    qs = super().get_queryset()
    qs = qs.filter(
    Q(username=self.request.user)
    )
    return qs
```


> 통계
* 2-5 가장 많은 사용자가 구매한 상품 리스트 조회(단순 주문 수 X)

```py
class BestProductSerializer(serializers.ModelSerializer):
  product = serializers.SerializerMethodField('find_best_product')

  class Meta:
    model = Product
    fields = "__all__"

  def find_best_product(self, product):
    li=[n.count for n in product.objects.all()]
    index=li.index(max(li))
    best_product=product.objects.all()[index]
    return best_product
```
(웹에선 작동은 되지만, API는 구현 하지못하였습니다.)


### Model 설계

서비스 회원정보 모델. 회원의 프로필 사진을 포함하고 Django User 와 연동되는 프로필 모델이다.

> Profile Model

```py
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
```

> Product Model

상품정보를 저장하는 모델. 각 상품은 다수의 상품 사진을 포함한다. 아래 첨부한 상품 데이터를 적절히 활용합니다.

```py
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
```


> Order Model
상품의 주문정보를 저장하는 모델. 본 모델은 구매자의 구매관리 에 활용한다.

```py
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
```




