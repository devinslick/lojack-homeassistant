from .lojack_tracker import LoJackDeviceTracker

def setup(hass, config):
    return LoJackDeviceTracker(hass, config)
