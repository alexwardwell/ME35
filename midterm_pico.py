# TM LINK: https://teachablemachine.withgoogle.com/models/oBmEtTy7r/


import time
from mqtt import MQTTClient
import asyncio
from machine import Pin, PWM
from BLE_CEEO import Yell
from hcsr04 import HCSR04
import network

# Define frequencies for notes (in Hz)
notes = {
    'B0': 23,
    'C1': 24,
    'CS1': 25,
    'D1': 26,
    'DS1': 27,
    'E1': 28,
    'F1': 29,
    'FS1': 30,
    'G1': 31,
    'GS1': 32,
    'A1': 33,
    'AS1': 34,
    'B1': 35,
    'C2': 36,
    'CS2': 37,
    'D2': 38,
    'DS2': 39,
    'E2': 40,
    'F2': 41,
    'FS2': 42,
    'G2': 43,
    'GS2': 44,
    'A2': 45,
    'AS2': 46,
    'B2': 47,
    'C3': 48,
    'CS3': 49,
    'D3': 50,
    'DS3': 51,
    'E3': 52,
    'F3': 53,
    'FS3': 54,
    'G3': 55,
    'GS3': 56,
    'A3': 57,
    'AS3': 58,
    'B3': 59,
    'C4': 60,
    'CS4': 61,
    'D4': 62,
    'DS4': 63,
    'E4': 64,
    'F4': 65,
    'FS4': 66,
    'G4': 67,
    'GS4': 68,
    'A4': 69,
    'AS4': 70,
    'B4': 71,
    'C5': 72,
    'CS5': 73,
    'D5': 74,
    'DS5': 75,
    'E5': 76,
    'F5': 77,
    'FS5': 78,
    'G5': 79,
    'GS5': 80,
    'A5': 81,
    'AS5': 82,
    'B5': 83,
    'C6': 84,
    'CS6': 85,
    'D6': 86,
    'DS6': 87,
    'E6': 88,
    'F6': 89,
    'FS6': 90,
    'G6': 91,
    'GS6': 92,
    'A6': 93,
    'AS6': 94,
    'B6': 95,
    'C7': 96,
    'CS7': 97,
    'D7': 98,
    'DS7': 99,
    'E7': 100,
    'F7': 101,
    'FS7': 102,
    'G7': 103,
    'GS7': 104,
    'A7': 105,
    'AS7': 106,
    'B7': 107,
    'C8': 108,
    'CS8': 109,
    'D8': 110,
    'DS8': 111,
    'REST': 0
}

# Tempo
tempo = 114

# Melody and duration
rick = [
    'D5', -4, 'E5', -4, 'A4', 4,
    'E5', -4, 'FS5', -4, 'A5', 16, 'G5', 16, 'FS5', 8,
    'D5', -4, 'E5', -4, 'A4', 2,
    'A4', 16, 'A4', 16, 'B4', 16, 'D5', 8, 'D5', 16,
    'D5', -4, 'E5', -4, 'A4', 4,
    'E5', -4, 'FS5', -4, 'A5', 16, 'G5', 16, 'FS5', 8,
    'D5', -4, 'E5', -4, 'A4', 2,
    'A4', 16, 'A4', 16, 'B4', 16, 'D5', 8, 'D5', 16,
    'REST', 4, 'B4', 8, 'CS5', 8, 'D5', 8, 'D5', 8, 'E5', 8, 'CS5', -8,
    'B4', 16, 'A4', 2, 'REST', 4,
    'REST', 8, 'B4', 8, 'B4', 8, 'CS5', 8, 'D5', 8, 'B4', 4, 'A4', 8,
    'A5', 8, 'REST', 8, 'A5', 8, 'E5', -4, 'REST', 4,
    'B4', 8, 'B4', 8, 'CS5', 8, 'D5', 8, 'B4', 8, 'D5', 8, 'E5', 8, 'REST', 8,
    'REST', 8, 'CS5', 8, 'B4', 8, 'A4', -4, 'REST', 4,
    'REST', 8, 'B4', 8, 'B4', 8, 'CS5', 8, 'D5', 8, 'B4', 8, 'A4', 4,
    'REST', 8, 'A5', 8, 'A5', 8, 'E5', 8, 'FS5', 8, 'E5', 8, 'D5', 8,
    'REST', 8, 'A4', 8, 'B4', 8, 'CS5', 8, 'D5', 8, 'B4', 8,
    'REST', 8, 'CS5', 8, 'B4', 8, 'A4', -4, 'REST', 4,
    'B4', 8, 'B4', 8, 'CS5', 8, 'D5', 8, 'B4', 8, 'A4', 4, 'REST', 8,
    'REST', 8, 'E5', 8, 'E5', 8, 'FS5', 4, 'E5', -4,
    'D5', 2, 'D5', 8, 'E5', 8, 'FS5', 8, 'E5', 4,
    'E5', 8, 'E5', 8, 'FS5', 8, 'E5', 8, 'A4', 8, 'A4', 4,
    'REST', -4, 'A4', 8, 'B4', 8, 'CS5', 8, 'D5', 8, 'B4', 8,
    'REST', 8, 'E5', 8, 'FS5', 8, 'E5', -4, 'A4', 16, 'B4', 16, 'D5', 16, 'B4', 16,
    'FS5', -8, 'FS5', -8, 'E5', -4, 'A4', 16, 'B4', 16, 'D5', 16, 'B4', 16,
    'E5', -8, 'E5', -8, 'D5', -8, 'CS5', 16, 'B4', -8, 'A4', 16, 'B4', 16, 'D5', 16, 'B4', 16,
    'D5', 4, 'E5', 8, 'CS5', -8, 'B4', 16, 'A4', 4, 'A4', 8,
    'E5', 4, 'D5', 2, 'A4', 16, 'B4', 16, 'D5', 16, 'B4', 16,
    'FS5', -8, 'FS5', -8, 'E5', -4, 'A4', 16, 'B4', 16, 'D5', 16, 'B4', 16,
    'A5', 4, 'CS5', 8, 'D5', -8, 'CS5', 16, 'B4', 8, 'A4', 16, 'B4', 16, 'D5', 16, 'B4', 16,
    'D5', 4, 'E5', 8, 'CS5', -8, 'B4', 16, 'A4', 4, 'A4', 8,
    'E5', 4, 'D5', 2, 'REST', 4
]


