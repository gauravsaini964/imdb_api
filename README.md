# IMDB Movie Scrapper/ RestAPI

Project is a collection of RestAPI which allows user to register and add movies to their to-be-watched list or already watched list. APIs allows use to see his stats like total time spend on watching all the movies in minutes.

# Tech Stack

1.  Python 3.8.2
2.  Django 2.2
3.  Beautiful Soup for scraping
4.  DjangoRestFramework
5.  JWT for Auth

## Steps to run

- Method 1

      	 1. Clone the project
      	 2. Make new virtual env based on python 3.8.2
      	 3. Activate virtual env
      	 4. Run "pip install -r requirements.txt" inside virtual env
      	 5. Run "python manage.py migrate" in root folder
      	 6. Run "python manage.py runserver" to start application server'

* Method 2: Using Dockerfile - In root directory execute "docker build -t yourDockerUsername/imdbApp -f Dockerfile.dev ." - Then run "docker run -p 8000:8000 yourDockerUsername/imdbApp"

- Method 3: Using Docker-Compose - Run "docker-compose up -build" for first run. - For subsequent run, execute "docker-compose up".

## API List

The project contains 10 APIs in total.
Here is the postman collection for the APIs:
[API - Collection](https://www.getpostman.com/collections/82689d6d2e1e640deeff)

## Steps to populate Movies table

- Method 1: - After step 6 in "Steps to run" section - Use API "3. Scrapper API" from the collection shared \*_API might time out depending upon your network speed, as ingestion from IMDB takes time. Will optimize this by using celery/redis queue. See todo list_
- Method 2: - After step 5 in "Steps to run" section - Run "python manage.py shell" to open python shell - Execute following code:
  `from api.utils.data_ingestion import DataIngestion #imports DataIngestion class data_ingest = DataIngestion("https://www.imdb.com/chart/top/") data.fetch_movie_data()`

## ToDo

- [x] Dockerize this application
- [ ] Add Celery for data ingestion async task
- [ ] Use Redis to fetch movies name for user's history
- [ ] Heroku Deployment
