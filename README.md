# API reservas y hoteles

Pequeña API que dado un destino como parámetro retorna un JSON con dos campos:

* Lista de reservas (ID y fecha) para ese destino (ordenadas por fecha)
* Lista de hoteles de la ciudad destino (nombre y dirección).

## Requerimientos

* MySQL Server
* Python3
* Librerias varias de Python provistas en requirements.txt

## Instalación y configuración

 Una vez clonado el repositorio ubicarse en el directorio principal. Ingresar al archivo de configuración de nombre `cfg.py` y editar los parámetros de la conexión de la base de datos como corresponda del JSON correspondiente a la variable de nombre `productionConfigParameters`. Ejemplo:

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
- En la tabla `flights_reservations` definí un id independiente del id propio de la reserva para que sea más robusto. Si la API proveedora presentara algún error o repitiera algún id por algún motivo, todo sigue funcionando (por eso tampoco le puse UNIQUE al campo `reservation_id` de la tabla).
- Cuando cualquiera de las apis que consumo falla, capturo el error y muestro el mensaje correspondiente. Una opción posible para el caso de que falle la api de Heroku podría ser registrar el error, pero aún así retornar un resultado extraido de la base de datos (aunque este no sería actualizado)
- En la ejecución de fondo que consume los datos de la api de Heroku (para que no se pierdan), si hay un error solo se registra, pero no muere por una cuestión lógica, de que debe seguir intentando consumir las reservas.
- Utilizo el contenido de 'formattedAddress' provisto como respuesta de la api foursquare, en lugar de 'address', ya que si se consulta por un pais como destino (es decir, sin dar una ciudad particular) la dirección a secas podria ser ambigua. Con la dirección completa, queda más claro.
- No guardo datos de foursquare en base de datos porque no parece necesario. Además mantener la tabla actualizada tendría un costo adicional
- Cuando se le hace un request a la api, se manda un request a las 2 apis consumidas en el momento, para devolver información lo más actualizada posible.
- Si bien la clase VenuesAPIClient podría contar con más métodos para utilizar todas las formas y parámetros de consulta que ofrece la API, solo implementé un único método, ya que es suficiente para el desarrollo de esta api.

Comentarios sobre los tests:
- No agregué tests para verificar que se lance HTTPError cuando falle el request a alguna de las apis, porque de eso se encarga la librería requests, mediante "response.raise_for_status()". Además como estoy mockeando los responses no puedo invocar a la verdadera función, y tampoco tiene sentido lanzar una excepción desde el objeto mock, ya que no testea la funcionalidad real.
- Ya que mockeamos los requests.get no se estaría testeando el armado de la url. Lo hice de esta forma, considerando que nos metemos demasiado dentro de la implementación específica del método. Si aún asi quisiera testearse, se podría agregar lógica a la función mockeada para que valide la url que recibe contra alguna esperada que se podría pasar como argumento adicional en la función auxiliar setUpMockRequest.
- No agregué tests de HotelsAPIClient ni de FlightsReservationsAPIClient considerando que no contienen lógica compleja que testear y que dependen del uso de internet para probar su correcto uso (usar mock requests a este nivel ya no tendría sentido)

