# CS50 Bill Split
#### Video Demo: https://www.youtube.com/watch?v=RYUjCkttgGM&ab_channel=FooKarJun
#### Description:
A bill splitting web-application that can be used to calculate shared group expenses and split them in the most efficient method. This web-application can be utilised for all group settings to equally split/portion carryover between users and display 

This web-application can be utilised when there is more than one payee for (equally split) group-expenses. To avoid having unneccesary two-way transfers between payees, we calculate the following:
- the average amount each person has to pay
- using the average, 

## Technologies
Main Language used: Python
Design Language: HTML, CSS, JS
Framework:Flask, Flask SQLalchemy

## Files

### Core algo
`bill.py`
Where the function "calculate" is defined and handles the main calculation of this web-application

By creating dict to store unique users this function calculates the cost per user by taking the total cost inputted and divide it by the total number of unique users added to the dict (to get the average cost per user)  

After which an array is created to store the items of the dictionary and sort it in ascending order by value(Amount paid by each user). From here two seperate arrays are created :
1) The amount paid per user - the calculated average cosat per user
2) The key, names of the respective user

For each name, initialise an empty dictionary to contain all eventual transactions concerning them (owe or receive).
Place all these dictionaries into a parent dict tagged to the respective names.

The last while-loop in the calculate() function is responsible for calculating the bill splitting among the users. The loop iterates from the start and end of the paidArray, which contains the amount paid by each user minus the cost per user. The loop continues until the start index payeeIdx is equal to or greater than the end index excessIdx.

Inside the loop, the code checks the balance value to determine whether the current payer still owes money or has excess funds to distribute. If the balance is negative, it means the current payer owes money and cannot fully fill the next person's outstanding balance. If the balance is positive, it means the current payer has excess funds that can be used to fill the next person's outstanding balance. If the balance is zero, it means the current payer has just enough funds to fill the next person's outstanding balance.

There are three possible cases to consider inside the loop:

    Case 1: The excess amount is less than the amount owed by the current payer. In this case, the code assigns the excess amount to the current payer's debt to the excess payer and updates the balance accordingly. The loop then moves on to the next excess payer by decrementing the excessIdx.

    Case 2: The excess amount is greater than the amount owed by the current payer. In this case, the code assigns the amount owed by the current payer to the excess payer's debt to the current payer and updates the balance accordingly. The loop then moves on to the next current payer by incrementing the payeeIdx.

    Case 3: The excess amount is exactly equal to the amount owed by the current payer. In this case, the code assigns the excess amount to the current payer's debt to the excess payer and updates the balance to zero. The loop then moves on to the next current payer by incrementing the payeeIdx and to the next excess payer by decrementing the excessIdx.

The loop continues until all users' debts and excess funds have been fully allocated among each other, and the final bill split is returned in the bill dictionary.

### Authentication & routing
`auth.py:`
This is a Python Flask web application with authentication functionality using Flask-Login and SQLAlchemy ORM.

The auth Blueprint is defined to handle login, logout, and sign-up routes.

The login route handles the user authentication by retrieving the email and password from the request form, querying the database for a user with that email, and verifying the password using the check_password_hash function. If the user is authenticated, they are logged in using login_user function with the remember=True parameter and redirected to the views.users page. Otherwise, an appropriate flash message is displayed.

The logout route logs out the current user using logout_user function and redirects them to the login page.

The sign_up route handles user registration. It retrieves the email, first name, and password from the request form and performs validation checks. If the email is already in use, an appropriate flash message is displayed. If the email is less than 4 characters, the first name is less than 2 characters, or the password is less than 7 characters, then an appropriate flash message is displayed. Otherwise, a new user is created with a hashed password using the generate_password_hash function, added to the database, and logged in using login_user function with the remember=True parameter. Finally, an appropriate flash message is displayed, and the user is redirected to the views.users page.

`view.py:`
This code defines a Flask web application that allows users to create and manage transactions with their friends. The application has several routes:

/users: displays the list of current user's friends and allows the user to add new friends.
/: displays the home page where the user can input transactions and view the bill.
/delete-transaction: deletes a specific transaction.
/delete-user: deletes a specific user from the user's friends list.
/flash-copied-text: displays a flash message when the user copies a shareable link.

The application interacts with a SQLite database that stores information about users, transactions, and friends. The code defines a valid_dollar_amount function that checks if a string is a valid dollar amount. The application uses this function to validate user input. The code also imports a bill.py module that contains a function to calculate the bill for each user based on their transactions. The application uses this function to display the current bill for the user. The Flask-Login extension is used to protect certain routes from unauthenticated users.


