import csv

import pandas as pd

from data_entries import light, sensor, switch, binary_sensor, climate, cover

# lists for the different types of data entries, that will be written to the output file
lights = []
binary_sensors = []
covers = []
climates = []
sensors = []
switches = []

# config
lcn_host = "192.168.17.8"
lcn_port = "4114"
lcn_user = "lcn"
lcn_password = "!secret lcn_password"  # password reference to secrets.yaml

# lcn address format: "{lcn_name}.{lcn_section}.{module}"
lcn_name = "lcnvisu"
lcn_section = "s0"

# input csv structure
csv_sensors_start_index = 8
csv_sensors_end_index = 16
csv_binary_sensors_start_index = csv_sensors_end_index
csv_binary_sensors_end_index = 24
csv_binary_sensors_lock_start_index = csv_binary_sensors_end_index
csv_binary_sensors_lock_end_index = 26

lcn_connection_yaml_string = f"""connections:
  - name: {lcn_name}
    host: {lcn_host}
    port: {lcn_port}
    username: {lcn_user}
    password: {lcn_password}
\n"""


# adds light to the list
def add_light(module, name, output_number, dimmable):
    lights.append(light.Light(module, name, output_number, dimmable))


# adds binary sensor to the list
def add_binary_sensor(module, name, sensor_number):
    binary_sensors.append(binary_sensor.BinarySensor(module, name, source="binsensor", sensor_number=sensor_number))


# adds binary sensor lock to the list
def add_binary_sensor_lock(module, name, sensor_number):
    binary_sensors.append(binary_sensor.BinarySensor(module, name, source="", sensor_number=sensor_number))


# adds cover to the list
def add_cover(module, name, motor_number):
    covers.append(cover.Cover(module, name, motor_number))


# adds climate to the list
def add_climate(module, name, sensor_name):
    climates.append(climate.Climate(module, name, sensor_name))


# adds sensor to the list
def add_sensor(module, name, source, unit_of_measurement="°C"):
    sensors.append(sensor.Sensor(module, name, source, unit_of_measurement))


# adds switch to the list
def add_switch(module, name, relay_number):
    switches.append(switch.Switch(module, name, relay_number))


# adds light switch to the list
def add_light_switch(module, name, relay_number):
    lights.append(switch.Switch(module, name, relay_number))


def read_input_data(input_filename: str):
    """
    Reads the input data from the csv file and adds the devices to the respective lists.
    :param input_filename: filename of the input csv file, accepts only csv files
    """
    with open(input_filename, newline='', encoding='utf-8') as csvfile:
        # read csv and convert to list
        rows = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
        # iterate over rows and columns, ignoring the first header row
        for entry in rows[1:]:
            for i in range(len(entry)):
                # ignore fields starting with *
                if entry[i].startswith("*"):
                    entry[i] = ""

            # extract general data from csv
            module = entry[0]
            a1 = entry[1]
            a1_dimmable = entry[2] == "1" or entry[2] == "1.0"
            a2 = entry[3]
            a2_dimmable = entry[4] == "1" or entry[4] == "1.0"
            r1var = entry[5]
            r2var = entry[6]
            tvar = entry[7]

            # add light if entry is not empty
            if a1:
                add_light(module, a1, 1, a1_dimmable)
            if a2:
                add_light(module, a2, 2, a2_dimmable)

            # add climate and sensor if entry is not empty
            if r1var:
                add_climate(module, r1var, "r1var")
                add_sensor(module, r1var, "r1var")
            if r2var:
                add_climate(module, r2var, "r2var")
                add_sensor(module, r2var, "r2var")
            if tvar:
                add_sensor(module, tvar, "tvar", "NATIVE")

            # iterate over sensor columns
            for i in range(csv_sensors_start_index, csv_sensors_end_index):
                # interpret entry as sensor if it starts with "Jalousie" and takes up two columns
                if entry[i].startswith("Jalousie") and entry[i] and not entry[i + 1]:
                    add_cover(module, entry[i], int((i - csv_sensors_start_index + 2) / 2))
                # interpret entry as light switch if it contains "licht" or "fluter"
                elif entry[i] and ("licht" in entry[i].lower() or "fluter" in entry[i].lower()):
                    add_light_switch(module, entry[i], i - csv_sensors_start_index + 1)
                # interpret entry as switch otherwise
                elif entry[i]:
                    add_switch(module, entry[i], i - csv_sensors_start_index + 1)

            # iterate over binary sensor columns
            for i in range(csv_binary_sensors_start_index, csv_binary_sensors_end_index):
                if entry[i]:
                    add_binary_sensor(module, entry[i], i - csv_binary_sensors_start_index + 1)

            # iterate over binary sensor lock columns
            for i in range(csv_binary_sensors_lock_start_index, csv_binary_sensors_lock_end_index):
                if entry[i]:
                    # extract sensor number and name from entry by splitting at pipe character
                    entry_data = entry[i].split("|")
                    sensor_number = entry_data[0]
                    name = entry_data[1]
                    add_binary_sensor_lock(module, name, sensor_number)


def write_list_data(list_data, data_entry_name: str, file):
    """
    Writes each data entry in the list to the given file.
    :param list_data: list of data entries
    :param data_entry_name: name of the data entry type, this is used as yaml key for the list of data entries
    :param file: file to write the data to
    """
    file.write(f"###################### {data_entry_name.upper()}\n")
    file.write(f"{data_entry_name}:")
    for item in list_data:
        file.write(str(item))


def write_output_data(output_filename: str):
    """
    Creates the formatted output data and writes it to the output file.
    :param output_filename: filename of the output yaml file
    """
    with open(output_filename, 'w', encoding='utf-8') as file:
        # write lcn connection data header
        file.write(lcn_connection_yaml_string)

        write_list_data(lights, "lights", file)
        write_list_data(binary_sensors, "binary_sensors", file)
        write_list_data(covers, "covers", file)
        write_list_data(climates, "climates", file)
        write_list_data(sensors, "sensors", file)
        write_list_data(switches, "switches", file)


def convert(input_filename="input.csv", output_filename="output.yaml"):
    """
    Converts the input file to a yaml file for home assistant config file.
    If the input file is an .ods file, it will be converted to a .csv file first.
    :param input_filename: filename of the input table data file. Accepts .csv and .ods files
    :param output_filename: filename of the output yaml file
    """
    # convert ods to csv and write to input.csv
    if input_filename.endswith('.ods'):
        # read excel using pandas library, define data types for specific columns
        df = pd.read_excel(input_filename, converters={'M': int, 'dimA1': int, 'dimA2': int})
        # write to csv without automatically generated index column
        df.to_csv('input.csv', index=False)
        input_filename = 'input.csv'

    read_input_data(input_filename)
    write_output_data(output_filename)


# main function to run the converter
if __name__ == '__main__':
    filename = "\\\\SynologyPrivat\\familie\\LCN Bussystem Doku\\_Übersicht Master.ods"
    convert(input_filename=filename)
