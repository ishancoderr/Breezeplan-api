import os
import json
from fastapi import HTTPException

class CategorizeFileRetriever:
    def __init__(self, data):
        self.data = data
              
    async def categorize_files(self):
        q_table_file = os.path.join(os.path.dirname(__file__), "../testData/q_table.json")
        try:
            with open(q_table_file, "r") as file:
                q_table = json.load(file)
                print(q_table)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Q-table file not found.")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Failed to decode Q-table JSON file.")
