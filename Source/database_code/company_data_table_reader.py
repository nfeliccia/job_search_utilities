import json
import os
from pathlib import Path


def read_json_to_dict(file_path: Path) -> dict:
    """Reads a JSON file into a dictionary and returns it.

    Args:
        file_path (Path): The path to the JSON file.

    Returns:
        dict: The parsed JSON data as a dictionary.

    Raises:
        FileNotFoundError: If the file is not found.
        JSONDecodeError: If the file cannot be parsed as JSON.
    """

    try:
        with file_path.open("r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The JSON file was not found: {file_path}") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON file: {file_path}") from e


# Example usage:
os.chdir(r"F:/job_search_utilities")
company_data_table = read_json_to_dict(Path("./Data/no_sql/company_data_table.json"))
