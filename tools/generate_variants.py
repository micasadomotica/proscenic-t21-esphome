from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "packages"
SOURCE = PACKAGES / "proscenic-t21.yaml"


TRANSLATIONS = {
    "Integracion local validada en una Proscenic T21 real.": "Locally validated on a real Proscenic T21.",
    "Los controles escriben exclusivamente datapoints documentados y observados.": "Controls only write documented and observed datapoints.",
    "Iniciar o pausar coccion": "Start/Pause Cooking",
    "Duracion de mantener caliente": "Keep Warm Time Set",
    "Minutos de inicio diferido": "Delayed Cook Time Set",
    "Temperatura configurada": "Configured Temperature",
    "Temperatura interna": "Internal Temperature",
    "Ajustar tiempo de coccion": "Cooking Time Set",
    "Ajustar temperatura": "Cooking Temperature Set",
    "Mantener caliente activo": "Keep Warm Active",
    "Inicio diferido activo": "Delayed Cook Active",
    "Tiempo configurado": "Configured Cooking Time",
    "Tiempo restante": "Cooking Time Remaining",
    "Tiempo encendido ESP": "ESP Uptime",
    "Estado de coccion": "Cooking Mode",
    "Conexion ESPHome": "ESPHome Connection",
    "Coccion iniciada": "Cooking Started",
    "Cesta retirada": "Basket Removed",
    "Seleccionar programa": "Cookbook",
    "Mantener caliente": "Keep Warm",
    "Inicio diferido": "Delayed Cook",
    "Codigo de error": "Error Code",
    "Senal WiFi": "WiFi Signal",
    "Version ESPHome": "ESPHome Version",
    "Personalizado": "Custom",
    "Precalentar": "Preheat",
    "Finalizada": "Cooking Complete",
    "Desconocido": "Unknown",
    "Cocinando": "Cooking",
    "En espera": "Standby",
    "Apagada": "Off",
    "Encendida": "Fryer Powered",
    "Encendido": "Activate Fryer",
    "Programa": "Program",
    "Ninguno": "None",
    "Patatas": "Fries",
    "Gambas": "Shrimp",
    "Pollo": "Chicken",
    "Pescado": "Fish",
    "Filete": "Steak",
}


def english(text: str) -> str:
    for source, target in sorted(TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(source, target)
    return text


def fahrenheit(text: str) -> str:
    text = text.replace(
        '''id(t21_temperatura_control).publish_state(
              roundf((static_cast<float>(x) - 32.0f) * 5.0f / 9.0f)
            );''',
        '''id(t21_temperatura_control).publish_state(static_cast<float>(x));''',
    )
    text = text.replace(
        '''    min_value: 77
    max_value: 204
    step: 1
    unit_of_measurement: "°C"''',
        '''    min_value: 170
    max_value: 400
    step: 1
    unit_of_measurement: "°F"''',
        1,
    )
    text = text.replace(
        '''          id(t21_mcu).set_integer_datapoint_value(
            103,
            static_cast<uint32_t>(roundf(x * 9.0f / 5.0f + 32.0f))
          );''',
        '''          id(t21_mcu).set_integer_datapoint_value(
            103,
            static_cast<uint32_t>(roundf(x))
          );''',
    )
    text = text.replace(
        '''    unit_of_measurement: "°C"
    device_class: temperature
    accuracy_decimals: 0
    icon: mdi:thermometer
    filters:
      - lambda: return roundf((x - 32.0f) * 5.0f / 9.0f);''',
        '''    unit_of_measurement: "°F"
    device_class: temperature
    accuracy_decimals: 0
    icon: mdi:thermometer''',
        1,
    )
    text = text.replace(
        '''    unit_of_measurement: "°C"
    device_class: temperature
    state_class: measurement
    accuracy_decimals: 0
    icon: mdi:thermometer''',
        '''    unit_of_measurement: "°F"
    device_class: temperature
    state_class: measurement
    accuracy_decimals: 0
    icon: mdi:thermometer
    filters:
      - lambda: return roundf(x * 9.0f / 5.0f + 32.0f);''',
        1,
    )
    return text


def main() -> None:
    spanish_celsius = SOURCE.read_text(encoding="utf-8")
    variants = {
        "proscenic-t21-es-celsius.yaml": spanish_celsius,
        "proscenic-t21-es-fahrenheit.yaml": fahrenheit(spanish_celsius),
        "proscenic-t21-en-celsius.yaml": english(spanish_celsius),
        "proscenic-t21-en-fahrenheit.yaml": fahrenheit(english(spanish_celsius)),
    }
    for filename, content in variants.items():
        (PACKAGES / filename).write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
