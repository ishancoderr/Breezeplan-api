import json
import hashlib
import os

class DataSaveService:
    def __init__(self, data, group_size, tem, time_range):
        # Initialize the data, group_size, and temperature
        self.data = data
        self.group_size = group_size
        self.tem = tem
        self.time_range = time_range

    async def create_file_if_not_exists(self, folder_name, file_name):
        """Check if the file exists; if not, create it with an empty structure."""
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                print(f"Folder '{folder_name}' was created.")
            
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, "r") as file:
                return
        except FileNotFoundError:
            with open(file_path, "w") as file:
                json.dump({}, file, indent=4)
            print(f"File '{file_name}' was created in folder '{folder_name}' with an empty structure.")

    async def convert_sets_to_lists(self, obj):
        """Recursively convert any sets in the object to lists."""
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, tuple):
            return tuple([await self.convert_sets_to_lists(item) if isinstance(item, set) else item for item in obj])
        elif isinstance(obj, dict):
            return {key: await self.convert_sets_to_lists(value) if isinstance(value, (set, list, tuple, dict)) else value for key, value in obj.items()}
        elif isinstance(obj, list):
            return [await self.convert_sets_to_lists(item) if isinstance(item, (set, list, tuple, dict)) else item for item in obj]
        return obj
        
    async  def fetch_activity_values(self, activity_file):
        """Fetch activity data from a JSON file and calculate values dynamically."""
        try:
            with open(f"outdoor_activity_data/{activity_file}", "r") as file:
                activities = json.load(file)

            activity_values = {activity["activity"]:0 for activity in activities}

            return activity_values
        except Exception as e:
            print(f"Error reading activities file: {e}")
            return {}
        
    async def write_to_json_file(self, folder_name, file_name, output_data):
        """Write the output_data to the specified JSON file."""
        file_path = os.path.join(folder_name, file_name)
        try:
            # Load existing data
            with open(file_path, "r") as file:
                existing_data = json.load(file)
            
            # Update or append the new data
            existing_data.update(output_data)

            # Write updated data back to the file
            with open(file_path, "w") as file:
                json.dump(existing_data, file, indent=4)
            
            print(f"Data written successfully to '{file_name}'.")
        except Exception as e:
            print(f"Error writing to file '{file_name}': {e}")


    async def save_to_json(self):
        print('Saving data to JSON...')
        
        converted_data = await self.convert_sets_to_lists(self.data)

        # Get the filenames based on group size , time range and temperature
        file_name = await self.get_file_name(self.group_size, self.tem, self.time_range)
        outdoor_activity_file_name = await self.get_outdoor_activity_file_name(self.group_size, self.tem, self.time_range)

        await self.create_file_if_not_exists("data", file_name)
        await self.create_file_if_not_exists("outdoor_activity_data", outdoor_activity_file_name)

        activity_values = await self.fetch_activity_values(outdoor_activity_file_name)
        
        hash_key = hashlib.md5(json.dumps(converted_data, sort_keys=True).encode()).hexdigest()
        print('hash_key', hash_key)

        output_data = {
            hash_key: {
                "key": converted_data,
                "values": activity_values
            }
        }
    
        await self.write_to_json_file("data", file_name, output_data)

    async def get_file_name(self, group_size, temperature, time_range):
        file_name_map = {
            (g, t, r): f"{g.lower().replace(' ', '_')}_{t.lower()}_{r.lower()}.json"
            for g in ["Single", "Couple", "Small Group", "Large Group"]
            for t in ["Cold", "Mild", "Warm", "Hot"]
            for r in ["Short", "Moderate", "Long", "Extended"]
        }
        return file_name_map.get((group_size, temperature, time_range), "default.json")

    async def get_outdoor_activity_file_name(self, group_size, temperature, time_range):
        outdoor_activity_file_name_map = {
            (g, t, r): f"outdoor_activity_{g.lower().replace(' ', '_')}_{t.lower()}_{r.lower()}.json"
            for g in ["Single", "Couple", "Small Group", "Large Group"]
            for t in ["Cold", "Mild", "Warm", "Hot"]
            for r in ["Short", "Moderate", "Long", "Extended"]
        }
        return outdoor_activity_file_name_map.get((group_size, temperature, time_range), "outdoor_activity_default.json")

    async def output_hash(self):
        converted_data = await self.convert_sets_to_lists(self.data)
        hash_key = hashlib.md5(json.dumps(converted_data, sort_keys=True).encode()).hexdigest()
        return hash_key
