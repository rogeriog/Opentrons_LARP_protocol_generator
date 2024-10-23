import pandas as pd
import numpy as np
import re
from collections import OrderedDict
import os
# Read the Excel file
df = pd.read_excel('protocol_setup.xlsx')

# display everything
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Find all rows where 'WELLS', 'SOLUTION', and 'QUANTITY' appear in the same row
keyword_rows = df[df.isin(['WELLS', 'SOLUTION', 'QUANTITY']).sum(axis=1) >= 2].index

# Initialize a list to store extracted data
extracted_data = []


# Loop through each keyword row and extract rows below "WELLS"
for idx in keyword_rows:
    # Identify the column where "WELLS" appears in the current row
    wells_col = df.iloc[idx].eq('WELLS')
    
    # If "WELLS" is found in a specific column, extract the index
    for wells_col_idx in np.where(wells_col)[0]:
        
        # Now find the range of rows below this one in the "WELLS" column
        rows_below = df.iloc[idx+1:, wells_col_idx]
        
        # Get rows below until the first NaN is encountered
        first_nan_idx = rows_below[rows_below.isna()].index[0] if rows_below.isna().any() else rows_below.index[-1]
        
        # Append the range of interest (rows between idx+1 and first_nan_idx)
        block = df.iloc[idx-4:first_nan_idx+1, wells_col_idx:wells_col_idx+3]
        # remove trailing NaN values, if all values in a row are NaN
        block = block.dropna(how='all')
        # reset indexes 
        block = block.reset_index(drop=True)
        block[block.iloc[:,0]=='LABWARE'].values[0][1]
        extracted_data_block = {
            'Labware': block[block.iloc[:,0]=='LABWARE'].values[0][1],
            'Max Volume': block[block.iloc[:,0]=='MAX VOLUME'].values[0][1],
            'Position': block[block.iloc[:,0]=='POSITION'].values[0][1],
        } 
        # Extract well data (WELLS, SOLUTION, QUANTITY)
        well_data = { }
        start_idx = block[block.iloc[:,0]=='WELLS'].index[0]+1
        for i in range(start_idx, len(block)):
            well = block.iloc[i,0] 
            solution = block.iloc[i,1] if pd.notna(block.iloc[i,1]) else None
            quantity = block.iloc[i,2] if pd.notna(block.iloc[i,2]) else None
            if pd.notna(well):  # Only process rows with well data
                well_data[well] = {'Solution': solution, 'Quantity': quantity}

        # Add the well data to the extracted info
        extracted_data_block['Wells'] = well_data
        extracted_data.append(extracted_data_block)



labware_strs = []
unique_solutions = {
    'precursors': OrderedDict(),
    'ligands': OrderedDict(),
    'additives': OrderedDict(),
    'antisolvents': OrderedDict(),
}
for data_block in extracted_data:
    # Extract labware and volume data
    labware = data_block['Labware']
    max_volume = data_block['Max Volume']
    position = data_block['Position']

    # Determine labware type based on position
    if position in [1, 4, 7]:
        labware_str = 'precursors'
    elif position in [2, 5, 8]:
        labware_str = 'intermediate'
    elif position in [3, 6, 9]:
        labware_str = 'final'

    # Create the labware string
    labware_str = labware_str + '_vol' + str(max_volume) + '_pos' + str(position)
    # = protocol.load_labware("lamaiufrgspreto24_24_tuberack_5000ul",  location='3')
    labware_str = labware_str + ' = protocol.load_labware("' + labware + '", location=\'' + str(position) + '\')'
    labware_strs.append(labware_str)
    # Extract well data
    wells = data_block['Wells']

    # Classify each solution based on well and position
    for well, well_data in wells.items():
        solution = well_data['Solution']
        
        # Only add valid solutions (not None)
        if solution:
            if position in [7]:  # Precursors
                unique_solutions['precursors'][solution] = None
            elif position in [4]: # Ligands additives
                if well.startswith('A') or well.startswith('B'):
                    unique_solutions['ligands'][solution] = None
                elif well.startswith('C') or well.startswith('D'):
                    unique_solutions['additives'][solution] = None
            elif position in [1]: # Antisolvents
                unique_solutions['antisolvents'][solution] = None

