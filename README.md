# PLUTUSFI Market Maker

## RUN SERVER

application developed using web technologies like django and rest api.

### config environment file

Create an .env file in the project root and add the following variables for project initialization.

    # case utilize SQLITE db
    DATABASE_URL="sqlite:///db.sqlite3"
    # case utilize MySQL db
    DATABASE_URL="mysql://user:password@host:port/db_name"
    
    ALLOWED_HOSTS="*," # for allow all hosts
    ALLOWED_HOSTS="127.0.0.1, localhost" # for allow localhost only
    CORS_ALLOWED_ORIGINS="http://127.0.0.1:8000,

### Logger

    This version need permission to write /var/log in linux systens.
    Logger have an configuration file at markertmaker package, they are *.ini files
