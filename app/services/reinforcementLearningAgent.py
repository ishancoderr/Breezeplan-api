import json
import random
import time
import os


class ReinforcementLearningAgent:
    def __init__(self, actions):
        self.actions = actions
        self.q_table = {} 
        self.alpha = 0.1 
        self.gamma = 0.9 
        self.epsilon = 0.2 
        self.q_table_file = os.path.join(os.path.dirname(__file__), "../testData/q_table.json")

    def encode_state(self, state):
        return tuple(state.values())

    def choose_action(self, state):
        encoded_state = self.encode_state(state)
        print(f"Encoded State: {encoded_state}")

        # Choose an action
        if random.uniform(0, 1) < self.epsilon:
            chosen_action = random.choice(self.actions)  # Exploration
        else:
            chosen_action = max(
                self.q_table.get(encoded_state, {}),
                key=self.q_table.get(encoded_state, {}).get,
                default=random.choice(self.actions)  # Exploitation fallback
            )
            filename = "reinforcementData.json"
            outfile_path = os.path.join(os.path.dirname(__file__), "../testData", filename)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(outfile_path), exist_ok=True)

            # Assuming chosen_action is defined earlier in your code
            print(f"Chosen action: {chosen_action}")

            # Load existing data or initialize an empty list
            if os.path.exists(outfile_path):
                with open(outfile_path, "r") as infile:
                    try:
                        records = json.load(infile)
                        if not isinstance(records, list):  # Ensure records is a list
                            records = []
                    except json.JSONDecodeError:
                        records = []
            else:
                records = []

            # Append the new record
            records.append({"encoded_state":encoded_state, "chosen_action": chosen_action, "timestamp": time.time()})

            # Save the updated records back to the JSON file
            with open(outfile_path, "w") as outfile:
                json.dump(records, outfile, indent=4)

            print("Action recorded successfully.")

            time.sleep(0.5)

        return chosen_action

    def update_q_value(self, state, action, reward):
        encoded_state = self.encode_state(state)
        if encoded_state not in self.q_table:
            self.q_table[encoded_state] = {a: 0 for a in self.actions}
        old_value = self.q_table[encoded_state][action]
        # Calculate new Q-value
        next_max = max(self.q_table[encoded_state].values())
        self.q_table[encoded_state][action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)

        self.save_q_table()

    def save_q_table(self):
        try:
            # Convert tuple keys to strings for JSON compatibility
            converted_q_table = {str(state): actions for state, actions in self.q_table.items()}

            with open(self.q_table_file, "w") as outfile:
                json.dump(converted_q_table, outfile, indent=4)

            print(f"Q-table saved successfully to {self.q_table_file}")
        except Exception as e:
            print(f"Error saving Q-table: {e}")