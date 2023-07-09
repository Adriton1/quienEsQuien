from django.urls import path

from quienEsQuien.views import introduccion, prediccion, login_user, register, password, loginError, logout_user, saveData, saveRecogidaDatos, recogidaDatos #importamos la vista que esta en el archivo views de mi proyecto DjangoTFG

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('introduccion/', introduccion, name = 'introduccion'), #como hemos puesto saludo/, deberemos poner eso en la url para que nos muestre el Hola mundo
    path('prediccion/', prediccion, name = 'prediccion'), #como hemos puesto saludo/, deberemos poner eso en la url para que nos muestre el Hola mundo
    path('recogida_Datos/', recogidaDatos, name = 'recogidaDatos'),
    path('', login_user, name = 'login'),
    path('logout/', logout_user, name = 'logout'),
    path('register/', register, name = 'register'),
    path('password/', password, name = 'password'),
    path('loginError/', loginError, name = 'loginError'),
    path('saveData', saveData),
    path('saveRecogidaDatos', saveRecogidaDatos),

]

urlpatterns += staticfiles_urlpatterns()