from django.urls import path

from quienEsQuien.views import introduccion, prediccion, explicatividad, login, register, password, loginError #importamos la vista que esta en el archivo views de mi proyecto DjangoTFG

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('introduccion/', introduccion, name = 'introduccion'), #como hemos puesto saludo/, deberemos poner eso en la url para que nos muestre el Hola mundo
    path('prediccion/', prediccion, name = 'prediccion'), #como hemos puesto saludo/, deberemos poner eso en la url para que nos muestre el Hola mundo
    path('explicatividad/', explicatividad, name = 'explicatividad'),
    path('login/', login, name = 'login'),
    path('register/', register, name = 'register'),
    path('password/', password, name = 'password'),
    path('loginError/', loginError, name = 'loginError'),

]

urlpatterns += staticfiles_urlpatterns()