mii = [
  
#   // Mii Channel theme 
#   // Score available at https://musescore.com/user/16403456/scores/4984153
#   // Uploaded by Catalina Andrade 
  
  'FS4',8, 'REST',8, 'A4',8, 'CS5',8, 'REST',8,'A4',8, 'REST',8, 'FS4',8, #//1
  'D4',8, 'D4',8, 'D4',8, 'REST',8, 'REST',4, 'REST',8, 'CS4',8,
  'D4',8, 'FS4',8, 'A4',8, 'CS5',8, 'REST',8, 'A4',8, 'REST',8, 'F4',8,
  'E5',-4, 'DS5',8, 'D5',8, 'REST',8, 'REST',4,
  
  'GS4',8, 'REST',8, 'CS5',8, 'FS4',8, 'REST',8,'CS5',8, 'REST',8, 'GS4',8, #//5
  'REST',8, 'CS5',8, 'G4',8, 'FS4',8, 'REST',8, 'E4',8, 'REST',8,
  'E4',8, 'E4',8, 'E4',8, 'REST',8, 'REST',4, 'E4',8, 'E4',8,
  'E4',8, 'REST',8, 'REST',4, 'DS4',8, 'D4',8, 

  'CS4',8, 'REST',8, 'A4',8, 'CS5',8, 'REST',8,'A4',8, 'REST',8, 'FS4',8, #//9
  'D4',8, 'D4',8, 'D4',8, 'REST',8, 'E5',8, 'E5',8, 'E5',8, 'REST',8,
  'REST',8, 'FS4',8, 'A4',8, 'CS5',8, 'REST',8, 'A4',8, 'REST',8, 'F4',8,
  'E5',2, 'D5',8, 'REST',8, 'REST',4,

  'B4',8, 'G4',8, 'D4',8, 'CS4',4, 'B4',8, 'G4',8, 'CS4',8, #//13
  'A4',8, 'FS4',8, 'C4',8, 'B3',4, 'F4',8, 'D4',8, 'B3',8,
  'E4',8, 'E4',8, 'E4',8, 'REST',4, 'REST',4, 'AS4',4,
  'CS5',8, 'D5',8, 'FS5',8, 'A5',8, 'REST',8, 'REST',4, 

  'REST',2, 'A3',4, 'AS3',4, #//17 
  'A3',-4, 'A3',8, 'A3',2,
  'REST',4, 'A3',8, 'AS3',8, 'A3',8, 'F4',4, 'C4',8,
  'A3',-4, 'A3',8, 'A3',2,

  'REST',2, 'B3',4, 'C4',4, #//21
  'CS4',-4, 'C4',8, 'CS4',2,
  'REST',4, 'CS4',8, 'C4',8, 'CS4',8, 'GS4',4, 'DS4',8,
  'CS4',-4, 'DS4',8, 'B3',1,
  
  'E4',4, 'E4',4, 'E4',4, 'REST',8,#//25

#   //repeats 1-25

  'FS4',8, 'REST',8, 'A4',8, 'CS5',8, 'REST',8,'A4',8, 'REST',8, 'FS4',8, #//1
  'D4',8, 'D4',8, 'D4',8, 'REST',8, 'REST',4, 'REST',8, 'CS4',8,
  'D4',8, 'FS4',8, 'A4',8, 'CS5',8, 'REST',8, 'A4',8, 'REST',8, 'F4',8,
  'E5',-4, 'DS5',8, 'D5',8, 'REST',8, 'REST',4,
  
  'GS4',8, 'REST',8, 'CS5',8, 'FS4',8, 'REST',8,'CS5',8, 'REST',8, 'GS4',8, #//5
  'REST',8, 'CS5',8, 'G4',8, 'FS4',8, 'REST',8, 'E4',8, 'REST',8,
  'E4',8, 'E4',8, 'E4',8, 'REST',8, 'REST',4, 'E4',8, 'E4',8,
  'E4',8, 'REST',8, 'REST',4, 'DS4',8, 'D4',8, 

  'CS4',8, 'REST',8, 'A4',8, 'CS5',8, 'REST',8,'A4',8, 'REST',8, 'FS4',8, #//9
  'D4',8, 'D4',8, 'D4',8, 'REST',8, 'E5',8, 'E5',8, 'E5',8, 'REST',8,
  'REST',8, 'FS4',8, 'A4',8, 'CS5',8, 'REST',8, 'A4',8, 'REST',8, 'F4',8,
  'E5',2, 'D5',8, 'REST',8, 'REST',4,

  'B4',8, 'G4',8, 'D4',8, 'CS4',4, 'B4',8, 'G4',8, 'CS4',8,# //13
  'A4',8, 'FS4',8, 'C4',8, 'B3',4, 'F4',8, 'D4',8, 'B3',8,
  'E4',8, 'E4',8, 'E4',8, 'REST',4, 'REST',4, 'AS4',4,
  'CS5',8, 'D5',8, 'FS5',8, 'A5',8, 'REST',8, 'REST',4, 

  'REST',2, 'A3',4, 'AS3',4, #//17 
  'A3',-4, 'A3',8, 'A3',2,
  'REST',4, 'A3',8, 'AS3',8, 'A3',8, 'F4',4, 'C4',8,
  'A3',-4, 'A3',8, 'A3',2,

  'REST',2, 'B3',4, 'C4',4, #//21
  'CS4',-4, 'C4',8, 'CS4',2,
  'REST',4, 'CS4',8, 'C4',8, 'CS4',8, 'GS4',4, 'DS4',8,
  'CS4',-4, 'DS4',8, 'B3',1,
  
  'E4',4, 'E4',4, 'E4',4, 'REST',8, #//25

#   //finishes with 26
#   //'FS4',8, 'REST',8, 'A4',8, 'CS5',8, 'REST',8, 'A4',8, 'REST',8, 'FS4',8
   
]



