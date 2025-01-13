import json
import random
import time
import os


class ReinforcementLearningAgent:
    def __init__(self):
        pass

    async def update_q_value(self, selected_names, out_hash, file_path):  # No 'self'
        print('selected names', selected_names)
        try:
            with open(file_path, 'r') as file:
                tables = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}.")
        
        if out_hash not in tables:
            raise KeyError(f"Hash {out_hash} not found in {file_path}")
        
        for name in selected_names:
            if name in tables[out_hash]["values"]:
                tables[out_hash]["values"][name] -= 1  
        
        # Write the updated JSON back to the file synchronously
        with open(file_path, 'w') as file:
            json.dump(tables, file, indent=4)
        
        print(f"Updated Q-values in {file_path}")    

    
