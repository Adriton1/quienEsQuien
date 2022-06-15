# Create your views here.
from django.http import  HttpResponse
import datetime
from django.http import JsonResponse
import psycopg2
import json
from quienEsQuien.models import Usuarios
from django.template import loader
from django.shortcuts import render, redirect
from .forms import UserResgisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from DjangoTFG import settings
from django.core.mail import send_mail
from .models import *

# Conexion a la bbdd
# try:
#     connection = psycopg2.connect(
#         host='localhost',
#         user='postgres',
#         password='manager',
#         database='quienesquien'
#     )
#     print("Conexion con la base de datos exitosa")
#
#     cursor = connection.cursor()
#     cursor.execute("SELECT version()")
#     row = cursor.fetchone()
#     print(row)
#     cursor.execute("SELECT * from prueba3")
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)
#     #Ejemplo para insertar en la tabla de datos insert into pruebasUsuarios values('Adri', ROW('{"2.35798", "5.63485"}', '{"2.35798", "5.63485"}', '{"2.35798", "5.63485"}'))
# except Exception as ex:
#     print(ex)

usersPrediction, timesPrediction, H1Prediction, H2Prediction, HPPrediction, PHPrediction, PPPrediction, HHPrediction = [], [], [], [], [], [], [], []

try:
    connection = psycopg2.connect(  # nos conectamos a la bbdd
        host='localhost',  # local
        # host='db', #App dockerizada
        user='postgres',
        password='manager',
        database='quienesquien',
        port='5432'
    )
    print("Conexion con la base de datos exitosa")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pruebapreprocesado")  # ejecutamos la query que nos devolvera los valores: username, tiempos, H1, H2, HP, PH, PP, HH y los almacenaremos en los arrays anteriormente definidos
    rows = cursor.fetchall()
    for row in rows:
        usersPrediction.append(row[0])
        timesPrediction.append(row[1])
        H1Prediction.append(row[2])
        H2Prediction.append(row[3])
        HPPrediction.append(row[4])
        PHPrediction.append(row[5])
        PPPrediction.append(row[6])
        HHPrediction.append(row[7])

    print(usersPrediction)
    print(timesPrediction)
    print(H1Prediction)
    print(H2Prediction)
    print(HPPrediction)
    print(PHPrediction)
    print(PPPrediction)
    print(HHPrediction)

    # Cerramos la conexion con la bbdd
    cursor.close()
    connection.close()

except Exception as ex:
    print(ex)  # si salta una excepcion la mostramos

def left(request):
    currentUser = request.user
    return render(request, 'left-navbar/left.html', {currentUser: "user"}) # Vista encargada de mostrar el template del left-navbar, se envia el usuario actual para poder acceder a sus respectivos atrivutos

def prediccion(request): # Vista encargada de mostrar el template de prediccion
    return render(request, 'partials/Prediccion.html',{})

def introduccion(request): # Vista encargada de mostrar el template de introduccion
    return render(request, 'partials/Introduccion.html', {})


def explicatividad(request): # Vista encargada de mostrar el template de explicatividad
    return render(request, 'partials/Explicatividad.html', {})

# def getDataPrediction():
#     try:
#         connection = psycopg2.connect(  # nos conectamos a la bbdd
#             host='localhost',  # local
#             # host='db', #App dockerizada
#             user='postgres',
#             password='manager',
#             database='quienesquien',
#             port='5432'
#         )
#         print("Conexion con la base de datos exitosa")
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM pruebapreprocesado")  # ejecutamos la query y le pasamos los valores tiempos, H1, H2, HP, PH, PP, HH (estos valores corresponderan a cada %s que tenga la query)
#         rows = cursor.fetchall()
#         for row in rows:
#             print(row)
#
#         # Cerramos la conexion con la bbdd
#         cursor.close()
#         connection.close()
#
#     except Exception as ex:
#         print(ex)  # si salta una excepcion la mostramos

def convertData(result): # funcion que se encargara de calcular los tiempos
    contador = 0
    tiempoKeyDown = []
    tiempoKeyPress = []
    tiempoKeyUp = []
    for tiempo in result: # Como en la bbdd se especifican que los tiempos deben ser de tipo real, deberemos recorrer los tiempos y acceder a cada timestamp guardandolo como float en los arrays declarados en las lineas anteriores
        for i in tiempo:
            if (contador == 0): #si contador = 0, significara que nos encontramos en el primer array de tiempos, en este caso tiempoKeyDown
                tiempoKeyDown.append(float(i))

            if contador == 1: #si contador = 1, significara que nos encontramos en el segundo array de tiempos, en este caso tiempoKeyPress
                tiempoKeyPress.append(float(i))

            if contador == 2: #si contador = 2, significara que nos encontramos en el tercer array de tiempos, en este caso tiempoKeyUp
                tiempoKeyUp.append(float(i))

        contador += 1

    tiempos = [tiempoKeyDown, tiempoKeyPress, tiempoKeyUp] # guardamos los 3 arrays en un arrar conjunto

    H1, H2, HP, PH, PP, HH = [], [], [], [], [], []  # declaramos 6 arrays, cada uno de ellos almacenara la diferencia de tiempos entre distintos timestamp de distintas teclas

    for i in range(len(tiempoKeyDown)): #usaremos la var i como referencia, en este caso i representara la tecla A e i+1 representara la tecla B
        if(len(tiempoKeyDown) - 1 >= i):
            H1.append(tiempoKeyUp[i] - tiempoKeyDown[i]) # tiempo de diferencia entre: tiempoKeyUp de la tecla A y entre tiempoKeyDown de la tecla A

            if (len(tiempoKeyDown) - 1 > i):

                H2.append(tiempoKeyUp[i+1] - tiempoKeyDown[i+1]) # tiempo de diferencia entre: tiempoKeyUp de la tecla B y entre tiempoKeyDown de la tecla B

                #HP.append(tiempoKeyUp[i] - tiempoKeyDown[i+1]) valores negativos
                HP.append(tiempoKeyDown[i + 1] - tiempoKeyUp[i]) # tiempo de diferencia entre: tiempoKeyDown de la tecla B y entre tiempoKeyUp de la tecla A

                PH.append(tiempoKeyUp[i+1] - tiempoKeyDown[i]) # tiempo de diferencia entre: tiempoKeyUp de la tecla B y entre tiempoKeyDown de la tecla B

                PP.append(tiempoKeyDown[i+1] - tiempoKeyDown[i]) # tiempo de diferencia entre: tiempoKeyDown de la tecla B y entre tiempoKeyDown de la tecla A

                HH.append(tiempoKeyUp[i+1] - tiempoKeyUp[i]) # tiempo de diferencia entre: tiempoKeyUp de la tecla B y entre tiempoKeyUp de la tecla A

        i+= 1

    return tiempos, H1, H2, HP, PH, PP, HH



