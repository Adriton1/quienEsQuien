//var texto = "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que viv´ia un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían las tres cuartas partes de su hacienda."
//var texto = "Hola buenas tardes.";
var texto = "Adrián";
var i = 0;
var errores = 0;
const text_in = document.getElementById('text_in');
var timestamp1;
var timestamp2;
var tilde = false;

const segundo = 1000;
var tiemposKeyUp = [];
var tiemposKeyPress = [];
var tiemposKeyDown = [];


//Prediccion de texto
document.addEventListener('keyup', function(evento){
    if(!(evento.key == texto[i])){
        errores ++;
        if(evento.key == 'Meta' || evento.key == 'Shift' || evento.key == 'CapsLock'){ // Detectamos los casos base Meta -> Inicio y,  Shift y  -> al hacer la mayuscula
            errores --;
        }
    }

    if(evento.key == texto[i]){
        console.log(evento.timeStamp / segundo);
        tiemposKeyUp.push(evento.timeStamp / segundo);
        // Empezar el contador de tiempo cuando escribe la primera letra o cuando le da al boton

        if(!tilde){
            text_in.textContent = text_in.textContent + texto[i];
        }

        console.log("Exito");
        // añadimos en el html
        i++;
    }

    if(evento.key == 'a' && i === 4){
        if(tilde){
            if(evento.key == 'a'){
                text_in.textContent = text_in.textContent + '\u00E1';
                tiemposKeyUp.push(evento.timeStamp / segundo);
            }
            tilde = false;
            i++;
            errores --;
        }

    }

    if(evento.key === 'Dead'){
        tilde = true;
        errores --;
    }


    console.log(evento.key);

    if(i === texto.length){
        console.log("Felicidades, has escrito bien la palabra");
        console.log("Has tardado un total de: " + (tiemposKeyUp[tiemposKeyUp.length - 1]) + " segundos");
        console.log(errores);
        console.log(tiemposKeyUp);
    }

// Cuando ha escrito toda la cadena hacer funcional el boton para enviar o enviar la informacion ya (mejor la 2 opcion)
});