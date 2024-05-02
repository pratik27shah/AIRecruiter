from flask import Flask, render_template, request
from hrModule import get_gemini_response_for_hr_intro

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        jobdescription = request.form.get('jobDescription')
        candidate_name=request.form.get('candidateName')
        info=get_gemini_response_for_hr_intro(jobdescription,candidate_name)
        # Render the template with the processed data
        return render_template('index.html', processed_data=info,candidate_name=candidate_name,job_description=jobdescription)
    else:
        # Render the template without any data initially
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
