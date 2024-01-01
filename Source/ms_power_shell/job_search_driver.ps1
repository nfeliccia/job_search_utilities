# Navigate to your project directory
Set-Location "F:\job_search_utilities\"

# Update the PATH
$env:PATH += ";F:\job_search_utilities;F:\job_search_utilities\Source;F:\job_search_utilities\Scripts"
& "F:\job_search_utilities\Scripts\activate.ps1"
python "F:\job_search_utilities\Source\readers\aramark_reader.py"
# Deactivate the virtual environment
& ".\Scripts\deactivate.bat"
