Multiuser Blog
===============

What is it? (Functionality)
---------------------------
It is a blogging site where multiple users can signup and write posts. Guests can read unlimited posts without signup. To write, like or comment on a post, guests would need to signup/signin. Commenting on posts is powered by Disqus. All sensitive user data is securely stored in Google Datastore.
The website is designed to render on all device sizes.


Last Update Date
-----------------
December 22, 2016


System-specific Notes
----------------------
*   The app is built using Google App Engine.
*   Backend is developed in Python 2.7 and uses Jinja 2 for templating.
*   Google Cloud Datastore is used to persist data.
*   External Dependencies - Tinymce, Disqus, Font-Awesome


Testing
-------
The website is tested for Edge and Chrome Browsers.
Though it has been designed to render on all device sizes, thourough testing on mobile devices is yet to be done.


Package Details (Files involved)
--------------------------------
Below is a brief description of the folders/files that have been used for this application.
1.  css - main.css contains all styling for the website. responsive.css contains media queries which has been created for organizing the styles but can be completely merged into main.css.

2.  fonts (a folder) - The website uses "OpenSans-CondLight" and so all font related files are here.

3.  images (a folder) - Contains all images used by the website.

4.  templates (a folder) - Contains all Jinja templates.

5.  app.yaml - Contains app configuration for deployment on Google App Engine.

6.  blog.py - The python file which receives requests and lists all handlers.

7.  readme.md - It's me!

8. handlers (a folder) - All web request handling code written in Python.

9. models (a folder) - All models for the datastore.




How to get started
-------------------
1. Go to https://udacity-shal-blog.appspot.com/

2. Read all blog posts from various writers.

3. To write a post, signup and use the "Write a story" link.

3. Come back, login and write more posts.

4. Like posts by clicking the "heart" with each post. All posts you have liked would have filled red heart when you are logged in. For guests, trying to like a post would redirect to signin page.

5. Comments are implemented using Disqus. To comment, Disqus wants us to login using an account Disqus, Google, Facebook, etc.

6. Edit/Delete something you had written.

7. To signout, use the "sign out" link on the home page.


Functionalities
----------------
1.  Read posts written by different writers all in the same place. All posts can be read without the need to login.

2.  Signup for new users
	Users can signup by providing a username, password and email (optional). The username and password can be 3-20 characters long.

3.  Signin
	Users can come back to the application anytime later and login and continue.

4.  Write a post
	Logged in users will have an option to write posts.

5.  Edit/Delete a post
	Logged in users can edit and delete posts written by them.

6.  Like and Comment on a post
	Logged in users can like or comment on a post. Users would not be able to like their own post. Commenting is powered by Disqus which requires the commenter to login to Disqus.


Known Issues(major/minor/impacting feature)
-------------
1.  On closing the browser, the user is not signed out (noticed mostly while testing on local machine). (major)

2.  The buttons styling has to be updated to have button text in one line. (minor)

3.  The python code has to be modularized and written in Python way (currently it looks more like Java code) (major)

4.  Use either post id or key in the code. (minor)

5.  While setting the cookie, use userid instead of username. (minor)


Features under planning
-----------------------
1.  Creating groups

2.  Allow content tagging

3.  Allow to add images to posts

4.  Allow users to write/import their profile


References, Credits & Acknowledgements
---------------------------------------
1.  Password Hashing: The functions are used from HW4 of Udacity's Intro to Backend course.

2.  https://disqus.com/ - For comments

3.  https://www.tinymce.com/

4.  http://fontawesome.io/ - For user and heart icons

5.  https://cloud.google.com/docs/

6.  http://stackoverflow.com/

7.  https://devopscloud.net/2014/11/30/a-real-quick-quick-start-with-google-cloud-platform-command-line-tools/

8.  https://github.com/sixrevisions/semi-transparent-buttons/blob/master/semi-transparent-buttons.css

9.  Validators
	1.	http://stackoverflow.com/questions/37939131/how-to-validate-jinja-syntax-without-variable-interpolation - Jinja
	2.	https://jigsaw.w3.org/css-validator/ - For CSS
	3.	https://validator.w3.org/ - For Base.html
	4.	http://pep8online.com/	- For Python

10.	Decorators
	1.	https://realpython.com/blog/python/primer-on-python-decorators/
	2.	http://thecodeship.com/patterns/guide-to-python-function-decorators/
	3.	http://www.artima.com/weblogs/viewpost.jsp?thread=240808


Contact Information
--------------------
For any comments, queries, issues, and bugs, please contact singhshalinis@gmail.com.