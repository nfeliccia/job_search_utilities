from dataclasses import dataclass
from pathlib import Path


# Defining the DataClass
@dataclass
class ReferenceValues:
    current_resume_path: Path
    email: str
    first_name: str
    last_name: str
    linkedin_url: str
    phone: str


# Creating two instances: one for actual values and one for dummy values
actual_values = ReferenceValues(
        current_resume_path=Path(r"C:\Users\nfeli\OneDrive\2023_career\resumes\Feliccia_0x57_000044.docx"),
        email="nic@secretsmokestack.com",
        first_name="Nicholas",
        last_name="Feliccia",
        linkedin_url="https://www.linkedin.com/in/nicfeliccia/",
        phone="215550s1642"
)

dummy_values = ReferenceValues(
        current_resume_path=Path(r"F:\job_search_utilities\Data\dummy_resume.docx"),
        email="bart_simpson@aol.com",
        first_name="Bart",
        last_name="Simpson",
        linkedin_url="https://www.linkedin.com/in/bart-simpson-4a2673b/",
        phone="3154431870"
)