NoteOn = 0x90
NoteOff = 0x80
StopNotes = 123
SetInstroment = 0xC1
Reset = 0xFF

velocity = {'off':0, 'pppp':8,'ppp':20,'pp':31,'p':42,'mp':53,
    'mf':64,'f':80,'ff':96,'fff':112,'ffff':127}

mqtt_broker = 'broker.hivemq.com' 
# mqtt_broker = 'broker.emqx.io'
port = 1883
topic_sub = 'ME35-24/alex1'       # this reads anything sent to ME35
topic_pub = 'ME35-24/alex2'

off_switch = True
pause_switch = False

channel = 0
cmd = NoteOn

channel = 0x0F & channel
timestamp_ms = time.ticks_ms()
tsM = (timestamp_ms >> 7 & 0b111111) | 0x80
tsL =  0x80 | (timestamp_ms & 0b1111111)

c =  cmd | channel
divider = 0
coff = NoteOff | channel

light = Pin(5, Pin.IN)
sensor = HCSR04(trigger_pin=7, echo_pin=6,echo_timeout_us=1000000)
m_pin1 = PWM(Pin(26, Pin.IN))
m_pin2 = PWM(Pin(27, Pin.IN))
m_pin1.freq(1000)
m_pin2.freq(1000)

volume = 80
speed = 114

melody = rick


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Tufts_Robot", "")

while wlan.ifconfig()[0] == '0.0.0.0':
    print('.', end=' ')
    time.sleep(1)


