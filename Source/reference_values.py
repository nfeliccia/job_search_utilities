from dataclasses import dataclass
from pathlib import Path


# Defining the DataClass
@dataclass
class ReferenceValues:
    first_name: str
    last_name: str
    phone: str
    email: str
    current_resume_path: Path


# Creating two instances: one for actual values and one for dummy values
actual_values = ReferenceValues(
        first_name="Nicholas",
        last_name="Feliccia",
        phone="215-550-1642",
        email="nic@secretsmokestack.com",
        current_resume_path=Path(r"C:\Users\nfeli\OneDrive\2023_career\resumes\Feliccia_0x57_000044.docx")
)

dummy_values = ReferenceValues(
        first_name="Bart",
        last_name="Simpson",
        phone="800-555-1212",
        email="bart_simpson@aol.com",
        current_resume_path=Path(r"F:\job_search_utilities\Data\dummy_resume.txt")  # This is a placeholder path for the dummy resume
)
