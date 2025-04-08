import json

def load_data(filename="movies.json"):
    try:
        with open(filename, "r") as file:
            data = file.read().strip()
            if not data:
                return {"movies": []}
            return json.loads(data)
    except FileNotFoundError:
        return {"movies": []}
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in movies file")


def save_data(data, filename="movies.json"):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise IOError(f"Failed to save data to {filename}: {e}")
