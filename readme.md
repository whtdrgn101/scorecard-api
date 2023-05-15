# Scorecard API Project
This project is the CRUD API overtop of the scorecard-db project.

## Files

### `api.py`
Main API file which gets invoked from uvicorn or main.py helper file.  Pulls in the route definitions and launches the FastAPI API.  

### `main.py`
Helper file to launch the API in a python debugging environment.

### `requirements.txt`
Contains all the required PIP packages to build a working Python environment.

### `Dockerfile`
Container deffinition file.

## Folder Structure

### `db` 
This folder contains models, dals (data access layers), and config helpers which allow the API to perform the CRUD operations against the database.  The database configuration is controlled by environment variables for DB config:
- SCORECARD_USER -- Database Username
- SCORECARD_PASS -- Database Password
- SCORECARD_HOST -- Host for the database server
- SCORECARD_DB -- Database name on for the scorecard DB

### `routes`
This folder contains the route definitions and route schemas for the API.  Also contains dependency injection helps for the DAL's to allow for better unit testing.

### `deployment`
This folder contains the kubernetes definition as well as the Helm chart