labware_strs = set(labware_strs)

# format the labware strings in a multiline string
print('\n\n------- Labware Strings ------- \n\n')    
labware_strs_multiline = '\n\n'.join(labware_strs)
print(labware_strs_multiline)
# Safely pop values from the ordered dicts, or assign None if the dict is empty
solution_nicknames = {
    'precursor_solution_1': unique_solutions['precursors'].popitem(last=False)[0] if unique_solutions['precursors'] else 'Precursor 1',
    'precursor_solution_2': unique_solutions['precursors'].popitem(last=False)[0] if unique_solutions['precursors'] else 'Precursor 2',
    'precursor_solution_3': unique_solutions['precursors'].popitem(last=False)[0] if unique_solutions['precursors'] else 'Precursor 3',
    'precursor_solution_4': unique_solutions['precursors'].popitem(last=False)[0] if unique_solutions['precursors'] else 'Precursor 4',
    'ligand_1' : unique_solutions['ligands'].popitem(last=False)[0] if unique_solutions['ligands'] else 'Ligand 1',
    'ligand_2' : unique_solutions['ligands'].popitem(last=False)[0] if unique_solutions['ligands'] else 'Ligand 2',
    'ligand_3' : unique_solutions['ligands'].popitem(last=False)[0] if unique_solutions['ligands'] else 'Ligand 3',
    'ligand_4' : unique_solutions['ligands'].popitem(last=False)[0] if unique_solutions['ligands'] else 'Ligand 4',
    'reactant_1': unique_solutions['additives'].popitem(last=False)[0] if unique_solutions['additives'] else 'Reactant 1',
    'reactant_2': unique_solutions['additives'].popitem(last=False)[0] if unique_solutions['additives'] else 'Reactant 2',
    'reactant_3': unique_solutions['additives'].popitem(last=False)[0] if unique_solutions['additives'] else 'Reactant 3',
    'antisolvent': unique_solutions['antisolvents'].popitem(last=False)[0] if unique_solutions['antisolvents'] else 'Antisolvent',
    'antisolvent_2': unique_solutions['antisolvents'].popitem(last=False)[0] if unique_solutions['antisolvents'] else 'Antisolvent 2',
    'intermediate_solution': unique_solutions['intermediate'].popitem(last=False)[0] if unique_solutions.get('intermediate') else 'Intermediate Solution',
}

## format the solution nicknames in a multiline string
solution_nicknames_str = "solution_nicknames = {\n"
for key, value in solution_nicknames.items():
    solution_nicknames_str += f'    "{key}": "{value}",\n'
solution_nicknames_str += "}"
print('\n\n------- Solution Nicknames ------- \n\n')
print(solution_nicknames_str)

# now we screen starting from the solution nicknames, I want to generate
# text entries in the following format:
## initial_solutions = {
        #   "precursor_solution_1": [
        #     {"container": precursors_20_pos7, "positions": ["A1", "B1"], 
        #      "volume": 10_000}
        # ],
        # "precursor_solution_2": [
        # ....
        # ]
# }
# therefore we need to iterate over the solution_nicknames dictionary and
# generate the text entries, then look at the datablocks in the extracted_data
# and find the corresponding wells and volume data for each solution nickname.

# Initialize the dictionary to store the final result
initial_solutions = {}

# Iterate over the solution_nicknames dictionary
for solution_name, solution_value in solution_nicknames.items():
    if not solution_value:
        continue  # Skip if the solution value is None

    # Search for the corresponding data block based on the solution name
    for data_block in extracted_data:
        wells = data_block['Wells']
        position = data_block['Position']
        if position not in [1, 4, 7]:
            continue # Skip if the position is not a precursor position
        max_volume = data_block['Max Volume']
        labware_str = 'precursors' + '_vol' + str(max_volume) + '_pos' + str(position)
        # Collect wells that correspond to the current solution value
        for well, well_data in wells.items():
            if well_data['Solution'] == solution_value:
                # Check if we already have an entry for the same container and volume
                match_found = False
                for entry in initial_solutions.get(solution_name, []):
                    if entry['container'] == labware_str and entry['volume'] == well_data['Quantity']:
                        # If match is found, append the well position
                        entry['positions'].append(well)
                        match_found = True
                        break
                if not match_found:
                    # If no match found, create a new entry
                    new_entry = {
                        'container': labware_str,
                        'positions': [well],
                        'volume': well_data['Quantity']
                    }
                    # If this solution name is not yet in the dictionary, initialize it
                    if solution_name not in initial_solutions:
                        initial_solutions[solution_name] = []
                    initial_solutions[solution_name].append(new_entry)

