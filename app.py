# app.py
import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from forms import UserDataForm

from werkzeug.utils import secure_filename
from sem_meter import sem
import webbrowser
from threading import Timer

def open_browser():
    # Opens the URL in a new browser tab/window
    webbrowser.open_new("http://127.0.0.1:5000/")

# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
# A secret key is needed for CSRF protection with Flask-WTF
#app.config['SECRET_KEY'] = 'your_very_secret_key_here'
app.config['SECRET_KEY'] = 'fdjvk33jgfvj4fje3fcdf'
# Define a folder to temporarily store generated files
app.config['GENERATED_FILES_FOLDER'] = 'generated_files'
os.makedirs(app.config['GENERATED_FILES_FOLDER'], exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# for non-wtforms version, so unused but keep for reference
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# If the user does not select a file, the browser submits an
		# empty file without a filename.
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('download_file', name=filename))

# For wtforms multi-file version (https://www.elearningsolutions.co.in/file-uploads-with-flask-wtf/ ) with ONLY the upload, no processing or d/l file
def upload_files():
    form = MultiFileUploadForm()
    if form.validate_on_submit():
        for file in form.files.data:
            # Process each uploaded file here
            # Save the file, validate its type, etc.
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return 'Files uploaded successfully!'
    return render_template('upload.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = UserDataForm()
	# Process valid form data
	if form.validate_on_submit():
		# date range
		#start_date = '2025-07-18'
		#end_date = '2025-8-17'
		start_date = form.start_date.data
		end_date = form.end_date.data

		# Save uploaded file if exists
		file = form.csv_in.data
		if file.filename == '':
			flash('No selected file')
			#return redirect(request.url)  # from non-WTF example, so not sure if right
			return render_template('form.html', form=form)
		if allowed_file(file.filename):
			filename = secure_filename(file.filename)
			csvfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(csvfile)
			newcsv = sem(csvfile).exe(start_date, end_date)
			# , '2025-07-18', '2025-8-17'
			#return redirect(url_for('download_file', name=filename))  # from elearningsolutions example

		# Process rest of form
#		 username_data = form.username.data
#		 file_content = f"The submitted username is: {username_data}"
#		 file_path = os.path.join(app.config['GENERATED_FILES_FOLDER'], f"{username_data}.txt")
		duedate_data = form.duedate.data
		csv_out = f'sem_{duedate_data} ({start_date} to {end_date}).csv'
		#file_content = f"The submitted duedate is: {duedate_data}\n"
		#file_content += f"The submitted file is: {form.csv_in.data}\n"
		#file_content += f"{newcsv}\n"
		file_content = f"{newcsv}\n"
		file_path = os.path.join(app.config['GENERATED_FILES_FOLDER'], f"{csv_out}")

		# Create the file
		with open(file_path, 'w') as f:
			f.write(file_content)

		# Redirect to a download route
		return redirect(url_for('download_file', filename=f"{csv_out}"))

	# If GET request or validation failed, render the form with error messages
	return render_template('form.html', form=form)

@app.route('/download/<filename>')
def download_file(filename):
	# Send the generated file for download
	full_path = os.path.join(app.root_path, app.config['GENERATED_FILES_FOLDER'])
	return send_file(os.path.join(full_path, filename), as_attachment=True, download_name=filename)

if __name__ == "__main__":
    # Start a timer to open the browser after a short delay (e.g., 1 second)
    # This gives the Flask server a moment to spin up
    Timer(1, open_browser).start()
    # Run the Flask app
    app.run(port=5000, debug=True)
