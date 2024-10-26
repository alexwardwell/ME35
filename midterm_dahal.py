from machine import Pin, SoftI2C, PWM, ADC
import ssd1306
import adxl345
from mqtt import MQTTClient
import network
import time
import servo

servo1 = servo.Servo(Pin(2))

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Tufts_Robot", "")

while wlan.ifconfig()[0] == '0.0.0.0':
    print('.', end=' ')
    time.sleep(1)

# We should have a valid IP now via DHCP
# print(wlan.ifconfig())

mqtt_broker = 'broker.hivemq.com' 
# mqtt_broker = 'broker.emqx.io'
port = 1883
topic_sub = 'ME35-24/alex2'       # this reads anything sent to ME35
topic_pub = 'ME35-24/alex1'

message = "Start"

def callback(topic, msg):
    global message
    message = msg.decode()
    print((topic.decode(), msg.decode()))

client = MQTTClient('repl1', mqtt_broker , port, keepalive=60)
client.connect()
print('Connected to %s MQTT broker' % (mqtt_broker))
client.set_callback(callback)          # set the callback if anything is read
client.subscribe(topic_sub.encode())   # subscribe to a bunch of topics

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))

pot = ADC(Pin(3))
pot.atten(ADC.ATTN_11DB) # the pin expects a voltage range up to 3.3V


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


def check_first_character(s):
    if s and s[0].lower() in 'abcdefgr':
        return True
    return False


while True:
    
    client.check_msg()
    
    if check_first_character(message):
        screen = ssd1306.SSD1306_I2C(128,64,i2c)
        screen.text(message, 0, 0, 1) # to display text
        screen.show()
    else:
        int_message = string_to_int(message)
        servo1.write_angle(int_message)

    # print(pot.read())
    pot_val = pot.read()
    pot_val = str(pot_val)
    client.publish(topic_pub.encode(), pot_val.encode())

    time.sleep(0.2)
