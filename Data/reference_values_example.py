from dataclasses import dataclass
from pathlib import Path

"""

Note . For privacy reasons, the actual values are not included in this repository.
This file is for reference only.
"""


# Defining the DataClass
@dataclass
class ReferenceValues:
    current_resume_path: Path
    email: str
    first_name: str
    last_name: str
    linkedin_url: str
    phone: str


dummy_values = ReferenceValues(
        current_resume_path=Path(r"/Data/dummy_resume.docx"),
        email="bart_simpson@aol.com",
        first_name="Bart",
        last_name="Simpson",
        linkedin_url="https://www.linkedin.com/in/bart-simpson-4a2673b/",
        phone="3154431870"
)
