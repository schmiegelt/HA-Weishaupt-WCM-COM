"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import logging
from datetime import timedelta, datetime

from .const import DOMAIN
from .const import OILCONSUMPTION_KEY

from . import WeishauptBaseEntity



SCAN_INTERVAL = timedelta(minutes=1)


SENSOR_TYPES = {
    "oil_meter"
}

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    add_entities([WeishauptSensor(hass, config)])


class WeishauptSensor(WeishauptBaseEntity):
    """Representation of a Sensor."""

    def __init__(self, hass, config):
        super().__init__(hass, config)
        """Initialize the sensor."""
        self._state = None
        self._data = {}
        self._config = config

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Oil Meter'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'l'

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("Updating Sensor")
        super().update()
        try: 
            self._state = self.api().getData()[OILCONSUMPTION_KEY]
        except:
            self._state = None
