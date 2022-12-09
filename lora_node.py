#!/usr/bin/env python3
from rak811.rak811 import Mode, Rak811

lora = Rak811()
lora.hard_reset()
lora.mode = Mode.LoRaWan
lora.band = 'EU868'
lora.set_config(dev_eui='xxxxxxxxxxxxxxxx',   #Copy the result of the 'sudo rak811 get-config dev_eui' command
app_eui='xxxxxxxxxxxxxxxx',                   #AppEUI obtained from the TTN/Helium console
app_key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')   #AppKey obtained from the TTN/Helium console
lora.join_otaa()
lora.dr = 5
lora.send('Hello world')
lora.close()
