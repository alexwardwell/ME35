import time
from mqtt import MQTTClient
import network
from machine import Pin, PWM, UART
from BLE_CEEO import Yell, Listen
import asyncio
motorpin1 = PWM(Pin(26, Pin.OUT))
motorpin2 = PWM(Pin(27, Pin.OUT))
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
message = ""
stop_global = False
async def peripheral(name):
    try:
        p = Yell(name, verbose = True)
        if p.connect_up():
            print('P connected')
            await asyncio.sleep(2)
        # get the command from the teachable machine
        await tm_communication(p)
    except Exception as e:
        print(e)
    finally:
        p.disconnect()
        print('closing up')
    await asyncio.sleep(0.1)
async def tm_communication(p):
    while True:
        if p.is_any:
            message = p.read()
            predictions = message.split(',')
            classes = []
            values = []
            for i in range (0,len(predictions)):
                class_name = predictions[i].split(': ')[0]
                value = predictions[i].split(': ')[1]
                classes.append(class_name)
                values.append(float(value))
            max_index = values.index(max(values))
            predicted_class = classes[max_index]
            print(predicted_class)
            if predicted_class == "c 1":
                steer_both('forward')
            else:
                steer_both('stop')
        if not p.is_connected:
            print('lost connection')
            break
        await asyncio.sleep(1)
def wifi_connect():
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect("Tufts_Robot", "")
        while wlan.ifconfig()[0] == '0.0.0.0':
                print('.', end=' ')
                time.sleep(1)
        # We should have a valid IP now via DHCP
        print(wlan.ifconfig())
def callback(topic, msg):
        print((topic.decode(), msg.decode()))
        global message
        message = msg.decode()
# steering functions
def right():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(65535)
    motorpin2.duty_u16(0)
def left():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(0)
    motorpin2.duty_u16(0)
def fwd():
    motorpin1.freq(65535)
    motorpin2.freq(65535)
    motorpin1.duty_u16(65535)
    motorpin2.duty_u16(0)
def back():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(0)
    motorpin2.duty_u16(65535)
def stop():
    motorpin1.freq(1000)
    motorpin2.freq(1000)
    motorpin1.duty_u16(0)
    motorpin2.duty_u16(0)
def string_to_int(decimal_str):
    # Remove any leading or trailing whitespace
    decimal_str = decimal_str.strip()
    # Check if the string is empty
    if not decimal_str:
        raise ValueError("Input string is empty.")
    # Handle negative numbers
    is_negative = decimal_str[0] == '-'
    if is_negative or decimal_str[0] == '+':
        decimal_str = decimal_str[1:]
    # Split the string on the decimal point
    if '.' in decimal_str:
        whole_part, _, _ = decimal_str.partition('.')
    else:
        whole_part = decimal_str
    # Validate whole part
    if not whole_part.isdigit():
        raise ValueError(f"Invalid input: '{decimal_str}' is not a valid decimal number.")
    # Convert whole part to integer manually
    integer_value = 0
    for char in whole_part:
        integer_value = integer_value * 10 + (ord(char) - ord('0'))
    return -integer_value if is_negative else integer_value
# Function to send steering command to Secondary Pico via UART
def send_steering_command(command):
    uart.write(command + "\n")
    print(f"Sent command to Secondary Pico: {command}")
# Function to steer both the Main and Secondary Pico
def steer_both(command):
    # Control the Main Pico motors
    if command == "forward":
        fwd()
        stop_global = False
    elif command == "back":
        back()
    elif command == "left":
        left()
    elif command == "right":
        right()
    elif command == "stop":
        stop()
        stop_global = True
    # Send the same command to the Secondary Pico
    send_steering_command(command)
async def apr_tag_control(client):
    print('in apr tag control')
    while True:
        client.check_msg()
        global message
        if stop_global == False:
            if message:
            #     # Print the original message for debugging
            #     # print(f"Original message: '{message}'")
            #     # # Slice the message to remove the first and last characters
            #     # modified_message = message[1:-1]
            #     # print(f"Modified message: '{modified_message}'")  # Debugging the modified message
                try:
                #         # Convert the modified message to an integer
                    intmsg = string_to_int(message)
                    print(f"Converted integer: {intmsg}")  # Debugging the converted integer
                #         # Now perform your comparisons with the integer
                    if intmsg >= 330 or intmsg <= 30:
                        print("Moving forward")
                        steer_both('forward')
                    elif intmsg >= 70 and intmsg <= 110:
                        print("Turning left")
                        steer_both('left')
                    elif intmsg >= 160 and intmsg <= 200:
                        print("Moving backward")
                        steer_both('back')
                    elif intmsg >= 250 and intmsg <= 290:
                        print("Turning right")
                        steer_both('right')
                except ValueError:
                    print(f"Invalid message format; cannot convert '{message}' to integer.")
                #     # message = ""  # Clear message after processing
            else:
                print(".")
            await asyncio.sleep(0.5)
        else:
            steer_both('stop')
            await asyncio.sleep(0.5)
wifi_connect()
mqtt_broker = 'broker.hivemq.com'
port = 1883
topic_sub = 'ME35-24/ari'
topic_pub = 'ME35-24/ari'
client = MQTTClient('Alex', mqtt_broker , port, keepalive=60)
client.connect()
print('Connected to %s MQTT broker' % (mqtt_broker))
client.set_callback(callback)          # set the callback if anything is read
client.subscribe(topic_sub.encode())   # subscribe to a bunch of topics
async def main(client):
    await asyncio.gather(
        peripheral("Ari"),
        apr_tag_control(client)
    )
asyncio.run(main(client))
