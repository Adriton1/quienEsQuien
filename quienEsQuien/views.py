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
from config import config
from .models import *

from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.svm import OneClassSVM



def connect():
    """ Connect to the PostgreSQL database server """
    conn = None;
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            return conn


try:
    conn = connect()
    cursor = conn.cursor()
    print("Conexion con la base de datos general exitosa")
    cursor.execute("ALTER TABLE preprocesadorecogida ADD FOREIGN KEY (codigo_usuario) REFERENCES auth_user(id) ON DELETE CASCADE")
    cursor.execute("ALTER TABLE preprocesadoprediccion ADD FOREIGN KEY (codigo_usuario) REFERENCES auth_user(id) ON DELETE CASCADE")
    conn.commit()
    cursor.close()
    conn.close()
except Exception as ex:
    print(ex)


def left(request):
    currentUser = request.user
    return render(request, 'left-navbar/left.html', {currentUser: "user"}) # Vista encargada de mostrar el template del left-navbar, se envia el usuario actual para poder acceder a sus respectivos atrivutos

def prediccion(request): # Vista encargada de mostrar el template de prediccion
    return render(request, 'partials/Prediccion.html',{})

def introduccion(request): # Vista encargada de mostrar el template de introduccion
    return render(request, 'partials/Introduccion.html', {})

def recogidaDatos(request): # Vista encargada de mostrar el template de introduccion
    return render(request, 'partials/Recogida_Datos.html', {})

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


def saveRecogidaDatos(request): # vista a la que se hara la peticion POST desde el archivo mecanografia.js. Esta vista no devolvera ningun template
    if request.method == 'POST': #Comprobamos que la peticion que se ha hecho es POST
        userData = request.POST['userData'] # almacenamos en la var userData el valor que tenga la var userData de nuestro archivo mecanografia.js
        tiemposData = request.POST['tiemposData'] # almacenamos en la var tiemposData el valor que tenga la var tiemposData de nuestro archivo mecanografia.js
        result = json.loads(tiemposData) # parseamos el valor que contenga la var tiemposData a json y lo almacenamos en la var result
        tiempos, H1, H2, HP, PH, PP, HH = convertData(result) # Llamamos a la funcion convertData() y le pasamos como parametro de entrada la var result que contendra los tiempos en formato json. Almacenamos los datos en las variables tiempos, H1, H2, HP, PH, PP, HH
        try:
            conn = connect()
            cursor = conn.cursor()
            print("Conexion con la base de datos general exitosa")
            cursor.execute("select id from auth_user where username = %s", (userData,))
            rows = cursor.fetchall()
            idUser = rows[0]
            query = ("INSERT INTO preprocesadorecogida VALUES('" + userData + "', %s, %s, %s, %s, %s, %s, %s, %s)")  # predefinimos la query que se encargara de insertar los datos en la tabla de nuestra bbdd
            cursor.execute(query, (tiempos, H1, H2, HP, PH, PP, HH, idUser))  # ejecutamos la query y le pasamos los valores tiempos, H1, H2, HP, PH, PP, HH (estos valores corresponderan a cada %s que tenga la query)
            conn.commit()  # llamamos a la funcion commit que almacenara de manera persistente los datos en la tabla

            # Cerramos la conexion con la bbdd
            cursor.close()
            conn.close()
            a = "satisfactorio"
        except Exception as ex:
            print(ex) # si salta una excepcion la mostramos
            a = str(ex)
        return JsonResponse({"message": a})

def calculate_features(records):
    total_features = []
    for record in records:
        features = []
        for variable in record[2:]:
            features.append(np.mean(variable))
            features.append(np.std(variable))
            features.append(np.min(variable))
            features.append(np.max(variable))
        total_features.append(features)

    scaler = 1
    scaler = StandardScaler()
    total_features = scaler.fit_transform(total_features)

    return total_features,scaler

def make_prediction(userData,H1, H2, HP, PH, PP, HH):
    if True: # aqui deberia comprobarse si se ha seleccionado una hipotetica casilla de entrenar nuevamente el modelo..
        conn = connect()
        cursor = conn.cursor()
        print("Conexion con la base de datos exitosa")
        postgreSQL_select_Query = "select username, tiempos, H1, H2, HP, PH, PP, HH from preprocesadorecogida where username='"+userData+"'"
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()
        records.append(["", "", H1, H2, HP, PH, PP, HH])
        features, scaler = calculate_features(records)
        clf = OneClassSVM(gamma='auto', nu=0.1).fit(features)
        # pickle guardar modelo
        result = clf.predict(features)
    else:  # en caso de no haber seleccionado la casilla de entrenar el modelo...
        # cargar modelo previo y escaler
        # clf = pickle.load(../../..)
        pass
        # predecir
        # p_features,_ = calculate_features([["","",H1, H2, HP, PH, PP, HH]])
        # p_features = scaler.transform(p_features)
        # result = clf.predict(np.array(p_features[0]).reshape(1,-1))
    return result

    # Cerramos la conexion con la bbdd
    cursor.close()
    conn.close()
    return result

def saveData(request): # vista a la que se hara la peticion POST desde el archivo mecanografia.js. Esta vista no devolvera ningun template
    if request.method == 'POST': #Comprobamos que la peticion que se ha hecho es POST
        userData = request.POST['userData'] # almacenamos en la var userData el valor que tenga la var userData de nuestro archivo mecanografia.js
        tiemposData = request.POST['tiemposData'] # almacenamos en la var tiemposData el valor que tenga la var tiemposData de nuestro archivo mecanografia.js
        result = json.loads(tiemposData) # parseamos el valor que contenga la var tiemposData a json y lo almacenamos en la var result
        tiempos, H1, H2, HP, PH, PP, HH = convertData(result) # Llamamos a la funcion convertData() y le pasamos como parametro de entrada la var result que contendra los tiempos en formato json. Almacenamos los datos en las variables tiempos, H1, H2, HP, PH, PP, HH
        prediction = make_prediction(userData,H1, H2, HP, PH, PP, HH) # esta predicción se deebería guardar en preprocesadoprediccion y msotrar por pantalla
        try:
            conn = connect()
            cursor = conn.cursor()
            print("Conexion con la base de datos general exitosa")
            cursor.execute("select id from auth_user where username = %s", (userData,))
            rows = cursor.fetchall()
            idUser = rows[0]
            query = ("INSERT INTO preprocesadoprediccion VALUES('"+userData+"', %s, %s, %s, %s, %s, %s, %s, %s, %s)") # predefinimos la query que se encargara de insertar los datos en la tabla de nuestra bbdd
            cursor.execute(query, (tiempos, H1, H2, HP, PH, PP, HH, prediction.tolist(), idUser)) # ejecutamos la query y le pasamos los valores tiempos, H1, H2, HP, PH, PP, HH (estos valores corresponderan a cada %s que tenga la query)
            conn.commit() # llamamos a la funcion commit que almacenara de manera persistente los datos en la tabla

            predictionResult = prediction.tolist()
            # Cerramos la conexion con la bbdd
            cursor.close()
            conn.close()
            if (predictionResult[len(predictionResult) - 1] == -1):
                messages.success(request, ("Tras analizar la prueba de predicción, se ha llegado a la conclusión de que no eres " + userData))
            else:
                messages.success(request, ("Tras analizar la prueba de predicción, se ha llegado a la conclusión de que eres " + userData))
        except Exception as ex:
            print(ex) # si salta una excepcion la mostramos

        #return JsonResponse({"Tras analizar la prueba de predicción, se ha llegado a la conclusión de que eres " : userData})
        return JsonResponse({"message": str(prediction.tolist())})

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



