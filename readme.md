# Flask API

API for the application of genetic algorithms in tourism

## Dependencies

- [flask](https://palletsprojects.com/p/flask/): Python server of choise

## Set Up

1. Check out the code
2. Install requirements
    ```
    pip install -r requirements.txt
    ```
3. create the config file named `config.py` 
4. Start the server with:
    ```
    flask run
    ```
   
4. Visit http://127.0.0.1:5000/viajero for consume the api


## Data Collection
This feature needs to improve the scraper app with a framework
1. send a delete request to .../... for flush all the data
2. For fetch scraped data, visit http://localhost:8000/index.html and keep alive the connection for 5 sec until the process finishes
3. Then send a post request to /generate_matrices for consume google maps api service and calculate the matrices
4. Finally, visit http://127.0.0.1:5000/viajero for consume the api 