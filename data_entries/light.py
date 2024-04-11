import converter
from data_entries.entry import DataEntry


class Light(DataEntry):
    def __init__(self, module, name, output_number, dimmable=True):
        super().__init__(module, name)
        self.output_number = output_number
        self.dimmable = dimmable
        self.transition = 1 if self.dimmable else 0

    def __str__(self):
        return f"""
  - name: {self.get_name()}
    address: {converter.lcn_name}.{converter.lcn_section}.m{self.module}
    output: output{self.output_number}
    dimmable: {str(self.dimmable).lower()}
    transition: {self.transition}
"""
