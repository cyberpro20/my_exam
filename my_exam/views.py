from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from my_exam.forms import LoginForm, RegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from my_exam.models import Iphone, Cart, CartItem


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            mobile_or_email = form.cleaned_data['mobile_or_email']
            password = form.cleaned_data['password']

            try:
                validate_email(mobile_or_email)
                user = authenticate(request, email=mobile_or_email, password=password)
            except ValidationError:
                user = None

            if user is None:
                user = authenticate(request, username=mobile_or_email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неправильні дані для входу. Спробуйте ще раз.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print("Форма недійсна. Помилки:", form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        else:
            print("Форма недійсна. Помилки:", profile_form.errors)
    else:
        profile_form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'profile_form': profile_form})

@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Оновлення сеансу з новим паролем
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def iphone_view(request):
    iphones_list = Iphone.objects.all()
    paginator = Paginator(iphones_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.items.count()
    return render(request, 'iphone.html', {'page_obj': page_obj, 'cart_count': cart_count})


def add_to_cart(request):
    if request.method == 'POST':
        iphone_id = request.POST.get('iphone_id')
        if iphone_id:
            iphone = get_object_or_404(Iphone, pk=iphone_id)
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, item=iphone)

                if not created:
                    cart_item.quantity += 1
                else:
                    cart_item.quantity = 1

                cart_item.total_price = cart_item.item.price * cart_item.quantity
                cart_item.save()  # Оновлення або створення об'єкта CartItem

                total_price = CartItem.objects.filter(cart=cart).aggregate(total=Sum('total_price'))['total'] or 0

                cart_count = cart.items.count()
                return JsonResponse({'success': True, 'cart_count': cart_count, 'total_price': total_price})
            else:
                return JsonResponse({'success': False, 'message': 'Ви повинні увійти, щоб додати товар до корзини.'})
    return JsonResponse({'success': False, 'message': 'Неприпустимий запит.'})


def confirm_order(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        total_price = cart_items.aggregate(total=Sum('total_price')).get('total', 1)
        return render(request, 'confirm_order.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('login')


def get_cart_count(request):
    if request.user.is_authenticated:
        total_quantity = CartItem.objects.filter(cart__user=request.user).aggregate(total_quantity=Sum('quantity'))[
                             'total_quantity'] or 0
        return JsonResponse({'cart_count': total_quantity})
    return JsonResponse({'cart_count': 0})


def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Item does not exist'})
