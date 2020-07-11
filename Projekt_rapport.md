# Liftarens guide till IoT-galaxen
## Nenad Cuturic, LNU-ID: nc222fz
Projektet går ut på att testa och jämföra så många kommunikationsteknologier och verktyg för IoT som möjligt.
Därför är det svårt att prata om tid det skulle ta för "projektet"  för det är inget klassiskt projekt utan består av ett antal mer eller mindre löst kopplade delar men för att göra allt och gå igenom samtliga delar skulle det krävas kanske 5-6 timmar.

---
## Innehållsförteckning
[TOC]

---
## Mål
Jag har en bakgrund inom både elektronik och IT där jag under många år professionallt sysslat mest med IT och som hobby hållit på med små elektronikprojekt. Däremot har mitt intresse för inbyggda system funnits kvar och jag har relativt ytligt följt utveckling av IoT.

Syftet med projektet är att försöka få ett överblick över de aktuella teknologierna som används inom IoT-området. Baserat på det kommer jag förhoppningsvis lägga en grund för att kunna bedöma både luckorna i kompetensen samt kunna välja åt vilket håll jag skall eller bör gå i framtiden vad det gäller framtida sysselsättning professionellt.
## Material
Jag var väldigt tidigt ute med att börja beställa komponenterna för jag hoppades kunna få dess så fort som möjligt (ganska långt före kursstarten) för att jag hoppades på att kunna börja med att labba så fort jag fått hem grejerna. Corona gjorde att jag hade en hel del ledig tid på jobbet som jag kunde lägga på annat samtidigt som jag blev klar med en annan distanskurs lag läst under våren.

Tyvärr blev det inte riktigt som jag hade hoppats på för corona både hjälpte och själpte: jag hade tid över på jobbet men samtidigt blev leveranstiderna väldigt långa.
Samtidigt skulle jag försöka återanvända en del komponenter, kablar mm. jag hade hemma sedan tidigare.

Till slut fick jag använda följande komponenter:

