# PotoAltered
This project is a work in progress. Contributions and feedback are welcome.

## Features
This app offers a comprehensive solution for tracking your **Altered** collection. Key features include:

- Card Inventory: View a detailed list of all your cards, including their names, sets, and quantities.
- Card Aggregation: Automatically consolidate cards by name, regardless of their edition or condition.
- Missing Cards: Identify which cards you need to complete your collection.
- Excess Cards: Determine cards you have in excess and consider trading or selling.

## How to use

**Pull the docker image**

`docker pull willymaillot87/potoaltered:v1.0`


**Run the docker app**

`docker run -p 8501:8501 willymaillot87/potoaltered:v1.0`


**Use the app** 

* Connect to http://localhost:8501/ on your browser.
* **First time users:** You'll need to obtain a token to download your collection.
