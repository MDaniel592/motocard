# Seguimiento de precios em productos de Motocard

Se hace uno de una servidor NATS para la gestión de mensajes entre microservicios. El proyecto se divide en dos partes:
  - Consultar de stock y precio de products (productor)
  - Aviso por mensajes telegram (consumidor)

Requisitos para hacerlo funcionar:
  1. Tener Docker
  2. Renombrar el fichero .env_example y añadir el TOKEN de un BOT + el CHAT_ID donde recibir el mensaje.
  3. Modificar la lista de tuples en el productor