import json
import datetime


class PlayerStats:
    current_date = None

    def __init__(self, start_date=datetime.date(1939, 1, 1), intel_data = None):

        self.start_date = start_date

        if not PlayerStats.current_date:
            PlayerStats.current_date = start_date

        self.research_progress = {}
        for i in range(1, 10):
            self.research_progress[i] = 0

        #self.stats.intel_progress = { intel_data[a][0] : 0 for a in range(len(intel_data))}
        self.intel_progress = { intel_data[a][0] : 0 for a in range(len(intel_data))}

        self.places = []

    def dummy_research_progress(self):
        self.research_progress = { 1: 100, 2: 80, 3: 40, 4: 25, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0 }

    def dummy_intel_progress(self):
        self.intel_progress[9] = 100
        self.intel_progress[71] = 70
        self.intel_progress[75] = 100
        self.intel_progress[78] = 60
        self.intel_progress[80] = 70

    def increase_research_progress(self, research_id, progress):
        if research_id in self.research_progress:
            self.research_progress[research_id] += progress

    def add_place(self, place_id, place_info):
        place = {"place_id": place_id, "place_info": place_info}
        self.places.append(place)

    def reset_stats(self):
        for research_id in self.research_progress:
            self.research_progress[research_id] = 0
        self.places = []

    def display_stats(self):
        print("Research Progress:")
        for research_id, progress in self.research_progress.items():
            print(f"Research {research_id}: {progress}%")

        print("\nPlaces:")
        for place in self.places:
            print(f"Place ID: {place['place_id']}, Place Info: {place['place_info']}")

    def save(self, file_path):
        data = {
            "research_progress": self.research_progress,
            "intel_progress": self.intel_progress,
            "places": self.places,
            "start_date": self.start_date.isoformat(),
            "current_date": self.current_date.isoformat()
        }
        with open(file_path, "w") as file:
            json.dump(data, file)

    @classmethod
    def load(cls, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        start_date = datetime.datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        stats = cls(start_date)
        stats.research_progress = data["research_progress"]
        stats.places = data["places"]
        return stats

"""
# Usage example:
stats = PlayerStats()
stats.increase_research_progress(1, 50)
stats.increase_research_progress(2, 30)
stats.add_place(1, "Washington DC")
stats.display_stats()

# Save the game progress to a file
save_file = "game_stats.json"
stats.save(save_file)

# Load the saved game progress from the file
loaded_stats = PlayerStats.load(save_file)
loaded_stats.display_stats()
"""