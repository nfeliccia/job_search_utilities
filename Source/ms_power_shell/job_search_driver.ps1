# Navigate to your project directory

# Update the PATH
$env:PATH += ";F:\job_search_utilities;F:\job_search_utilities\Source;F:\job_search_utilities\Scripts"
& "F:\job_search_utilities\Scripts\activate.ps1"
Set-Location "F:\job_search_utilities\"
# python "F:\job_search_utilities\Source\readers\aramark_reader.py"
# python "F:\job_search_utilities\Source\readers\b_yond_reader.py"
# python "F:\job_search_utilities\Source\readers\beacon_hill_reader_uploader.py"
# python "F:\job_search_utilities\Source\readers\bimbo_reader_uploader.py"
# python "F:\job_search_utilities\Source\readers\captech_reader_uploader.py"
# python "F:\job_search_utilities\Source\readers\collabera_reader_uploader.py"
# python "F:\job_search_utilities\Source\readers\comcast_reader.py"
# python "F:\job_search_utilities\Source\readers\cvs_reader.py"
# python "F:\job_search_utilities\Source\readers\fedex_reader_uploader.py"
# python "F:\job_search_utilities\Source\readers\flexential.py"
# python "F:\job_search_utilities\Source\readers\juno_reader.py"
# python "F:\job_search_utilities\Source\readers\mission_staff_reader.py"
# python "F:\job_search_utilities\Source\readers\susquehanna_international_reader.py"

# Deactivate the virtual environment
& ".\Scripts\deactivate.bat"
