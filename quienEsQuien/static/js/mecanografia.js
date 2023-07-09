var texto = "De vez en cuando, una nueva tecnología, un antiguo problema y una gran idea se convierten en una innovación.";
//const texto = document.getElementById('textoPrediccion')
var contadorKeyUp = 0;
var contadorKeyDown = 0;
var contadorKeyPress = 0;
var errores = 0;
const text_in = document.getElementById('text_in');
const botonEnviarPrediccion = document.getElementById('botonEnviarPrediccion');
var tildeKeyUp = false;
var tildeKeyDown = false;
var tildeKeyPress = false;
var primeraLetra = false;
const idNombre = document.getElementById('nombreUsuario');
var username =  idNombre.textContent.replace(/\s+/g, '')

const segundo = 1000;
var tiempos = [[], [], []]


function iniciarPrueba() {

    // Comenzamos KEYDOWN
    document.addEventListener('keydown', function(evento){

        if(evento.key == texto[contadorKeyDown]){
            if(contadorKeyDown===0){
                primeraLetra = true;
            }

            if(!tildeKeyDown){
                text_in.textContent = text_in.textContent + texto[contadorKeyDown];
                contadorKeyDown++;
                tiempos[0].push(evento.timeStamp / segundo);
            }

            console.log("Exito");

        }

        if((evento.key == 'i'|| evento.key == 'í') && contadorKeyDown === 36 ){
            if(tildeKeyDown){
                text_in.textContent = text_in.textContent + '\u00ED';
                tiempos[0].push(evento.timeStamp / segundo);
                tildeKeyDown = false;
                contadorKeyDown++;
            }
        }

        if((evento.key == 'o'|| evento.key == 'ó') && contadorKeyDown === 105 ){
            if(tildeKeyDown){
                text_in.textContent = text_in.textContent + '\u00F3';
                tiempos[0].push(evento.timeStamp / segundo);
                tildeKeyDown = false;
                contadorKeyDown++;
            }
        }

        if((evento.key === 'Dead' || evento.key === '´') && (contadorKeyDown === 36 || contadorKeyDown === 105)){
            tildeKeyDown = true;
            tildeKeyPress = true;
        }

        console.log(evento.key);
    });


    // Comenzamos KEYPRESS
    document.addEventListener('keypress', function(evento){

        if(evento.key == texto[contadorKeyPress]){
            tiempos[1].push(evento.timeStamp / segundo);
            console.log("Exito");
            contadorKeyPress++;
        }

        if((evento.key == 'i'|| evento.key == 'í') && contadorKeyPress === 36 ){
            if(tildeKeyPress){
                tiempos[1].push(evento.timeStamp / segundo);
                tildeKeyPress = false;
                contadorKeyPress++;
            }
        }

        if((evento.key == 'o'|| evento.key == 'ó') && contadorKeyPress === 105 ){
            if(tildeKeyPress){
                tiempos[1].push(evento.timeStamp / segundo);
                tildeKeyPress = false;
                contadorKeyPress++;
            }
        }
        console.log(evento.key);
    });



    // Comenzamos KEYUP
    document.addEventListener('keyup', function(evento){

        if(!(evento.key == texto[contadorKeyUp])){
            errores ++;
            if(evento.key == 'Meta' || evento.key == 'Shift' || evento.key == 'CapsLock'){ // Detectamos los casos base Meta -> Inicio y,  Shift y  -> al hacer la mayuscula
                errores --;
            }
        }

        if(evento.key == texto[contadorKeyUp] || primeraLetra){
            if(contadorKeyUp === 0){
                primeraLetra = false;
            }
            tiempos[2].push(evento.timeStamp / segundo);
            console.log("Exito");
            contadorKeyUp++;
        }

        if((evento.key == 'i'|| evento.key == 'í') && contadorKeyUp === 36 ){
            if(tildeKeyUp){
                tiempos[2].push(evento.timeStamp / segundo);
                tildeKeyUp = false;
                contadorKeyUp++;
                errores --;
            }
        }

        if((evento.key == 'o'|| evento.key == 'ó') && contadorKeyUp === 105 ){
            if(tildeKeyUp){
                tiempos[2].push(evento.timeStamp / segundo);
                tildeKeyUp = false;
                contadorKeyUp++;
                errores --;
            }
        }

        if((evento.key === 'Dead' || evento.key === '´') && (contadorKeyUp === 36 || contadorKeyUp === 105)){ //comprobamos que para poner la tilde pulsa la tecla Dead y que estamos en la posicion que nos interesa
            tildeKeyUp = true;
            errores --;
        }

        console.log(evento.key);

        if (contadorKeyUp === texto.length){ //Hemos terminado de escribir la cadena de texto
            console.log( "Has cometido: " +errores + " errores");
            console.log(tiempos);
            botonEnviarPrediccion.classList.remove("disabled")
        }
    });
}

function finalizarPrueba() {
    $.ajax({
        method: "POST",
        url: "/saveData",
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            userData: username,
            tiemposData: JSON.stringify(tiempos)
        }
    })
        .done(function (response){
            console.log(response)
        })
        .fail(function (response){
            console.log(response)
        })
}

