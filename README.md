CS395 Project - System Monitoring
Description

This project monitors system statistics like CPU usage, memory usage, and disk usage. It includes a backend server (in Python) that fetches system stats and a frontend (HTML) that displays them in a web browser.
How to Run the Code

Follow these steps to run the project:
1. Clone the repository

First, clone the project to your local machine:

git clone https://github.com/ygtkync/CS395Project.git
cd CS395Project

2. Install dependencies

Install the necessary Python dependencies. You’ll need Python 3.x installed on your system. Run the following command:

pip install -r requirements.txt

This will install the required libraries, including psutil to fetch system stats.
3. Run the backend server

Start the backend server by running:

python3 src/server.py

The server will start, and it will begin monitoring your system stats.
4. Open the frontend

Open your web browser and go to http://localhost:5000. You should see the system stats displayed in the frontend.
Project Structure

CS395Project/
│
├── src/
│   ├── server.py            # Python backend that fetches system stats
│   ├── monitor.html         # HTML frontend to display stats
│   └── utils.py             # Helper functions for fetching system data
│
├── requirements.txt         # List of required Python libraries
└── README.md                # This file
