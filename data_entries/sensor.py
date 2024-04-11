import converter
from data_entries.entry import DataEntry


class Sensor(DataEntry):
    def __init__(self, module, name, source, unit_of_measurement="°C"):
        super().__init__(module, name)
        self.source = source
        self.unit_of_measurement = unit_of_measurement

    def __str__(self):
        return f"""
  - name: {self.get_name()}
    address: {converter.lcn_name}.{converter.lcn_section}.m{self.module}
    source: {self.source}
    unit_of_measurement: {self.unit_of_measurement}
"""
