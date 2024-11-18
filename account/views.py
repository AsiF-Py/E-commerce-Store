from django.shortcuts import render,redirect,HttpResponse
from .forms import RegisterForm,LoginFrom,UserProfileUpdateForm,AddressFrom
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as dj_login
from product.models import Category,Product
from django.db.models import Sum
from .models import Address
def home(request):
    categorys = Category.objects.all()
    # best_seller = Product.objects.filter(is_available=True)
    best_seller = Product.objects.annotate(total_sold=Sum('order_items__quantity')).order_by('-total_sold')[:4]

    return render(request,'account/home.html',{'categorys':categorys,'best_seller':best_seller})
def display_category(request):
    category_id = request.POST.get('categoryId')

    products = Product.objects.filter(category=category_id).values()  # Convert QuerySet to a list of dictionaries
    best_seller = products.annotate(total_sold=Sum('order_items__quantity')).order_by('-total_sold').values()


    return JsonResponse({'result': 'success','data':list(best_seller)[0:4]})


def register(request):
    login_form = LoginFrom(request.POST)
    register_form = RegisterForm(request.POST)
    if request.method == 'POST':
        if 'register_submit' in request.POST:
            if register_form.is_valid():
                user = register_form.save()
                user.save()
                Address.objects.create(user=user)
                dj_login(request, user)  # Log the user in after registration
                return redirect('home')
        elif 'login_submit' in request.POST:
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user:
                    dj_login(request, user)
                    return redirect('home')

    else:
        register_form = RegisterForm()
    return render(request,'account/register.html',{'register_form':register_form,'login_form':login_form})

@login_required
def profile_view(request):
    return render(request,'account/profile.html')


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')

            if old_password and new_password1 and new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)  # To prevent the user from being logged out
                return redirect('home')  # or wherever you want to redirect after changing the password

            form.save()
            return redirect('home')  # or wherever you want to redirect after updating the profile
    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, 'account/profile.html', {'form': form})


def update_address(request):
    form = AddressFrom(request.POST, instance=request.user)
    return render(request,'account/address.html',{'form':form})