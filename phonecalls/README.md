
# Phone Call Project

## Description



## Setup

This project runs over python **3.5** version.

This section doesn't cover environment setup. Just make sure the **python3.5** command is available on your path and the *dependencies are installed*.


### Installing dependencies

The dependencies are split in production and development. Install the development dependencies using the command:

    python3.5 -m pip install -r requirements/development.txt

This will install the production dependencies plus the development packages, such as *coverage* and *flake8* tools.


### Configure .env file

Create and configure .env file inside phonecalls path. Add the in .env file configuration, example:
   
   DEBUG=on
   SECRET_KEY=8ag1(#)igb)6nw!idtly0ka#+i_@i=m)%83^60lns3kbq*$ko4
   DATABASE_URL=psql://user:password@ip:port/databasename


### Testing

You can execute the project tests available on **tests/** folder by invoking Makefile command *test*:

    make test

This command invokes **pytest** to discover tests around the project working folder, execute them and show the code coverage.

**ATTENTION**: Make sure the dependencies are installed.


### Running

    make run

This command invokes **migrate** followed by **runserver** django command.


### API Documentation

For api documentation see:

    http://localhost:8000/api/docs/


### Work environment

Computer and system

    |-----------------------|----------------------------------------------------|
    | Computer              | Core i3, 4GB memory and 30gb ssd                   |
    | Operational system    | Linux ubuntu 15.04                                 |
    | Text editor           | Sublime Text build 3126                            |


Libraries
    
    |        Lib                | Version   |
    |---------------------------|-----------|
    | Django                    | 2.0.5     |
    | djangorestframework       | 3.8.2     |
    | python-dateutil           | 2.7.3     | 
    | coreapi                   | 2.3.3     |
    | django-filter             | 1.1.0     |
    | psycopg2                  | 2.7.4     |
    | django-environ            | 0.4.4     |
    | pytest                    | 3.6.1     |
    | pytest-cov                | 2.5.1     |
    | pytest-django             | 3.1.2     |
    | pytest-flakes             | 3.0.2     |
    | pytest-pythonpath         | 0.7.2     |
    | pytest-sugar              | 0.9.1     |