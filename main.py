import pandas as pd
from config import API_URL, API_TOKEN
from canvasapi import Canvas

def read_csv(fname):
    if not fname.lower().endswith('.csv'):
        raise ValueError("Error: The file must be a CSV.")
    
    try:
        data = pd.read_csv(fname)

        # Check if required columns exist
        required_columns = {"course", "assignment_id"}
        missing_columns = required_columns - set(data.columns)

        if missing_columns:
            raise ValueError(f"Error: Missing required columns: {', '.join(missing_columns)}")

        return data

    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")

def create_canvas_session(API_URL,API_TOKEN):
    if not API_URL or not API_TOKEN:    
        API_URL = input("Please input your canvas url, e.g 'https://canvas.liverpool.ac.uk': ")
        API_TOKEN = input("Please input your API token: ") 
    canvas = Canvas(API_URL,API_TOKEN) 
    return canvas   

def get_submissions(canvas, course_sis_id, assignment_id):
    submissions = [x for x in canvas.get_course(course_sis_id, use_sis_id=True).get_assignment(assignment_id).get_submissions(include=['submission_comments'])]
    return submissions



if __name__=="__main__":
    fname = input("Please enter filename, e.g 'assignments.csv': ")
    data = read_csv(fname)
    canvas = create_canvas_session(API_URL,API_TOKEN) 
    print(canvas.get_current_user())
    data = data.sample(1)
    for i,row in data.iterrows():
        print("course: ", row.course)
        submissions = get_submissions(canvas,row.course,row.assignment_id)
        print(len(submissions))



