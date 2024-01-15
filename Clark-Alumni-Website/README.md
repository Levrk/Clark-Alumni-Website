# README #

## What is this repository for? ##
### Quick summary ###
* This repository tracks all code for the Clark University Student-Alumni Interaction website
* Version: 0.0.1
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

## Housekeeping ##
When developing code for this project, we should implement some standard practices so we have clean, readable code, and a well organized repository. Please add to this list if there's anything you think we should do!
* Before committing and pushing code, please format your python code by running the commands `isort .` and `black -l 100 .`
* Configure your pre-commit settings to use the .pre-commit-config.yaml as this file will run both black and isort for you when you commit. This reduces the manual work you'll need to remember to do. See the Pre-commit section below for more info.
* Commit message should start with the ticket name. For example "SCRUM-7 Added new User model". Jira will automatically turn the SCRUM-7 into a link that navigates to the ticket. This will help ensure that if we are looking through commits, we know exactly which ticket it was a part of.

## How do I get set up? ##
### Getting your local environment set up ###

* Install [Docker](https://www.docker.com/), you may need to restart your computer after installing
* If using Windows, open the command prompt and run `wsl --update`
* All necessary python packages will be installed to the local environment by Docker and do not necessarily need to be installed on your machine. However, you should install `black` and `isort` on your machine. `isort` will organize your python imports alphabetically for organization. And `black` will format your code according to PEP8 standards. Both of these packages will help ensure that our code follows the same format and is easy to read.
+ To run Docker and get the project running on your local environment, open your terminal and `cd` to the project repo folder. 
    + Run `docker-compose up -d --build`
        * This will "build" the environment --> set up the container and install packages from the requirements.txt file. 
    + You can open Docker Desktop and click on "Containers" on the left side of the window, this will show you a visual representation of the active container. You can click on it to see logs and images in the container.
    + Run `docker-compose down` to exit the container
        * You should do this when you're done using the app so that Docker isn't using up CPU power.
    + Run `docker-compose up` to start up the container again
        * This restarts it from an exited state. If the container has been deleted, or if you have made changes to any database models in the code, you will need to rebuild using the `docker-compose up -d --build` command
    + Run `docker-compose exec alumni_backend bash` to enter the container.
        * `alumni_backend` is the name I used for the service, this is configured in the docker-compose.yml file.
        * Aftering entering the container, you can run commands here like you normally would in terminal, but the commands that you run here will only affect the virtual environment that Docker is running.
+ Commands to run inside the Docker container `alumni_backend` service
    + NOTE: I made an alias for `python manage.py` so we don't have to keep typing that out. Instead you can use `m` to do the same thing.
    + `m makemigrations`
        * "migrations" are used in Django to apply changes to a database structure. For example, if you create a new table (referred to as "models" in Django), or edit the fields on an existing table, or delete a table, then you will need to run the makemigrations command for Django to create migration files, which it will use to build the Postgres database. 
    + `m migrate`
        * Use this command to apply migrations. The prior command creates the migration files, and this command will apply them to the database.
    + `m createsuperuser`
        * This command will grant you an admin account in your local environment so that you can login to the backend application. It will ask for a username, email, and password. Since this is a local environment, we aren't concerned about security. So you can enter anything you want. The email doesn't even need to be valid :) We should be more careful if using this command in a production environment, however! I've also included in the startup scripts to create an admin@clarku.edu superuser on startup (password is `admin`). This should be available to you by default on a non-production environment.
+ Accessing our app in your browser
    * The app is configured to use port 8000, so you can navigate to [localhost:8000/admin/](http://localhost:8000/admin/) to access the admin page of Django. Login using the credentials you created in the `createsuperuser` step (or just use the admin user)
    * From here you should see a list of models. You can click on them, create new objects, and edit existing ones.
    * The admin screen is just for administrator use; this page will not be accessible by our end users. It just provides an easy way into the backend of our application.
+ Pre-commit hooks
    * We can use pre-commit hooks to make sure code is formatted properly before committing. So since we're using isort and black, we can use a hook to force those commands to be run. Make sure pre-commit is installed `pip install pre-commit` and make sure `git` is installed (if you're on Windows you may need to use the special git bash terminal to run pre-commit). I have already set up the pre-commit settings in `.pre-commit-config.yaml`, you will just need to run `pre-commit install` to create the `pre-commit` file in your .git folder. This folder is not committed as it just contains local settings.
+ Migration errors
    * I've noticed an issue when I make changes to models and then makemigrations and migrate, and then try to do something that utilizes these new changes. I might be hit with a ProgrammingError or an UndefinedTable error. Usually these errors mean that migrations weren't applied. If migrations were applied and you still get these errors, go into Docker and delete everything in Containers, Images, and Volumes (all are tabs on the left side of the window). Then re-run the build command. I think these errors occur because it didn't refresh the database, and clearing everything else will force it to rebuild from scratch.

## NEXT STEPS ##
* We need to prepare Django settings for production environment.
* Need to finish up documentation for what we have so far.
* There's also a backlog of ticket items we weren't able to complete during this course.

## Who do I talk to? ##

* **Repo owner and admin:** Ivy Palmer ipalmer@clarku.edu
* **Product Owner:** Betty Jean Jaskoviak bjjasko@gmail.com
You can also refer to our [Confluence](https://clarku.atlassian.net/wiki/home) for more info about the team and our processes
