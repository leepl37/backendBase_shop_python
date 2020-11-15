from django.db.models import F
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from product.form import OrderForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from product.models import Product, Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from accounts.models import Profile
from django.shortcuts import render
# Create your views here.


@login_required
def list(request):
    if request.method == "POST":
        q = request.POST.get('q', '')
        product = Product.objects.all().filter(p_name__icontains=q)
    else:
        product = Product.objects.all()

    # 페이지네이션
    paginator = Paginator(product, 3)
    if request.GET.get('page') == None:
        page = 1
    else:
        page = request.GET.get('page')
    product = paginator.get_page(page)
    return render(request, 'product/list.html', {
        'product': product,
        'paginator': paginator,
        'page': page,
        'form': OrderForm,
    })


def product_of_week(request):

    timesince = timezone.now() - timedelta(days=7)
    product = Product.objects.all().filter(
        created_at__gte=timesince)[::-1]
    paginator = Paginator(product, 3)
    if request.GET.get('page') == None:
        page = 1
    else:
        page = request.GET.get('page')
    product = paginator.get_page(page)
    return render(request, 'product/list.html', {
        'product': product,
        'paginator': paginator,
        'page': page,
        'form': OrderForm,
    })


@login_required
def shop_basket(request):
    product = request.user.order_set.all()

    paginator = Paginator(product, 5)
    if request.GET.get('page') == None:
        page = 1
    else:
        page = request.GET.get('page')
    product = paginator.get_page(page)
    return render(request, 'product/shop_basket.html', {
        'product': product,
        'paginator': paginator,
        'page': page,
    })


@login_required
def list_add(request, post_pk):
    product = get_object_or_404(Product, pk=post_pk)

    if request.method == "POST":
        order = OrderForm(request.POST)
        if order.is_valid():
            form = order.save(commit=False)
            form.basket_user = request.user
            form.basket_order = product
            form.save()
            messages.info(request, "상품 장바구니에 추가되었습니다.")
            return redirect('product:list')
        else:
            messages.info(request, "상품 99개 이상은 주문할 수 없습니다.")
            return redirect('product:list')


@login_required
def list_remove(request, post_pk):
    order = get_object_or_404(Order, pk=post_pk, basket_user=request.user)
    # product = Post.objects.all().filter(pk = post_pk)
    order.delete()
    messages.success(request, "장바구니에 상품을 제거하였습니다.")
    return redirect('product:shop_basket')


@login_required
def buying_product(request, post_pk):
    order = get_object_or_404(Order, pk=post_pk, basket_user=request.user)
    request.user.buying_order.add(order.basket_order)
    product = Product.objects.all().filter(pk=order.basket_order.pk)
    product[0].plus_count(product[0])
    order.delete()
    return render(request, 'product/buying_product.html', {
        'product': product[0],
        'product_count': product[0].count
    })


def buying_product_list(request):
    # product = request.user_buying_order.all
    return render(request, 'product/buying_product.html')


def buying_delete(request, post_pk):
    order = get_object_or_404(Product, pk=post_pk)
    request.user.buying_order.remove(order)
    return render(request, 'product/buying_product.html')


def best_buying_product(request):
    Product.objects.all()
    li=[n.count for n in Product.objects.all()]
    index=li.index(max(li))
    best_product=Product.objects.all()[index]
    return render(request, 'product/best_buying_product.html',{
        'best_product':best_product,
    })
