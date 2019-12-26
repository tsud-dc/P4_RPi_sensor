#!/usr/bin/python3

import ADC0832
import time
import datetime
import paho.mqtt.client as mqtt
from rgb_led import *
import os
import ds18b20
import sys
import setenv

th_temp_l = int(os.environ.get('th_temp_l'))
th_temp_h = int(os.environ.get('th_temp_h'))
th_photo = int(os.environ.get('th_photo'))
temp_topic = os.environ.get('temp_topic')
light_topic = os.environ.get('light_topic')
broker_address = os.environ.get('broker_address')

print(temp_topic, light_topic)

col_list = ['r', 'g', 'b']

def init():
    ADC0832.setup()

def photo():
    res = ADC0832.getResult() - 80
    if res < 0:
        res = 0
    if res > 100:
        res = 100
    return res

def select_col(temp, photo):
    col_list = [0, 0, 0]
    if temp < th_temp_l or temp > th_temp_h:
        col_list[0] = 1
    if photo < th_photo:
        col_list[2] = 1
    if col_list[0] == 1 and col_list[2] == 1:
        col_list = [0, 1, 0]
    if col_list[0] == 1:
        col = 'r'
    elif col_list[1] == 1:
        col = 'g'
    elif col_list[2] == 1:
        col = 'b'
    else:
        col = 'n'

    return col

def send_mq(topic, date, res):
    print("creating new instance")
    client = mqtt.Client() #create new instance
    client.connect(broker_address) #connect to broker

    msg = "date,{},value,{}".format(date, res)
    
    print("MQ Publishing message: {} to topic: {}".format(msg, topic))
    client.publish(topic,msg)
    

def loop():
    led_cond = 'n'
    while True:
        ch_time = datetime.datetime.now()
        ch_time_str = ch_time.strftime('%Y/%m/%d %H:%M:%S')
        ch_time_mq = ch_time.strftime('%Y/%m/%d %H:%M')

        res_p = photo()
        # thermo sensor process
        res_t = ds18b20.readSensors()
        print('photo:{}, {}, {}'.format(ch_time_str, res_p, res_t))

        col = select_col(res_t, res_p)
        
        if col in col_list:
            if led_cond in col_list: turn_off(pins, led_cond)
            turn_on(pins, col)
            led_cond = col
        else:
            if led_cond in col_list:
                turn_off(pins, led_cond)

        #mq process
        #print(ch_time_str[-5:])
        if ch_time_str[-5:] in ['00:00', '15:00', '30:00', '45:00']:
            for i in zip([temp_topic, light_topic], [res_t, res_p]):
                send_mq(i[0], ch_time_mq, i[1])

        time.sleep(0.1)

if __name__ == '__main__':
    init()
    rgb_init(pins)
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('Cleanup ADC!')
        gpio_cleanup()
        ds18b20.destroy()
