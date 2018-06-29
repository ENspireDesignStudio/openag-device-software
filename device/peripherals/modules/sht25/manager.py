# Import standard python modules
from typing import Optional, Tuple, Dict

# Import device utilities
from device.utilities.modes import Modes

# Import peripheral parent class
from device.peripherals.classes.peripheral_manager import PeripheralManager

# Import sht25 elements
from device.peripherals.modules.sht25.events import SHT25Events
from device.peripherals.modules.sht25.driver import SHT25Driver
from device.peripherals.modules.sht25.exceptions import DriverError


class SHT25Manager(PeripheralManager, SHT25Events):
    """ Manages an sht25 temperature and humidity sensor. """

    def __init__(self, *args, **kwargs):
        """ Instantiates manager Instantiates parent class, and initializes 
            sensor variable name. """

        # Instantiate parent class
        super().__init__(*args, **kwargs)

        # Initialize variable names
        self.temperature_name = self.parameters["variables"]["sensor"][
            "temperature_celcius"
        ]
        self.humidity_name = self.parameters["variables"]["sensor"]["humidity_percent"]

    @property
    def temperature(self) -> None:
        """ Gets temperature value. """
        return self.state.get_peripheral_reported_sensor_value(
            self.name, self.temperature_name
        )

    @temperature.setter
    def temperature(self, value: float) -> None:
        """ Sets temperature value in shared state. Does not update environment from calibration mode. """
        self.state.set_peripheral_reported_sensor_value(
            self.name, self.temperature_name, value
        )
        if self.mode != Modes.CALIBRATE:
            self.state.set_environment_reported_sensor_value(
                self.name, self.temperature_name, value
            )

    @property
    def humidity(self) -> None:
        """ Gets humidity value. """
        return self.state.get_peripheral_reported_sensor_value(
            self.name, self.humidity_name
        )

    @humidity.setter
    def humidity(self, value: float) -> None:
        """ Sets humidity value in shared state. Does not update environment from calibration mode. """
        self.state.set_peripheral_reported_sensor_value(
            self.name, self.humidity_name, value
        )
        if self.mode != Modes.CALIBRATE:
            self.state.set_environment_reported_sensor_value(
                self.name, self.humidity_name, value
            )

    def initialize(self) -> None:
        """Initializes manager."""
        self.logger.info("Initializing")

        # Clear reported values
        self.clear_reported_values()

        # Initialize health
        self.health = 100.0

        # Initialize driver
        try:
            self.driver = SHT25Driver(
                name=self.name,
                bus=self.parameters["communication"]["bus"],
                mux=int(self.parameters["communication"]["mux"], 16),
                channel=self.parameters["communication"]["channel"],
                address=int(self.parameters["communication"]["address"], 16),
                simulate=self.simulate,
                mux_simulator=self.mux_simulator,
            )
        except DriverError as e:
            self.logger.exception("Manager unable to initialize")
            self.health = 0.0
            self.mode = Modes.ERROR
            return

        # Successful initialization!
        self.logger.info("Initialized successfully")

    def setup(self) -> None:
        """Sets up sensor."""
        self.logger.info("No setup required")

    def update(self) -> None:
        """Updates sensor by reading temperature and humidity values then 
        reports them to shared state."""

        # Read temperature
        try:
            temperature = self.driver.read_temperature(retry=True)
        except DriverError:
            self.logger.exception("Unable to read temperature")
            self.mode = Modes.ERROR
            self.health = 0.0
            return

        # Read humidity
        try:
            humidity = self.driver.read_humidity(retry=True)
        except DriverError:
            self.logger.exception("Unable to read humidity")
            self.mode = Modes.ERROR
            self.health = 0.0
            return

        # Update reported values
        self.temperature = temperature
        self.humidity = humidity
        self.health = 100.0

    def reset(self) -> None:
        """ Resets sensor. """
        self.logger.info("Resetting")

        # Clear reported values
        self.clear_reported_values()

        # Reset driver if not in error mode
        try:
            if self.mode != Modes.ERROR:
                self.driver.reset()
        except DriverError:
            self.logger.exception("Unable to reset driver")

        # Sucessfully reset!
        self.logger.debug("Successfully reset!")

    def shutdown(self) -> None:
        """ Shuts down sensor. """
        self.logger.info("Shutting down")

        # Clear reported values
        self.clear_reported_values()

        # Successfully shutdown
        self.logger.info("Successfully shutdown!")

    def clear_reported_values(self):
        """ Clears reported values. """
        self.temperature = None
        self.humidity = None