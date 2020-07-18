# Coffee Cafe Full Stack

## Full Stack Nano - IAM Final Project


The Coffee cafe  is a full stack drink menu application which includes below usage:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.


The project contains two directories for better implementation and isolation

### Backend

The `./backend` directory contains a Flask server with a SQLAlchemy module to simplify your data needs. Includes the required endpoints, configure, and integrate Auth0 for authentication.


### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. Updated environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
