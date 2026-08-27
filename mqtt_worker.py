import os
import json
import django
import paho.mqtt.client as mqtt

# Configura o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from api_rover.models import Rover, Telemetria


# Quando conectar no broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT conectado com sucesso!")

        client.subscribe("rover/telemetria")

        print("📡 Inscrito no tópico: rover/telemetria")
    else:
        print(f"❌ Erro ao conectar. Código: {rc}")


# Quando receber uma mensagem
def on_message(client, userdata, msg):
    print("\n📩 Mensagem recebida!")
    print(f"Tópico: {msg.topic}")

    try:
        # Converte a mensagem recebida para texto
        mensagem = msg.payload.decode()

        print(f"Mensagem: {mensagem}")

        # Converte o JSON para Python
        dados = json.loads(mensagem)

        # Pega o ID do Rover
        id_rover = dados.get("id_rover")

        if not id_rover:
            print("❌ Erro: id_rover não foi enviado.")
            return

        # Procura o Rover no banco
        try:
            rover = Rover.objects.get(id_rover=id_rover)
        except Rover.DoesNotExist:
            print(f"❌ Rover '{id_rover}' não encontrado no banco.")
            return

        # Cria a telemetria no banco
        telemetria = Telemetria.objects.create(
            rover=rover,
            umidade_solo=dados.get("umidade_solo"),
            umidade_ar=dados.get("umidade_ar"),
            temperatura_ar=dados.get("temperatura_ar"),
            qualidade_ar=dados.get("qualidade_ar"),
            latitude=dados.get("latitude"),
            longitude=dados.get("longitude"),
            sinal_lora_rssi=dados.get("sinal_lora_rssi")
        )

        print("✅ Telemetria salva com sucesso!")
        print(f"🆔 Rover: {rover.id_rover}")
        print(f"🌱 Umidade do solo: {telemetria.umidade_solo}%")
        print(f"💧 Umidade do ar: {telemetria.umidade_ar}%")
        print(f"🌡️ Temperatura: {telemetria.temperatura_ar}°C")
        print(f"📡 RSSI: {telemetria.sinal_lora_rssi} dBm")

    except json.JSONDecodeError:
        print("❌ Erro: a mensagem recebida não é um JSON válido.")

    except Exception as e:
        print(f"❌ Erro ao salvar telemetria: {e}")


# Cria o cliente MQTT
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message


# Broker de teste
BROKER = "test.mosquitto.org"
PORTA = 1883

print("🔌 Conectando ao broker MQTT...")

client.connect(BROKER, PORTA, 60)

# Mantém o MQTT funcionando
client.loop_forever()