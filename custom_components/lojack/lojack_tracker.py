import lojack-clients

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity import Entity

def setup_platform(hass, config, add_entities, discovery_info=None):
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]

    lojack_tracker = LoJackTracker(hass, username, password)
    lojack_tracker.update()
    add_entities(lojack_tracker.device_list)

    async_track_time_interval(hass, lojack_tracker.update, minutes=15)

class LoJackTracker:
    def __init__(self, hass, username, password):
        self.hass = hass
        self.username = username
        self.password = password

        self.device_list = []
        self.update()

    def update(self):
        identity_client = lojack-clients.IdentityClient.from_login(self.username, self.password)
        token_response = lojack-clients.get_identity_token.sync(client=identity_client)

        services_client = lojack-clients.ServicesClient.from_token(token_response.token)
        assets_response: lojack-clients.GetAllUserAssetsResponse200 = lojack-clients.get_all_user_assets.sync(client=services_client)

        self.device_list = []
        for asset in assets_response.assets:
            device = LoJackDevice(asset)
            self.device_list.append(device)

class LoJackDevice(Entity):
    def __init__(self, asset):
        self.asset = asset

    @property
    def name(self):
        return self.asset.name

    @property
    def device_state_attributes(self):
        return self.asset.attributes