# Generate the multiline string representation
def dict_to_multiline_string(d, indent=0):
    result = []
    indent_str = ' ' * indent
    for key, value in d.items():
        result.append(f'{indent_str}"{key}": [')
        for entry in value:
            result.append(f'{indent_str}  {{"container": {entry["container"]}, "positions": {entry["positions"]}, "volume": {entry["volume"]}}},')
        result.append(f'{indent_str}],')
    return '\n'.join(result)

# Convert initial_solutions dictionary to a multiline string
initial_solutions_str = "initial_solutions = {\n" + dict_to_multiline_string(initial_solutions, indent=4) + "\n}"

# Display the generated multiline string
print('\n\n------- Initial solutions ------- \n\n')
print(initial_solutions_str)

# now i need the intermediate solutions
# intermediate_solutions = [ 
        # {"container": intermediate_solutions_15_pos5, "positions": ["A1"], 
        #  "solutions": {
        #     "precursor_solution_1": 2_000,
        #     "precursor_solution_2": 2_000,
        #     "ligand_1": 200,
        #     "ligand_2": 200,
        #     }},
# the entries for them will be in the extracted_data with position 2, 5, 8
# and they will appear separated by comma with the same names of the nickname
# dictionary, entries in the wells will be like:
# A1	precursor1, precursor2, oleic acid, oleylamine	1000, 1000, 100, 100
# A2	precursor1, precursor2, oleic acid, oleylamine	1000, 1000, 200, 100
# so each correspond to a different solution.
# Initialize the list to store the intermediate solutions
intermediate_solutions = []

# Iterate over the solution_nicknames dictionary to ensure proper mapping
solution_lookup = {v: k for k, v in solution_nicknames.items() if v}

# Iterate through the extracted data for intermediate positions (2, 5, 8)
for data_block in extracted_data:
    wells = data_block['Wells']
    position = data_block['Position']

    # Only process intermediate positions (2, 5, 8)
    if position not in [2, 5, 8]:
        continue

    max_volume = data_block['Max Volume']
    labware_str = 'intermediate' + '_vol' + str(max_volume) + '_pos' + str(position)

    # Iterate through wells to parse solutions and volumes
    for well, well_data in wells.items():
        solutions_str = well_data['Solution']
        volumes_str = well_data['Quantity']

        # Skip if no valid solutions or quantities
        if pd.isna(solutions_str) or pd.isna(volumes_str):
            continue

        # Split solutions and volumes by commas
        solutions_list = [s.strip() for s in solutions_str.split(',')]
        volumes_list = [int(v.strip()) for v in volumes_str.split(',')]

        # Create a dictionary of solutions mapped to their volumes
        solutions_dict = {}
        for solution, volume in zip(solutions_list, volumes_list):
            solution_nickname = solution_lookup.get(solution)
            if solution_nickname:
                solutions_dict[solution_nickname] = volume

        # If we found valid solutions, add to the intermediate_solutions list
        if solutions_dict:
            entry = {
                "container": labware_str,
                "positions": [well],
                "solutions": solutions_dict
            }

            # If there is already an entry for the same container and position, update it
            match_found = False
            for intermediate_entry in intermediate_solutions:
                if intermediate_entry['container'] == labware_str and intermediate_entry['positions'] == [well]:
                    intermediate_entry['solutions'].update(solutions_dict)
                    match_found = True
                    break

            if not match_found:
                intermediate_solutions.append(entry)
