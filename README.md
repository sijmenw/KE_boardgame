#################################################################################################################
# 																												#
# 												Knowledge Engineering 											#
# 									Boardgame Recommender Knowledge Based system 								#
# 										Based on CommonKADS Classification Model 								#
#																												#
#################################################################################################################
#																												#
# 									Authors: Justyna Kleczar & Sijmen van der Willik							#
# 																												#
#################################################################################################################
# 
# Prerequisites: 
# Python 2.7 
# pip
# virtualenv
#
#
# It is recommended to use a Linux based system for running this application. 
# To run the application locally, please follow these steps:
# 
# 1. Unzip the contents of KE_BoardgameRecommender into KE_BoardgameRecommender 
#    directory.
#
# 2. Change directory location to KE-BoardgameRecommender:
#
# ~$ cd KE_BoardgameRecommender
#
# 3. Create a virtual environment named eb-virt:
#
# ~$ virtualenv ~/eb-virt
#
# 4. Activate the virtual environment:
#
# ~$ source ~/eb-virt/bin/activate
# (eb-virt) ~$
#
# You will see (eb-virt) prepended to your command prompt, indicating that you're in a virtual environment.
#
# 5. Use pip to install Flask by typing:
#
# (eb-virt)~$ pip install flask==0.10.1
# 
# 6. To verify that Flash has been installed, type: 
#
# eb-virt)~$ pip freeze
# Flask==0.10.1
# itsdangerous==0.24
# Jinja2==2.7.3
# MarkupSafe==0.23
# Werkzeug==0.10.1
# 
# This command lists all of the packages installed in your virtual environment. 
# Later you will use the output of this command to configure your project for use with Elastic Beanstalk.
#
# 7. Run application.py with Python:
# 
# (eb-virt) ~/eb-flask$ python application.py
# 
# Flask will start a web server and display the URL to access your application with. 
# For example:
# 
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
# * Restarting with stat
# 
# 8. Open the URL in your web browser. 
# You should see the application running, showing the index page.
# 
# 9. Input your game profile and hit the "Recommend" button.
# 
# 10. You can stop the web server and return to your virtual environment by typing Ctrl+C.
# 
# 11. Deactivate your virtual environment by with the deactivate command:
# 
# (eb-virt) ~$ deactivate
# 
#################################################################################################################
#																												#
# The guide for configuring flask application for Elastic Beanstalk is based on AWS 							#
# guide which can be viewed here:																				#
#																												#
# http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html#python-flask-install 	#
#																												#
#################################################################################################################





