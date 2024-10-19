# LARP protocol setup
This folder contains the setup files for the Opentrons LARP protocol generator via Excel. The folder includes:

- **`protocol_setup.xlsx`**: An Excel file with the setup information for the protocol generator. This file is utilized by the `xlsx_to_protocol.py` script to create the final protocol script. It is recommended to only modify the indicated cells in the Excel file to avoid errors during the generation of the final protocol script.

- **`xlsx_to_protocol.py`**: A Python script that generates the final protocol script from the `protocol_setup.xlsx` file. This script processes the setup information in the Excel file to produce the final protocol script.

- **`generated_protocol_v001.py`**: An example of a generated protocol script from the `protocol_setup.xlsx` file. This script is created by the `xlsx_to_protocol.py` script. You can verify this protocol by running the script with `SIMULATE_MODE = True`. To run it on the Opentrons robot, set `SIMULATE_MODE = False`.

