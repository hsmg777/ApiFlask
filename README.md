CORE Restaurante (React + Flask + Ngrok)

Este proyceto "MVC Restaurante" fue desadesarrollado de la siguiente manera:
FRONT END -> REACT
API MVC -> FLASK
BASE DE DATOS -> SQL SERVER MANAGMENT

En este mini core el frontend fue deployado en vercel con el siguiente URL: 
https://preact-mauve.vercel.app
el cual se conecta con el link de ngrok "https://1b0a-181-198-15-238.ngrok-free.app" que simula un despliegue de la API local de FLASK para poder consumir todos sus métodos CRUD, la api se conecta con l base de datos para poder obtener los datos.

ESTA aplicación fue diseñada para ayudar a una mejor gestión de el pedido de platos de un menú de un restaurante asi como mejorar la experiencia del usuario al ir a un restaurante.
 
POR EL MOMENTO LA APP esta en desarrollo tiene en funcionamiento la parte de el ADMINISTRADOR Y TODO LO QUE EL PUEDE REALIZAR (Gestionar usuarios, Gestionar Mesas, Historial de ordenes, Historial de horas laboradas por los empleados y gestión de platos del menú)

Para su funcionamiento tendrás que: 
 En el código de la API:
 - verificar la conexión con la base de datos de SQL 
 - verificar que tengas todas las instalaciones necesarias para Flask, etc
 EN SQL:
	 CREAR UNA BD CON EL NOMBRE: "INGWEB"
	CREAR TABLAS DE ("Mesa", "Orden", "Plato", "registroHoras", 	"Usuario")
 
/* OJO TIENES QUE CORRER LA API LOCALMENTE PRIMERO CON Python app.py*/
luego en un cmd correr el comando (ngrok http 50000)
el link que te da ngrok lo usaras en el frontend
 EN REACT:
	- verificar el link de ngrok
	y la despliegas en vercel nuevamente 


con estas indicaciones el proyecto esta listo para usarse
 link de api: 
 https://github.com/hsmg777/ApiFlask
 link de react: 
 https://github.com/hsmg777/preact
 

contacto:
hayland.montalvo@udla.edu.ec


