# Python Web Framework - Final Project: the Bookshelf

# About the Project

This is a defense project for the ReactJS course at SoftUni.

## General Description

TheBookshelf is an application aimed at helping people exchange opinions on something we all love - books.

The application is similar to a blog system - users can create authors and books (linked to an author they or another
user has created), belonging to specific genres. Other users can then
view them and interact with them via reviews and likes.

The home page showcases the last three added books in a carousel, together with news, uploaded by admins.

There is a feedback form, available to all logged-in users.

NB! Deleting content cascades through all objects with a ForeignKey to that content.

## Permissions

### General

Logged-in users have full CRUD permissions over the content they have created.

Superusers and staff users see an additional button in the main application, called `Statistics`. It provides
information about the books with most likes and reviews.

### Admin site

There are superusers who have control over all content.

The application is supposed to work with `two permission groups`. Staff users added to one of them - the news moderator
group, have `full CRUD` permissions over the News model entities. The other group - the feedback (quality control) group
includes staff users who have `read only` permissions over the feedback submitted by users.

# Architecture

The project is divided into four separate applications - `accounts`, `book`, `author`, `common`. The application follows
the `MTV` pattern. The application tries to adhere to the readily provided by Django directory and file structure.

## Static files

The `\staticfiles` directory contains a few .css files, imported
into a `base.html`, as well as some static images. Reset.css used is `normalize.css`, taken
from `github.com/necolas/normalize.css`. Box-sizing approach is border-box.

## Templates

All templates for a specific application can be found in a directory dedicated to that application in `\templates`.

## Forms

Each application has a separate `/forms`
directory containing specific form classes inheriting from Django's `Form` \ `ModelForm` \ `UserCreationForm`
\ `AuthenticationForm`. Data validation is handled in those forms.

## Tests

There are unit/integration tests developed, covering some functionality of the `accounts` application, as well as
the `book` application.

The application uses `Bootstrap 5` as a tool for rendering most views.

## Database

The application uses PostgresSQL as a DB solution.

## Models and Views

Models and views are located at the respective `\models.py` and `\views.py` for each application.

Models that users interact with are ordered by descending date of creation.

The AppUser model extends Django's `AbstractBaseUser`. It has its own manager, located in `\accounts\managers.py`,
defining the way in which users and superusers are created. A `signal` is used to instantiate a profile for each user on
the (save) event of new registration.

# Additional Information

The application implements 404 error handling, using handler404 at the project level urls.

# Running the application

Make sure venv is activated. To activate venv, use the command `venv\Scripts\activate`.

To run the application with all staticfiles and css and see the 404 error handling functionality, the project needs to
be started with `DEBUG=False` in `settings.py` with the command `python manage.py runserver --insecure`. Note, that this
command is suitable for development usage only.

To link a postgresSQL database, you will need to fill in your DB credentials in `settings.py` and then
run `python manage.py migrate`.

## Dependencies

    asgiref==3.5.2 
    beautifulsoup4==4.11.1
    Django==4.1.3
    django-bootstrap-v5==1.0.11
    psycopg2-binary==2.9.5
    reverse==0.1.0
    soupsieve==2.3.2.post1
    sqlparse==0.4.3
    tzdata==2022.6

