from django.shortcuts import render
from django.views import generic
from .models import Car, CarInstance, Profile, Rating

from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def main(request):
    CarListView.as_view()
    return render(
        request,
        'main.html',
    )


def aboutUs(request):
    return render(
        request,
        'about us.html',
    )


def authorisation(request):
    return render(
        request,
        'authorisation.html',
    )


def registration(request):
    return render(
        request,
        'registration.html',
    )


def carList(request):
    return render(
        request,
        'car_list.html',
    )


class CarListView(generic.ListView):
    model = Car
    # context_object_name = 'car_list'
    template_name = 'catalog/main.html'
    context_object_name = 'car'


class CarDetailView(generic.DetailView):
    model = Car
    template_name = 'catalog/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.model
        return context


class ProfileDetailView(generic.DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'catalog/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.user.username
        return context


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')

        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        first_name=name,
                                        last_name=surname)
        user.save()
        login(request, user, backend=None)
        return JsonResponse({'message': 'Пользователь успешно создан!'})

    return JsonResponse({'message': 'Ошибка при создании пользователя'},
                        status=400)


def get_client_ip(request):
    """
    Get user's IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get(
        'REMOTE_ADDR')
    return ip


class RatingCreateView(generic.View):
    model = Rating

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        car_id = request.POST.get('car_id')
        value_str = request.POST.get('value')
        if value_str == 'NaN':
            return JsonResponse({'error': 'Invalid value for rating'}, status=400)
        try:
            value = int(value_str)
        except ValueError:
            return JsonResponse({'error': 'Invalid value format for rating'},
                                status=400)

        ip_address = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        rating, created = self.model.objects.get_or_create(
            car_id=car_id,
            ip_address=ip_address,
            defaults={
                'value': value,
                'user': user
            },
        )
        if not created:
            if rating.value == value:
                rating.delete()
                return JsonResponse({
                    'status': 'deleted',
                    'rating_sum': rating.car.get_sum_rating()
                })
            else:
                rating.value = value
                rating.user = user
                rating.save()
                return JsonResponse({
                    'status': 'updated',
                    'rating_sum': rating.car.get_sum_rating()
                })
        return JsonResponse({
            'status': 'created',
            'rating_sum': rating.car.get_sum_rating()
        })


@csrf_exempt
def UploatRating(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        try:
            rating = Rating.objects.filter(car_id=car_id)[0]
        except ObjectDoesNotExist:
            print(car_id)
        return JsonResponse({'rating': rating.car.get_sum_rating(),
                             'message': 'Рейтинг обнавлен'})

    return JsonResponse({'message': 'Ошибка в обнавлении рейтинга'},
                        status=400)


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """
    next_page = 'catalog'

from django.contrib.auth import authenticate,login


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request,username=username,password=password)
            print(user)
            if user:
                login(request,user,backend=None)
                return JsonResponse({'message':'Пользователь успешно авторизирован'})
            return JsonResponse({'message':'Неверный логин или в пароль'})
        return JsonResponse({'message':'Введите логин и пароль'})
    return {'status': True}


class OrderCar(generic.View):
    model = CarInstance
    def post(self, request, *args, **kwargs):
        carId = request.POST.get('carId')
        dateStart = request.POST.get('dateStart')
        dateEnd = request.POST.get('dateEnd')
        address = request.POST.get('address')
        cost = request.POST.get('cost')

        carInstance = self.model.objects.create(car_id=carId,
                                        due_start=dateStart,
                                        due_back=dateEnd,
                                        cost=cost,
                                        address=address)
        user = request.user if request.user.is_authenticated else None
        Profile.objects.filter(user=user).update(order_id=carInstance)

        return JsonResponse({
            'status': 'created',
        })




