# PFO3 - Sistema Distribuido en Python

## 1. Descripción del proyecto

Este proyecto corresponde a la Práctica Formativa Obligatoria 3 (PFO3) de la materia Sistemas Distribuidos.

El objetivo es desarrollar una aplicación cliente-servidor utilizando Python y sockets TCP, donde un servidor recibe tareas enviadas por los clientes y las distribuye a un conjunto de workers para su procesamiento.

El sistema permite enviar mensajes de texto y ejecutar operaciones matemáticas, devolviendo al cliente el resultado obtenido.

## 2. Objetivos

- Implementar la comunicación entre un cliente y un servidor mediante sockets TCP.
- Recibir y enviar información utilizando el formato JSON.
- Distribuir las tareas recibidas utilizando un pool de workers.
- Procesar diferentes tipos de tareas.
- Implementar el registro de eventos y errores mediante logs.
- Representar una arquitectura distribuida mediante un diagrama.

## 3. Arquitectura del sistema

La arquitectura propuesta contempla los siguientes componentes:

- **Clientes:** aplicaciones web, móviles o clientes Python que envían solicitudes.
- **Balanceador de carga (Nginx/HAProxy):** distribuye las solicitudes entre los servidores disponibles.
- **Servidores workers:** procesan las solicitudes recibidas. Cada servidor cuenta con su propio pool de hilos.
- **RabbitMQ:** permite la comunicación y distribución de mensajes entre los servidores.
- **PostgreSQL:** almacenamiento de información estructurada.
- **Amazon S3:** almacenamiento de archivos y objetos.

### Diagrama de arquitectura

El siguiente diagrama representa la arquitectura distribuida propuesta:

![Diagrama de arquitectura](diagrama-arquitectura.png)

**Aclaración:** Nginx/HAProxy, RabbitMQ, PostgreSQL y Amazon S3 forman parte del diseño arquitectónico propuesto. No se encuentran implementados ni desplegados en esta versión del proyecto.

La implementación desarrollada en Python utiliza un servidor TCP, un pool de workers y un cliente que se comunica directamente con el servidor.

## 4. Implementación en Python

El proyecto se compone de un cliente y un servidor que se comunican mediante sockets TCP.

### 4.1. Servidor

El servidor se encuentra implementado en `servidor/servidor.py`.

Sus principales responsabilidades son:

- Crear un socket TCP para escuchar conexiones entrantes.
- Aceptar conexiones de clientes.
- Recibir las tareas enviadas en formato JSON.
- Distribuir las tareas al pool de workers.
- Procesar las solicitudes y generar una respuesta.
- Enviar el resultado al cliente.
- Registrar eventos y errores.

#### Pool de workers

Se utiliza `ThreadPoolExecutor` de Python para administrar un conjunto de cinco workers:

`ThreadPoolExecutor(max_workers=5)`

Cada tarea recibida se envía al pool mediante `submit()`, permitiendo que los workers ejecuten el procesamiento.

El servidor también utiliza hilos para atender las conexiones de los clientes.

#### Tipos de tareas procesadas

El servidor permite procesar dos tipos de solicitudes:

**1. Mensajes de texto**

El cliente puede enviar un mensaje para que el servidor lo procese.

Ejemplo de solicitud:

```json
{
    "mensaje": "Hola servidor"
}
```

Respuesta:

```json
{
    "estado": "OK",
    "resultado": "Tarea procesada correctamente: Hola servidor"
}
```

**2. Operaciones matemáticas**

El servidor permite ejecutar las siguientes operaciones:

- Sumar.
- Restar.
- Multiplicar.
- Dividir.

Ejemplo de solicitud:

```json
{
    "operacion": "sumar",
    "numero1": 20,
    "numero2": 10
}
```

Respuesta:

```json
{
    "estado": "OK",
    "resultado": 30
}
```

También se contemplan situaciones de error, como intentar dividir por cero o enviar valores incorrectos.

### 4.2. Cliente

El cliente se encuentra implementado en `cliente/cliente.py`.

Sus principales responsabilidades son:

- Conectarse al servidor mediante un socket TCP.
- Mostrar un menú de opciones.
- Permitir al usuario seleccionar el tipo de tarea.
- Solicitar los datos necesarios para cada operación.
- Enviar las solicitudes al servidor en formato JSON.
- Recibir y mostrar los resultados.
- Permitir finalizar la conexión.

#### Opciones disponibles

Al ejecutar el cliente se muestra el siguiente menú:

```text
========== MENU ==========
1 - Sumar
2 - Restar
3 - Multiplicar
4 - Dividir
5 - Enviar mensaje de texto
0 - Salir
==========================
```

El usuario selecciona una opción, ingresa los datos solicitados y el cliente envía la tarea al servidor.

Por ejemplo, si selecciona la opción 1 (Sumar), puede ingresar los números 20 y 10. El servidor procesa la operación y devuelve el resultado 30.

### 4.3. Comunicación mediante sockets y JSON

La comunicación entre cliente y servidor se realiza mediante sockets TCP.

Los mensajes se intercambian utilizando JSON, lo que permite estructurar los datos de las solicitudes y las respuestas.

Para identificar el final de cada mensaje se utiliza un salto de línea (`\n`).

