from django.shortcuts import render

# Create your views here.
from django.http import  HttpResponse
import datetime
from quienEsQuien.models import Usuarios
from django.template import loader
# doc_externo = loader.get_template('base.html')
# documento = doc_externo.render({})


from django.shortcuts import render, redirect

prueba="""<html>
<body>
<h1>
Hola Mundo
</h1>
</body>
</html>
"""


def prediccion(request): #primera vista, debemos linkarla a una url en urls.py
    return render(request, 'partials/Prediccion.html', {})

def introduccion(request): #primera vista, debemos linkarla a una url en urls.py
    return render(request, 'partials/Introduccion.html', {})

def explicatividad(request): #primera vista, debemos linkarla a una url en urls.py
    return render(request, 'partials/Explicatividad.html', {})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def password(request):
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

