#Mayara Celestino de Oliveira
#Nathália Maria Martins

import machine
import dht
import time
import urequests
import network

SSID = "Isabella 2g"
PASSWORD = "isabella0707"
thingspeak = 'UAEM5CEP6OXTB0RE'  

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

print("Conectando ao Wi-Fi...", end=" ")
while not station.isconnected():
    print('.', end='')
    time.sleep(0.5)

print('\nConectado!')
print('Endereço IP: ', station.ifconfig()[0])


d = dht.DHT11(machine.Pin(4))
r = machine.Pin(2, machine.Pin.OUT)
r.value(0) 

while True:
    try:
        d.measure()  
        temp = d.temperature()
        umid = d.humidity()
        print("Temperatura: ", temp, "ºC | Umidade: ", umid, "%")
        
        if temp > 31 or umid > 70:
            r.value(1)  
            rele_estado = 1
            print("Relé LIGADO.")
        else:
            r.value(0)  
            rele_estado = 0
            print("Relé DESLIGADO.")
        
        
        url = "https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}".format(
            thingspeak, temp, umid, rele_estado)
        resposta = urequests.get(url)
        resposta.close()

    except Exception as e:
        print("Erro: ", e)

    time.sleep(5)  
