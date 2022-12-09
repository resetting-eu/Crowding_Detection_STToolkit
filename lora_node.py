#!/usr/bin/env python3
from rak811.rak811 import Mode, Rak811

lora = Rak811()
lora.hard_reset()
lora.mode = Mode.LoRaWan
lora.band = 'EU868'
lora.set_config(dev_eui='3939353466385117',
app_eui='190E110342012981',
app_key='CBDF9117D3E1A7F9AA11166ED97BF8F6')
lora.join_otaa()
lora.dr = 5
lora.send('Hello world')
lora.close()