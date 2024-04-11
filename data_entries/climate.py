import converter
from entry import DataEntry


class Climate(DataEntry):
    def __init__(self, module, name, sensor_name, min_temp=17, max_temp=25, lockable=True, unit_of_measurement="°C"):
        super().__init__(module, name)
        self.sensor_name = sensor_name
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.lockable = lockable
        self.unit_of_measurement = unit_of_measurement

    def __str__(self):
        return f"""
  - name: {self.get_name()}
    address: {converter.lcn_name}.{converter.lcn_section}.m{self.module}
    source: {self.sensor_name}
    setpoint: {self.sensor_name}setpoint
    min_temp: {self.min_temp}
    max_temp: {self.max_temp}
    lockable: {str(self.lockable).lower()}
    unit_of_measurement: {self.unit_of_measurement}
"""
