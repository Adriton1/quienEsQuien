var texto_Recogida = "De vez en cuando, una nueva tecnología, un antiguo problema y una gran idea se convierten en una innovación." //tilde en la 36 y 105
var contadorKeyUp = 0;
var contadorKeyDown = 0;
var contadorKeyPress = 0;
var errores = 0;
const text_in_Recogida = document.getElementById('text_in_Recogida');
const botonEnviarRecogidaDatos = document.getElementById('botonEnviarRecogidaDatos');
var tildeKeyUp = false;
var tildeKeyDown = false;
var tildeKeyPress = false;
var primeraLetra = false;
const idNombre_Recogida = document.getElementById('nombreUsuario');
var username =  idNombre_Recogida.textContent.replace(/\s+/g, '')

const segundo_Recogida = 1000;
var tiempos = [[], [], []]


function iniciarRecogida() {

    // Comenzamos KEYDOWN
    document.addEventListener('keydown', function(evento){

        if(evento.key == texto_Recogida[contadorKeyDown]){
            if(contadorKeyDown===0){
                primeraLetra = true;
            }

            if(!tildeKeyDown){
                text_in_Recogida.textContent = text_in_Recogida.textContent + texto_Recogida[contadorKeyDown];
                contadorKeyDown++;
                tiempos[0].push(evento.timeStamp / segundo_Recogida);
            }

            console.log("Exito");

        }

        if((evento.key == 'i'|| evento.key == 'í') && contadorKeyDown === 36 ){
            if(tildeKeyDown){
                text_in_Recogida.textContent = text_in_Recogida.textContent + '\u00ED';
                tiempos[0].push(evento.timeStamp / segundo_Recogida);
                tildeKeyDown = false;
                contadorKeyDown++;
            }
        }

        if((evento.key == 'o'|| evento.key == 'ó') && contadorKeyDown === 105 ){
            if(tildeKeyDown){
                text_in_Recogida.textContent = text_in_Recogida.textContent + '\u00F3';
                tiempos[0].push(evento.timeStamp / segundo_Recogida);
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

        if(evento.key == texto_Recogida[contadorKeyPress]){
            tiempos[1].push(evento.timeStamp / segundo_Recogida);
            console.log("Exito");
            contadorKeyPress++;
        }

        if((evento.key == 'i'|| evento.key == 'í') && contadorKeyPress === 36 ){
            if(tildeKeyPress){
                tiempos[1].push(evento.timeStamp / segundo_Recogida);
                tildeKeyPress = false;
                contadorKeyPress++;
            }
        }

        if((evento.key == 'o'|| evento.key == 'ó') && contadorKeyPress === 105 ){
            if(tildeKeyPress){
                tiempos[1].push(evento.timeStamp / segundo_Recogida);
                tildeKeyPress = false;
                contadorKeyPress++;
            }
        }
        console.log(evento.key);
    });



    // Comenzamos KEYUP
    document.addEventListener('keyup', function(evento){

        if(!(evento.key == texto_Recogida[contadorKeyUp])){
            errores ++;
            if(evento.key == 'Meta' || evento.key == 'Shift' || evento.key == 'CapsLock'){ // Detectamos los casos base Meta -> Inicio y,  Shift y  -> al hacer la mayuscula
                errores --;
            }
        }

        if(evento.key == texto_Recogida[contadorKeyUp] || primeraLetra){
            if(contadorKeyUp === 0){
                primeraLetra = false;
            }
            tiempos[2].push(evento.timeStamp / segundo_Recogida);
            console.log("Exito");
            contadorKeyUp++;
        }

        if((evento.key == 'i'|| evento.key == 'í') && contadorKeyUp === 36 ){
            if(tildeKeyUp){
                tiempos[2].push(evento.timeStamp / segundo_Recogida);
                tildeKeyUp = false;
                contadorKeyUp++;
                errores --;
            }
        }

        if((evento.key == 'o'|| evento.key == 'ó') && contadorKeyUp === 105 ){
            if(tildeKeyUp){
                tiempos[2].push(evento.timeStamp / segundo_Recogida);
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

        if (contadorKeyUp === texto_Recogida.length){ //Hemos terminado de escribir la cadena de texto
            console.log( "Has cometido: " +errores + " errores");
            console.log(tiempos);
            botonEnviarRecogidaDatos.classList.remove("disabled")
        }
    });

}

function finalizarRecogidaDatos() {
    $.ajax({
        method: "POST",
        url: "/saveRecogidaDatos",
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

