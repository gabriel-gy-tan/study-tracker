# study.Now() ~ CS50x Final Project
#### Video Demo:  https://youtu.be/HFob03URjOE  
#### Description:
A simple study tracker web application that allows users to create studying categories and then start a timer to record their studying sessions. They can then choose to save their session or delete it and then view their saved sessions in the history tab. 

The backend is all using an SQLite database that has 3 distinct tables: users, categories, sessions. 

There is a simple log-in and registration page which is similar to CS50's finance problem

There is a category page allowing users to add new studying categories and allows them to view all their existing ones, they can also delete categories or update the names of the categories. 

The frontpage is the main part which uses JavaScript to create a functioning stopwatch at the very front. It allows users to choose from a select menu which includes all of the categories created. The user can then start the stopwatch and upon pressing the stop button, they can press the continue button to continue with that session, they can delete the session, or they can finish and save the session.

Upon pressing the finish button they are greeted with a page that asks for a short description of what the user did in their session. Then they can submit.

Final page is the history page which simply displays the sessions which they have studied sorted in descending order by the date and time. 
