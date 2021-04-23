1. Register - user send first name, last name, email, password and receive JWT token for authentication
2. Login - user send email, password and receive JWT token for authentication
3. Get list of users - user receive a list with id and full name of all users from application
4. Create a task - user send title, description and receive new task id, the new task is assigned to current user
5. View list of tasks - user receive a list with id and title of all created tasks from application
6. View task details by id - user send task_id and receive task details: id, title, description, status, owner
7. View my tasks - user receive a list with id and title of tasks assigned to him
8. View Completed tasks - user receive a list with id and title of tasks with status completed
9. Assign a task to user - user send task_id and user_id and receive successful response after update task owner
10. Complete a task - user send task_id and receive successful response after update of task status in completed
11. Remove task - user send task_id and receive successful response after task deletion
12. Add comment to task - user send task_id, comment text and receive id of the new comment
13. View task comments - user send task id and receive list of all comments added to this task
14. Add email notification then task is assigned to me
15. Add email notification then my task in commented
16. Add email notification then commented task is completed
17. Search task by title - user send search term and receive list of tasks that match