De esta manera, el cliente puede enviar varias tareas durante una misma conexión sin necesidad de reconectarse para cada solicitud.

### 4.4. Registro de eventos (Logging)

El registro de eventos se encuentra implementado en `servidor/logger.py`.

Se utiliza el módulo `logging` de Python para registrar:

- Inicio y detención del servidor.
- Conexiones y desconexiones de clientes.
- Mensajes recibidos.
- Operaciones matemáticas ejecutadas.
- Resultados de las operaciones.
- Errores de procesamiento y comunicación.

Los registros se guardan en el archivo:

`logs/servidor.log`

Además, los eventos se muestran por consola durante la ejecución del servidor.

## 5. Estructura del proyecto

```text
PFO3/
│
├── cliente/
│   └── cliente.py
│
├── servidor/
│   ├── servidor.py
│   └── logger.py
│
├── logs/
│   └── servidor.log
│
├── diagrama-arquitectura.png
├── .gitignore
└── README.md
```

Descripción de los archivos:

| Archivo | Descripción |
|---|---|
| `cliente.py` | Permite conectarse al servidor, seleccionar y enviar tareas, y recibir resultados. |
| `servidor.py` | Recibe las solicitudes, las distribuye a los workers y devuelve las respuestas. |
| `logger.py` | Configura el registro de eventos y errores. |
| `servidor.log` | Archivo donde se almacenan los registros de ejecución. |
| `diagrama-arquitectura.png` | Representación gráfica de la arquitectura propuesta. |
| `.gitignore` | Excluye archivos temporales y logs del repositorio. |

## 6. Tecnologías utilizadas

- **Python:** lenguaje de programación utilizado para desarrollar el cliente y el servidor.
- **Sockets TCP:** mecanismo de comunicación entre cliente y servidor.
- **JSON:** formato utilizado para intercambiar información.
- **Threading:** permite atender conexiones de clientes mediante hilos.
- **ThreadPoolExecutor:** administra el pool de cinco workers para procesar tareas.
- **Logging:** permite registrar eventos y errores del sistema.
- **Visual Studio Code:** entorno de desarrollo utilizado.

No se requieren librerías externas para ejecutar la implementación actual.

## 7. Cómo ejecutar el proyecto

Para ejecutar la aplicación es necesario iniciar primero el servidor y luego el cliente.

### Paso 1. Abrir el proyecto

Abrir la carpeta principal del proyecto `PFO3` desde Visual Studio Code.

### Paso 2. Iniciar el servidor

Abrir una terminal en Visual Studio Code y ejecutar desde la carpeta raíz del proyecto:

```powershell
py servidor/servidor.py
```

El servidor comenzará a escuchar conexiones en:

```text
127.0.0.1:5000
```

Se mostrará un mensaje indicando que el servidor está escuchando.

**Importante:** dejar esta terminal abierta mientras se utiliza el cliente.

### Paso 3. Iniciar el cliente

Abrir una segunda terminal en Visual Studio Code, manteniendo el servidor en ejecución.

Ejecutar:

```powershell
py cliente/cliente.py
```

El cliente establecerá una conexión con el servidor y mostrará el menú de opciones.

### Paso 4. Enviar tareas

Seleccionar una de las opciones disponibles.

Por ejemplo:

```text
Seleccione una opcion: 1

Ingrese el primer numero: 20
Ingrese el segundo numero: 10

Resultado: 30.0
```

También se pueden enviar mensajes de texto seleccionando la opción 5.

### Paso 5. Finalizar la ejecución

Para finalizar la conexión desde el cliente, seleccionar la opción:

```text
0 - Salir
```

Para detener el servidor, presionar `Ctrl + C` en la terminal donde se encuentra ejecutándose.

## 8. Manejo de errores

El sistema contempla diferentes situaciones de error:

- Imposibilidad de establecer una conexión con el servidor.
- Recepción de mensajes JSON inválidos.
- Ingreso de valores no numéricos en las operaciones.
- Intento de división por cero.
- Errores durante el procesamiento de las tareas.
- Interrupciones o errores de comunicación entre cliente y servidor.

Las respuestas de error se envían al cliente y los eventos correspondientes quedan registrados en el archivo de log.

## 9. Alcance de la implementación

En esta versión se implementó la comunicación cliente-servidor mediante sockets TCP, el intercambio de información en formato JSON y el procesamiento de tareas utilizando un pool de cinco workers.

El cliente permite enviar mensajes de texto y realizar operaciones matemáticas de suma, resta, multiplicación y división.

La arquitectura distribuida propuesta contempla componentes adicionales como Nginx/HAProxy, RabbitMQ, PostgreSQL y Amazon S3, que se incluyen en el diagrama como parte del diseño, pero no forman parte de la implementación funcional actual.

## 10. Conclusión

El desarrollo permitió implementar una aplicación cliente-servidor utilizando Python, aplicando conceptos fundamentales de sistemas distribuidos.

Se logró establecer la comunicación mediante sockets TCP, intercambiar información estructurada utilizando JSON y distribuir tareas para su procesamiento mediante un pool de workers.

Además, se incorporó un mecanismo de registro de eventos y errores, facilitando el seguimiento de la ejecución del sistema.

La solución desarrollada permite comprender el funcionamiento de una arquitectura distribuida básica y constituye una base para futuras ampliaciones.