| Komponent(er)  | Användning                        | Butik/Pris |
| ---------------|-----------------------------------|------------|
| [Raspb.Pi3b](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/),8GB | TIG-stack, Docker, Ubuntu         | Hade sedan tidigare |
| [FiPy Multipack](https://pycom.io/product/fipy-multipack/) | Huvudenhet för IoT, ESP32-baserad | Pycom: €116 (1 uppsättning) |
| [DHT11](https://www.adafruit.com/product/386) Sensor   | Temperatur & fuktighetssensor     | Banggood: 141kr ([kit 37 sensorer](https://www.banggood.com/Geekcreit-37-In-1-Sensor-Module-Board-Set-Starter-Kits-Geekcreit-products-that-work-with-official-Arduino-boards-p-1137051.html?rmmds=myorder&cur_warehouse=CN)) |
| MicroUSB kabel | Programmering och strömförsöjning | Hade sedan tidigare (1) |
| Jumper-kablar  | Ihopkoppling fipy och sensorn     | Hade sedan tidigare (3 skulle räcka för en enkell uppkoppling) |
| Breadboard     | För att koppla ihop fypi/sensor       | Hade sedan tidigare (1 räcker) |


---

### Fipy: Pinnar med beteckningar
![Fipy](https://i.imgur.com/V0lDqJ0.png)


---

### Expansionsskort 3.0: Pinnar med beteckningar
![](https://i.imgur.com/h5dFgas.png)


---

Jag har valt FyPy Multipack-varianten för att fipy stödjer flest kommunikationsprotokoll: BLE, WiF, LoRa/SigFox och LTE dvs. i teorin skall man kunna testa samtliga.

## Utvecklingsverktyg och datorplatform

Som utvecklingsverktyg har jag valt [Atom](https://atom.io/) + [pymakr pluggin](https://docs.pycom.io/pymakr/installation/atom/) av flera skäl: det blev rekommenderat på kursen, jag ville testa det och det stöds av pycom.
Installationsproceduren är rättfram och väl beskriven på de sidorna bakom länkarna ovanför så jag skall inte upprepa instruktionen här.
Jag hade sedan tidigare [node.js](https://github.com/nodesource/distributions/blob/master/README.md) installerad men har man inte det måste det tydligen installeras för att det skall fungera.
På debian-baserad distributioner:
```bash=
sudo apt install nodejs
```
Utvecklingsplattformen blev linux ([kubuntu](https://kubuntu.org) 20.04 LTS) som kopplades ihop med Expansion board 3.1 med hjälp av en microusb-kabel. Pycom erbjuder väldigt bra verktyg för linux och jag använder det på skrivbordet. Dessutom fungerar det utan att man behöver installera några nya drivrutiner. Samma usb-kabel används både som strömkälla och för datakommunikation.
:::warning
:bulb: **OBS!** Man måste använda en usb-kabel som stödjer datakommunikation vilket oftast inte är fallet med usb-kablar som kommer med mobilladdare.
Dessutom skall man inte glöma att lägga den egna användaren i gruppen dialout:
```bash=
sudo usermod -a -G dialout $USER
```
:::
En bra och detaljerad [beskrivning](https://docs.pycom.io/pytrackpysense/installation/firmware/) av hur man uppdaterar firmware för Expansion borad finns på pycom så jag skall inte upprepa det här. Pycom rekommenderar att uppgradera firmware först. Därefter piggyback-ansluts fipy till expansionskortet ...
![](https://i.imgur.com/7AmMR32.png)
för att uppdatera fipy-firmware se [pycom-fwtool](https://docs.pycom.io/gettingstarted/installation/firmwaretool/) (både cli och gui finns). Efteråt kan man göra det även via [pybytes](https://pybytes.pycom.io/) där man först behöver skapa ett gratis-konto. Pycom rekommenderat att göra det innan man börjar använda fipy-enheten. Dessutom registeras enheten för 2-års gratis [SigFox](https://www.sigfox.com/en) anslutningsabonnemnag i samband med registreringen.
Efter att firmware är uppdaterat installera Atom + [pymakr](https://docs.pycom.io/pymakr/installation/atom/) om de inte redan är installerade enligt instruktionen ovan anslut usb-kabeln och utvecklingen kan påbörjas.
Om allt fungerar kommer pymakr känna av enheten så fort expansionskortet ansluts med usb-kabeln. Atom indikerar att enheten är ansluten genom att visa **>>>** och blinkande kursor i pymakr konsolen.
Uppladdning (och nedladdning) av koden sker via två knapparna i vänstra menyn med pilarna upp/ner (se nedan).
![](https://i.imgur.com/SR4XOtX.png)
Fypi kommer automatiskt köra main.py i rotmappen vid varje omstart.
Enskillda skript kan köras genom att markera det i Atom klicka på pilen i konsolens vänstra meny (markerad med röd elips nedan).
![](https://i.imgur.com/0ymynXL.png)

### Elektriskt schema
![](https://i.imgur.com/MQNuU1N.png)

... och fysisk anslutning med hjälp av breadbord och jumper-kablar (detta är också bilden på den färdiga "produkten"):
![](https://i.imgur.com/zT0zKK3.jpg)
Här kan man se microusb-kabeln ansluten till expansionskortet i den högra kanten. Färgerna på jumper-kablarna motsvarar färgerna på det elektriska schemat ovan.
Sensorn DHT11 är en integrerad temperatur- och luftfuktighetssensor. Tyvärr verkar luftfuktighetssensorn vara trasig för den har det lägsta värdet på 95% (det kan gå upp men inte ner). Därför skall man ignorera dess mätvärden där dessa dyker upp senare i dokumentet.
På bilden ser man också LoRaWan/SigFox antenn som är ansluten till Fipy-kortet.

Hur är det då med strömförbrukningen? All strömförsöjning sker via usb-kabeln så detta är inte kritiskt så länge lasten inte överskrider nominala värden (DHT11 ligger långt under dessa).
Betydligt större energiförbrukning går åt den trådlösa kommunikationen via WiFi men den behöver man inte ta hänsyn till heller på grund av usb-anslutningen.

## Nätverkstopologi
IoT-enheter har oftast krav på sig att vara extremt energisnåla för att kunna fungera under lång tid med matning från ett litet batteri. Dessutom behöver de kunna kommunicera över långa avstånd.
Därför har man lagt extra mycket resurser för att utveckla olka energinsnåla trådlösa kommunikationsprotokoll:
* BLE = Bluetoth Low energy
* LoRA = Low-power wide-area
* SigFox
* LPWAN (Low Power Wide Area Networks)
    * NB-IoT = 3GPP (3rd generation partnership project) Narrowband IoT
    * LTE-M = LTE Machine Type Communication

BLE används redan brett i en mängd konsumentprodukter så det är ett etablerat protokol och är inte så intresant att testas.
LPWAN är fortfarande i en testfas och ganska dyr teknologi. Jag hade veltat testa det men blev inte godkänd av Tele2 för test kit. Andra alteranativet var Telenor men de hade inget alteranativ som var helt gratis så de föll bort också.
Då återstod LoRa och SigFox. LoRa visades sig vara extremt svår att få signal med både hemma hos mig samt i centrala Stockholm. Därför blev bara SigFox kvar som enda kandidat för test för lågeffekt trådlös kommunikation men på grund av tidsbrist (det är trots allt bara en grundkurs) blev det bara ett rudminentärt test. Det blev WiFi för nästan hela slanten.

Majoritet av testerna därmed hängde på att fipy kommunicerade via WiFi vilket illustreras på bilden nedan.

![](https://i.imgur.com/zXfp32b.png)
**Legenden**
* Raka linjer representerar kommunikation genom fysiska medier
    1. Heldragna = trådbunden
    2. Prickade = trådlös
* Rundade sträckade linjer representerar logisk kommunikation genom olika fysiska medier
    * Pilarna i ändarna visar kommunikationsrikting

Nedan redovisas hur de olika testerna har genoförts och vad som blev utfallet. Bara källkoden för ett testall redovisas medan resten finns på [github](https://github.com/neskoc/guide_till_IoT_galaxen).
### Trådlös teknologi
#### LoRaWAN ([The Things Network](https://www.thethingsnetwork.org/))
Jag har lagt sammanlagt kanske en veckas tid i försöka att få till test av lora men först i slutet lyckades jag få TTN att visa lite metadata men utan att enheten blev registrerad (se nedan den gröna pricken = sett enheten, men frames up/down=0).
![](https://i.imgur.com/VQfpHiW.png)
Metadata har till slut avslöjat att RSSI/SNR värdena är på gränsen elle under specifikationen.
![](https://i.imgur.com/Vd4e8Vj.png)

#### [SigFox](https://www.sigfox.com/en)
Med SigFox har jag enbart testat att ansluta enheten och skicka lite testadata (se bilden nedan). Det har fungerat utan problem där lora misslyckats (antingen beroende av starkare signal, bättre avkodningsteknik alternativt en kombination)
Stora nackdelen är att väldigt lite data får skickas med SigFox per dag.
![](https://i.imgur.com/k8YDiWh.png)
SigFox använder annars ett eget kommunikationsprotokoll/stack (phy->SigFox MAC->Application layer) för kommunikation mellan klienten och SigFox-basstationen. Därefter paketeras data i standard ip-stack och sedan skickar över internet som standard tcp-paket.

#### WiFi
Koden nedan illustrerar hur fipy ansluts via WiFi till en accesspunkt och skickar data till sjolab.lnu.se med hjälp av mqtt-protokollet. Resten av koden hittas på [github](https://github.com/neskoc/guide_till_IoT_galaxen).
Sensordata läses av och skickas var 30:e sekund.
##### Python källkod
```python=
from network import WLAN
import machine
from machine import Pin
import time
import pycom
import json
import _thread
import ubinascii
import hashlib
from lib.dth import DTH
from lib.umqtt.robust import MQTTClient

pycom.heartbeat(False)

# skapa objekt th (temperatur/humidity) av klassen DTH samt ange att det är Pin 23 som skall användas
# Type 0 = dht11
dht_type = 0
th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN), dht_type)
time.sleep(2)

# läs konfigurationsvärdena
with open('my_config.json') as f:
    config = json.load(f)

# för att inte ständigt ändra pycom_config (nätverk hemma och på jobbet)
# kolla vilket nätverk som är tillgängligt och anslut till det
def connect_wlan():
    wlan = WLAN(mode=WLAN.STA)
    print('Scanning wlan!')
    nets = wlan.scan()
    time.sleep(5)
    for net in nets:
        if net.ssid == config['wifi_work']['ssid']:
            print('Network found: ', net.ssid)
            wlan.connect(net.ssid, auth=(net.sec, config['wifi_work']['password']), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            break
        elif net.ssid == config['wifi_home']['ssid']:
            print('Network found: ', net.ssid)
            wlan.connect(net.ssid, auth=(net.sec, config['wifi_home']['password']), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting
            print('WLAN connection succeeded!')
            break

connect_wlan()

# används för att visa med LED att data skickas ut
def blink_led():
    for n in range(1):
        pycom.rgbled(0xfcfc03)
        time.sleep(0.5)
        pycom.rgbled(0x000000)
        time.sleep(0.2)

# för att visa med LED att kommandot har mottagit (olika färger för olika kommandon)
def sub_cb(topic, msg):
   if msg == b'{"Command":"Red"}': pycom.rgbled(0xff0000)
   if msg == b'{"Command":"Blue"}': pycom.rgbled(0x0004ff)
   if msg == b'{"Command":"Green"}': pycom.rgbled(0x00ff04)
   if msg == b'{"Command":"Yellow"}': pycom.rgbled(0xe5ff00)
   if msg == b'{"Command":"White"}': pycom.rgbled(0xe5ff00)
   if msg == b'{"Command":"Off"}': pycom.rgbled(0x000000)
   print((topic, msg))

# skicka data med jämna mellanrum t_ i tråden
def interval_send(t_):
    while True:
        send_value()
        time.sleep(t_)

# skicka data till sjolab
def send_value():
    try:
        print("Sending sensor data")
        result = th.read()
        while not result.is_valid():
            time.sleep(.5)
            result = th.read()

        client.publish(topic_pub,'{"fipy_nc_sensor": {"dht temp":' + str(result.temperature) +
                                                ',"dht RH":' + str(result.humidity) +
                          '}}')
        print('Sensor data sent! Temperature: {} | Humidity: {}'.format(result.temperature,result.humidity))
        blink_led()
        client.check_msg()

    except (NameError, ValueError, TypeError) as err:
        print('Failed to send!', err)

# ange topic/sub för mqtt
topic_pub = 'nenad/home-sens/'
topic_sub = 'nenad/home-sens/control'
broker_url = 'sjolab.lnu.se'
client_name = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac
print('client_name:',client_name)

# skapa client-objekt för mqtt-kommunikation (data från config-filen)
client = MQTTClient(client_name, broker_url, user=config['sjolab_mqtt']['user_mqtt'], password=config['sjolab_mqtt']['pass_mqtt'], keepalive=600)

# förberedd för kommunikation
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic_sub)

# skapa tråd som skall köra var 30:e sekund (skicka sensordata)
_thread.start_new_thread(interval_send,[30])

```
### Serverapplikationer (lokalt och molntjänster)
När man jobbar med IoT får man välja vad man vill köra lokalt och vad i molnet och vart. Det finns en uppsjö olika tjänster som oftast i begränsad omfattning är gratis men sedan kostar pengar.
Kör man lokalt har man full kontroll och med rätt teknologi kan vara billigare samt säkrare.
Jag har haft en raspberry pi på hyllan vilket gjorde att jag hade ett lätt val. Sedan har det visat sig vara ett klokt val också :smiley: 
Det blev kostndaseffektivt samtidigt och för mig blev det lätt att komma igång trots att jag använde Docker + TIG-stack för första gången (mer info kommer lite längre ner)
#### [Pybytes](https://pybytes.pycom.io/) (Pycom)
Man har möjlighet att spara sensordata (signals) hos pycoms molnplattform pybytes upp till en månad gratis. Se exempel nedan.
![](https://i.imgur.com/kQ0vy7k.png)
Sedan kan man enkellt ansluta till en gratis broker (webhook) varifrån data kan hämtas för vidarebehandling (se exempel nedan).
#### [webhook.site](https://webhook.site/)
Så fort man besöker webhook.site url får man en unik url som kan användas för att skicka data till med hjälp av http/post i json format.
![](https://i.imgur.com/2Lgx8Vy.png)
Via pybytes integrations:
![](https://i.imgur.com/GCgXmHD.png)
kan man sedan skapa en webhook dit:
![](https://i.imgur.com/b2z2HA5.png)
... och så här:
![](https://i.imgur.com/gsPPZfM.png)
ser sensoradata ut efter att det har tryckts ut till den genererade länken.
Nackdelen är att sensordata inte lagras där utan måste kontinuerligt hämtas.
#### [Node-RED](https://nodered.org/) ([IBM cloud](https://cloud.ibm.com/login))
Ibm erbjuder en gratis node-red applikation per konto och det är enkellt att komma igång (följ denna [guide](https://nodered.org/docs/getting-started/ibmcloud)).
Sensordata hämtas från sjolab.lnu.se med hjälp av mqtt-protokollet.
Node-red applikationen är gratis och kan köras lokalt som ett alternativ.
Jag har valt följade testarkitektur (flöden):
![](https://i.imgur.com/G8hMDOX.png)
samt skapat ett "dashboard" där jag kan klicka på knapparna och skicka kommandon tillbaka till fipy (källkoden ovan demonstrerar klientsidan).
Fredrik har lagt en [video på kursens youtubekanal](https://youtu.be/iUU6vhGuH8o?t=1587) där han gått igenom grunderna kring node-red så jag skall ange nedan bara vad som är specifikt för min arkitektur.
1. Hemsensorer-block är en "mqtt in" symbol som hämtar data från sjolab
![](https://i.imgur.com/yZvHoK6.png)
2. Data filtreras (luftfuktighetsvärdena tas bort)/omformas med hjälp en "switch"![](https://i.imgur.com/UmwYYbH.png)![](https://i.imgur.com/yYU7TlV.png)
3. ... och presenteras på dashboard med en "chart" symbol![](https://i.imgur.com/b1OmMB4.png)
4. Knapparna som genererar kommandon läggs via "button":s (bara "RED" illustreras nedan)![](https://i.imgur.com/oSIKndG.png)
5. Och till slut skickas dessa kommandon tillbaka till fipy via sjolab med hjälp av "mqtt ut"![](https://i.imgur.com/icYHNx7.png)

---
**Dashboard**
![](https://i.imgur.com/KODBC0q.png)

#### RaspberryPi 3B
Jag har valt att använda RaspberryPi som en utmärkt och billig lösning för:
* databaslagring (**[InfluxDB](https://www.influxdata.com/)**), samt
* presentation av sensordata(**[Grafana](https://grafana.com/)**)

Själva data hämtas från sjolab.lnu.se med hjälp av **Telegraf** (via mqtt-protokollet).
##### [Docker](https://www.docker.com/)
Docker är en lättviktsplattform utecklad för isolering av olika processer vilka körs som "containers".
Docker kommer inte förinstallerad så den måste installeras manuellt först. Se följande [guide för raspberry pi](https://phoenixnap.com/kb/docker-on-raspberry-pi).
För att kunna köra fler docker-behållare (containers) behöver man installera även docker-compose. Jag hade lite problem med att göra det på min ubuntu-variant för RPi så jag har gjort det via pip (python) se rad 1 nedan.
```bash=
pip3 install docker-compose
git clone https://github.com/neskoc/applied-iot-20.git
cd applied-iot-20/tig-stack/
vim.tiny telegraf.conf
docker-compose up -d
```
Resten av kommandon förklaras rad för rad:
* 2: klona hela projektet från github
* 3: byt till mappen där tig-stack konfiguration finns
* 4: ändra inställningarna för telegraf så att det passar egna värden (för detta labb har jag valt att inte ändra angivna värden)
* 5: starta samtliga (3) behållare i demon mode (i bakgrunden), inställningarna hittas i docker-compose.yml
```yaml=
influxdb:
    image: influxdb:latest
    ports:
        - 8086:8086
    environment:
        INFLUXDB_HTTP_AUTH_ENABLED: "true"
        INFLUXDB_DB: "iot"
        INFLUXDB_ADMIN_USER: "iotlnu"
        INFLUXDB_ADMIN_PASSWORD: "micropython"
        
    volumes:
        - ./data/influxdb:/var/lib/influxdb

grafana:
    image: grafana/grafana:latest
    user: "1001"
    ports: 
        - 3000:3000
    links:
        - "influxdb:influxdb"
    environment:
        GF_SECURITY_ADMIN_USER: admin
        GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
        - ./data/grafana:/var/lib/grafana
    restart: always        

telegraf:
    image: telegraf:latest
    environment:
        HOST_NAME: "telegraf"
        INFLUXDB_HOST: "influxdb"
        INFLUXDB_PORT: "8086"
        DATABASE: "iot"
    links:
        - "influxdb:influxdb"
    volumes:
        - ./telegraf.conf:/etc/telegraf/telegraf.conf
    tty: true
    privileged: true

```
Standardlösenord för Grafanas admin-konto (admin) ändras efter den första inloggningen på 
http://<tilldelad-ip-adress>:3000
där Grafanas standardport är 3000.

Nedan illustreras start av 3 TIG-stack behållare
![](https://i.imgur.com/UAd0K0q.png)
##### [TIG-stack](https://github.com/iot-lnu/applied-iot-20/tree/master/tig-stack)
Valet föll på TIG för att det är en standardiserad lättviktslösning, skriven i öppen källkod som visat sig fungera bra och kan lätt skalas upp. Så det kan köras minimalistisk alternativt maximalistiskt utifrån tillgängliga resurser och behovet.
Mer om TIG-stacken hittas här : [How to Install TIG Stack (Telegraf, InfluxDB, and Grafana) on Ubuntu 18.04 LTS](https://www.howtoforge.com/tutorial/how-to-install-tig-stack-telegraf-influxdb-and-grafana-on-ubuntu-1804/)
![](https://i.imgur.com/482H5GT.png)

1. TIG står för Telegraf, InfluxDB och Grafana.
2. Dessa körs som docker-behållare.
3. Telegraf ser till att data hämtas (kan prata olika protokoll) och sparas i [InfluxDB](https://www.influxdata.com/) samt presenteras i [Grafana](https://grafana.com/).
4. Telegraf-agenten är konfigurerard att körs var 15:e sekund och hämtad data lagras i DB (jag har experimenterat med olika tidsintervall men data kan aldrig lagras oftare än det genereras och fipy koden ovan skickar data var 30:e sekund).
5. InfluxDB automatiskt lagrar data med en tidsstämpel vilket gör att det blir lätt att presentera på en tidsskala.
6. Grafana kan annars hämta data från i princip samtliga kända DB-system.

Nedan illustreras hur en Grafana-Dashboard kan se ut.
![](https://i.imgur.com/cyQJDXy.png)
I stället för att skicka data ut till någon extern tjänst skulle man även kunna lägga en [Eclipse Mosquitto](https://mosquitto.org/) meddelandemäklare (messsage broker) för att undvika skicka data ut till tjänster man inte har kontroll över. Med det blir cirkeln sluten och inga potentiellt känsliga sensordata kommer i orätta händer.
##### [Discord](https://discord.com) alerts
I Grafana kan man skapa automatiska larm utifrån fördefinerade kriterier vilka kan sedan skickas ut på ett antal olika sätt bl.a. som mejl eller till exempel till Discord (detta illustreras nedan).
![](https://i.imgur.com/fjzkdHH.png)
1. Man behöver registrera sig på Discord först (gratis konto)
2. Skapa en egen server med kommandot Add a Server (det gröna plustecknet i vänstra spalten på bilden ovan).
3. Därefter välj edit-channel (kugghjul till höger om kanalens hashtag)
4. Klicka på webhooks
![](https://i.imgur.com/uuW99ai.png)
5. Välj "Create Webhook" och ge det ett namn samt kopiera url som skall användas i Grafana för att skcika alerter
6. I Grafana gå till Alerting (ringklocka i i den vänstra spalten)
![](https://i.imgur.com/J4PYWvw.png)
7. Välj fliken "Notification channels" och välj "New Channel"
![](https://i.imgur.com/pqzABmE.png)
8. Ange namnet, välj Type "Discord" och lägg i webhook länk skapad i Discord
9. Gå till Dashboard och välj "Edit" för panel som skall generera alert samt gå till fliken "Alert" och ange önskade värden/konfiguration
![](https://i.imgur.com/ZdMbogw.png)
10. Klicka på "Test rule" och kolla på Discord om det har fungerat. Till slut klicka på "Apply"/"Save" i den övre högra hörnan av panelen.


### Verktyg
#### [MQTT Explorer](http://mqtt-explorer.com/)
När man arbetar med mqtt-protokoll finns ett utmärkt verktyg (mqtt-klient) som stöd. Absolut ett måste för varje person som arbetar med mqtt-protokollet.
Bilden nedan illusterar hur jag använt det verktyget för att titta på mina sensordata jag skickat till sjolab.lnu.se
![](https://i.imgur.com/zqSxU5Z.png)

Ja, det var väl det jag hunit testa under kursens gång.
Dena guide kommer avslutas med några mer eller mindre kloka ord :smiley: 

## Avslutande analys
Jag börjar med RaspberryPi (RPi).
På bilden nedan demonstreras resursanvändningen då man kör en TIG-stack. Det är uppenbart att RPi knappast märker att det körs något. Visserligen var det ingen stor datamängd men den plattformen skulle klara av mycket, mycket mer.
Visning av kommandot htop:
![](https://i.imgur.com/KpATVao.png)

Så på frågan om man skall använda RPi är svaret: absolut!
Jag har inte testat Mosquitto och enligt olika källor skall det gå bra att köra även den på RPi parallellt med TIG-stacken.
Det är något jag ser fram emot att testa.

LoRaWAN har visat sig vara en besvikelse. Trots en hel del försök att få till signalen både inomhus och utomhus, på två olika stället som ligger 14km från varandra samt på olika våningar i centrala Stockholm har enbart lite metadata lyckats komma fram till TTN:
```json=
{
  "time": "2020-07-06T13:15:47.373431753Z",
  "frequency": 868.1,
  "modulation": "LORA",
  "data_rate": "SF7BW125",
  "coding_rate": "4/5",
  "gateways": [
    {
      "gtw_id": "eui-34fa40fffe14b497",
      "timestamp": 1527106795,
      "time": "2020-07-06T13:15:47.296694Z",
      "channel": 1,
      "rssi": -121,
      "snr": -8
    }
  ]
}
```
* RSSI = Received Signal Strength Indication
* SNA = Signal to Noise ration
Enligt specifikationen måste RSSI>-120dB och uppmätt styrka är -121 vilket är under specifikationen för att kunna avkoda signalen.
Ingen på kursen har lyckats få till lora via publika gateways vad jag hört.
Åtminstone vet jag nu att min utrustning är hel och att jag troligtivs inte har gjort något fel. Någon tröst trots allt.

Generell information om TTN's begränsningar hittas här: [Limitations: Data rate, packet size, 30 seconds uplink and 10 messages downlink per-day fair-access-policy guidelines/](https://www.thethingsnetwork.org/forum/t/limitations-data-rate-packet-size-30-seconds-uplink-and-10-messages-downlink-per-day-fair-access-policy-guidelines/1300)

### Nykomlingar
Förutom de nämnda kommunikationsprotokoll har det dykt upp 2 uppstickare:
* Symphony Link
    * Den är buggd ovanför lora-teknologi
    * Enligt uppgifterna är formad så att överkomma begränsningar med LoRa fast det är för lite data för att kunna dra några slutsatser
* 6LoWPAN = IPv6 over low power Wireless Personal Area Networks
    * tillhandahåller end-to-end IPv6
    * det är IEEE 802.15.4 standard baserad på 2.4 GHz low power trådlös kommunikation
    * för nuvarande utvecklas och implementeras för arbete med många andra trådlösa signalbärare inklusive Bluetooth Smart; power line control, PLC och låg-effekt Wi-Fi
Dessa protokoll har inte fått någon bred spridning än.