# Generate the multiline string representation for intermediate_solutions
def list_to_multiline_string(lst, indent=0):
    result = []
    indent_str = ' ' * indent
    for entry in lst:
        result.append(f'{indent_str}{{"container": {entry["container"]}, "positions": {entry["positions"]}, "solutions": {{')
        for sol_name, vol in entry["solutions"].items():
            result.append(f'{indent_str}    "{sol_name}": {vol},')
        result.append(f'{indent_str}}}}},')
    return '\n'.join(result)

# Convert intermediate_solutions list to a multiline string
intermediate_solutions_str = "intermediate_solutions = [\n" + list_to_multiline_string(intermediate_solutions, indent=4) + "\n]"


# Display the generated multiline string
print('\n\n------- Intermediate solutions ------- \n\n')
print(intermediate_solutions_str)

# Initialize the list to store the final solutions
final_solutions = []
intermediate_solution_references = []


# Define a regex pattern to match positions like '5 A1, 5 B2, 2 A2'
position_pattern = re.compile(r'\d+\s+[A-H]\d', re.IGNORECASE)

# Iterate through the extracted data for final positions (3, 6, 9)
for data_block in extracted_data:
    wells = data_block['Wells']
    labware = data_block['Labware']
    max_volume = data_block['Max Volume']
    position = data_block['Position']
    # Only process final positions (3, 6, 9)
    if position not in [3, 6, 9]:
        continue
    labware_str = 'final' + '_vol' + str(max_volume) + '_pos' + str(position)
    # Check if any well in the block contains a position-like pattern
    # this is because the final solution block repeat
    # skip_block = False
    for well, well_data in wells.items():
        solutions_str = well_data['Solution']
        volumes_str = well_data['Quantity']
        # Skip if no valid solutions or quantities
        if pd.isna(solutions_str) or pd.isna(volumes_str):
            continue
        # If the solution data matches the position pattern, mark block to be skipped
        if position_pattern.search(solutions_str):
            
            matching_pattern = re.compile(r'(\d+)\s+([A-H]\d)', re.IGNORECASE)
            matches = matching_pattern.findall(solutions_str)
            intermediate_position = int(matches[0][0])
            intermediate_well = matches[0][1]
            # from the labware position we can get the intermediate labware from intermediate_solutions
            # by matching the position
            intermediate_labware = None
            for intermediate_entry in intermediate_solutions:
                if intermediate_entry['container'].endswith(f'_pos{intermediate_position}'):
                    intermediate_labware = intermediate_entry['container']
                    break

            if intermediate_labware:
                intermediate_solution_reference = {
                    "final_container": labware_str,
                    "final_well": well,
                    "container": intermediate_labware,
                    "well": intermediate_well,
                    "volume": volumes_str
                }
            intermediate_solution_references.append(intermediate_solution_reference)
        else: # this is the case of a final block with the antisolvent prescription only
            # Iterate through wells to parse final solutions
            solutions_str = well_data['Solution']
            volumes_str = well_data['Quantity']
            # Skip if no valid solutions or quantities
            if pd.isna(solutions_str) or pd.isna(volumes_str):
                continue
            
            # Split solutions and volumes by commas
            solutions_list = [s.strip() for s in solutions_str.split(',')]
            # Handle cases where volumes_str is already an integer or is a string
            if isinstance(volumes_str, int):
                volumes_list = [volumes_str]  # Use directly as a list with one item
            else:
                volumes_list = [int(v.strip()) for v in volumes_str.split(',')]

            # Create the final solutions dictionary, assume first solution is antisolvent and the rest are ligands
            solutions_dict = {}
            solutions_dict["antisolvent"] = volumes_list[0]  # Assuming antisolvent is always the first
            ligand_idx = 1

            # Map the remaining solutions to ligand_2, ligand_3, etc.
            for solution, volume in zip(solutions_list[1:], volumes_list[1:]):
                solutions_dict[f"ligand_{ligand_idx}"] = volume
                ligand_idx += 1

            # solutions_dict["intermediate_solution"] = intermediate_solution_reference

            # Build the final entry for this well
            entry = {
                "container": labware_str,
                "positions": [well],
                "solutions": solutions_dict
            }

            # Add the entry to the final_solutions list
            final_solutions.append(entry)


