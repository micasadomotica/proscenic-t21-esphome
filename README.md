# Proscenic T21 con ESPHome

Primera fase: diagnostico Tuya MCU con D1 mini ESP8266. Version objetivo ESPHome 2026.8.2. Todavia no validado fisicamente en la freidora. No incluye controles de coccion.

## Configuracion

El paquete utiliza el componente Tuya MCU incluido en ESPHome. No necesita external_components ni MQTT. La API nativa conecta con Home Assistant.

1. En Device Builder crea el dispositivo `proscenic-t21` para ESP8266.
2. Conserva la clave API generada por Device Builder. En su editor de secretos guarda `wifi_ssid`, `wifi_password`, `t21_api_key` y una contrasena propia `t21_ota_password`. No publiques estos datos.
3. Usa `examples/proscenic-t21.yaml`. Para instalar desde archivos locales, coloca la carpeta `packages` junto al YAML del dispositivo y usa `t21: !include packages/proscenic-t21.yaml`.
4. Para cargar el paquete desde GitHub, sustituye esa entrada por:

```yaml
packages:
  t21: github://micasadomotica/proscenic-t21-esphome/packages/proscenic-t21.yaml@main
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

## Mapa de referencia pendiente de validacion

| DP | Funcion propuesta por Blakadder |
| --- | --- |
| 1 / 2 | Encendido / inicio-pausa |
| 3 / 5 | Programa / estado de coccion |
| 6 / 7 / 8 | Inicio diferido / duracion / minutos restantes |
| 12 | Errores (bitmask) |
| 102 | Cesta presente; polaridad pendiente |
| 103 | Consigna en Fahrenheit; la tabla original indica tipo booleano pero los comandos usan entero: verificar |
| 104 / 105 / 106 | Mantener caliente / duracion / habilitar inicio diferido |
| 107 | Temperatura interna, Celsius segun referencia |
| 10 / 108 / 109 | Significado incompleto; no exponer controles |

No se aplican aun estas interpretaciones a entidades de control. La siguiente fase requiere registros reales para comprobar tipos, unidades, limites y comportamiento al reiniciar.

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
- Pendiente: carga en placa y validacion de la comunicacion con la T21.
