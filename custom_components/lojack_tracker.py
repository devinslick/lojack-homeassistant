from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.entity import Entity
from lojack_clients.identity import AuthenticatedClient as IdentityClient
from lojack_clients.identity.api.default import get_identity_token
from lojack_clients.services import AuthenticatedClient as ServicesClient
from lojack_clients.services.api.default import get_all_user_assets
from lojack_clients.services.models import GetAllUserAssetsResponse200
from lojack_clients.services.types import Response as ServicesResponse

class LoJackSensor(Entity):
    def __init__(self, hass, config):
        self.hass = hass
        self.username = config[CONF_USERNAME]
        self.password = config[CONF_PASSWORD]

        self.attributes = {}
        self.update()

    def update(self):
        identity_client = IdentityClient.from_login(self.username, self.password)
        token_response = get_identity_token.sync(client=identity_client)

        services_client = ServicesClient.from_token(token_response.token)
        assets_response: GetAllUserAssetsResponse200 = get_all_user_assets.sync(client=services_client)

        self._state = assets_response.num_assets
        self.attributes = {}
        for asset in assets_response.assets:
            self.attributes[asset.name] = asset.id

        for asset in assets_response.assets:
            if asset['id'] not in self.devices:
                self.asset[assets_response.assets['id']] = asset
                self.hass.states.set(f"{DOMAIN}.{asset['name']}", asset['status'], {
                    'friendly_name': asset['name'],
                    'icon': 'mdi:car'
                })
            else:
                self.hass.states.set(f"{DOMAIN}.{asset['name']}", asset['status'], {
                    'friendly_name': asset['name'],
                    'icon': 'mdi:car'
                })


    @property
    def name(self):
        return 'LoJack Sensor'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self.attributes
