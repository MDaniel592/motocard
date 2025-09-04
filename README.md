# Seguimiento de Precios de Productos en Motocard

Este proyecto permite monitorear el **stock** y **precio** de productos de Motocard, enviando notificaciones automáticas a través de **Telegram** mediante un sistema de microservicios conectado con **NATS**.

## Arquitectura del proyecto

El sistema se compone de dos microservicios principales:

1. **Productor:** consulta periódicamente el stock y precio de los productos especificados.  
2. **Consumidor:** recibe los mensajes del productor y envía notificaciones a Telegram.

## Requisitos

- [Docker](https://www.docker.com/) instalado y funcionando.  
- Una cuenta de Telegram con un bot creado (obtener `TOKEN`) y el `CHAT_ID` del chat donde se recibirán los mensajes.

## Configuración

1. Copia y renombra el archivo `.env_example` a `.env`.  
2. Añade los valores correspondientes para:  
   ```
   TOKEN=tu_token_de_telegram
   CHAT_ID=tu_chat_id
   ```

3. Modifica la lista de tuplas en el productor para definir los productos que deseas monitorear.

Con Docker, puedes iniciar los microservicios con:
## Uso

Con Docker, puedes iniciar los microservicios con:

```bash
docker compose build && docker compose up
```

El productor comenzará a consultar los productos y enviará mensajes al consumidor, que notificará vía Telegram cualquier cambio en stock o precio.