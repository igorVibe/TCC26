from django.db import models

class Rover(models.Model):
    id_rover = models.CharField(max_length=50, primary_key=True) # ex: 'ROVER-01'
    nome = models.CharField(max_length=100)
    bateria = models.FloatField(default=100.0)
    ultima_conexao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Telemetria(models.Model):
    rover = models.ForeignKey(Rover, on_delete=models.CASCADE)
    
    # Solo
    umidade_solo = models.FloatField(null=True, blank=True)
    
    # Ar
    umidade_ar = models.FloatField(null=True, blank=True)
    temperatura_ar = models.FloatField(null=True, blank=True)
    qualidade_ar = models.FloatField(null=True, blank=True)
    
    # GPS
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # LoRa
    sinal_lora_rssi = models.IntegerField(null=True, blank=True) # dBm
    
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rover.id_rover} - {self.data_hora}"