from lojack_sensor import LoJackSensor

def setup(hass, config):
    return LoJackSensor(hass, config)