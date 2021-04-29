Milestone 3

Add these new functions to your task application to help users to track time spent on completion of each task. 
User will start time when start working on task and stop it when complete the task or take a pause.

~~1. Start a timer for my task - user send task id and receive successful response after logging the start of task in DB~~
~~2. Stop timer for the started task - user send task id and receive successful response after adding a time log for this task with duration of work for current date~~
3. Add time log for a task on a specific date - user manually send in task id, date, duration in minutes and receive successful response of save
4. Get a list of time logs records by task - user send task id and receive list of all time logs created for this task
5. Change get list of tasks endpoint get receive the sum of the time in minutes for each task
6. Get the logged time in last month - user send a request and receive total amount of time logged by him in last month
7. Get top 20 tasks in last month by time - user send request and receive list of id, title, time amount of tasks with bigger logged amount of time