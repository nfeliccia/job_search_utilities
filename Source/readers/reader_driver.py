import importlib

# Full list of reader class names
reader_class_names = [
    "AramarkReader", "BYondReader", "BeaconHillReader", "BimboJobSearcher",
    "CaptechReader", "CollaberaReader", "ComcastReader", "CVSReader",
    "CyberCodersReader", "FedexReaderUploader", "FlexentialReader", "MissionStaffReader"
]

# Module where these classes are defined
module_name = "readers"

# Dynamically import classes and create instances
reader_instances = []
for class_name in reader_class_names[-1:]:
    try:
        # Import the module
        module = importlib.import_module(module_name)

        # Get the class
        reader_class = getattr(module, class_name)

        # Create an instance of the class (assuming no arguments for the constructor)
        # Modify this part if you need to pass parameters from your AWS DynamoDB database
        instance = reader_class()
        reader_instances.append(instance)

    except AttributeError:
        print(f"Class {class_name} not found in module {module_name}")
    except Exception as e:
        print(f"Error occurred while importing class {class_name}: {e}")

# Now, reader_instances contains instances of each reader class
