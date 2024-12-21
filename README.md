# Server Monitor Project

## Overview
The **Server Monitor Project** is a real-time web-based application designed to monitor server performance metrics, manage processes, and display system logs and user activity. It provides a graphical interface and uses WebSockets for live updates. The backend is powered by Python with the `aiohttp` library, and it integrates various system tools to gather detailed server statistics.

## Features
- **Real-time Statistics:** Displays live CPU, memory, and disk usage, along with system load averages and uptime.
- **Process Management:** Lists top processes sorted by CPU, memory, or PID usage.
- **System Logs:** Displays the last 50 lines of system logs.
- **User Activity:** Shows the last 10 logged-in users and currently logged-in users.
- **Secure Authentication:** Basic authentication is required to access the monitor page.
- **Responsive Design:** User-friendly and visually appealing interface designed with HTML and CSS.

## Prerequisites
- Python 3.7+
- `aiohttp` library
- `psutil` library
- SSL certificate and private key for secure connections

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install the required Python packages:
   ```bash
   pip install aiohttp psutil
   ```
3. Place your SSL certificate and private key in the appropriate directory:
   - **Certificate file:** `cert/localhost.crt`
   - **Key file:** `cert/localhost.key`

## Usage
1. Start the server:
   ```bash
   python <filename>.py
   ```
2. Open a web browser and navigate to:
   ```
   https://localhost:8765/monitor
   ```
3. Log in using one of the following credentials:

   | Username | Password |
   |----------|----------|
   | admin    | password |
   | yigit    | 123456   |
   | deneme   | deneme   |
   | elayadi  | 654321   |

4. View live server statistics and manage processes.

## Project Structure
```
<project-folder>/
├── monitor.html          # Frontend interface
├── <filename>.py         # Main Python application
├── cert/
│   ├── localhost.crt     # SSL certificate
│   └── localhost.key     # SSL private key
```

## API Endpoints
### HTTP Endpoints
- `/hello`: Basic test endpoint that returns a "Hello" response.
- `/monitor`: Serves the monitoring HTML page (requires authentication).

### WebSocket Endpoint
- `/ws`: WebSocket endpoint for real-time updates. Sends system statistics as JSON.

## System Metrics
- **CPU Usage:** Real-time CPU utilization percentage.
- **Memory Usage:** Total, used, and available memory.
- **Disk Usage:** Total, used, and available disk space.
- **Load Averages:** System load averages over 1, 5, and 15 minutes.
- **Uptime:** Server uptime since the last reboot.

## Security
This application uses Basic Authentication to secure access to the monitoring page. User credentials are hardcoded in the `valid_users` dictionary within the Python script. For production use, replace this mechanism with a more secure authentication method.

## Known Issues
- **System Logs:** Logs retrieval may fail if the file path does not exist or lacks read permissions.
- **Process Data:** Process information may occasionally fail due to system-level changes during execution.

## Future Improvements
- Add process management functionality (e.g., kill or restart processes).
- Integrate advanced authentication methods (e.g., OAuth or JWT).
- Improve log parsing and presentation with filtering options.
- Extend compatibility with multiple operating systems.

## License
This project is licensed under the MIT License.



