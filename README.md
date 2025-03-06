# Canvas Global Comment

## Authors

This tool was created by Jack Foster and Robert Treharne from the School of Bioscience's Technology Enhanced Learning (TEL) team at the University of Liverpool.

## Overview
This tool allows you to add an automated comment to student submissions that have already been graded and have feedback posted. It integrates with the Canvas LMS API to fetch submissions, check their grading status, and post a comment if it is not already present.

## Features
- Reads course and assignment details from a CSV file.
- Connects to Canvas via the API using user-provided credentials.
- Retrieves all submissions for specified assignments.
- Checks if submissions are graded and feedback is posted.
- Adds an automated comment to eligible submissions.

## Virtual Environment Setup
To create a virtual environment and install dependencies:
1. Create a virtual environment named `.venv`:
   ```sh
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - On macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### 1. Prepare the CSV File
Create a CSV file (e.g., `assignments.csv`) with the following columns:
- `course`: The course SIS ID.
- `assignment_id`: The assignment ID.

Example CSV content:
```csv
course,assignment_id
ptc-treharne,304962
LIFE223-202425,281730
```

### 2. Run the Script
Execute the script using:
```sh
python script.py
```

### 3. Follow the Prompts
The script will:
1. Ask for the CSV filename.
2. Prompt for Canvas API credentials (if not provided in `config.py`).
3. Retrieve submissions for the specified assignments.
4. Display a summary of the action to be performed.
5. Ask for confirmation before proceeding.
6. Process submissions and add comments where necessary.

### 4. Example Output
```sh
Please enter filename, e.g. 'assignments.csv': assignments.csv
Please input global comment: Please review the feedback carefully.

The following message will be posted as a comment on 15 submissions across 3 assignments.

AUTOMATED MESSAGE: Please review the feedback carefully.

Are you sure you wish to proceed? (y/n): y
Processing submissions:  60%|██████    | 9/15 [00:30<00:10, 1.67s/submission]
```

## Configuration
For convenience, you can store API credentials in a `config.py` file:
```python
API_URL = "https://canvas.example.com"
API_TOKEN = "your_api_token_here"
```
This will prevent the script from prompting you each time.

## Notes
- The script only adds a comment if the submission is graded and feedback has been posted.
- It avoids duplicate comments by checking for existing automated messages.
- If an assignment has no submissions or an error occurs, it skips gracefully.

## License
This project is released under the MIT License.

