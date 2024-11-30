CORE Restaurante (React + Flask + Ngrok)

Esta API forma parte del proyceto "MVC Restaurante" que fue desadesarrollado de la siguiente manera:
FRONT END -> REACT
API MVC -> FLASK
BASE DE DATOS -> SQL SERVER MANAGMENT

En este mini core el frontend fue deployado en vercel con el siguiente URL: 
https://preact-mauve.vercel.app
el cual se conecta con el link de ngrok "https://1b0a-181-198-15-238.ngrok-free.app" que simula un despliegue de la API local de FLASK para poder consumir todos sus métodos CRUD, la api se conecta con l base de datos para poder obtener los datos.

ESTA aplicación fue diseñada para ayudar a una mejor gestión de el pedido de platos de un menú de un restaurante asi como mejorar la experiencia del usuario al ir a un restaurante.
 
La api tiene como funcionamiento el crud de TODAS las tablas de la base de datos(Gestionar usuarios, Gestionar Mesas, Historial de ordenes, Historial de tiempo que los empleados se demoran al realizar una orden y gestión de platos del menú)
a su vez existen endpoints que realizan pediciones mediante QUERYS  a la base de datos para obtener la informacion necesaria para poder mostrarla

Para su funcionamiento tendrás que: 
 En el código de la API:
 - verificar la conexión con la base de datos de SQL si es localmente o en azure si la tienes en azure 
 - verificar que tengas todas las instalaciones necesarias para Flask, etc
 EN SQL o Azure:
	 CREAR UNA BD CON EL NOMBRE: "INGWEB"
	CREAR TABLAS DE ("Mesa", "Orden", "Plato", "registroTiempo", "Usuario")
 
/* OJO TIENES QUE CORRER LA API LOCALMENTE PRIMERO CON Python app.py*/
luego en un cmd correr el comando (ngrok http 50000)
el link que te da ngrok lo usaras en el frontend 

con estas indicaciones el proyecto esta listo para usarse.



 link de api: 
 https://github.com/hsmg777/ApiFlask
 link de react: 
 https://github.com/hsmg777/preact
 
contacto:
hayland.montalvo@udla.edu.ec


