//var texto = "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que viv´ia un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches, duelos y quebrantos los sábados, lantejas los viernes, algún palomino de añadidura los domingos, consumían las tres cuartas partes de su hacienda."
//var texto = "Hola buenas tardes.";
var texto = "Adrián";
var contadorKeyUp = 0;
var contadorKeyDown = 0;
var contadorKeyPress = 0;
var errores = 0;
const text_in = document.getElementById('text_in');
var tildeKeyUp = false;
var tildeKeyDown = false;
var tildeKeyPress = false;
var primeraLetra = false;
const nombreUsuario = document.getElementById('nombreUsuario');

const segundo = 1000;
var tiempos = [[], [], []]

const boton = document.getElementById('botonPrueba');

function iniciarPrueba() {
    document.addEventListener('keydown', function(evento){

        if(evento.key == texto[contadorKeyDown]){
            if(contadorKeyDown===0){
                primeraLetra = true;
            }
            tiempos[0].push(evento.timeStamp / segundo);
            // Empezar el contador de tiempo cuando escribe la primera letra o cuando le da al boton

            if(!tildeKeyDown){
                text_in.textContent = text_in.textContent + texto[contadorKeyDown];
            }

            console.log("Exito");
            contadorKeyDown++;

        }


        if(evento.key == 'a' && contadorKeyDown === 4){
            if(tildeKeyDown){
                if(evento.key == 'a'){
                    text_in.textContent = text_in.textContent + '\u00E1';
                    tiempos[0].push(evento.timeStamp / segundo);
                }
                tildeKeyDown = false;
                contadorKeyDown++;
            }

        }

        if(evento.key === 'Dead'){
            tildeKeyDown = true;
            tildeKeyPress = true;

        }


        console.log(evento.key);


    // Cuando ha escrito toda la cadena hacer funcional el boton para enviar o enviar la informacion ya (mejor la 2 opcion)
    });

    //KeyPress
    document.addEventListener('keypress', function(evento){

        if(evento.key == texto[contadorKeyPress]){
            tiempos[1].push(evento.timeStamp / segundo);
            // Empezar el contador de tiempo cuando escribe la primera letra o cuando le da al boton

            console.log("Exito");
            contadorKeyPress++;
        }

        if(evento.key == 'a' && contadorKeyPress === 4){
            if(tildeKeyPress){
                if(evento.key == 'a'){
                    tiempos[1].push(evento.timeStamp / segundo);
                }
                tildeKeyPress = false;
                contadorKeyPress++;
            }

        }


        console.log(evento.key);


    // Cuando ha escrito toda la cadena hacer funcional el boton para enviar o enviar la informacion ya (mejor la 2 opcion)
    });

    //KeyUp
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
            // Empezar el contador de tiempo cuando escribe la primera letra o cuando le da al boton

            console.log("Exito");
            // añadimos en el html
            contadorKeyUp++;
        }

        if(evento.key == 'a' && contadorKeyUp === 4){
            if(tildeKeyUp){
                if(evento.key == 'a'){
                    tiempos[2].push(evento.timeStamp / segundo);
                }
                tildeKeyUp = false;
                contadorKeyUp++;
                errores --;
            }

        }

        if(evento.key === 'Dead'){
            tildeKeyUp = true;
            errores --;
        }

        console.log(evento.key);

        if (contadorKeyUp === texto.length){
            console.log(nombreUsuario.textContent);
            console.log(tiempos);
        }

    // Cuando ha escrito toda la cadena hacer funcional el boton para enviar o enviar la informacion ya (mejor la 2 opcion)
    });
}
