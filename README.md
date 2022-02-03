# Simple Task Logger API

### Setup

Some steps before start work on tasks.

1. Install python requirements ```pip install -r requirements.txt```
2. Database is SQLite, local, and execute ```python manage.py migrate```
3. Start the project ```python manage.py runserver```
4. In swagger click "Authorize" button and type ```<access token from response>```

### Milestone 1

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

### Milestone 2

Add these new functions to your task application to help users to track time spent on completion of each task.
User will start time when start working on task and stop it when complete the task or take a pause.

1. Start a timer for my task - user send task id and receive successful response after logging the start of task in DB
2. Stop timer for the started task - user send task id and receive successful response after adding a time log for this task with duration of work for current date
3. Add time log for a task on a specific date - user manually send in task id, date, duration in minutes and receive successful response of save
3. Get a list of time logs records by task - user send task id and receive list of all time logs created for this task 
4. Change get list of tasks endpoint get receive the sum of the time in minutes for each task
5. Get the logged time in last month - user send a request and receive total amount of time logged by him in last month
6. Get top 20 tasks in last month by time - user send request and receive list of id, title, time amount of tasks with bigger logged amount of time

### Milestone 3

In this milestone we start to improve our application.

1. Add unit tests for each endpoint
2. Add coverage package and generate report to be sure in 100% test coverage
3. Install PostgreSQL docker container and move your app on PostgreSQL
4. Create a script that will add random 25.000 tasks and 50.000 time logs
4. Install PGHero docker container and connect it to your db
5. Manual test all endpoints and check with PGHero that all sql queries use db indexes
6. Install Redis docker container and configure Django to cache with 1 minute TTL the endpoint with Top 20 tasks by time for each user
7. Create Dockerfile for your application to run it with docker-compose command
