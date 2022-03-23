# Create your views here.
from django.http import  HttpResponse
import datetime
from quienEsQuien.models import Usuarios
from django.template import loader
# doc_externo = loader.get_template('base.html')
# documento = doc_externo.render({})
from django.shortcuts import render, redirect
from .forms import UserResgisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from DjangoTFG import settings
from django.core.mail import send_mail
from .models import *

prueba="""<html>
<body>
<h1>
Hola Mundo
</h1>
</body>
</html>
"""

def left(request):
    currentUser = request.user
    return render(request, 'left-navbar/left.html', {currentUser: "user"})
def prediccion(request): #primera vista, debemos linkarla a una url en urls.py
    return render(request, 'partials/Prediccion.html',{})

def introduccion(request): #primera vista, debemos linkarla a una url en urls.py
    return render(request, 'partials/Introduccion.html', {})

def explicatividad(request): #primera vista, debemos linkarla a una url en urls.py
    return render(request, 'partials/Explicatividad.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Has iniciado sesión"))
            return redirect('introduccion')
        else:
            return redirect('loginError')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("Has cerrado sesión"))
    return redirect('introduccion')

def register(request):
    if request.method == 'POST':
        form = UserResgisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Usuario creado"))
            return redirect('introduccion')
    else:
        form = UserResgisterForm()

    return render(request, 'register.html',{"form":form})

def password(request):
    if request.method == 'POST':
        subject = 'Cambio de contraseña'
        menssage = 'Para cambiar de contraseña accede al siguiente enlace:  http://127.0.0.1:8000/register/'
        email_from = settings.EMAIL_HOST_USER
        email_to = request.POST['email']
        send_mail(subject, menssage, email_from, [email_to])
        return redirect('login')
    return render(request, 'password.html')

def loginError(request):
    return render(request, 'loginError.html')

def dameFecha(request):
    fecha_actual=datetime.datetime.now() #no

    documento = """<html>
    <body>
    <h3>
    %s
    </h3>
    </body>
    </html>
    """ %fecha_actual

    return HttpResponse(documento)

# def calculaEdad(request, edad, agno):
#     periodo= agno - 2022
#     edadFutura = edad + periodo
#     documento = """<html>
#     <body>
#     <h3>
#     En el año %s tendras %s años
#     </h3>
#     </body>
#     </html>
#     """ %(agno, edadFutura)
#
#     return HttpResponse(documento)

def calculaEdad(request,edadActual, agno): #Usamos datos recogidos por la url y los usamos en la funcion
    periodo= agno - 2022
    edadFutura = edadActual + periodo
    documento = """<html>
    <body>
    <h3>
    En el año %s tendras %s años
    </h3>
    </body>
    </html>
    """ %(agno, edadFutura)

    return HttpResponse(documento)

