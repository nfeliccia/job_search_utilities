"""
The purpose of this function is to create the config json from the config template
"""
import json
from pathlib import Path

config_template = {
    "about_this_template": "This is the config template for the General Reader",
    "standard_timeout": 1000,
    "standard_sleep": 2,
}
config_string = json.dumps(config_template)
template_path = Path(r".\Data\scraping_parameters_config.json")
with open(template_path, 'w') as f:
    f.write(config_string)
