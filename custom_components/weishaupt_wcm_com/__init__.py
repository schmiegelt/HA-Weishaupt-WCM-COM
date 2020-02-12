"""Weishaupt WCM-COM."""

from .const import DOMAIN
import logging
from homeassistant.helpers.entity import Entity
from datetime import timedelta, datetime
from weishaupt_wcm_com import heat_exchanger
import json
import voluptuous as vol
import homeassistant.helpers.config_validation as cv


from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
)

_LOGGER = logging.getLogger(__name__)

WEISHAUPT_PLATFORMS = ['sensor']
SCAN_INTERVAL = timedelta(seconds=100)


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms

    host = config[DOMAIN][CONF_HOST]
    username = config[DOMAIN][CONF_USERNAME]
    passwort = config[DOMAIN][CONF_PASSWORD]

    api = WeishauptAPI(host, username, passwort)

    hass.data[DOMAIN] = api

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True


class WeishauptBaseEntity(Entity):  
    def __init__(self, hass, config):
        self._api = hass.data[DOMAIN]
        
    def api(self):
        return self._api


    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("Super Updating")

        #SERVER = "http://192.168.0.33" 
        #USER = "admin"
        #PASSWORD = "eAFh7J9uZJ3Afh" 
        self._api.update()


class WeishauptAPI:
    def __init__(self, host, username, password):
        self._host = host
        self._username = username
        self._password = password
        self._data = {}

    def getData(self):
        return self._data

    def update(self):
        result = heat_exchanger.process_values(self._host, self._username, self._password)
        _LOGGER.debug(result)
        if result != None:
            self._data = json.loads(result)
        else:
            _LOGGER.debug("Cannot Update Data")
    
