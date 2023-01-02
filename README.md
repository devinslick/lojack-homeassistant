# LoJack integration for Home Assistant
This integration allows you to track the location of your LoJack-enabled devices in Home Assistant.

## Installation
Install the integration through HACS (Home Assistant Community Store).
Add the following to your configuration.yaml file:
````
lojack:
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
````
Restart Home Assistant.
The integration will automatically create a device_tracker entity for each LoJack device connected to your account.

## Configuration
The integration requires a LoJack account with a valid username and password.

You can specify the username and password in the configuration.yaml file:
````
lojack:
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
````
## Features
Automatically creates a device_tracker entity for each LoJack device connected to your account.
Updates the location of the device_tracker entities in real-time.

## Credits
This integration is powered by the lojack-clients Python library.

## Support
If you have any issues with this integration, please open an issue on GitHub.