import copy
from opentrons import protocol_api
import sys , pdb

### YOU SHOULD CHANGE TO FALSE BEFORE UPLOADING TO OPENTRONS!!
SIMULATE_MODE = True

if SIMULATE_MODE:
     import plotly.graph_objects as go
     import os

# metadata
metadata = {
    "protocolName": "Protocol for the synthesis of perovskite nanocrystals",
    "author": "Rogério",
    "description": """This protocol is intended for the synthesis of perovskite nanocrystals
    using the LARP method. The protocol is divided into the step of preparing the precursor+ligands
    solutions, and then the step of mixing the antisolvent with the precursor+ligands solutions.
    After configuring this script, you have to load the labware in the appropriate positions with the corresponding solutions in the precursor
    area, also the json files for the labware must have been uploaded into the opentrons app beforehand.
    The robot will do the rest.""",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.18"}

# protocol run function
def run(protocol: protocol_api.ProtocolContext):   

     
     # LABWARE SETTINGS (YOU PROBABLY WON'T NEED TO CHANGE THIS)
     tiprack = protocol.load_labware(
          "opentrons_96_tiprack_1000ul", location="11"
     )
     right_pipette = protocol.load_instrument(
        "p1000_single_gen2", mount="right", tip_racks=[tiprack]
     )
     MAX_VOLUME = 1000 # maximum volume the pipette can handle
     ## definir numero de antisolvent solutions por step para trocar a pipeta.
     
     ##### starting deck ##### YOU SHOULDN'T HAVE TO CHANGE THIS
     precursors_20_pos7 = protocol.load_labware("lamaiufrgscinza_12_tuberack_20000ul",  location='7')
     precursors_15_pos4 = protocol.load_labware("lamaiufrgsbranco_12_tuberack_15000ul",  location='4')
     precursor_reservoir_pos1 = protocol.load_labware("nest_1_reservoir_290ml",  location='1')
     # lamaiufrgsreservatoriotemp_1_reservoir_80000ul
     # precursor_reservoir_pos2 = protocol.load_labware("nest_1_reservoir_290ml",  location='2')

     intermediate_solutions_15_pos5 = protocol.load_labware("lamaiufrgsbranco_12_tuberack_15000ul",  location='5')

     resulting_solutions_20_pos9 = protocol.load_labware("lamaiufrgscinza_12_tuberack_20000ul",  location='9')
     resulting_solutions_5_pos6 = protocol.load_labware("lamaiufrgspreto24_24_tuberack_5000ul",  location='6')
     resulting_solutions_5_pos3 = protocol.load_labware("lamaiufrgspreto24_24_tuberack_5000ul",  location='3')


      ## colors available are: red, green, blue, yellow, magenta, cyan, brown, orange
     solution_colors = {  
     'precursor_solution_1': 'red',
     'precursor_solution_2': 'yellow',
     'precursor_solution_3': 'cyan',
     'precursor_solution_4': 'lime',
     'ligand_1' : 'magenta',
     'ligand_2' : 'green',
     'ligand_3' : 'pink',
     'ligand_4' : 'darkcyan',
     'reactant_1': 'brown',
     'reactant_2': 'orange',
     'reactant_3': 'purple',
     'antisolvent': 'blue',
     'antisolvent_2': 'golden',
     }
     
     solution_nicknames = {  ## modify accordingly
     'precursor_solution_1': 'Precursor 1',
     'precursor_solution_2': 'Precursor 2',
     'precursor_solution_3': 'Precursor 3',
     'precursor_solution_4': 'Precursor 4',
     'ligand_1' : 'Ligand 1',
     'ligand_2' : 'Ligand 2',
     'ligand_3' : 'Ligand 3',
     'ligand_4' : 'Ligand 4',
     'reactant_1': 'Reactant 1',
     'reactant_2': 'Reactant 2',
     'reactant_3': 'Reactant 3',
     'antisolvent': 'Antisolvent',
     'antisolvent_2': 'Antisolvent 2',
     'intermediate_solution': 'Intermediate Solution'
     }

     initial_solutions = {
          "precursor_solution_1": [
            {"container": precursors_20_pos7, "positions": ["A1", "B1", "C1", "A2", "B2", "C2"], 
             "volume": 15_000}
        ],
          "precursor_solution_2": [
            {"container": precursors_20_pos7, "positions": ["A3", "B3", "C3", "A4", "B4", "C4"], 
             "volume": 15_000}
        ],
          "ligand_1": [
            {"container": precursors_15_pos4, "positions": ["A1", "A2", "A3", "A4"], 
             "volume": 10_000}
        ],
          "ligand_2": [
            {"container": precursors_15_pos4, "positions": ["B1", "B2", "B3", "B4"], 
             "volume": 10_000}
        ],
          "antisolvent": [
            {"container": precursor_reservoir_pos1, "positions": ["A1"], 
             "volume": 290_000},
            {"container": precursors_15_pos4, "positions": ["C1", "C2", "C3", "C4"], 
             "volume": 10_000 },
        ]
     }

     intermediate_solutions = [ 
        {"container": intermediate_solutions_15_pos5, "positions": ["A1", "A2"], 
         "solutions": {
            "precursor_solution_1": 4_000,
            "precursor_solution_2": 4_000,
            "ligand_1": 50,
            "ligand_2": 50
            }},
        {"container": intermediate_solutions_15_pos5, "positions": ["A3", "A4"], 
         "solutions": {
            "precursor_solution_1": 4_000,
            "precursor_solution_2": 4_000,
            "ligand_1": 100,
            "ligand_2": 100
            }},
            {"container": intermediate_solutions_15_pos5, "positions": ["B1", "B2"], 
         "solutions": {
            "precursor_solution_1": 4_000,
            "precursor_solution_2": 4_000,
            "ligand_1": 150,
            "ligand_2": 150
            }},
        {"container": intermediate_solutions_15_pos5, "positions": ["B3", "B4"],
            "solutions": {
                "precursor_solution_1": 4_000,
                "precursor_solution_2": 4_000,
                "ligand_1": 200,
                "ligand_2": 200
                }},
        {"container": intermediate_solutions_15_pos5, "positions": ["C1", "C2"],
            "solutions": {
                "precursor_solution_1": 4_000,
                "precursor_solution_2": 4_000,
                "ligand_1": 250,
                "ligand_2": 250
                }},
        {"container": intermediate_solutions_15_pos5, "positions": ["C3", "C4"],
            "solutions": {
                "precursor_solution_1": 4_000,
                "precursor_solution_2": 4_000,
                "ligand_1": 300,
                "ligand_2": 300
                }}
        ]
     
     final_solutions = [
        {"container": resulting_solutions_5_pos6, "positions": ["A1", "A2", "A3", "A4", "A5", "A6"],
            "solutions": {
                "antisolvent": 1_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A1",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":1_000}
                }},
        {"container": resulting_solutions_5_pos6, "positions": ["B1", "B2", "B3", "B4", "B5", "B6"],
            "solutions": {
                "antisolvent": 2_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A2",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":1_000}
                }},
        {"container": resulting_solutions_5_pos6, "positions": ["C1", "C2", "C3", "C4", "C5", "C6"],
            "solutions": {
                "antisolvent": 3_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A2",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":1_000}
                }},
        {"container": resulting_solutions_5_pos6, "positions": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "solutions": {
                "antisolvent": 4_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A2",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":1_000}
                }},
        {"container": resulting_solutions_5_pos3, "positions": ["A1", "A2", "A3", "A4", "A5", "A6"],
            "solutions": {
                "antisolvent": 2_500,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A1",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":500}
                }},
        {"container": resulting_solutions_5_pos3, "positions": ["B1", "B2", "B3", "B4", "B5", "B6"],
            "solutions": {
                "antisolvent": 3_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A1",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":500}
                }},
        {"container": resulting_solutions_5_pos3, "positions": ["C1", "C2", "C3", "C4", "C5", "C6"],
            "solutions": {
                "antisolvent": 3_500,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A1",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":500}
                }},
        {"container": resulting_solutions_5_pos3, "positions": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "solutions": {
                "antisolvent": 4_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A1",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":500}
                }},
        {"container": resulting_solutions_20_pos9, "positions": ["A1", "A2", "A3", "A4", "B1", "B2"],
            "solutions": {
                "antisolvent": 9_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A1",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":1_000}
                }},
        {"container": resulting_solutions_20_pos9, "positions": ["B3", "B4", "C1", "C2", "C3", "C4"],
            "solutions": {
                "antisolvent": 10_000,
                "intermediate_solution": {"container": intermediate_solutions_15_pos5,
                                          "well": "A1",
                                          # "wells": ["A1", "A2"], ## depois implementar checar wells
                                          "volume":1_000}
                }}
    ]


     ### NOTHING TO CHANGE BELOW THIS LINE
     backup_final_solutions = [ {**solution} for solution in final_solutions ]
     starting_deck = {}
     for deck_slot in protocol.loaded_labwares:
          labware = protocol.loaded_labwares[deck_slot]
          print(f"Deck slot {deck_slot}: {labware}, {labware.load_name}")
          starting_deck[deck_slot] = {
               'name': labware.load_name,
               'well_volume': labware.wells()[0].max_volume,
               'position': deck_slot,
               'ordering': labware._core.get_definition()['ordering'],
          }
     print(starting_deck)

     redWater = protocol.define_liquid(
     name="red",
     description="Red colored water for demo",
     display_color="#FF0000",
     )
     greenWater = protocol.define_liquid(
          name="green",
          description="Green colored water for demo",
          display_color="#00FF00",
     )
     blueWater = protocol.define_liquid(
          name="blue",
          description="Blue colored water for demo",
          display_color="#0000FF",
     )
     yellowWater = protocol.define_liquid(
          name="yellow",
          description="Yellow colored water for demo",
          display_color="#FFFF00",
     )

     magentaWater = protocol.define_liquid(
          name="magenta",
          description="Magenta colored water for demo",
          display_color="#FF00FF",
     )

     cyanWater = protocol.define_liquid(
          name="cyan",
          description="Cyan colored water for demo",
          display_color="#00FFFF",
     )
     brownWater = protocol.define_liquid(
          name="brown",
          description="Brown colored water for demo",
          display_color="#A52A2A",
     )

     orangeWater = protocol.define_liquid(
     name="orange",
     description="Orange colored water for demo",
     display_color="#FFA500",
     )
     purpleWater = protocol.define_liquid(
     name="purple",
     description="Purple colored water for demo",
     display_color="#800080",
     )
     pinkWater = protocol.define_liquid(
     name="pink",
     description="Pink colored water for demo",
     display_color="#FFC0CB",
     )
     goldenWater = protocol.define_liquid(
     name="golden",
     description="Golden colored water for demo",
     display_color="#FFD700",
     )

     darkcyanWater = protocol.define_liquid(
     name="darkcyan",
     description="Dark Cyan colored water for demo",
     display_color="#008B8B",
     )

     limeWater = protocol.define_liquid(
     name="lime",
     description="Lime colored water for demo",
     display_color="#00FF00",
     )

     allWaters = [redWater, greenWater, blueWater, yellowWater, magentaWater, 
               cyanWater, brownWater, orangeWater, purpleWater, pinkWater, goldenWater, 
               darkcyanWater, limeWater]
     
     def get_liquid(color):
          for liquid in allWaters:
               if liquid.name == color:
                    return liquid
          return None

     starting_deck_total_vols = {}
     for solution_name, solution_data in initial_solutions.items():
          for data in solution_data:
               container = int(str(data["container"]._wells_by_name['A1']).split()[-1])
               positions = data["positions"]
               volume = data["volume"]
               for position in positions:
                    if container not in starting_deck:
                         starting_deck[container] = {}
                    if position not in starting_deck[container]:
                         starting_deck[container][position] = {"solutions": {}}
                    starting_deck[container][position]["solutions"][solution_name] = volume
                    ## summing up the total volume of each solution
                    if solution_name not in starting_deck_total_vols:
                         starting_deck_total_vols[solution_name] = 0
                    starting_deck_total_vols[solution_name] += volume

     # update liquid in each entry
     for solution_name, solution_data in initial_solutions.items():
          for data in solution_data:
               # add liquid to each entry according to the color
               liquid = get_liquid(solution_colors[solution_name])
               data['liquid'] = protocol.define_liquid(
                    name=solution_nicknames[solution_name],
                    description=liquid.description,
                    display_color=liquid.display_color,
               )

     ######################################################
     #############  GRAPHICAL DIAGNOSTIC ##################
     ######################################################
     if SIMULATE_MODE:
          print("Do you want to see a graphical diagnostic of the protocol? (y/n)")
          user_input_graph = input()
     else:
          user_input_graph = 'n'
     if user_input_graph == 'y':
          # make a copy of the starting deck
          intermediate_deck = copy.deepcopy(starting_deck)
          # clear all solutions from the intermediate deck
          for container in intermediate_deck:
               ordered_list_of_positions = intermediate_deck[container]['ordering']
               list_of_wells = [item for sublist in ordered_list_of_positions for item in sublist]
               keys = list(intermediate_deck[container].keys())
               for key in keys:
                    if key in list_of_wells:
                         del intermediate_deck[container][key]
          
          # pdb.set_trace()
          intermediate_total_vols = {}
          for solution in intermediate_solutions:
               container = int(str(solution["container"]._wells_by_name['A1']).split()[-1])
               positions = solution["positions"]
               solutions = solution["solutions"]
               for position in positions:
                    if container not in intermediate_deck:
                         intermediate_deck[container] = {}
                    if position not in intermediate_deck[container]:
                         intermediate_deck[container][position] = {"solutions": {}}
                    intermediate_deck[container][position]["solutions"] = solutions
                    ## summing up the total volume of each solution
                    for solution in solutions:
                         if solution not in intermediate_total_vols:
                              intermediate_total_vols[solution] = 0
                         intermediate_total_vols[solution] += solutions[solution]

          
          # we need to set the antisolvent solutions in the intermediate deck too
          for solution in final_solutions:
               container = int(str(solution["container"]._wells_by_name['A1']).split()[-1])
               positions = solution["positions"]
               # pdb.set_trace()
               for solution_type in solution["solutions"]:
                    if solution_type == 'intermediate_solution':
                         continue
                    if container not in intermediate_deck:
                         intermediate_deck[container] = {}
                    for position in positions:
                         if position not in intermediate_deck[container]:
                              intermediate_deck[container][position] = {"solutions": {}}
                         intermediate_deck[container][position]["solutions"][solution_type] = solution["solutions"][solution_type]
                         ## summing up the total volume of each solution
                         if solution_type not in intermediate_total_vols:
                              intermediate_total_vols[solution_type] = 0
                         intermediate_total_vols[solution_type] += solution["solutions"][solution_type]
          
          # pdb.set_trace()
          # check keys in intermediate deck
          for key in intermediate_deck:
               # check if the subkeys contain solutions
               for subkey in intermediate_deck[key]:
                    if isinstance(intermediate_deck[key][subkey], dict):
                         if 'solutions' in intermediate_deck[key][subkey]:
                              solutions = intermediate_deck[key][subkey]['solutions']
                              total_vol = 0
                              for sol in solutions:
                                   total_vol += solutions[sol]
                              print(f"Total volume in container {key} position {subkey}: {total_vol}")

          # make a copy of the starting deck
          final_deck = copy.deepcopy(starting_deck)
          # clear all solutions from the intermediate deck
          for container in final_deck:
               ordered_list_of_positions = final_deck[container]['ordering']
               list_of_wells = [item for sublist in ordered_list_of_positions for item in sublist]
               keys = list(final_deck[container].keys())
               for key in keys:
                    if key in list_of_wells:
                         del final_deck[container][key]
          # now we set the final solutions in the final deck
          # final_solutions_copy = copy.deepcopy(final_solutions)
          final_total_vols = {"intermediate_solution": 0}
          for solution in final_solutions:
               container = int(str(solution["container"]._wells_by_name['A1']).split()[-1])
               positions = solution["positions"]
               solutions = solution["solutions"]
               for position in positions:
                    if container not in final_deck:
                         final_deck[container] = {}
                    if position not in final_deck[container]:
                         final_deck[container][position] = {"solutions": {}}
                    final_deck[container][position]["solutions"] = solutions
                    ## we sum the total volume of each solution
                    for solution in solutions:
                         if solution != 'intermediate_solution':
                              if solution not in final_total_vols:
                                   final_total_vols[solution] = 0
                              final_total_vols[solution] += solutions[solution]                  

                    ### now we need to set the actual intermediate solution in the final deck
                    ### notice that it will repeat for the other positions
                    if isinstance(final_deck[container][position]["solutions"]["intermediate_solution"], dict):
                         intermediate_sol_origin = final_deck[container][position]["solutions"]["intermediate_solution"]
                         intermediate_sol_container = intermediate_sol_origin["container"]
                         intermediate_sol_well = intermediate_sol_origin["well"]
                         intermediate_sol_vol = intermediate_sol_origin["volume"]
                         ### sum the total volume of intermediate solution
                         final_total_vols["intermediate_solution"] += intermediate_sol_vol
                         ###
                         intermediate_sol_slot = int(str(intermediate_sol_container._wells_by_name[intermediate_sol_well]).split()[-1])
                         intermediate_solution = intermediate_deck[intermediate_sol_slot][intermediate_sol_well] 
                         # sum volumes in intermediate solution
                         total_vol = 0
                         for sol in intermediate_solution["solutions"]:
                              total_vol += intermediate_solution["solutions"][sol]
                         vol_frac = intermediate_sol_vol / total_vol
                         for sol in intermediate_solution["solutions"]:
                              final_deck[container][position]["solutions"][sol] = intermediate_solution["solutions"][sol] * vol_frac
          # pdb.set_trace()


          def set_deck_from_dict(number, deck, deck_params):
               if not isinstance(deck, dict):
                    print(f"Error: Expected a dictionary for deck, but got {type(deck).__name__}")
                    return None
               labware = deck.get(number, None)
               # pdb.set_trace()
               if labware is not None:
                    # get rows and columns from ordering
                    inner_rect_width = deck_params['subdivision_width_x'] / 1.2
                    inner_rect_height = deck_params['subdivision_width_y'] / 1.2
                    inner_x0 = deck_params['x0'] + (deck_params['subdivision_width_x'] - inner_rect_width) / 2
                    inner_y0 = deck_params['y0'] + (deck_params['subdivision_width_y'] - inner_rect_height) / 2
                    inner_x1 = inner_x0 + inner_rect_width
                    inner_y1 = inner_y0 + inner_rect_height
                    fig.add_shape(
                         type="rect",
                         x0=inner_x0,
                         y0=inner_y0,
                         x1=inner_x1,
                         y1=inner_y1,
                         line=dict(color="Black", width=2),
                         fillcolor="White"
                    )
                    # Add circles in a grid in the labware corresponding to the wells
                    n_rows = len(labware['ordering'][0])
                    n_cols = len(labware['ordering'])
                    for k in range(n_cols):
                         for l in range(n_rows):
                              get_index = labware['ordering'][k][l]
                              circle_x = inner_x0 + (k + 0.5) * (inner_rect_width / n_cols)
                              circle_y = inner_y1 - (l + 0.5) * (inner_rect_height / n_rows)
                              ## draw circles for wells
                              fig.add_shape(
                                   type="circle",
                                   x0=circle_x - 1,
                                   y0=circle_y - 1,
                                   x1=circle_x + 1,
                                   y1=circle_y + 1,
                                   line=dict(color="Black", width=2),
                                   fillcolor="White",
                                   opacity=0.5)
                              
                              ## add solutions to the circles as other circles
                              if get_index in labware:
                                   # get keys
                                   solutions = labware[get_index]['solutions']
                                   hover_text = ''
                                   for key in solutions:
                                        # round to decimals and add to hover text
                                        if key != 'intermediate_solution':
                                             hover_text += solution_nicknames[key] + ': ' + str(round(solutions[key], 2)) + '<br>'
                                        else: # make it red
                                             hover_text += '~~' + solution_nicknames[key] + ': ' + str(round(solutions[key]['volume'], 2)) + '~~<br>'
                                   for solution in solutions:
                                        if solution == 'intermediate_solution':
                                             continue
                                        # pdb.set_trace()
                                        radius = solutions[solution] / (labware['well_volume'] * 0.8)
                                        fig.add_shape(
                                             type="circle",
                                             x0=circle_x - radius,
                                             y0=circle_y - radius,
                                             x1=circle_x + radius,
                                             y1=circle_y + radius,
                                             line=dict(color="Black", width=0.1),
                                             fillcolor=solution_colors[solution],
                                             opacity=0.5)
                              else:
                                   hover_text = ''
                              fig.add_annotation(
                                   x=circle_x,
                                   y=circle_y,
                                   text='O',
                                   showarrow=False,
                                   font=dict(size=25, color="white"),
                                   opacity=0.0,
                                   hovertext=hover_text
                              )

          ##############################################################
          # Create a blank figure
          fig = go.Figure()

          # Define the dimensions of the main rectangle
          main_rectangle_width = 63
          main_rectangle_height = 57

          # Number of subdivisions
          subdivisions_x = 3
          subdivisions_y = 4

          # Calculate the width of each subdivision
          subdivision_width_x = main_rectangle_width / subdivisions_x
          subdivision_width_y = main_rectangle_height / subdivisions_y

          # Number of copies
          num_stages = 3

          # Create the subdivisions for each copy
          for n_stage in range(num_stages):
               number = 1
               x_offset = n_stage * (main_rectangle_width + 5)  # Shift each copy horizontally
               
               # Add big centralized text above each large rectangle area
               stages = ['Precursor + Ligands', 'Intermediate', 'Final']
               fig.add_annotation(
                    x=x_offset + main_rectangle_width / 2,
                    y=main_rectangle_height + 2,
                    text=f"{stages[n_stage]}",
                    showarrow=False,
                    font=dict(size=18, color="black")
               )

               # now for each deck I want to have a summary of the 
               # total quantity of each solution in the deck
               if n_stage == 0:
                    total_vols = starting_deck_total_vols
               elif n_stage == 1:
                    total_vols = intermediate_total_vols
               else:
                    total_vols = final_total_vols
               
               # create annotation for total volumes below the deck image
               for solution, volume in total_vols.items():
                    fig.add_annotation(
                         x=x_offset + main_rectangle_width / 2,
                         y= -2 - 2 * (list(total_vols.keys()).index(solution)),
                         text=f"{solution_nicknames[solution]}: {volume} uL",
                         # text=f"{solution}: {volume} uL",
                         showarrow=False,
                         font=dict(size=12, color="black")
                    )

               
               for j in range(subdivisions_y):
                    for i in range(subdivisions_x):
                         # Define the coordinates of the current subdivision
                         x0 = x_offset + i * subdivision_width_x
                         y0 = j * subdivision_width_y
                         x1 = x_offset + (i + 1) * subdivision_width_x
                         y1 = (j + 1) * subdivision_width_y
                         deck_params = {'x0': x0, 'y0': y0, 'subdivision_width_x': subdivision_width_x, 'subdivision_width_y': subdivision_width_y}

                         if n_stage == 0:
                              if number in [1,4,7]:
                                   fillcolor = "LightBlue"
                              else:
                                   fillcolor = "Grey"
                         elif n_stage == 1:
                              if number in [2,5,8,3,6,9]:
                                   fillcolor = "LightBlue"
                              else:
                                   fillcolor = "Grey"
                         else:
                              if number in [3,6,9]:
                                   fillcolor = "LightBlue"
                              else:
                                   fillcolor = "Grey"
                         # Create the rectangle
                         fig.add_shape(
                              type="rect",
                              x0=x0,
                              y0=y0,
                              x1=x1,
                              y1=y1,
                              line=dict(color="Grey", width=1),
                              fillcolor=fillcolor if number != 12 else "Black"
                         )

                         # Add the number annotation
                         fig.add_annotation(
                              x=(x0 + x1) / 2,
                              y=(y0 + y1) / 2,
                              text=str(number),
                              showarrow=False,
                              font=dict(size=16, color="black")
                         )

                         # Add labware to the subdivisions
                         # Assume set_deck_from_dict is defined elsewhere in the code
                         if n_stage == 0:
                              set_deck_from_dict(number, starting_deck, deck_params)
                         elif n_stage == 1:
                              set_deck_from_dict(number, intermediate_deck, deck_params)
                         else:
                              set_deck_from_dict(number, final_deck, deck_params)

                         number += 1

          # Set the layout of the figure
          fig.update_layout(
          margin=dict(l=20, r=20, t=40, b=40),
          title="Three Stages of the Synthesis of Perovskite Nanocrystals",
          xaxis=dict(range=[0, main_rectangle_width * num_stages + 10], zeroline=False),
          yaxis=dict(range=[-8, main_rectangle_height-0.5], scaleanchor="x", scaleratio=1, zeroline=False),
          showlegend=False
          )
          # Hide x and y axis
          fig.update_xaxes(visible=False)
          fig.update_yaxes(visible=False)
          # Show the figure
          # prefix from script filename
          prefix = sys.argv[1].split(".")[0]
          fig.write_html(f"{prefix}_interactive_plot.html")
          fig.show()
          ############### END OF GRAPHICAL DIAGNOSTIC ##################
          ##############################################################
     # continue for the rest of the protocol
     if SIMULATE_MODE:
          print("Do you want to continue with the protocol? (y/n)")
          user_input_simulate = input()
     else:
          user_input_simulate = 'y'
     if user_input_simulate != 'y':
          sys.exit(0)
     else:
          print("Running protocol...")
          # Initialize the liquid in each container
          for solution_type, details in initial_solutions.items():
               for entry in details:
                    container = entry["container"]
                    positions = entry["positions"]
                    volume = entry["volume"]
                    liquid = entry["liquid"]
                    for position in positions:
                         # Load the liquid into the corresponding container and position
                         container[position].load_liquid(liquid=liquid, volume=volume)
                         container[position].liquid = [liquid]  ## there should exist by default but i couldnt find.
                         container[position].volume = volume 
                         # import pdb; pdb.set_trace()
                    print(f"Loaded {liquid.name} corresponding to {solution_type} into {container} positions {positions} with volume {volume}")
          # PARAMETERS AND BASE FUNCTIONS FOR THE PROTOCOL
          ## default speed is 400
          right_pipette.default_speed = 300  ## moves way slower, good to check protocol
          def update_liquid(src, dest, volume):
               if hasattr(dest,"liquid") :
                    # if all src.liquid item is in dest liquid
                    if all(item in dest.liquid for item in src.liquid):
                         pass
                    else:
                         # add liquids that are not in dest.liquid
                         for item in src.liquid:
                              if item not in dest.liquid:
                                   dest.liquid.append(item)   
               else:
                    dest.liquid = src.liquid
                    dest.volume = 0
               
               print(f"Destination liquid: {[liquid.name for liquid in dest.liquid]}")
               src.volume -= volume
               dest.volume += volume

          def transfer(volume, src, dest, dispense_from_center=False):
               right_pipette.aspirate(volume, 
                                   src.bottom(z=2), ## 2 mm acima do fundo 
                                   rate=1.0)
               right_pipette.move_to(src.top(z=-1))
               protocol.delay(seconds=3)
               right_pipette.touch_tip(src,
                              radius=0.96,
                              v_offset=-1.5, # 1mm abaixo do topo
                              speed=200) # mais rapido para eliminar droplets
               if dispense_from_center:
                    right_pipette.dispense(volume, 
                                   dest.center(), 
                                   rate=2)
               else:
                    right_pipette.dispense(volume, 
                                        dest.top(z=1), # 1mm acima do topo
                                        rate=2)
               right_pipette.touch_tip(dest,
                              radius=0.96,
                              v_offset=-1.5, # 1mm abaixo do topo
                              speed=200) # mais rapido para eliminar droplets
               update_liquid(src, dest, volume)

          def mix(target, volume=MAX_VOLUME, repetitions=3):
               for _ in range(repetitions):
                    right_pipette.aspirate(volume, target.bottom(z=2), ## 2 mm acima do fundo 
                                        rate=1.0)
                    right_pipette.dispense(volume, target.top(z=1), # 1mm acima do topo
                                        rate=3.65)
                    right_pipette.blow_out(target.top(z=1))

          def composed_transfer(volume, src, dest, MAX_VOLUME=MAX_VOLUME):
               # repeat transfer until volume is completely transferred
               while volume > 0:
                    # calculate the volume to transfer in this step
                    transfer_volume = min(volume, MAX_VOLUME)
                    # transfer the volume from the src to each destination
                    transfer(transfer_volume, src, dest)
                    # update the remaining volume
                    volume -= transfer_volume
          def select_source(solution_type, volume):
               source_details = initial_solutions[solution_type]
               for entry in source_details:
                    source_container = entry["container"]
                    source_positions = entry["positions"]
                    for source_position in source_positions:
                         if source_container[source_position].volume >= volume:
                              return source_container[source_position]
               print(f"No source found for {solution_type} with volume {volume}")
               sys.exit(1)

          DISPOSAL_ORDER = ['precursor_solution_1', 'precursor_solution_2', 'precursor_solution_3', 'precursor_solution_4',
                            'ligand_1', 'ligand_2', 'ligand_3', 'ligand_4', 'reactant_1', 'reactant_2', 'reactant_3',
                            'antisolvent', 'antisolvent_2']
          # Perform composed transfers from precursor solutions to intermediate solutions
          for disposing_type in DISPOSAL_ORDER:
               if disposing_type not in initial_solutions:
                    continue
               right_pipette.pick_up_tip()
               IS_WET = False
               source_details = initial_solutions[disposing_type]
               for intermediate in intermediate_solutions:
                    container = intermediate["container"]
                    positions = intermediate["positions"]
                    solutions = intermediate["solutions"]
                    if disposing_type in solutions:
                         volume = solutions[disposing_type]
                    else:
                         continue
                    for position in positions:
                         for entry in source_details:
                              TRANSFER_DONE = False
                              source_container = entry["container"]
                              source_positions = entry["positions"]
                              for source_position in source_positions:
                              # check if source_position contains enough solution
                                   if source_container[source_position].volume < volume:
                                        print(f"Skipping transfer from {source_container[source_position]} to {container[position]}")
                                        continue
                                   else:
                                        if not IS_WET: ## wets tip
                                             mix(source_container[source_position],repetitions=1)
                                             IS_WET = True
                                        composed_transfer(volume, source_container[source_position], container[position])
                                        print(f"Transferred {volume} from {source_container[source_position]} to {container[position]}")
                                        TRANSFER_DONE = True
                                        break # if transfer was successful, not necessary to check other source positions
                              if TRANSFER_DONE:
                                   break # if transfer was successful, not necessary to check other source entries
                         if not TRANSFER_DONE:
                              print(f"Could not transfer {volume} from {disposing_type} to {container[position]}")
                              print(f"There is an error in protocol, please check the volumes and positions.")
                              sys.exit(1)
               right_pipette.drop_tip()
          # now I want to print for each intermediate solution the volume of each liquid
          print('-------------------------HEALTH CHECK-----------------------------')
          for intermediate in intermediate_solutions:
               container = intermediate["container"]
               positions = intermediate["positions"]
               solutions = intermediate["solutions"]
               for position in positions:
                    print(f"Intermediate solution at {container[position]}")
                    for solution_type, volume in solutions.items():
                         print(f"Volume of {solution_type}: {volume}")
          print('-----------------THESE SHOULD BE THE FINAL VOLUMES----------------')

          # now i want to fill the resulting solutions with antisolvent
          # I should read the antisolvent_solutions and transfer the antisolvent volume
          # corresponding to each resulting solution
          for antisolvent_solution in backup_final_solutions:
               # pdb.set_trace()
               container = antisolvent_solution["container"]
               positions = antisolvent_solution["positions"]
               solutions = antisolvent_solution["solutions"]

               for solution_type, volume in solutions.items():
                    if solution_type == "antisolvent":
                         right_pipette.pick_up_tip()
                    for position in positions:
                         if solution_type == "antisolvent":
                              selected_source = select_source(solution_type, volume)
                              composed_transfer(volume, selected_source, container[position])
                              print(f"Transferred {volume} of antisolvent to {container[position]} from {source_container[source_position]}")
                         elif solution_type == 'intermediate_solution':
                              right_pipette.pick_up_tip()
                              intermediate_container = solutions[solution_type]["container"]
                              intermediate_well = solutions[solution_type]["well"]
                              intermediate_volume = solutions[solution_type]["volume"]
                              composed_transfer(intermediate_volume, container[position], intermediate_container[intermediate_well])
                              print(f"Transferred {intermediate_volume} of intermediate solution {intermediate_container[intermediate_well]} to {container[position]} ")
                              right_pipette.drop_tip()
                         else:
                              pass
                              # just ignore
                    if solution_type == "antisolvent":
                         right_pipette.drop_tip()
          # now I want to print for each intermediate solution the volume of each liquid
          print('-------------------------HEALTH CHECK-----------------------------')
          for anti_solution in final_solutions:
               container = anti_solution["container"]
               positions = anti_solution["positions"]
               solutions = anti_solution["solutions"]
               for position in positions:
                    print(f"Resulting solution at {container[position]}")
                    for solution_type, volume in solutions.items():
                         print(f"Volume of {solution_type}: {volume}")