### Database
`models.py:`
This code defines two SQLAlchemy models, Transaction and User, and sets up their relationships.

The Transaction model has columns for id, user_id (which references the id column of the User model via a foreign key), name, remarks, and cost.

The User model has columns for id, email (which must be unique), password, first_name, and friends. It also has a relationship with the Transaction model, defined by transactions = db.relationship('Transaction'). This allows a user to have multiple transactions associated with them.

The User model also extends the UserMixin class from Flask-Login, which provides default implementations for methods like is_authenticated and get_id.

### Templates & Client-side processing
`base.html:`
This is an HTML template file for a Flask web application. It includes various CSS and JavaScript libraries, such as Bootstrap and jQuery, which provide styling and interactivity to the web pages.

The main body of the file contains a navigation bar with links to different pages, which change depending on whether the user is authenticated or not. The file also includes code for displaying flash messages, which are short messages that can be displayed to the user after certain actions are taken, such as successful login or registration.

The actual content of the web pages is inserted into the template using the {% block content %} and {% endblock %} tags, which allow other files to extend this template and add their own content in the designated area.


`home.html:`
This is a template for a web application that allows users to split expenses and keep track of transactions. The template includes a form where users can input a user name, expense description, and cost, and submit the data to add a new transaction. The template also includes a list of transactions for each user and a section that calculates how much each user owes or is owed by other users.

The code uses the Flask framework's template engine, Jinja2, to dynamically generate HTML content with data from the Flask application's back-end. Specifically, the template extends a base HTML file and defines blocks for the title and content of the page. It also includes a loop that generates a drop-down list of user names for the form, and loops through the transactions of each user to display them in a list.

The most significant part of the code is the section that calculates how much each user owes or is owed by other users. This section uses a nested loop to iterate through the dictionary of payments between users, and it uses conditional logic to determine whether each payment is a debt or a credit. The code also includes a button that allows users to copy the payment information to the clipboard. Finally, the template includes a script that sets the active tab to the first user's payment section when the page loads.

`login.html:`
This code defines a template for a login page. The template extends a base template called "base.html" and defines two blocks: "title" and "content". The "title" block sets the title of the page to "Login".

The "content" block contains a login form with two input fields for the user's email address and password, respectively. The form is set to submit data using the HTTP POST method. The form also includes a submit button with the label "Login".

Overall, this template is used to render a login page where users can enter their credentials to access a protected area of a website or application.

`signup.html:`
This code is a Flask template for a sign-up form. The form allows users to create a new account by providing their email address, first name, and password. The form includes four input fields:

Email Address: This is a required field where the user is expected to enter their email address.

First Name: This is a required field where the user is expected to enter their first name.

Password: This is a required field where the user is expected to enter their chosen password. The password is not displayed on the screen as it is typed for security purposes.

Password (Confirm): This is a required field where the user is expected to re-enter their password to confirm it. This field helps prevent typos or mistakes when entering the password.

There is also a "Submit" button that the user can click to submit the form. Once submitted, the data from the form is sent to the server for processing.

`users.html:`
This code defines a web page that displays a list of users and allows the user to add or delete users from the list. The page is rendered by extending a base template called "base.html".

The main content of the page is contained within a block called "content". The block contains an HTML form that allows the user to add a new user to the list. The form has a text input field and a "Add User" button.

Below the form, the page displays a list of existing users in a "ul" element. Each user is displayed as a list item ("li") with a "span" element containing the user's name and a delete button ("button") with an "onclick" event that calls a JavaScript function to delete the user from the list.

At the bottom of the page, there is a "Done" button that redirects the user back to the home page ("/") when clicked.

The page expects to receive data from the server via a POST request, including a list of users to display and any new users to add.

`style.css:`
This is CSS code that defines two style rules:
.userInput sets the width of an input field to 100%.
.active changes the text color and background color of an element to black and light gray, respectively. The !important keyword is used to override any other styles that may be applied to the same element.

`index.js:`
1. deleteTransaction(transactionId): Sends a request to the server to delete a transaction with a given ID, and then redirects the user to the home page.
2. openPeople(peopleName): Shows the content of a tab with a given name (peopleName) while hiding the contents of all other tabs. Also applies the "active" class to the selected tab and removes it from all other tabs.
3. deleteUser(name): Sends a request to the server to delete a user with a given name, and then redirects the user to the Users page.
4. copyText(elementId): Copies the text content of an HTML element with a given ID to the clipboard, and then sends the copied text to the server to be stored temporarily. After that, it redirects the user to the home page.




