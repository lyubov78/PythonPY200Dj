from django.shortcuts import render
from .models import get_random_text
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import TemplateForm, CustomUserCreationForm
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView


class MyLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True  # Данный флаг не позволит авторизированному
    # пользователю зайти на страницу с авторизацией и сразу его перенаправит на
    # ссылку редиректа. По умолчанию redirect_authenticated_user = False


class MyFormView(FormView):
    template_name = 'app/template_form.html'  # Шаблон который будет рендерится
    form_class = TemplateForm  # Класс формы который будет валидироваться
    success_url = '/'  # Ссылка для перехода при удачной валидации

    def form_valid(self, form):
        return JsonResponse(form.cleaned_data)


class MyTemplView(TemplateView):
    template_name = 'app/template_form.html'

    def post(self, request, *args, **kwargs):
        received_data = request.POST  # Приняли данные в словарь

        form = TemplateForm(received_data)  # Передали данные в форму
        if form.is_valid():  # Проверили, что данные все валидные
            my_text = form.cleaned_data.get("my_text")  # Получили очищенные данные
            my_select = form.cleaned_data.get("my_select")
            my_textarea = form.cleaned_data.get("my_textarea")

            # TODO Получите остальные данные из формы и сделайте необходимые обработки (если они нужны)
            my_date = form.cleaned_data.get('my_date')
            my_number = form.cleaned_data.get('my_number')
            my_email = form.cleaned_data.get('my_email')
            my_password = form.cleaned_data.get('my_password')
            my_checkbox = form.cleaned_data.get('my_checkbox')
            # TODO Верните HttpRequest или JsonResponse с данными
            return JsonResponse(form.cleaned_data,
                                json_dumps_params={'indent': 4, 'ensure_ascii': False})

        context = self.get_context_data(**kwargs)  # Получаем контекст, если он есть
        context["form"] = form  # Записываем в контекст форму
        return self.render_to_response(context)  # Возвращаем вызов метода render_to_response


class TemplView(View):
    def get(self, request):
        return render(request, 'app/template_form.html')

    def post(self, request):
        received_data = request.POST  # Приняли данные в словарь

        form = TemplateForm(received_data)  # Передали данные в форму
        if form.is_valid():  # Проверили, что данные все валидные
            my_text = form.cleaned_data.get("my_text")  # Получили очищенные данные
            my_select = form.cleaned_data.get("my_select")
            my_textarea = form.cleaned_data.get("my_textarea")

            # TODO Получите остальные данные из формы и сделайте необходимые обработки (если они нужны)
            my_date = form.cleaned_data.get('my_date')
            my_number = form.cleaned_data.get('my_number')
            my_email = form.cleaned_data.get('my_email')
            my_password = form.cleaned_data.get('my_password')
            my_checkbox = form.cleaned_data.get('my_checkbox')
            # TODO Верните HttpRequest или JsonResponse с данными
            return JsonResponse(form.cleaned_data,
                                json_dumps_params={'indent': 4, 'ensure_ascii': False})

        return render(request, 'app/template_form.html', context={"form": form})


def template_view(request):
    if request.method == "GET":
        return render(request, 'app/template_form.html')

    if request.method == "POST":
        received_data = request.POST  # Приняли данные в словарь

        form = TemplateForm(received_data)  # Передали данные в форму
        if form.is_valid():  # Проверили, что данные все валидные
            my_text = form.cleaned_data.get("my_text")  # Получили очищенные данные
            my_select = form.cleaned_data.get("my_select")
            my_textarea = form.cleaned_data.get("my_textarea")

            # TODO Получите остальные данные из формы и сделайте необходимые обработки (если они нужны)
            my_date = form.cleaned_data.get('my_date')
            my_number = form.cleaned_data.get('my_number')
            my_email = form.cleaned_data.get('my_email')
            my_password = form.cleaned_data.get('my_password')
            my_checkbox = form.cleaned_data.get('my_checkbox')
            # TODO Верните HttpRequest или JsonResponse с данными
            return JsonResponse(form.cleaned_data,
                                json_dumps_params={'indent': 4, 'ensure_ascii': False})

        return render(request, 'app/template_form.html', context={"form": form})

        # data = {}
        # data['my_text'] = received_data.get('my_text')
        # data['my_select'] = received_data.get('my_select')
        # data['my_textarea'] = received_data.get('my_textarea')
        # data['my_date'] = received_data.get('my_date')
        # data['my_number'] = received_data.get('my_number')
        # data['my_email'] = received_data.get('my_email')
        # data['my_password'] = received_data.get('my_password')
        # data['my_checkbox'] = received_data.get('my_checkbox')
        # return JsonResponse(data, json_dumps_params={'indent': 4,
        #                                              'ensure_ascii': False})

        # как пример получение данных по ключу `my_text`
        # my_text = received_data.get('my_text')


def login_view(request):
    if request.method == "GET":
        return render(request, 'app/login.html')

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Авторизируем пользователя
            return redirect("app:user_profile")
        return render(request, "app/login.html", context={"form": form})


def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("/")


def register_view(request):
    if request.method == "GET":
        return render(request, 'app/register.html')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Возвращает сохраненного пользователя из данных формы
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("app:user_profile")

        return render(request, 'app/register.html', context={"form": form})


def reset_view(request):
    if request.method == "GET":
        return render(request, 'app/reset.html')

    if request.method == "POST":
        return render(request, 'app/register.html')


def index_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("app:user_profile")
        return render(request, 'app/index.html')


def user_detail_view(request):
    if request.method == "GET":
        return render(request, 'app/user_details.html')

def get_text_json(request):
    if request.method == "GET":
        return JsonResponse({"text": get_random_text()},
                            json_dumps_params={"ensure_ascii": False})

