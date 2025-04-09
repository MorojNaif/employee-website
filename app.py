from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_excel('employee_projects.xlsx')

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    message = ""
    search_type = ""
    if request.method == 'POST':
        emp_id = request.form.get('employee_id')
        project_name = request.form.get('project_name')
        department = request.form.get('department')

        if emp_id:
            search_type = "employee"
            try:
                emp_id = int(emp_id)
                employee_data = df[df['EmployeeID'] == emp_id]
                if not employee_data.empty:
                    name = employee_data.iloc[0]['Name']
                    message = f"Welcome, {name}! These are your assigned projects:"
                    results = employee_data[['Project Name', 'Department', 'Cost']].to_dict('records')
                else:
                    message = "Employee ID not found."
            except ValueError:
                message = "Invalid Employee ID format."

        elif project_name:
            search_type = "project"
            project_data = df[df['Project Name'].str.lower() == project_name.lower()]
            if not project_data.empty:
                message = f"These employees are assigned to the project '{project_name}':"
                results = project_data[['Name', 'Department', 'Cost']].to_dict('records')
            else:
                message = "No data found for this project."

        elif department:
            search_type = "department"
            dept_data = df[df['Department'].str.lower() == department.lower()]
            if not dept_data.empty:
                message = f"These are the projects under the department '{department}':"
                results = dept_data[['Project Name', 'Cost']].drop_duplicates().to_dict('records')
            else:
                message = "No data found for this department."

    return render_template("index.html", results=results, message=message, search_type=search_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

