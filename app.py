from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_excel('employee_projects.xlsx')

# تنظيف أسماء الأعمدة من أي مسافات
df.columns = df.columns.str.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    message = None
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        try:
            emp_id = int(emp_id)
            employee_data = df[df['EmployeeID'] == emp_id]

            if employee_data.empty:
                message = "Employee ID not found."
            else:
                name = employee_data.iloc[0]['Name']
                projects = employee_data[['Project Name', 'Department', 'Cost']].to_dict('records')
                
                if not projects:
                    message = f"Hello {name}, you are not assigned to any projects."
                else:
                    result = {
                        'name': name,
                        'projects': projects
                    }
        except ValueError:
            message = "Invalid Employee ID. Please enter a number."

    return render_template('index.html', result=result, message=message)
    
if __name__ == '__main__':
    app.run(debug=True)
