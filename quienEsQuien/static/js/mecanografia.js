//var texto = "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían las tres cuartas partes de su hacienda."
var texto = "Esta que llaman por ahí Fortuna es una mujer borracha y antojadiza, y sobre todo, ciega, y así no ve lo que hace, ni sabe a quien derriba." //tilde en la 22
//var texto = "Adrián";
var contadorKeyUp = 0;
var contadorKeyDown = 0;
var contadorKeyPress = 0;
var errores = 0;
const text_in = document.getElementById('text_in');
var tildeKeyUp = false;
var tildeKeyDown = false;
var tildeKeyPress = false;
var primeraLetra = false;
const idNombre = document.getElementById('nombreUsuario');
var username =  idNombre.textContent.replace(/\s+/g, '')

const segundo = 1000;
var tiempos = [[], [], []]


function iniciarPrueba() {
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


        if((evento.key == 'i'|| evento.key == 'í') && (contadorKeyDown === 22 || contadorKeyDown === 93)){
            if(tildeKeyDown){
                text_in.textContent = text_in.textContent + '\u00ED';
                tiempos[0].push(evento.timeStamp / segundo);
                tildeKeyDown = false;
                contadorKeyDown++;
            }

        }

        if((evento.key === 'Dead' || evento.key === '´') && (contadorKeyDown === 22 || contadorKeyDown === 93)){
            tildeKeyDown = true;
            tildeKeyPress = true;
        }

        console.log(evento.key);
    });

    //KeyPress
    document.addEventListener('keypress', function(evento){

        if(evento.key == texto[contadorKeyPress]){
            tiempos[1].push(evento.timeStamp / segundo);
            console.log("Exito");
            contadorKeyPress++;
        }

        if((evento.key == 'i'|| evento.key == 'í') && (contadorKeyPress === 22 || contadorKeyPress === 93)){
            if(tildeKeyPress){
                tiempos[1].push(evento.timeStamp / segundo);
                tildeKeyPress = false;
                contadorKeyPress++;
            }

        }
        console.log(evento.key);
    });

    //KeyUp
    document.addEventListener('keyup', function(evento){

        if(!(evento.key == texto[contadorKeyUp])){
            errores ++;
            if(evento.key == 'Meta' || evento.key == 'Shift' || evento.key == 'CapsLock'){ // Detectamos los casos base Meta -> Inicio y,  Shift y  -> al hacer la mayuscula
                errores --;
            }
        }

        if(evento.key == texto[contadorKeyUp] || primeraLetra || contadorKeyDown === 25){
            if(contadorKeyUp === 0){
                primeraLetra = false;
            }
            tiempos[2].push(evento.timeStamp / segundo);
            console.log("Exito");
            contadorKeyUp++;
        }

        if((evento.key == 'i'|| evento.key == 'í') && (contadorKeyUp === 22 || contadorKeyUp === 93)){
            if(tildeKeyUp){
                tiempos[2].push(evento.timeStamp / segundo);
                tildeKeyUp = false;
                contadorKeyUp++;
                errores --;
            }

        }

        if(evento.key === 'Dead' && (contadorKeyUp === 22 || contadorKeyUp === 93)){ //comprobamos que para poner la tilde pulsa la tecla Dead y que estamos en la posicion que nos interesa
            tildeKeyUp = true;
            errores --;
        }

        console.log(evento.key);

        if (contadorKeyUp === texto.length){ //Hemos terminado de escribir la cadena de texto
            console.log( "Has cometido: " +errores + " errores");
            console.log(tiempos);
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

