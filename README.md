# PFO 3 – Sistema Distribuido Cliente-Servidor

## Descripción

Desarrollo de un sistema distribuido utilizando Python y sockets, basado en una arquitectura cliente-servidor.

El objetivo es permitir la comunicación entre múltiples clientes y servidores, distribuyendo tareas para mejorar la disponibilidad, escalabilidad y eficiencia del sistema.

## Objetivos

- Implementar comunicación mediante sockets TCP.
- Gestionar múltiples clientes.
- Distribuir tareas entre servidores workers.
- Implementar un Thread Pool para administrar los hilos.
- Incorporar autenticación de clientes.
- Registrar eventos mediante Logging.
- Implementar timeout para conexiones inactivas.
- Incorporar un protocolo de mensajería.
- Evaluar el uso de multiprocesos.
- Integrar RabbitMQ, PostgreSQL y almacenamiento distribuido.
- Incorporar balanceo de carga mediante Nginx.

## Tecnologías

- Python
- TCP Sockets
- Threading
- Multiprocessing
- RabbitMQ
- PostgreSQL
- Nginx
- Git y GitHub

## Estructura del proyecto

```text
pfo3-sistema-distribuido/
│
├── servidor/
│   └── server.py
│
├── cliente/
│
├── logs/
│
└── README.md
```

## Estado del desarrollo

### Etapa 1 – Configuración inicial
- [x] Creación del repositorio GitHub.
- [x] Configuración del proyecto en Visual Studio Code.
- [x] Creación de carpetas principales.

### Etapa 2 – Comunicación Cliente-Servidor
- [x] Creación del servidor TCP básico.
- [X] Implementación del cliente TCP.
- [X] Prueba de envío y recepción de mensajes.

### Etapa 3 – Mejoras del servidor
- [ ] Thread Pool.
- [ ] Autenticación de clientes.
- [ ] Logging de actividad.
- [ ] Timeout de conexiones.
- [ ] Protocolo de mensajería.

### Etapa 4 – Arquitectura distribuida
- [ ] Servidores Workers.
- [ ] Comunicación mediante RabbitMQ.
- [ ] Integración con PostgreSQL.
- [ ] Balanceador Nginx.
- [ ] Almacenamiento distribuido.

### Etapa 5 – Pruebas y documentación
- [ ] Pruebas de concurrencia.
- [ ] Pruebas de comunicación.
- [ ] Diagrama de arquitectura.
- [ ] Documentación final.