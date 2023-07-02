# bizpole-interview
interview
Question:

Using the API: https://www.boredapi.com/documentation

Create an API driven CRUD application, in which the End-User would register themselves by choosing one of the type:

"education",
"recreational",
"social",
"diy",
"charity",
"cooking",
"relaxation",
"music",
"busywork"

On successful registration, fetch 10 activities based on the user's selected type and store against the User
and send a welcome mail to the User.

List the Activities on the Activities Listing Page, with 3 activities per page.

The User should have the option to fetch more activities, with a limit of no more than 2 activities per day.
If the User attempts more, return a warning message.

The User would have the right to edit and update the activity details.
The permissions associated with the Admin would be
- View the Activity
- Delete the Activity

NOTE: The activities associated with a User should be Unique.

Bonus Points:
- captcha Integration on Registration Page
- Data Validation


Example: "Bob", register himself into the application by choosing the "education" type.
He is redirected to the activities page which has a list of 10 activities of the education type 
and also receives a welcome mail from the Application.
"Bob" has the option to fetch more activities, but is limited to 2 new activities per day.
"Bob" could also edit and update the activity attributes but he does not have the privilege to delete the activity.
"Alice" the administrator could view the activities in the application and has the permission to delete any activity.
