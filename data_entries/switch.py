import converter
from data_entries.entry import DataEntry


class Switch(DataEntry):
    def __init__(self, module, name, relay_number):
        super().__init__(module, name)
        self.relay_number = relay_number

    def __str__(self):
        return f"""
  - name: {self.get_name()}
    address: {converter.lcn_name}.{converter.lcn_section}.m{self.module}
    output: relay{self.relay_number}
"""
