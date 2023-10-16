import os

import pandas as pd


# Function to find the latest CSV file in the specified directory
def find_latest_csv(flc_directory: str) -> str:
    """
    Process the CSV file from Clockify and generate an Excel report showing the total hours worked per week.
    The report is saved in the same directory as the script.

    Args:
        csv_file_path: The path to the CSV file to process.

    Returns:
        None. The function saves the report in Excel format.
    
    Find the latest CSV file in the specified directory
    Args:
        flc_directory: Directory where the CSV files are located output from Clockify

    Returns:
        Path to the latest CSV file

    """

    # Check if the directory exists
    if not os.path.exists(flc_directory):
        print(f"Directory does not exist: {flc_directory}")
        raise NotADirectoryError

    # Get all files in the directory
    files = os.listdir(flc_directory)

    # Filter out non-CSV files
    csv_files = [f for f in files if f.endswith('.csv')]

    # If there are no CSV files, return None
    if not csv_files:
        print("No CSV files found in the directory.")
        raise FileNotFoundError

    # Find the latest file
    latest_file = max(csv_files, key=lambda f: os.path.getctime(os.path.join(flc_directory, f)))
    latest_path = os.path.join(flc_directory, latest_file)
    return latest_path


# Function to process the CSV file and generate the Excel report
def process_time_tracking_report(csv_file_path: str):
    """
    Process the CSV file from Clockify and generate an Excel report showing the total hours worked per week.
    The report is saved in the same directory as the script.

    Args:
        csv_file_path: The path to the CSV file to process.

    Returns:
        None. The function saves the report in Excel format.
    """

    # Read the file with pandas
    report_df = pd.read_csv(csv_file_path)

    # Ensure data types are correct
    report_df['Billable'] = report_df['Billable'].apply(lambda x: x == 'Yes')
    start_date_ = report_df['Start Date']
    start_date_ = pd.to_datetime(start_date_, format='%m/%d/%Y')
    report_df['End Date'] = pd.to_datetime(report_df['End Date'], format='%m/%d/%Y')
    report_df['Start Time'] = pd.to_datetime(report_df['Start Time'], format='%I:%M:%S %p').dt.time
    report_df['End Time'] = pd.to_datetime(report_df['End Time'], format='%I:%M:%S %p').dt.time
    report_df['Duration (decimal)'] = report_df['Duration (decimal)'].astype(float)

    # Extract the year and week from the Start Date
    report_df['Year'] = start_date_.dt.isocalendar().year
    report_df['Week'] = start_date_.dt.isocalendar().week

    # Group by year, week and sum the duration
    yw_grouper = ["Year", "Week"]
    dd_ = "Duration (decimal)"
    weekly_hours_df = report_df.groupby(yw_grouper)[dd_].sum().reset_index()
    weekly_hours_df = weekly_hours_df.rename(columns={dd_: "Total Hours"})

    # Define the path to save the Excel file
    filename, _ = os.path.splitext(csv_file_path)
    excel_filename = f"{filename}_by_week.xlsx"

    # Correct the save_path and ensure the directory exists

    # Extract the base directory to avoid duplication in the path
    output_directory = os.path.dirname(csv_file_path)
    base_output_directory = '\\'.join(output_directory.split('\\')[:-1])  # Windows specific path handling
    # The script saves the Excel file in the current working directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    save_path = os.path.join(base_output_directory, excel_filename)

    # Calculate the Monday of each week
    weekly_hours_df['Monday'] = weekly_hours_df.apply(
            lambda row: pd.to_datetime(f"{int(row['Year'])}-W{int(row['Week'])}-1", format='%G-W%V-%u'),
            axis=1
    )
    # Reorder the columns to place 'Monday' between 'Week' and 'Total Hours'
    correct_order = ['Year', 'Week', 'Monday', 'Total Hours']
    weekly_hours_df = weekly_hours_df[correct_order]
    # Save to Excel
    with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
        weekly_hours_df.to_excel(writer, sheet_name='by week', index=False)

    print(f"Report saved at: {save_path}")


# Main execution: The script will find the latest CSV file in the specified directory
if __name__ == "__main__":
    import sys

    directory = sys.argv[1] if len(
            sys.argv) > 1 else "Data/time_tracking_data"  # The script saves the Excel file in the current working directory
    latest_csv = find_latest_csv(directory)
    if latest_csv:
        process_time_tracking_report(latest_csv)
