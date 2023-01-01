from homeassistant.components.device_tracker import DOMAIN
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.event import track_time_change
import lojack_clients

class LoJackDeviceTracker:
    def __init__(self, hass, config):
        self.hass = hass
        self.username = config[CONF_USERNAME]
        self.password = config[CONF_PASSWORD]
        self.devices = {}

        track_time_change(self.hass, self.update_devices, minute=range(0, 60, 15))

    def update_devices(self, now):
        lojack_api = lojack_clients.Client(self.username, self.password)
        devices = lojack_api.get_devices()

        for device in devices:
            if device['id'] not in self.devices:
                self.devices[device['id']] = device
                self.hass.states.set(f"{DOMAIN}.{device['name']}", device['status'], {
                    'friendly_name': device['name'],
                    'icon': 'mdi:car'
                })
            else:
                self.hass.states.set(f"{DOMAIN}.{device['name']}", device['status'], {
                    'friendly_name': device['name'],
                    'icon': 'mdi:car'
                })
