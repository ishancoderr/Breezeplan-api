import statistics


class UserInputCategorizer:
    def __init__(self, temperature, humidity, wind_speed, precipitation, time_range, members):
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.time_range = time_range
        self.members = members
        self.time_range = time_range
        self.group_type = None
        '''
    async def categorize_calories(self):
        if self.calories < 1000:
            return "Low"
        elif 1000 <= self.calories <= 2000:
            return "Moderate"
        else:
            return "High"
        '''
    async def categorize_temperature(self):
        if self.temperature < 10.0:
            return "Cold"
        elif 10 <= self.temperature < 20.0:
            return "Mild"
        elif 20 <= self.temperature < 30.0:
            return "Warm"
        else:
            return "Hot"

    async def categorize_humidity(self):
        if self.humidity < 30.0:
            return "Low"
        elif 30 <= self.humidity <= 60.0:
            return "Moderate"
        else:
            return "High"

    async def categorize_wind_speed(self):
        if self.wind_speed < 5.0:
            return "Calm"
        elif 5 <= self.wind_speed <= 15.0:
            return "Breezy"
        else:
            return "Windy"

    async def categorize_precipitation(self):
        if self.precipitation == 0.0:
            return "No Precipitation"
        elif self.precipitation < 10.0:
            return "Light Rain"
        else:
            return "Heavy Rain"

    async def encode_members(self):
        num_members = len(self.members)
        if num_members == 1:
            self.group_type = "Single"
        elif num_members == 2:
            self.group_type = "Couple"
        elif 3 <= num_members <= 5:
            self.group_type = "Small Group"
        else:
            self.group_type = "Large Group"

        # Calculate age categories
        print('members', self.members)
        gender = [member[0] for member in self.members]
        ages = [member[1] for member in self.members]
        fitness_level = [member[2] for member in self.members]
            # Determine the lowest fitness level
        fitness_priority = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
        lowest_fitness_level = min(fitness_level, key=lambda level: fitness_priority.get(level, float("inf")))
        mode_fitness_level = statistics.mode(fitness_level)

        age_categories = set()

        for age in ages:
            if age < 12:
                age_categories.add("Child")
            elif 13 <= age <= 18:
                age_categories.add("Teen")
            elif 19 <= age <= 29:
                age_categories.add("Young Adult")
            elif 30 <= age <= 55:
                age_categories.add("Adult")
            else:
                age_categories.add("Senior")
        
        age_categories = sorted(age_categories)

        male_max_age = max((member[1] for member in self.members if member[0] == 'male'), default=None)
        female_max_age = max((member[1] for member in self.members if member[0] == 'female'), default=None)

        if male_max_age is not None and female_max_age is not None:
            if female_max_age > male_max_age:
                dominant_gender = "Female"
                dominant_age = female_max_age
            else:
                dominant_gender = "Male"
                dominant_age = male_max_age
        elif male_max_age is not None:
            dominant_gender = "Male"
            dominant_age = male_max_age
        elif female_max_age is not None:
            dominant_gender = "Female"
            dominant_age = female_max_age
        else:
            dominant_gender = "Unknown"
            dominant_age = None

        if dominant_age is not None:
            if dominant_age <= 12:
                dominant_age_group = "Child"
            elif 13 <= dominant_age <= 17:
                dominant_age_group = "Teen"
            elif 18 <= dominant_age <= 29:
                dominant_age_group = "Young Adult"
            elif 30 <= dominant_age <= 45:
                dominant_age_group = "Adult"
            elif 46 <= dominant_age <= 65:
                dominant_age_group = "Middle Aged"
            else:
                dominant_age_group = "Senior"
        else:
            dominant_age_group = "Unknown"

        return self.group_type, dominant_age_group , age_categories, dominant_gender, lowest_fitness_level, mode_fitness_level

    async def categorize_time_range(self):
        try:
            # Handle cases where time_range is an integer
            if isinstance(self.time_range, int):
                minutes = self.time_range
            elif isinstance(self.time_range, str):
                minutes = int(self.time_range.split()[0])
            else:
                return "Invalid"

            if 0 <= minutes < 30:
                return "Short"
            elif 30 <= minutes < 90:
                return "Moderate"
            elif 90 <= minutes <= 120:
                return "Long"
            else:
                return "Extended"
        except (ValueError, AttributeError):
            return "Invalid"

    async def get_encoded_key(self):
        temp_category = await self.categorize_temperature()
        humidity_category = await self.categorize_humidity()
        wind_category = await self.categorize_wind_speed()
        precip_category = await self.categorize_precipitation()
        time_category = await self.categorize_time_range()
        group_type, dominant_age_group, age_categories, dominant_gender, lowest_fitness_level, mode_fitness_level = await self.encode_members()
        #calorie_category = await self.categorize_calories()

        return (
            temp_category,
            humidity_category,
            wind_category,
            precip_category,
            time_category,
            group_type,
            dominant_age_group,
            age_categories,
            dominant_gender,
            lowest_fitness_level,
            mode_fitness_level
            #calorie_category
        )

