import mraa, requests, time
from upm import pyupm_th02
from upm import pyupm_grove
from upm import pyupm_jhd1313m1

display = pyupm_jhd1313m1.Jhd1313m1(0,0x3E, 0x62)
photo = pyupm_grove.GroveLight(0)
th02 = pyupm_th02.TH02(6,0x40)
pir = mraa.Gpio(2)
ledtest = mraa.Gpio(13)
buzzer = mraa.Gpio(6)

pir.dir(mraa.DIR_IN)
ledtest.dir(mraa.DIR_OUT)
buzzer.dir(mraa.DIR_OUT)

temperature = 0
humidity = 0
light = 0
event = 0
error = 0

display.setColor(255,255,255)
display.setCursor(0,0)
display.write('Connecting...')
time.sleep(3)

while True:

    temperature = th02.getTemperature()
    humidity = th02.getHumidity()
    light = photo.raw_value()

    if pir.read() == 1:
        event+=1

    print 'Temp:  ' + str(temperature) + ' C'
    print 'Hum:   ' + str(humidity) + ' %'
    print 'Light: ' + str(light) + ' lux'
    print 'Event: ' + str(event) + ' x'
    
    display.setCursor(0,0)
    display.write('Temp: ' + str(temperature))
    display.setCursor(1,0)
    display.write('Humi: ' + str(humidity))

    try:
        r = requests.post('http://172.31.112.199/laboratorio/alta.php', data={'var1':temperature,'var2':humidity,'var3':light,'var4':event},timeout=1 )
        error = 0
    except:
        print ('error conexion')
        error = 1

    if error == 1:
        display.setColor(255,0,0)
        buzzer.write(1)
        time.sleep(.1)
        buzzer.write(0)
    else:
        display.setColor(0,255,0)
        ledtest.write(1)
        time.sleep(.1)
        ledtest.write(0)

    time.sleep(9.9)
    print('Completed')
