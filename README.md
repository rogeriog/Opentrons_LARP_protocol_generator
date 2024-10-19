# Opentrons LARP protocol generator and graphical prognostic
This repository contains code to design and evaluate LARP (Ligand-assisted reprecipitation) synthesis protocols to be performed using the OT-2 liquid handler robot. The code can be evaluated using the `opentrons_simulate` API to verify any inconsistencies. Additionally, a graphical interface is provided to visualize the different stages of the LARP synthesis.

![Graphical Prognostic of LARP Protocol](https://github.com/user-attachments/assets/83c2734d-7202-4edf-8638-41f5334a6729)
*Example of graphical prognostic of the LARP protocol.*

## Installation
Clone the repository and install the required packages using the following command:
```bash
pip install -r requirements.txt
```

## Usage
There are two ways to use the code:

1. **Using the LARP Protocol Script**:
   - Navigate to the `protocol_scripts` folder and copy the desired script to a new folder.
   - Edit the entries such as pipette tips, labware, and reagents according to your lab setup in the appropriate variables.
   - Ensure any custom labware files used by the protocol are in the same folder.
   - Run the script using Python:
     ```bash
     python3 larp_script_v001.py
     ```
   - If `SIMULATE_MODE` is set to `True`, the script will run in simulation mode, generating a graphical interface to visualize the different stages of the LARP synthesis. If `SIMULATE_MODE` is set to `False`, the script can be uploaded directly to the OT-2 robot.
   - Verify the run using the following command from the Opentrons API:
     ```bash
     opentrons_simulate larp_script_v001.py
     ```
   - Ensure the `SIMULATE_MODE` variable in the script is set to `False` and the labware JSON files are in the same folder.

   If all goes well, you can upload the script to the OT-2 robot and run the LARP synthesis.

2. **Generating Protocol from Excel File**:
   - In the `protocol_setup` folder, there is an Excel file named `protocol_setup.xlsx` which provides a user-friendly way to declare all necessary variables for the protocol generator.
   - Modify only the indicated cells in the Excel file to avoid errors during the generation of the final protocol script.
   - Use the `xlsx_to_protocol.py` script to create the final protocol script.
   - The final script can be used to generate the graphical prognostic of the LARP synthesis or be uploaded to the OT-2 robot, just as in the first method.

## Conclusion
This repository provides a comprehensive solution for designing and evaluating LARP synthesis protocols using the OT-2 liquid handler robot. Whether you prefer scripting directly or using an Excel-based setup, the tools provided will help ensure accurate and efficient protocol execution.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Brazilian funding agency CNPq for the financial support throughout this project.
- [Opentrons](https://opentrons.com/) for devoloping the OT-2 liquid handler robot and API.