from lojack_tracker import LoJackSensor

def setup(hass, config):
    return LoJackSensor(hass, config)