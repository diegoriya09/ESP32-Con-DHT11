from machine import Pin
import time
import dht
try:
  import urequests as requests
except:
  import requests
import network
import umail

ssid = 'D-I-E-G-O'
password = 'juan12345'

#Your phone number in international format
phone_number = '+573122469899'
#Your callmebot API key
api_key = '1681817'

HTTP_HEADERS = {'Content-Type': 'application/json'} 
THINGSPEAK_WRITE_API_KEY = '7OCGN4WFC6PZYCBN'
UPDATE_TIME_INTERVAL = 5000  # in ms 
last_update = time.ticks_ms() 

sensor = dht.DHT11(Pin(5))

sensor.measure()
t = sensor.temperature()
h = sensor.humidity()
print('Temperatura: %3.1f C' %t)
print('Humedad: %3.1f %%' %h)
    
def connect_wifi(ssid, password):
  #Connect to your network
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Conectado Correctamente')
  print(station.ifconfig())
  
connect_wifi(ssid, password)

def is_ascii(s):
    return (ord(s) > 33) and ( ord(s) < 128) 

def urlencode(mensaje):
  #data = urlencoded_text.encode()
  encoded_mensaje = ""
  for char in mensaje:
      if (is_ascii(char)) or char in "-_.~":
          encoded_mensaje += char
          #print("if")
      else:
          encoded_mensaje += "%{:02x}".format(ord(char))
          #print("else")
  print(encoded_mensaje)
  return encoded_mensaje
  
def enviar_mensaje_whatsapp(phone_number, api_key, mensaje):
  #set your host URL
  url = 'https://api.callmebot.com/whatsapp.php?phone='+phone_number+'&text='+str(urlencode(mensaje))+'&apikey='+api_key

  #make the request
  response = requests.get(url)
  #check if it was successful
  if response.status_code == 200:
    print('Todo salio bien!')
  else:
    print('Error')
    print(response.text)

def enviar_mensaje_correo(sender_email, sender_name, sender_app_password, recipient_email, email_subject, mensaje):
    # Send the email
    # Connect to the Gmail's SSL port
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    # Login to the email account using the app password
    smtp.login(sender_email, sender_app_password)
    # Specify the recipient email address
    smtp.to(recipient_email)
    # Write the email header
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    # Write the body of the email
    smtp.write(mensaje)
    # Send the email
    smtp.send()
    # Quit the email session
    smtp.quit()
    print('Email enviado')
    
if(t<17 and h<40):
    mensaje = 'Preparate para el frio, y para un ambiente muy seco, cuidate de la aparicion de bacterias y virus'
    enviar_mensaje_whatsapp(phone_number, api_key, mensaje)
    print('Todo salio perfecto')
else:
    if(t>=17 and h>=40 and h<=60):
        sender_email = 'esp32correoarquitectura@gmail.com' # Replace with the email address of the sender
        sender_name = 'ALERTA' # Replace with the name of the sender
        sender_app_password = 'obokjhabkhgywjxe' # Replace with the app password of the sender's email account
        recipient_email ='juan_rivera82211@elpoli.edu.co' # Replace with the email address of the recipient
        email_subject ='Advertencia' # Subject of the email
        mensaje = "Ten cuidado. Se aproxima una fuerte temperatura, pero seguimos en un buen porcentaje de humedad."
        enviar_mensaje_correo(sender_email, sender_name, sender_app_password, recipient_email, email_subject, mensaje)
        enviar_mensaje_whatsapp(phone_number, api_key, mensaje)
    else:
        if(t>=23 and h>60):
            sender_email = 'esp32correoarquitectura@gmail.com' # Replace with the email address of the sender
            sender_name = 'ALERTA' # Replace with the name of the sender
            sender_app_password = 'obokjhabkhgywjxe' # Replace with the app password of the sender's email account
            recipient_email ='juan_rivera82211@elpoli.edu.co' # Replace with the email address of the recipient
            email_subject ='Advertencia, ' # Subject of the email
            mensaje = "Mucho cuidado. Estas en pasando por temperatura demasiado alta y por una humedad demasiado alta."
            enviar_mensaje_correo(sender_email, sender_name, sender_app_password, recipient_email, email_subject, mensaje)
            enviar_mensaje_whatsapp(phone_number, api_key, mensaje)

if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
    dth11_readings = {'field1':t, 'field2':h} 
    request = requests.post( 'http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json = dth11_readings, headers = HTTP_HEADERS )  
    request.close() 
    print(dth11_readings) 
# while True:
#     try:
#         sleep(2)
#         sensor.measure()
#         t = sensor.temperature()
#         h = sensor.humidity()
#         print('Temperatura: %3.1f C' %t)
#         print('Humedad: %3.1f %%' %h)
#     except OSError as e:
#         print('No se esta leyendo el sensor')
