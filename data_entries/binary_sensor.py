import converter
from data_entries.entry import DataEntry


class BinarySensor(DataEntry):
    def __init__(self, module, name, source, sensor_number):
        super().__init__(module, name)
        self.source = source + str(sensor_number)

    def __str__(self):
        return f"""
  - name: {self.get_name()}
    address: {converter.lcn_name}.{converter.lcn_section}.m{self.module}
    source: {self.source}
"""
