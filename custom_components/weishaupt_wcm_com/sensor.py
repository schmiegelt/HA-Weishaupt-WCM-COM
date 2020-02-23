"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import logging
from datetime import timedelta, datetime

from .const import DOMAIN
from .const import NAME_PREFIX

from .const import OIL_CONSUMPTION_KEY
from .const import OUTSIDE_TEMPERATURE_KEY
from .const import LOAD_SETTING_KEY
from .const import WARM_WATER_TEMPERATURE_KEY 
from .const import FLOW_TEMPERATURE_KEY
from .const import FLUE_GAS_TEMPERATURE_KEY

from . import WeishauptBaseEntity



SENSOR_TYPES = {
    "oil_meter"
}

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return
    add_entities(
        [
            WeishauptSensor(hass, config, OIL_CONSUMPTION_KEY, "l"),
            WeishauptSensor(hass, config, OUTSIDE_TEMPERATURE_KEY, "°C"),
            WeishauptSensor(hass, config, LOAD_SETTING_KEY, "kW"),
            WeishauptSensor(hass, config, WARM_WATER_TEMPERATURE_KEY, "°C"),
            WeishauptSensor(hass, config, FLOW_TEMPERATURE_KEY, "°C"),
            WeishauptSensor(hass, config, FLUE_GAS_TEMPERATURE_KEY, "°C")
        ]
    )


class WeishauptSensor(WeishauptBaseEntity):
    """Representation of a Sensor."""

    def __init__(self, hass, config, sensor_name, sensor_unit):
        super().__init__(hass, config)
        """Initialize the sensor."""
        self._state = None
        self._data = {}
        self._config = config

        self._name = sensor_name
        self._unit = sensor_unit

    @property
    def name(self):
        """Return the name of the sensor."""
        return NAME_PREFIX + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("Updating Sensor")
        super().update()
        try: 
            self._state = self.api().getData()[self._name]
        except:
            self._state = None