def callback(topic, msg):
    print((topic.decode(), msg.decode()))
    global off_switch, volume, melody
    if msg.decode() == "on":
        off_switch = False
    elif msg.decode() == "off":
        off_switch = True
    # elif msg.decode() == "test":
    #     melody = rick  # Test switching to rick
    elif check_first_character(msg.decode()):
        get_predictions(msg.decode())
        if get_predictions(msg.decode()) == "c2":
            melody = rick
            # print("Switched to rick melody")
        elif get_predictions(msg.decode()) == "c1":
            melody = mii
            # print("Switched to mii melody")
    elif string_to_int(msg.decode()) >= 1 or string_to_int(msg.decode()) <= 4095:
            volume = msg.decode()
            volume = string_to_int(volume) * (127 / 4095)
            # print(volume)


def check_first_character(s):
    if s and s[0].lower() in 'c':
        return True
    return False


def light_sensor(pin):
    global pause_switch
    # print(light.value())
    if light.value() == 0:
        pause_switch = False
    else:
        pause_switch = True
    # print(pause_switch)

async def connect_MIDI():
    global p
    p = Yell('Alex', verbose = True, type = 'midi')
    p.connect_up()

def get_dist():
    distance = sensor.distance_cm()
    speed = 114 * (distance / 30)  # Avoid division by zero
    if speed <= 25:
        speed = 25
    elif distance >= 90:
        speed = 114
    return speed


def play_GB(client):
    global c, coff, melody, pause_switch, volume, speed
    for i in range(0, len(melody), 2):
        speed = get_dist()
        # print(distance)

        wholenote = (60000 * 4) // speed
        note = melody[i]
        divider = melody[i + 1]

        if divider > 0:
            note_duration = wholenote // divider
        else:
            note_duration = (wholenote // abs(divider)) * 1.5  # Dotted note

        if note != 'REST':
            payload = bytes([tsM, tsL, c, notes[note], int(volume)])  # Set to half duty cycle (50%)
        else:
            payload = bytes([tsM, tsL, coff, notes[note], int(volume)])

        p.send(payload)
        client.publish(topic_pub.encode(), note.encode())

        time.sleep(((note_duration * 0.9) / 1000) / 2)

        servo_angle = str(int(volume * (180 / 127)))
        client.publish(topic_pub.encode(), servo_angle.encode())

        time.sleep(((note_duration * 0.9) / 1000) / 2)

        payload = bytes([tsM, tsL, coff, notes[note], velocity['f']])
        p.send(payload)

        while pause_switch:  # Check for pause
            client.check_msg()
            time.sleep(0.01)  # Slight pause to prevent busy-waiting

        client.check_msg()
        if off_switch:
            break

        motors(speed)

        
def motors(speed):
    motor_speed = int(speed * 1000)
    if motor_speed >= 65535:
        motor_speed = 65535
    m_pin1.duty_u16(motor_speed)
    m_pin2.duty_u16(0)


def get_predictions(message):
    # Remove brackets and split the string into individual predictions
    message = message.strip("[]'")  # Remove surrounding brackets and quotes
    predictions = message.split(', ')  # Split by comma and space
    
    classes = []
    values = []
    
    for prediction in predictions:
        class_name, value_str = prediction.split(': ')
        value_str = value_str.strip("'")
        class_name = class_name.strip("'")
        classes.append(class_name)
        values.append(float(value_str))  # Convert to float
    
    max_index = values.index(max(values))
    predicted_class = classes[max_index]
    # print(predicted_class)
    # print(f"Predicted class: {predicted_class}, Values: {values}")
    return predicted_class


def string_to_int(s):
    # Handle negative numbers
    is_negative = False
    if s[0] == '-':
        is_negative = True
        s = s[1:]  # Remove the negative sign for processing

    # Initialize result
    result = 0

    # Iterate over each character in the string
    for char in s:
        if '0' <= char <= '9':  # Check if character is a digit
            digit_value = ord(char) - ord('0')  # Convert char to its integer value
            result = result * 10 + digit_value  # Build the result

    return -result if is_negative else result


client = MQTTClient('ME35_alex', mqtt_broker , port, keepalive=60)
client.connect()
print('Connected to %s MQTT broker' % (mqtt_broker))
client.set_callback(callback)          # set the callback if anything is read
client.subscribe(topic_sub.encode())   # subscribe to a bunch of topics



light.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=light_sensor)


async def main():
    await connect_MIDI()
    while True:
        client.check_msg()
        if off_switch == False:
            if pause_switch == False:
                play_GB(client)
                # get_dist()
        await asyncio.sleep(0.001)

asyncio.run(main())

        
