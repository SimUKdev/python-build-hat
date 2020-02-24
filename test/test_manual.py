import random
import resource
import unittest

# Start fakeHat manually before this line
import hub


# These tests should pass regardless of the state of the hat
class GeneralTestCase(unittest.TestCase):
	def test_hub_type(self):
		{'BT_VCP', 'Image', 'USB_VCP', 'battery', 'ble', 'bluetooth', 'button', 'display', 'firmware', 'info', 'led', 'motion', 'port', 'power_off', 'sound', 'status', 'supervision', 'temperature', 'text'}.issubset(dir(hub))

	def test_hub_info_type(self):
		assert isinstance(hub.info(), dict)
		assert len(hub.info())>=2
		assert {'hardware_revision', 'device_uuid'}.issubset(hub.info().keys()) # From real hub

	def test_battery_type(self):
		assert {'BATTERY_BAD_BATTERY', 'BATTERY_HUB_TEMPERATURE_CRITICAL_OUT_OF_RANGE', 'BATTERY_NO_ERROR', 'BATTERY_TEMPERATURE_OUT_OF_RANGE', 'BATTERY_TEMPERATURE_SENSOR_FAIL', 'BATTERY_VOLTAGE_TOO_LOW', 'CHARGER_STATE_CHARGING_COMPLETED', 'CHARGER_STATE_CHARGING_ONGOING', 'CHARGER_STATE_DISCHARGING', 'CHARGER_STATE_FAIL', 'USB_CH_PORT_CDP', 'USB_CH_PORT_DCP', 'USB_CH_PORT_NONE', 'USB_CH_PORT_SDP', 'capacity_left', 'charger_detect', 'current', 'info', 'temperature', 'voltage'}.issubset(dir(hub.battery)) 

	def test_battery_info_type(self):
		assert {'temperature', 'charge_voltage', 'charge_current', 'charge_voltage_filtered', 'error_state', 'charger_state', 'battery_capacity_left'}.issubset(hub.battery.info().keys())

	def test_battery_functionality(self):
		assert 0 <= hub.battery.capacity_left() <= 100
		assert 0 <= hub.battery.charger_detect() <= 4 # Number says what kind of charger
		assert 0 <= hub.battery.current() < 100 # In milliamps Assumes nothing is plugged in, goes up when motor is running
		assert 10<= hub.battery.temperature() <= 40 # In C. Assuming we're indoors
		assert 6 <= hub.battery.voltage() <= 10 # Voltage in milivolts

	def test_port_types(self):
		ports = [hub.port.A, hub.port.B, hub.port.C, hub.port.D, hub.port.F]
		random.shuffle(ports)
		for P in ports:
			assert {'callback', 'device', 'info', 'mode', 'pwm'}.issubset(dir(P))
			assert isinstance(P.info(), dict)
			assert {'type'}.issubset(P.info().keys())

	@unittest.skip("Not implemented")
	def test_port_mode_implemented(self):
		ports = [hub.port.A, hub.port.B, hub.port.C, hub.port.D, hub.port.F]
		random.shuffle(ports)
		for P in ports:
			P.mode()

# These tests must be done with a dummy attached to port A
class DummyAttachedATestCase(unittest.TestCase):
	def test_dummy_port_info(self):
		assert isinstance(hub.port.A.info(), dict)
		assert {'type', 'fw_version', 'hw_version', 'modes', 'combi_modes'}.issubset(hub.port.A.info().keys())
		assert isinstance(hub.port.A.info()['modes'], list)
		assert {'name', 'raw', 'pct', 'si', 'symbol', 'map_out', 'map_in', 'capability', 'format'}.issubset(hhub.port.A.info()['modes'][1].keys())

	def test_port_device_mode(self):
		assert {'mode'}.issubset(dir(hub.port.A.device))
		try:
			isinstance(hub.port.A.device.mode())
		except NotImpelementedError:
			self.skipTest('Mode not implemented')

# These tests must be done with nothing attached to port F
class PortDetachedBTestCase(unittest.TestCase):
	def test_port_info(self):
		assert isinstance(hub.port.F.info(), dict)
		assert hub.port.F.info() == {'type': None}

	def test_port_device(self):
		assert hub.port.F.device is None

# These tests must be done with a motor attached to port A
class MotorAttachedATestCase(self):
 	def test_port_A_type_with_motor_connected(self):
		P = hub.port.A
		assert {'callback', 'device', 'info', 'mode', 'motor', 'pwm'}.issubset(dir(P)) 
		assert isinstance(P.info(), dict)
		assert {'type', 'fw_version', 'hw_version', 'modes', 'combi_modes'}.issubset(P.info().keys())

	def test_motor_A_type_with_motor_connected(self):
		assert {'BUSY_MODE', 'BUSY_MOTOR', 'EVENT_COMPLETED', 'EVENT_INTERRUPTED', 'FORMAT_PCT', 'FORMAT_RAW', 'FORMAT_SI', 'PID_POSITION', 'PID_SPEED', 'STOP_BRAKE', 'STOP_FLOAT', 'STOP_HOLD', 'brake', 'busy', 'callback', 'default', 'float', 'get', 'hold', 'mode', 'pair', 'pid', 'preset', 'pwm', 'run_at_speed', 'run_for_degrees', 'run_for_time', 'run_to_position'}.issubset(dir(hub.motor.A))

	def test_motor_A_functionality_with_motor_connected(self):
		hub.port.A.motor.run_for_time(1000, 127) # run for 1000ms at maximum clockwise speed
		hub.port.A.motor.run_for_time(1000, -127) # run for 1000ms at maximum anticlockwise speed
		hub.port.A.motor.run_for_degrees(180, 127) # turn 180 degrees clockwise at maximum speed
		hub.port.A.motor.run_for_degrees(720, -127) # Make two rotations anticlockwise at maximum speed
		hub.port.A.motor.run_to_position(0, 127) # Move to top dead centre at maximum speed (positioning seems to be absolute)
		hub.port.A.motor.run_to_position(180, 127) # Move to 180 degrees forward of top dead centre at maximum speed

# Touch sensor must be connected to port B
class TouchSensorBTestCase(self):
	def test_touch_sensor_B_type(self):
		assert {'FORMAT_PCT', 'FORMAT_RAW', 'FORMAT_SI', 'get', 'mode', 'pwm'}.issubset(dir(hub.port.B.device))

	def test_touch_sensor_B_functionality(self):
		assert hub.port.B.device.get() <= 1 # Without button pressed
		assert hub.port.B.device.get() >= 0 # At all times
		assert hub.port.B.device.get() <= 9 # At all times

if __name__ == '__main__':
    unittest.main()
