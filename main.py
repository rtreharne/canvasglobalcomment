import pandas as pd
from canvasapi import Canvas
from tqdm import tqdm

def read_csv(fname):
    # Ensure the file is a CSV
    if not fname.lower().endswith('.csv'):
        raise ValueError("Error: The file must be a CSV.")
    
    try:
        data = pd.read_csv(fname)

        # Check if required columns exist in the CSV
        required_columns = {"course", "assignment_id"}
        missing_columns = required_columns - set(data.columns)

        if missing_columns:
            raise ValueError(f"Error: Missing required columns: {', '.join(missing_columns)}")

        return data

    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")

def create_canvas_session(API_URL, API_TOKEN):
    # Prompt for API credentials if not provided
    if not API_URL or not API_TOKEN:    
        API_URL = input("Please input your Canvas URL, e.g. 'https://canvas.liverpool.ac.uk': ")
        API_TOKEN = input("Please input your API token: ") 
    
    # Create and return a Canvas API session
    canvas = Canvas(API_URL, API_TOKEN) 
    return canvas   

def get_submissions(canvas, course_sis_id, assignment_id):
    # Retrieve all submissions for the given assignment in the specified course
    try:
        submissions = [x for x in canvas.get_course(course_sis_id, use_sis_id=True).get_assignment(assignment_id).get_submissions(include=['submission_comments'])]
        return submissions
    except:
        return []

def check_graded_and_posted(submission):
    # Check if the submission has been graded and posted
    return submission.workflow_state == "graded" and submission.posted_at is not None

def main(API_URL=None, API_TOKEN=None):
    # Prompt the user for a CSV filename
    fname = input("Please enter filename, e.g. 'assignments.csv': ")
    
    # Read the CSV file and load data
    data = read_csv(fname)

    print("data", data)
    
    # Create a Canvas API session
    canvas = create_canvas_session(API_URL, API_TOKEN) 
    
    # Construct an automated message to be posted as a comment
    message = "AUTOMATED MESSAGE: "
    message += input("Please input global comment: ")

    submissions = []
    
    for i, row in tqdm(data.iterrows(), desc='Getting submissions ...'):
        
        # Get all submissions for the given course and assignment
        submissions.extend(get_submissions(canvas, row.course, row.assignment_id))

    number_of_submissions = len(submissions)
    number_of_assignments = len(set([x.assignment_id for x in submissions]))

    print(
        f"""
        The following message will be posted as a comment on {number_of_submissions} submissions across {number_of_assignments} assignments.
        """          
          )
    print(
        f"""
        {message}
        """
        )
    
    confirm = input("Are you sure you wish to proceed? (y/n): ")

    if confirm.lower() == "y":
        
        for submission in tqdm(submissions, desc="Processing submissions"):
            # Only proceed if the submission is graded and posted
            if check_graded_and_posted(submission):
                
                # Extract existing comments and concatenate them into a string
                comment_string = " ".join([x["comment"] for x in submission.submission_comments]) 
                
                # Avoid duplicate automated messages
                if "AUTOMATED MESSAGE" not in comment_string: 
                    
                    # Post the automated message as a comment
                    submission.edit(comment={"text_comment": message})
    else:
        print("Script exited. No changes made.")

if __name__ == "__main__":
    # Import API credentials from a config file
    from config import API_URL, API_TOKEN
    
    # Run the script
    main(API_URL, API_TOKEN)
