import statistics

class UserInputCategorizer:
    def __init__(self, temperature, humidity, wind_speed, precipitation, fitness_level, members, time_range):
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.fitness_level = fitness_level
        self.members = members
        self.time_range = time_range
        self.group_type = None

    async def categorize_temperature(self):
        if self.temperature < 10.0:
            return "Cold"
        elif 10 <= self.temperature <= 25.0:
            return "Mild"
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
        ages = [member[1] for member in self.members]
        gender = [member[0] for member in self.members]
        gender_set = set(gender)
        print(gender_set)
        age_mean = statistics.mean(ages)
        age_stdev = statistics.stdev(ages) if len(ages) > 1 else 0

        age_categories = set()
        for age in ages:
            if age < age_mean - age_stdev:
                age_categories.add("Young")
            elif age_mean - age_stdev <= age <= age_mean + age_stdev:
                age_categories.add("Average")
            else:
                age_categories.add("Older")

        return self.group_type, age_categories

    async def categorize_time_range(self):
        try:
            minutes = int(self.time_range.split()[0])
        except ValueError:
            return "Invalid"

        if 0 <= minutes < 30:
            return "Short"
        elif 30 <= minutes < 90:
            return "Moderate"
        elif 90 <= minutes <= 120:
            return "Long"
        else:
            return "Extended"

    async def get_encoded_key(self):
        temp_category = await self.categorize_temperature()
        humidity_category = await self.categorize_humidity()
        wind_category = await self.categorize_wind_speed()
        precip_category = await self.categorize_precipitation()
        time_category = await self.categorize_time_range()
        group_type, age_categories = await self.encode_members()

        return (
            temp_category,
            humidity_category,
            wind_category,
            precip_category,
            group_type,
            age_categories,
            time_category,
        )

