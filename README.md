# sem-meter
Process a sem-meter .csv file to output only certain circuits with different multipliers to support multi-family household

## Installation
```
$ mkdir -p ~/code/
$ git clone https://github.com/Flurrywinde/sem-meter.git
$ cd sem-meter
$ python -m venv .venv				# Create python virtual environment
$ source .venv/bin/activate.fish	# Activate it
$ pip install -r requirements.txt	# Install needed modules into the virtual environment
```
Modify the above commands to suit your system, e.g. where you place your cloned repos and which shell you use. I do `activate.fish` because I use the Fish Shell.

You must also modify `sem_meter.py` to suit your household and circuit configurations.

	our_circuits = {
		"<circuit name in the .csv file>": <percentage of this circuit you pay for>,
		"Example: laundry room": .5,
		...
	}

### Optional
```
$ cp sem.fish ~/.config/fish/functions/
```
This creates a new command `sem`. (This script has the additional feature of always updating the repo via `git pull`.)

### Hardware Setup
This repo assumes you have a working sem-meter device setup:

* Install a sem-meter device in your circuit box and connect it to the circuits you want monitored.
* Install and setup the sem-meter app on your phone or tablet.

## Usage
* Export latest .csv file from the sem-meter app.
* Run this repo's auto-calculator app:
	If you `cp`'ed `sem.fish`, just run `sem`. Otherwise:
	```
	$ cd ~/code/sem-meter
	$ source .venv/bin/activate.fish
	$ python app.py
	```
* Go to the page sent to your default browser to upload the .csv file and input data from your electric bill. Hit the Generate button.
* This will generate and automatically download a new .csv file. Open this in your spreadsheet program.
* See subtotals of only your electricity usage, your KWh usage, and who pays what, all calculated for you automatically!

## TODO
### Make it configurable
IOW, stop hardcoding things (e.g. the `our_circuits` dict)!

### Make it installable
* https://www.kevinlaw.info/blog/2016-04-15-distributing-flask-as-a-package/
* https://www.quora.com/What-is-the-process-to-upload-a-Python-Flask-project-to-GitHub-and-run-it-on-a-real-IP
* https://share.google/aimode/YWe78vxuZV1tG9DxN

To make your Flask project distributable and installable from a GitHub repo, structure it as a Python package with  (or ), include a , and use Gunicorn/WSGI for deployment; then, you can link it to platforms like Render or PythonAnywhere for hosting, or let users  directly from your repo for local setup, explains Flask documentation (https://flask.palletsprojects.com/en/stable/tutorial/install/) and Reddit users (https://www.reddit.com/r/learnpython/comments/1bismq5/how_can_i_run_a_flask_app_for_completely_free/). [1, 2, 3, 4, 5]  
1. Package Your Flask App (Make it Installable) 

• Create  (Modern Way): Define your project metadata (name, version, dependencies) using  or  within this file. 
• Create : List all Python dependencies (Flask, Gunicorn, etc.). 
• Add a  directory: Place your main app package (e.g., ) inside  for cleaner structure. 
• Entry Point: Define an application entry point in  (e.g., ) so  or Gunicorn knows where to find it. [1, 3]  

2. Set Up Your GitHub Repository 

• Initialize Git: In your project root: , , . 
• Create Remote Repo: On GitHub, create a new repo and link it: , . [5, 6]  

3. Deploy (Hosting Options) 

• Render.com (Recommended for Ease): 

	• Connect your GitHub repo to Render. 
	• Set Build Command: . 
	• Set Start Command:  (adjust  to your main file/instance). 
	• Add environment variables (like , ) in Render's environment settings. 

• PythonAnywhere / Vercel: Similar setup, often using their web-based UIs to connect to GitHub and configure commands, notes Reddit users (https://www.reddit.com/r/flask/comments/17wagjg/how_can_i_deploy_my_flask_project_on_github/). 
• Self-Hosting (AWS/DigitalOcean): Involves SSH, Nginx, Gunicorn, systemd, and SSL setup, as shown in Miguel Grinberg's tutorial (https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux) and Medium article. [1, 2, 5, 7, 8, 9]  

4. For Local Installation (Users) 

• Users can clone your repo and run  (editable mode) or  (wheel) to install your app and its dependencies in their environment, making it importable from anywhere, as described in the Flask documentation tutorial. [3, 10]  

AI responses may include mistakes.

[1] https://github.com/learn-co-curriculum/python-p4-deploying-flask-react-app-to-render
[2] https://www.reddit.com/r/flask/comments/17wagjg/how_can_i_deploy_my_flask_project_on_github/
[3] https://flask.palletsprojects.com/en/stable/tutorial/install/
[4] https://www.reddit.com/r/learnpython/comments/1bismq5/how_can_i_run_a_flask_app_for_completely_free/
[5] https://www.youtube.com/watch?v=vwoUriuqcio
[6] https://www.youtube.com/watch?v=uwyd64lLTeU
[7] https://github.com/dandalpiaz/flask-linux-guide
[8] https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux
[9] https://medium.com/@yhv.142/step-by-step-guide-for-deploying-a-flask-application-from-github-on-aws-ec2-2178e12d733b
[10] https://github.com/pallets/flask/blob/main/docs/tutorial/install.rst
