# sem-meter
Process a sem-meter .csv file to output only certain circuits with different multipliers to support multi-family household

## Make it installable
* https://www.kevinlaw.info/blog/2016-04-15-distributing-flask-as-a-package/
* https://www.quora.com/What-is-the-process-to-upload-a-Python-Flask-project-to-GitHub-and-run-it-on-a-real-IP

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
