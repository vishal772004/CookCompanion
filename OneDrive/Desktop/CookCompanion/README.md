COOK COMPANION
Video Demo:https://youtu.be/bkz36bnl_O0
Description:

Welcome to Cook Companion , a web development project which makes use of javascript, python(flask) and sqlite3. Here in this website it provides the user recipes of their choice asking the user for one or more ingredients and other parameters like diet type, type of dish ,allergies or restrictions and type of cuisine .
Then after submitting the request , I made use of spoonacular api which provide recipes through api requests then after getting the response displaying it to the user with the image of the food.I have added another feature to bookmark or save the recipe in a separate file. All of this was possible with the help of youtube video of recifilter from whom i have taken inspiration and created my own essence and design of the website and Chatgpt which helped me when i got stuck in a function and also stackoverflow helped me if Chatgpt couldnt resolve the issue.

So I will explain in detail about the code structure and what each file do. In the main app.py file i have copied few code from my previous assignment finance consisting of session and login required decorator function which is a must so that user does not access other webpages without logging in. I have also imported Session from flask_session which creates a session for each user and allows multiple users to access the website creating their own session.

Then i have made use of cs50 codespace for sqlite3 database for storing user datails like username and password .For the password i have imported generate_password_hash for converting the password to a hashed password for security concerns and check_password_hash for checking the password if it is of the same user for logging the user inside the website.

The first webpage that the user arrives is the login page where the user has to enter his credentials such as username and password . If the entered credentials are correct he can log inside the website creating his own session. If the user did not not register himself their is a option in the log in page asking sign up.If he clicks on it renders register webpage where the user can enter his preferred username, password and confirm the password for assuring the correct password.Then after registering himself the user is redirected to login so that he can login with the credentials he has registered.

After logging in the user arrives at the home page where there is a form that has input box for entering the ingredients and I have also added a button beside it to dynamically create a new input box and a button to add another input box. Using this the user can enter multiple ingredients and he can also delete it as i have changed the event listener for the button to remove if clicked once for adding . So you can add and delete input boxes but one always remain even if its empty.Then I have created some filters for the recipe by adding dropdown boxes that indicate multiple options to check and there are four filtering parameters .

The first one is for dish type like main or side dish. Then second one is for diet types like low sugar , low calories etc. The third one is for allergies or restrictions like peanut or dairy allergy or vegetarian restriction. The fourth and final parameter is for cuisine type that indicates the nationality or origin of the recipe. Then finally a button for  showing the recipes that match the information that the user provides and this button renders the user another webpage which i named as result.

Then comes the result webpage which displays all the recipes images, ingredients and two buttons .One for saving the recipe and the other for redirecting the user to another webpage that has detailed information about the recipe. This is displayed as a card for each recipe. The minimum number of recipes is 12 for each request and as mentioned i have used spoonacular api for requesting the recipe information .

I have made two requests from spoonacular api ,one for sending the request of the user using complex search api call that returns id of the recipe.Then using those ids i made another api request that gets the recipes ingredients,image and many more for displaying.As i have used free subscription of the spoonacular platform there is a limit for the api calls that i can perform.

In the home page i have added three links on the nav bar .One for viewing the saved recipes ,another for  settings to change the password and final one called logout that logs out user ending the session.In the result webpage when the user clicks on the save button the id and title of the recipes is stored in the database. This is then accessed when the saved recipes webpage is rendered the ids are then used for the api call and then the response i.e information regarding the recipe is then displayed like image and ingredients.User can view their saved recipe  by clicking the link in the home page.By clicking the settings link the user is rendered a webpage where the user has to enter username and new password then confirm the new password .Then by clicking change password the user's password can be changed.I have also added a feature to delete the recipe from the saved recipes if the user doesnt want it or his opinion changed.

This was my CS50 Final Project for Introduction To Computer Science for the Year 2024 .
Hope you like it!!
Thank You.



