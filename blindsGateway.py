#  Copyright (c) 2021. Ivan Zinin

import requests

# For now assign a static table of addresses for blinds:
blinds_table = {0: '192.168.0.158',
                1: '192.168.0.164'}

# Commands:
GO_UP = 'goUp'
GO_DOWN = 'goDown'
STOP = 'stop'
SET_MOTOR_PERIOD = 'setMotorPeriod'
SET_MOTOR_MODE = 'setMotorMode'


def setup():
    send_message(0, SET_MOTOR_MODE, 1)
    send_message(1, SET_MOTOR_MODE, 1)
    send_message(0, SET_MOTOR_PERIOD, 1)
    send_message(1, SET_MOTOR_PERIOD, 1)


def setup_quiet():
    send_message(0, SET_MOTOR_MODE, 2)
    send_message(1, SET_MOTOR_MODE, 2)
    send_message(0, SET_MOTOR_PERIOD, 1)
    send_message(1, SET_MOTOR_PERIOD, 1)


def send_message(blind_num, command, value):
    address = blinds_table.get(blind_num)
    url = f'http://{address}/postformCommand/'
    data = {'command': command, 'value': value}
    response = requests.post(url, data=data)
    print(response.text)
