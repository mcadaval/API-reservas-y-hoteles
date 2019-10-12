# API reservas y hoteles

Pequeña API que dado un destino como parámetro retorna un JSON con dos campos:

* Lista de reservas (ID y fecha) para ese destino (ordenadas por fecha).
* Lista de hoteles de la ciudad destino (nombre y dirección).

## Requerimientos

* MySQL Server
* Python3
* Pip3
* Librerias varias de Python provistas en `requirements.txt`.

## Instalación y configuración

 Una vez clonado el repositorio ubicarse en el directorio principal y ejecutar el siguiente comando, para instalar los módulos de Python necesarios:

`pip install -r requirements.txt`
 
 Luego, ingresar al archivo de configuración de nombre `cfg.py` y editar los parámetros de la conexión de la base de datos como corresponda, del JSON asociado a la variable de nombre `productionConfigParameters`. Ejemplo:

`'mysqlArguments' : {
  'host' : 'localhost',
  'user' : 'root',
  'passwd' : 'mipassderoot',
  'database' : 'api_database'
}`

El nombre por defecto de la base de datos es `api_database` pero también puede ser modificado de ser necesario.

Además se deben definir las credenciales (`clientId` y `clientSecret`) para el uso de la API de Foursquare.

Instalar la base de datos mediante el script `setUpApiDatabase.py`, ubicado en el directorio db. Esta se creará con el nombre definido anteriormente. Para ello ejecutar:

`python setUpApiDatabase.py`

El resto de los atributos configurables en `cfg.py` son opciones de debug y de ejecución propias de la API. Hay un breve comentario explicativo de cada una de ellas en el mismo archivo.

## Cómo iniciar la API

Para inicializar la API, ejecutar el siguiente comando:

`python api.py`

Inmediatamente se verán en la terminal algunas lineas que indican que comienza la ejecución de la API, y a medida que vaya recibiendo consultas, se van a ir actualizando en la misma.

La API se levanta en la siguinte url: http://127.0.0.1:5000/

## Cómo hacerle una consulta a la API

Para hacer consultas se debe utilizar una url con el siguiente formato : 

http://127.0.0.1:5000/recomendationSystem/Country/City/

Por ejemplo: http://127.0.0.1:5000/recomendationSystem/Argentina/Corrientes

IMPORTANTE: Los nombres de los paises y ciudades deben ser dados en Inglés.

#### Extra
Se pueden hacer consultas de país (sin ciudad) utilizando el mismo formato, pero omitiendo la ciudad:

http://127.0.0.1:5000/recomendationSystem/Country/

Por ejemplo: http://127.0.0.1:5000/recomendationSystem/Argentina/

## Cómo ejecutar los tests

Antes de ejecutar los tests configurar parámetros de la base de datos en el archivo `cfg.py`. Esta vez se deben modificar los valores asociados a la variable de nombre `testingConfigParameters`.
Por defecto la base de datos se llama `api_database_test`, pero puede ser modificado.

Obs: el resto de los parámetros dejarlos como están, ya que varios de ellos no tienen efecto.

Una vez configurados, ejecutar el siguiente comando en el directorio tests para que se ejecuten todos los test:

`python -m unittest discover`

Otra opción es ejecutarlos individualmente (por archivo) mediante:

`python archivoDeTests`

Por ejemplo: `python testHotelsManager.py`

## Decisiones de diseño

- Incorporé el uso de una base de datos para preservar localmente las reservas. Esto además permite hacer consultas rápidas y extraer las reservas ya ordenas por fecha.
- Dado que buscamos por pais y ciudad definí un índice compuesto entre estos dos campos en tabla `flights_reservations`. Además, definí un id independiente del id propio de la reserva para que sea más robusto. Si la API proveedora presentara algún error o repitiera algún id por algún motivo, todo sigue funcionando (por eso tampoco le puse UNIQUE al campo `reservation_id` de la tabla).
- Cuando cualquiera de las APIs consumidas falla, capturo el error y se devuelve como estado de la propia API. Otra opción posible para el caso de que falle la API de reservaciones podría ser registrar el error, pero aún así retornar un resultado extraido de la base de datos (aunque este no sería actualizado, ya que podrían faltar reservaciones).
- En la tarea de fondo que consume los datos de la API de reservaciones (para que no se pierdan), si hay un error solo se registra en un log, pero no se muere el proceso por una cuestión lógica, de que debe seguir intentando consumir las reservas.
- Utilizo el contenido de `formattedAddress` provisto como respuesta de la API Foursquare, en lugar de `address` (que es la dirección cortita), ya que si se consulta por un pais como destino (es decir, sin dar una ciudad particular) la dirección a secas podria ser ambigua. Con la dirección completa, queda más claro.
- No guardo localmente los datos provistos por la API de Foursquare porque no parece necesario. Es un caso distinto al de las reservaciones ya que por un lado no se pierde información si no se consume, y por el otro, mantener esa información localmente implicaría también la tarea de que esté actualizada, que es un costo adicional (no así con las reservaciones, ya que se acumulan y no se modifican).
- Cuando se le hace una consulta a la API, se les envía en el mismo momento una consulta a las dos APIs consumidas, para devolver información lo más actualizada posible.
- Si bien la clase VenuesAPIClient podría contar con más métodos para utilizar todas las formas y parámetros de consulta que ofrece la API de Foursquare, solo implementé un único método, ya que es suficiente para el desarrollo de esta API.
- Desarrollé las funcionalidades mediante distinas clases, para que el diseño sea modular y el código reutilizable. Además esto me permite testear mucho más ordenadamente. 
- No agregué tests para HotelsAPIClient ni para FlightsReservationsAPIClient considerando que no contienen lógica compleja que probar y que dependen del uso de internet para probar su correcto uso (usar mocks a este nivel ya no tendría sentido).

## Cómo mejorar la integración si podemos modificar el sistema de reservas 

Si se pudiera modificar el sistema de reservaciones, le agregaría funcionalidad propia para que cuándo está por perder reservas (por estar 10 minutos sin ser consultada), automáticamente le envíe las reservaciones a nuestra API (la que yo implementé).

Esto evitaría tener una tarea de fondo como es ahora, y seguiríamos sin perder ninguna reservación. Este cambio también implicaría introducir cambios en la nueva API, ya que debería ofrecer algún método para poder recibir dichas reservaciones. Se podría agregar un nuevo endpoint que funcione por POST, que reciba todas las reservaciones que le envian y las inserte en la base de datos.

Ante esta nueva funcionalidad es importante tener en cuenta que, si la API es de acceso público, debería contar con algún tipo de autenticación, para evitar que cualquiera nos envie datos falsos.