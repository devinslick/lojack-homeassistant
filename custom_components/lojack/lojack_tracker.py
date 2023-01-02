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
        self.update()

    def update(self):
        identity_client = IdentityClient.from_login(self.username, self.password)
        token_response = get_identity_token.sync(client=identity_client)

        services_client = ServicesClient.from_token(token_response.token)
        assets_response: GetAllUserAssetsResponse200 = get_all_user_assets.sync(client=services_client)

        self._state = assets_response.num_assets

        for asset in assets_response.assets:
            entity_id = "device_tracker.{}".format(asset.name)
            if entity_id not in self.hass.states:
                self.hass.states.set(entity_id, asset.id)
            self.device_attributes[entity_id] = asset.attributes
                
    @property
    def name(self):
        return 'LoJack Sensor'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self.attributes
