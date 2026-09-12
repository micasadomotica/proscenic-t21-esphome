# Proscenic T21 con ESPHome

Integracion local de la Proscenic T21 mediante un D1 mini ESP8266 y el componente Tuya MCU de ESPHome. Validada fisicamente con ESPHome 2026.8.2. Expone estados, sensores y controles de coccion en Home Assistant.

## Configuracion

El paquete utiliza el componente Tuya MCU incluido en ESPHome. No necesita external_components ni MQTT. La API nativa conecta con Home Assistant.

1. En Device Builder crea el dispositivo `proscenic-t21` para ESP8266.
2. Conserva la clave API generada por Device Builder. En su editor de secretos guarda `wifi_ssid`, `wifi_password`, `t21_api_key` y una contrasena propia `t21_ota_password`. No publiques estos datos.
3. Usa `examples/proscenic-t21.yaml`. Para instalar desde archivos locales, coloca la carpeta `packages` junto al YAML del dispositivo y usa `t21: !include packages/proscenic-t21.yaml`.
4. Para cargar el paquete desde GitHub, sustituye esa entrada por:

```yaml
packages:
  t21:
    url: https://github.com/micasadomotica/proscenic-t21-esphome
    files:
      - packages/proscenic-t21.yaml
    ref: main
    refresh: always
```

Posteriormente conviene fijar una etiqueta de version probada. Actualizar el repositorio no modifica el ESP hasta recompilar e instalar.

## Conexion

El usuario ha verificado el orden del conector con multimetro. Identificar por funcion y orientacion real, no por color del cable.

| Senal de la freidora | D1 mini |
| --- | --- |
| Alimentacion 5 V, una vez confirmada | 5V |
| GND | G |
| TX de la MCU | RX / GPIO3 |
| RX de la MCU | TX / GPIO1 |

Confirmar tambien que las senales UART son de 3,3 V: verificar el orden no confirma sus niveles. El ESP8266 no admite logica de 5 V en sus GPIO. Si son de 5 V, se necesita adaptacion de nivel antes de conectar. No conectar 5 V al pin 3V3.

Primera programacion por USB con el D1 mini completamente separado de la freidora. Desconectar el USB antes del montaje; no conectar un ordenador a la placa instalada y alimentada por la freidora. Montar con la freidora desenchufada, aislar y fijar la placa, conservar la proteccion termica y cerrar antes de alimentar. Conservar el modulo original.

UART inicial: 9600, 8N1. Es un punto de partida pendiente de confirmar con registros. Se desactiva el log serie para no mezclar texto con el protocolo. GPIO1/GPIO3 comparten conexion con el CH340 de esta placa; si hay fallos de recepcion, investigar esa conexion antes de cambiar el firmware o soldar. El ESP8266 emite mensajes de arranque por TX: desactivar logger serie no los elimina.

## Prueba de diagnostico

1. Cargar por USB y comprobar Wi-Fi y API con el ESP separado.
2. Desconectar USB y corriente de la freidora, sustituir el modulo y cerrar el montaje.
3. Alimentar la freidora y abrir Logs por Wi-Fi en Device Builder.
4. Guardar el bloque `Tuya`, `Product` y `Datapoint`, y cualquier aviso de UART. Dejar 60 segundos para la inicializacion. No publicar claves ni datos de red.
5. Sin iniciar calentamiento, observar cambios al retirar/insertar la cesta y seleccionar programa, tiempo y temperatura en el panel, si el aparato permite hacerlo en reposo.
6. Anotar cada accion fisica y el cambio de datapoint correspondiente. Si no hay comunicacion, revisar cableado y niveles antes de probar otra velocidad.

El componente Tuya envia inicializacion, consultas y mensajes de mantenimiento: este diagnostico no es una escucha pasiva. No define escrituras de consignas, restauracion de coccion ni controles de calentamiento. Los sensores HA iniciales son de diagnostico del ESP; los datos de la freidora se inspeccionan en Logs.

## Mapa observado en la unidad probada

| DP | Funcion propuesta por Blakadder |
| --- | --- |
| 1 / 2 | Encendido / inicio-pausa, confirmados |
| 3 / 5 | Programa / estado de coccion, confirmados |
| 6 / 7 / 8 | Inicio diferido / duracion / minutos restantes |
| 12 | Errores (bitmask) |
| 102 | `ON` con la cesta retirada y `OFF` con la cesta insertada |
| 103 | Consigna en Fahrenheit, confirmada como entero |
| 104 / 105 / 106 | Mantener caliente / duracion / habilitar inicio diferido |
| 107 | Temperatura interna en Celsius, valor ambiente coherente |
| 10 / 108 / 109 | Significado incompleto; no exponer controles |

## Controles disponibles

- Encendido y apagado (DP1).
- Inicio y pausa de coccion (DP2).
- Seleccion de los diez programas y modo personalizado (DP3).
- Tiempo de coccion de 1 a 60 minutos (DP7).
- Temperatura de 77 a 204 °C en pasos enteros. El ESP8266 la convierte al valor Fahrenheit que espera la freidora (DP103).
- Mantener caliente y su duracion de 1 a 60 minutos (DP104 y DP105).
- Inicio diferido y su espera de 5 a 720 minutos (DP106 y DP6).

Los controles reflejan el valor confirmado por la MCU y no usan estado optimista. Los DP10, DP108 y DP109 siguen sin exponerse porque su funcion no esta identificada.

## Fuentes

- https://templates.blakadder.com/proscenic_T21.html
- https://blakadder.com/proscenic-in-home-assistant/
- https://esphome.io/components/tuya/
- https://esphome.io/components/packages/

Adaptacion de la informacion del protocolo publicada por Blakadder. Las fotos de la unidad del usuario no se incluyen en el repositorio.

## Validacion realizada el 12 de septiembre de 2026

- ESPHome 2026.8.2: configuracion valida.
- Compilacion completa para d1_mini: SUCCESS.
- RAM: 31.784 / 81.920 bytes (38,8 %).
- Flash: 437.655 / 1.044.464 bytes (41,9 %).
- Se compilo una copia del ejemplo y del paquete con secretos ficticios y API cifrada. No se incluye ese binario: hay que compilar con los secretos propios en Device Builder.
## Validacion fisica

- Comunicacion Tuya MCU estable a 9600 baudios por GPIO1/GPIO3.
- Product ID recibido: `ngdn90sk1yqmk9ww`, firmware MCU `1.0.2`.
- Cesta retirada: DP102 cambia a `ON`; cesta insertada: vuelve a `OFF`.
- Programa de patatas: DP3=1, 18 minutos y 399 °F en la unidad probada.
- Programa de gambas: DP3=2, 8 minutos y 359 °F en la unidad probada.
- Los cambios manuales de tiempo y temperatura se reflejan en DP7 y DP103.
- El apagado devuelve DP1 y DP2 a `OFF`, DP3 a 0 y DP5 a 4.
