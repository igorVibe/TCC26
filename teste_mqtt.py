import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
PORTA = 1883
TOPICO = "rover/telemetria"

client = mqtt.Client()

print("🔌 Conectando ao broker...")

client.connect(BROKER, PORTA, 60)

mensagem = """
{
    "id_rover": "ROVER-01",
    "umidade_solo": 62.5,
    "umidade_ar": 70.2,
    "temperatura_ar": 28.4,
    "qualidade_ar": 85.0,
    "latitude": -21.20880000,
    "longitude": -50.43280000,
    "sinal_lora_rssi": -72
}
"""

client.publish(TOPICO, mensagem)

print("📤 Mensagem enviada!")
print(mensagem)

time.sleep(2)
client.disconnect()