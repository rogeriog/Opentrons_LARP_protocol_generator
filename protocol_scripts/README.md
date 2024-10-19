# Protocol scripts
This folder contains the base scripts for the Opentrons LARP protocol generator. These scripts are used to:

- Run the graphical interface (when `SIMULATE_MODE = True`) to verify the protocol before running it on the robot.
- Upload the scripts directly to the robot through the Opentrons software (when `SIMULATE_MODE = False`).

You can edit the scripts to adapt them to your specific needs by adjusting the labware and setup accordingly. The scripts are written in Python and use the Opentrons API to interact with the robot.

> We now provide an Excel file to facilitate the setup of the protocol. The file is located in the `protocol_setup` folder and is named `protocol_setup.xlsx`. This file must be edited and accessed by the `xlsx_to_protocol.py`, which will then generate a protocol script.


**Important:** The labware files used as examples are included in the `labware_examples` folder and should be accessible to the script and uploaded to the robot before running the protocol.