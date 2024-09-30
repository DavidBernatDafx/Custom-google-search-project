CUSTOM GOOGLE SEARCH

This is the project created for collabim onboarding attempt.

Project is created in Python, with use of Flask web development framework.
For needed request calls GoogleApi is used.
For generating a pdf file module wkhtmltopdf is used, but unfortunately I've found bug in this functionality, when pushed the project to a production
server.
Thus this functionality is now working only on developer localhost server, but with desired outcome, regarding packages possibilities.
About its possibilities, the package cannot process .css styles, nor Bootstrap, so only vanilla HTML is converted to .pdf file. 

For basic styling of the webpage i have used Bootstrap framework.

Due to GoogleApi free tier, there is only 100 requests per day.
I have implemented error handling logic that takes care in that case on the backend, and informs user too on the frontend.

If tested during this period, please be patient, and try it in few hours or next day.

All new points are very welcomed, so I can improve this project further.

=========
CHANGELOG
=========

- removed functionality to save html as pdf
-added functionality to save response json data structure as formatted json file
-added functionality of backgroun task, that removes files from cache directory, older than 1 hour
-added functionality of naming cached jsons with randomly generated (pseudo id) sequence

-refactored main.py code 
	- extracted 2 functions from index() to make code more readable and modular
	- first function is for googleApis request 
	- second function is saving temp file at backed into cache directory


Personal note:

I have interest more in backend programming, that is enjoying me more. That's why styling isn't perfect nor extensive. I have used Bootstrap, for this
webpage, so at least it's looking reasonable. 

I was trying to make this project as simple and as near to task assignment, but I have tried to add something more in a way of algorhyths, use of packages.
I also had a fun with this, project, so I added litlle easter egg. 

=====================================================================================
Live example of this project can be found at: https://davidbernat.pythonanywhere.com/
=====================================================================================

David Bernát
608190309
dafxer@gmailcom