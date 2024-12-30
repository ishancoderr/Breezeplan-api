import json

class DataSaveService:
    def __init__(self, data, group_size, dominant_gender):
        # Initialize the data, group_size, and dominant_gender
        self.data = data
        self.group_size = group_size
        self.dominant_gender = dominant_gender

    async def create_file_if_not_exists(self, file_name):
        """Check if the file exists; if not, create it with an empty structure."""
        try:
            with open(file_name, "r") as file:
                return
        except FileNotFoundError:
            with open(file_name, "w") as file:
                json.dump({}, file, indent=4)
            print(f"File '{file_name}' was created with an empty structure.")

    def convert_sets_to_lists(self, obj):
        """Recursively convert any sets in the object to lists."""
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, tuple):
            return tuple(self.convert_sets_to_lists(item) for item in obj)
        elif isinstance(obj, dict):
            return {key: self.convert_sets_to_lists(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_sets_to_lists(item) for item in obj]
        return obj

    async def save_to_json(self):
        print('Saving data to JSON...')
        
        # Convert sets in self.data to lists
        converted_data = self.convert_sets_to_lists(self.data)
        
        # Prepare the output data with the converted self.data
        output_data = {
            "9f6c6632f46f9f993eeffb7e366d4a92": {
                "key": converted_data,  # Use converted self.data here
                "values": {
                    "Jogging": 0.1,
                    "Cycling": 0,
                    "Outdoor Yoga": 0,
                    "Hiking": 0
                }
            }
        }

        # Mapping group size and dominant gender to specific file names
        file_name_map = {
            ("Single", "Male"): "single_male.json",
            ("Single", "Female"): "single_female.json",
            ("Couple", "Male"): "couple_male.json",
            ("Couple", "Female"): "couple_female.json",
            ("Small Group", "Male"): "small_group_male.json",
            ("Small Group", "Female"): "small_group_female.json",
            ("Large Group", "Male"): "large_group_male.json",
            ("Large Group", "Female"): "large_group_female.json",
        }
        
        # Determine the appropriate file based on group size and dominant gender
        file_key = (self.group_size, self.dominant_gender)
        file_name = file_name_map.get(file_key, "default.json")
        
        # Ensure the file exists, create it if not
        await self.create_file_if_not_exists(file_name)
        
        try:
            with open(file_name, "r") as file:
                existing_data = json.load(file)
        except Exception as e:
            print(f"Error reading file: {e}")
            existing_data = {}
        
        # Convert any sets in existing data to lists
        existing_data = self.convert_sets_to_lists(existing_data)
        
        # Add the hardcoded output data to the existing data
        existing_data.update(output_data)
        
        # Save the updated data back to the file
        with open(file_name, "w") as file:
            json.dump(existing_data, file, indent=4)
        
        print(f"Data saved to {file_name}")