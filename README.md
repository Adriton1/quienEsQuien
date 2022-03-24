# quienEsQuien

Members | Email | GitHub | LinkedIn
:------------: | :-----: | :------: | :-----:
Adrián López Couso | adrianlopezcouso@gmail.com | Adriton1 | https://www.linkedin.com/in/adrian-l%C3%B3pez-couso-657988180/

### COORDINATION APP:
https://trello.com/b/Q4gxKaU5/tfg

### MODELS:
- **User:** model made to contain the client data.
- **User prediction:** model that contains all the data related to the user prediction, How long did it take the user to perform the test?, How many times did the user press the Key-Back?, How many times did the user press the Key-Space?, ...

### USER TYPES:
- **Guest User:** Unregistered users will be able to navigate throughout the web page to see the app but, they wont be allowed to make the prediction (This template will be hide for this users).
- **Registered user:** The registered user will be able to perform everything the guest user can do, plus being able to make the prediction (This template will be showed to the registered users).
- **Admin:** He will be able perform everything the registered user can do, but he can also add, modify or delete users, and users predictions.


### ALGORITHM:
The app will be able to find out which user is typing once the prediction has been made. 3 base cases must be loaded so that, the first user to register in the app can carry out the prediction test with more cases analyzed apart from their own.


## PHASE 1

![Register page](/Phase1Images/Registro.png "Register")
In this page the users will be able to create a new account if they don't already have one.

![Login page](/Phase1Images/Login.png "Login")
This is the login where user will be able to log in to the web application if they have an existing account.

![LoginError page](/Phase1Images/LoginError.png "LoginError")
If something goes wrong with the login, the user will be redirected to this page and try again the login.

![Forgotten password page](/Phase1Images/Restaurar_Contraseña.png "Password Recovery Page")
If the users forget their passwords, they will be redirected to this page to get an email to change their password.

![Introduction page](/Phase1Images/Introducción.png "Introduction")
This page display the information related to the application: Application developer, algorithm developer and what programming language has been used to develop it.

![Prediction page](/Phase1Images/Predicción.png "Prediction")
This page display a test text, the user must write the same text in the space below. The algorithm will analyze your writing: speed, errors, time it takes to perform the test, etc.

![Explainability page](/Phase1Images/Explicatividad.png "Explainability")
This page display the information related to the algorithm: How does it work? How does the algorithm analyze the data that is provided?...

![Control panel page](/Phase1Images/Panel_de_Control.png "Control panel")
This page display the information related to the control panel: Users and User prediction's data

![User control panel page](/Phase1Images/Panel_de_Control Usuarios.png "User control panel")
This page display the information related to the users. Admins can add, modify, and delete users from this page. They can also filter by data or search users by their name or email.
