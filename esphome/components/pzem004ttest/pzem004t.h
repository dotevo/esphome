#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"

#ifndef DEVICES_NB
#define DEVICES_NB 1
#endif

namespace esphome {
namespace pzem004t {

class PZEM004T : public PollingComponent, public uart::UARTDevice {
 public:
  void set_map(const uint8_t *map) { this->map_ = map; }
  void set_voltage_sensor(uint8_t id, sensor::Sensor *voltage_sensor) { voltage_sensor_[id] = voltage_sensor; }
  void set_current_sensor(uint8_t id, sensor::Sensor *current_sensor) { current_sensor_[id] = current_sensor; }
  void set_power_sensor(uint8_t id, sensor::Sensor *power_sensor) { power_sensor_[id] = power_sensor; }
  void set_energy_sensor(uint8_t id, sensor::Sensor *energy_sensor) { energy_sensor_[id] = energy_sensor; }

  void setup() override;

  void loop() override;

  void update() override;

  void dump_config() override;

  const uint8_t *map_;

 protected:
  uint8_t current_ = 0;
  sensor::Sensor *voltage_sensor_[DEVICES_NB];
  sensor::Sensor *current_sensor_[DEVICES_NB];
  sensor::Sensor *power_sensor_[DEVICES_NB];
  sensor::Sensor *energy_sensor_[DEVICES_NB];

  enum PZEM004TReadState {
    SET_ADDRESS = 0xB4,
    READ_VOLTAGE = 0xB0,
    READ_CURRENT = 0xB1,
    READ_POWER = 0xB2,
    READ_ENERGY = 0xB3,
    DONE = 0x00,
  } read_state_{DONE};

  void write_state_(uint8_t id, PZEM004TReadState state);

  uint32_t last_read_{0};
};

}  // namespace pzem004t
}  // namespace esphome
