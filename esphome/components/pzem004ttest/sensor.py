import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_CURRENT,
    CONF_ID,
    CONF_POWER,
    CONF_VOLTAGE,
    CONF_ENERGY,
    CONF_RAW_DATA_ID,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_VOLT,
    UNIT_AMPERE,
    UNIT_WATT,
    UNIT_WATT_HOURS,
)

DEPENDENCIES = ["uart"]

pzem004t_ns = cg.esphome_ns.namespace("pzem004t")
PZEM004T = pzem004t_ns.class_("PZEM004T", cg.PollingComponent, uart.UARTDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(PZEM004T),
            cv.GenerateID(CONF_RAW_DATA_ID): cv.declare_id(cg.uint8),
            cv.Required("devices"): cv.All(
                cv.ensure_list(
                    {
                        cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                            unit_of_measurement=UNIT_VOLT,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_VOLTAGE,
                            state_class=STATE_CLASS_MEASUREMENT,
                        ),
                        cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                            unit_of_measurement=UNIT_AMPERE,
                            accuracy_decimals=2,
                            device_class=DEVICE_CLASS_CURRENT,
                            state_class=STATE_CLASS_MEASUREMENT,
                        ),
                        cv.Optional(CONF_POWER): sensor.sensor_schema(
                            unit_of_measurement=UNIT_WATT,
                            accuracy_decimals=0,
                            device_class=DEVICE_CLASS_POWER,
                            state_class=STATE_CLASS_MEASUREMENT,
                        ),
                        cv.Optional(CONF_ENERGY): sensor.sensor_schema(
                            unit_of_measurement=UNIT_WATT_HOURS,
                            accuracy_decimals=0,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Required("ip"): cv.int_,
                    }
                ),
                cv.Length(min=1, max=8),
            ),
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if "devices" in config:
        devices = config["devices"]
        cg.add_define("DEVICES_NB", len(devices))
        id = 0
        ips = []
        for device in devices:
            ips.extend([device["ip"]])

            if CONF_VOLTAGE in device:
                conf = device[CONF_VOLTAGE]
                sens = await sensor.new_sensor(conf)
                cg.add(var.set_voltage_sensor(id, sens))
            if CONF_CURRENT in device:
                conf = device[CONF_CURRENT]
                sens = await sensor.new_sensor(conf)
                cg.add(var.set_current_sensor(id, sens))
            if CONF_POWER in device:
                conf = device[CONF_POWER]
                sens = await sensor.new_sensor(conf)
                cg.add(var.set_power_sensor(id, sens))
            if CONF_ENERGY in device:
                conf = device[CONF_ENERGY]
                sens = await sensor.new_sensor(conf)
                cg.add(var.set_energy_sensor(id, sens))
            id = id + 1

        prog_arr = cg.progmem_array(config[CONF_RAW_DATA_ID], ips)
        cg.add(var.set_map(prog_arr))