# now we reprocess the final solutions to add the intermediate solutions
# according to the intermediate_solution_references, based on the final container 
# and the final well.
# Iterate through the intermediate_solution_references to update final solutions
for ref in intermediate_solution_references:
    final_container = ref["final_container"]
    final_well = ref["final_well"]
    intermediate_container = ref["container"]
    intermediate_well = ref["well"]
    volume = ref["volume"]

    # Find the corresponding final solution entry
    for final_entry in final_solutions:
        if final_entry["container"] == final_container and final_well in final_entry["positions"]:
            # Add the intermediate solution reference to the final entry
            if "intermediate_solution" not in final_entry:
                final_entry["solutions"]["intermediate_solution"] = []
            final_entry["solutions"]["intermediate_solution"].append({
                "container": intermediate_container,
                "well": intermediate_well,
                "volume": volume
            })



# Generate the multiline string representation for final_solutions
def final_list_to_multiline_string(lst, indent=0):
    result = []
    indent_str = ' ' * indent
    for entry in lst:
        result.append(f'{indent_str}{{"container": {entry["container"]}, "positions": {entry["positions"]}, "solutions": {{')
        for sol_name, vol in entry["solutions"].items():
            if isinstance(vol, list):  # Handle intermediate_solution references
                result.append(f'{indent_str}    "{sol_name}": ')
                for ref in vol:
                    result.append(f'{indent_str}        {{"container": {ref["container"]}, "well": "{ref["well"]}", "volume": {ref["volume"]}}}')
                # result.append(f'{indent_str}    ,')
            else:
                result.append(f'{indent_str}    "{sol_name}": {vol},')
        result.append(f'{indent_str}}}}},')
    return '\n'.join(result)

# Convert final_solutions list to a multiline string
final_solutions_str = "final_solutions = [\n" + final_list_to_multiline_string(final_solutions, indent=4) + "\n]"


# Display the generated multiline string
print('\n\n------- Final solutions ------- \n\n')
print(final_solutions_str)

def indent_multiline_string(multiline_str, indent_level=1):
    # Define the tab/space indentation
    indent = "     " * indent_level
    # Add indent to each line
    return "\n".join([indent + line if line.strip() else line for line in multiline_str.splitlines()])

# Indent these strings to match the code block level where they'll be inserted
labware_strs_multiline = indent_multiline_string(labware_strs_multiline, indent_level=1)
solution_nicknames_str = indent_multiline_string(solution_nicknames_str, indent_level=1)
initial_solutions_str = indent_multiline_string(initial_solutions_str, indent_level=1)
intermediate_solutions_str = indent_multiline_string(intermediate_solutions_str, indent_level=1)
final_solutions_str = indent_multiline_string(final_solutions_str, indent_level=1)

# Download the protocol file
filename_protocol = 'generated_protocol_v001.py'
# Function to generate a unique filename
def get_unique_filename(base_name):
    counter = 1
    unique_name = base_name
    while os.path.exists(unique_name):
        name, ext = os.path.splitext(base_name)
        unique_name = f"{name}_{counter}{ext}"
        counter += 1
    return unique_name

# Generate a unique filename
unique_filename_protocol = get_unique_filename(filename_protocol)

import urllib.request
version_script = 'v001'
url = f'https://raw.githubusercontent.com/rogeriog/Opentrons_LARP_protocol_generator/refs/heads/main/raw_protocol_scripts/raw_larp_script_{version_script}.py'
urllib.request.urlretrieve(url, filename_protocol)

# Open the downloaded file and read its content
with open(filename_protocol, 'r') as file:
    content = file.read()

# Replace the placeholders in the file with the corresponding multiline strings
content = content.replace('## LABWARE DEFINITIONS', labware_strs_multiline)
content = content.replace('## SOLUTION NICKNAMES', solution_nicknames_str)
content = content.replace('## INITIAL SOLUTIONS', initial_solutions_str)
content = content.replace('## INTERMEDIATE SOLUTIONS', intermediate_solutions_str)
content = content.replace('## FINAL SOLUTIONS', final_solutions_str)



# Write the modified content to the unique file
with open(unique_filename_protocol, 'w') as file:
    file.write(content)