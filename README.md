Register - user send first name, last name, email, password and receive JWT token for authentication
Login - user send email, password and receive JWT token for authentication
Get list of users - user receive a list with id and full name of all users from application
Create a task - user send title, description and receive new task id, the new task is assigned to current user
View list of tasks - user receive a list with id and title of all created tasks from application
View task details by id - user send task_id and receive task details: id, title, description, status, owner
View my tasks - user receive a list with id and title of tasks assigned to him
View Completed tasks - user receive a list with id and title of tasks with status completed
Assign a task to user - user send task_id and user_id and receive successful response after update task owner
Complete a task - user send task_id and receive successful response after update of task status in completed
Remove task - user send task_id and receive successful response after task deletion
Add comment to task - user send task_id, comment text and receive id of the new comment
View task comments - user send task id and receive list of all comments added to this task
Add email notification then task is assigned to me
Add email notification then my task in commented
Add email notification then commented task is completed
Search task by title - user send search term and receive list of tasks that match