def saveData(request): # vista a la que se hara la peticion POST desde el archivo mecanografia.js. Esta vista no devolvera ningun template
    if request.method == 'POST': #Comprobamos que la peticion que se ha hecho es POST
        userData = request.POST['userData'] # almacenamos en la var userData el valor que tenga la var userData de nuestro archivo mecanografia.js
        tiemposData = request.POST['tiemposData'] # almacenamos en la var tiemposData el valor que tenga la var tiemposData de nuestro archivo mecanografia.js
        result = json.loads(tiemposData) # parseamos el valor que contenga la var tiemposData a json y lo almacenamos en la var result
        tiempos, H1, H2, HP, PH, PP, HH = convertData(result) # Llamamos a la funcion convertData() y le pasamos como parametro de entrada la var result que contendra los tiempos en formato json. Almacenamos los datos en las variables tiempos, H1, H2, HP, PH, PP, HH
        try:
            connection = psycopg2.connect( #nos conectamos a la bbdd
                host='localhost', #local
                #host='db', #App dockerizada
                user='postgres',
                password='manager',
                database='quienesquien',
                port='5432'
            )
            print("Conexion con la base de datos exitosa")
            cursor = connection.cursor()
            query = ("INSERT INTO pruebapreprocesado VALUES('"+userData+"', %s, %s, %s, %s, %s, %s, %s)") # predefinimos la query que se encargara de insertar los datos en la tabla de nuestra bbdd
            cursor.execute(query, (tiempos, H1, H2, HP, PH, PP, HH)) # ejecutamos la query y le pasamos los valores tiempos, H1, H2, HP, PH, PP, HH (estos valores corresponderan a cada %s que tenga la query)
            connection.commit() # llamamos a la funcion commit que almacenara de manera persistente los datos en la tabla

            # Cerramos la conexion con la bbdd
            cursor.close()
            connection.close()

        except Exception as ex:
            print(ex) # si salta una excepcion la mostramos
        return JsonResponse({"message": "Recieve..."})


def login_user(request): # En esta vista se gestionara la parte del login
    if request.method == 'POST': # Comprobamos que la peticion que se ha hecho es POST
        username = request.POST['username'] #almacenamos en la var username el valor almacenado en el atributo name = "username" de la etiqueta input en nuestro archivo login.html
        password = request.POST['password'] #almacenamos en la var password el valor almacenado en el atributo name = "password" de la etiqueta input en nuestro archivo login.html
        user = authenticate(request, username = username, password = password) # autenticamos que exista un usuario con ese nombre y contraseña
        if user is not None:
            login(request, user) # En caso de que se haya autenticado con exito, llamamos a la funcion login
            messages.success(request, ("Has iniciado sesión"))
            return redirect('introduccion') # devolvemos el template de introduccion
        else:
            return redirect('loginError') #En caso de que se haya autenticado sin exito, devolvemos el template de loginError
    else:
        return render(request, 'login.html') # la vista devuelve el template de login e caso de que la peticion no sea POST

def logout_user(request): # En esta vista se gestionara la parte del logout
    logout(request) # llamamos a la funcion de logput
    messages.success(request, ("Has cerrado sesión"))
    return redirect('introduccion') # devolvemos el template de introduccion

def register(request): # En esta vista se gestionara la parte del registro
    if request.method == 'POST': # Comprobamos que la peticion que se ha hecho es POST
        form = UserResgisterForm(request.POST) # Creamos una varia form que almacenara el formulario para registrarse
        if form.is_valid(): # en caso de que los datos introducidos sean validos:
            form.save() # guardamos el formulario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Usuario creado"))
            return redirect('introduccion')
    else:
        form = UserResgisterForm() #En caso de que la peticion no sea POST, guardamos en una var form, el formulario que debe rellenar el usuario para registrarse

    return render(request, 'register.html',{"form":form}) # La vista devuelve el templace register, y pasamos por parametro el formulario que se debe rellenar

def password(request): # ¿Eliminar?
    if request.method == 'POST':
        subject = 'Cambio de contraseña'
        menssage = 'Para cambiar de contraseña accede al siguiente enlace:  http://127.0.0.1:8000/register/'
        email_from = settings.EMAIL_HOST_USER
        email_to = request.POST['email']
        send_mail(subject, menssage, email_from, [email_to])
        return redirect('login')
    return render(request, 'password.html')

def loginError(request): # Vista que devolvera el template de login error
    return render(request, 'loginError.html')



