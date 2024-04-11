import converter
from entry import DataEntry


class Cover(DataEntry):
    def __init__(self, module, name, motor_number):
        super().__init__(module, name)
        self.motor_number = motor_number

    def __str__(self):
        return f"""
  - name: {self.get_name()}
    address: {converter.lcn_name}.{converter.lcn_section}.m{self.module}
    motor: motor{self.motor_number}
"""
