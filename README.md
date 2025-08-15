# Weather Data Collection Application

A Python application that automatically collects weather data every 12 hours using the Open-Meteo API and stores it in a PostgreSQL database. The application also runs a simple HTTP server for basic web functionality.

## Features

- **Automated Weather Data Collection**: Fetches weather data every 12 hours
- **Database Storage**: Stores weather data in PostgreSQL database
- **HTTP Server**: Simple web server with basic HTML response
- **Environment Configuration**: Uses `.env` file for configuration
- **Error Handling**: Graceful shutdown with keyboard interrupt

## Project Structure

```
weather_app/
├── main.py           # Main application entry point
├── api.py            # Weather API integration
├── db/
│   └── querys.py     # Database operations
├── README.md         # This documentation
└── .env              # Environment variables (not included in repo)
```

## Requirements

- Python 3.x
- PostgreSQL database
- Required Python packages:
  - `requests` - For API calls
  - `psycopg2` - PostgreSQL adapter
  - `python-dotenv` - Environment variable management

## Installation

1. **Clone or download the project files**

2. **Install required packages:**

   ```bash
   pip install requests psycopg2-binary python-dotenv
   ```

3. **Set up PostgreSQL database:**

   - Create a database named according to your `.env` configuration
   - Create a table for weather data:

   ```sql
   CREATE TABLE weather_data (
       id SERIAL PRIMARY KEY,
       date TIMESTAMP,
       temperature DECIMAL
   );
   ```

4. **Create a `.env` file in the project root:**

   ```env
   # HTTP Server Configuration
   HOST=localhost
   PORT=8080

   # Database Configuration
   DATABASE=weather_db
   USER=your_username
   PASSWORD=your_password
   ```

## File Descriptions

### main.py

The main application file that:

- Sets up an HTTP server using Python's built-in `HTTPServer`
- Fetches weather data immediately on startup
- Runs a continuous loop that collects weather data every 12 hours
- Stores weather data in the PostgreSQL database
- Handles graceful shutdown with Ctrl+C

**Key Features:**

- Uses environment variables for configuration
- Tracks number of API requests made
- Provides console logging for monitoring

### api.py

Contains the weather API integration:

- `fetch_weather(longitude, latitude)` function
- Connects to Open-Meteo API (https://api.open-meteo.com/)
- Returns structured weather data including:
  - Latitude and longitude
  - Timestamp
  - Current temperature

**API Response Format:**

```python
{
    "latitude": float,
    "longitude": float,
    "time": "YYYY-MM-DDTHH:MM",
    "temperature": float
}
```

### db/querys.py

Database operations module:

- Establishes PostgreSQL connection using environment variables
- `add_weather_data(date, temperature)` function for inserting weather records
- Handles database commits and provides success confirmation

## Usage

1. **Start the application:**

   ```bash
   python main.py
   ```

2. **The application will:**

   - Start an HTTP server on the configured host and port
   - Immediately fetch and store weather data
   - Continue fetching weather data every 12 hours
   - Log all activities to the console

3. **Access the web server:**

   - Open browser to `http://localhost:8080` (or your configured host/port)
   - Returns a simple "Hello, World!" HTML page

4. **Stop the application:**
   - Press `Ctrl+C` to gracefully shutdown

## Configuration

The application uses the following environment variables:

| Variable | Description              | Default   | Required |
| -------- | ------------------------ | --------- | -------- |
| HOST     | HTTP server host         | localhost | No       |
| PORT     | HTTP server port         | 8080      | No       |
| DATABASE | PostgreSQL database name | -         | Yes      |
| USER     | PostgreSQL username      | -         | Yes      |
| PASSWORD | PostgreSQL password      | -         | Yes      |

## Location Configuration

Currently configured to collect weather data for:

- **Latitude**: 52.831503918
- **Longitude**: -1.179443426

To change the location, modify the coordinates in the `fetch_weather()` calls in `main.py`.

## Data Collection Schedule

- **Initial Collection**: Runs immediately when application starts
- **Recurring Collection**: Every 12 hours (43,200 seconds)
- **Data Stored**: Date/time and temperature in Celsius

## Error Handling

- **Database Connection**: Will fail if PostgreSQL is not running or credentials are incorrect
- **API Failures**: Handled in `api.py` with error response format
- **Keyboard Interrupt**: Graceful shutdown of HTTP server and application

## Monitoring

The application provides console output for:

- Server startup confirmation
- Weather data fetch results
- Database insertion confirmations
- Request counting
- Task execution timing

## Future Enhancements

**Planned AI Integration:**

- Integrate with an open-source AI model to evaluate collected weather data and generate predictions
- Store AI predictions in a separate database for comparison analysis
- Create analytics dashboard to compare predicted vs actual weather data
- Implement accuracy metrics and model performance tracking

**Additional Improvements:**

- Consider changing collection frequency (currently every 12 hours)
- Add more robust error handling and logging
- Implement comprehensive data visualization features
- Add API endpoints for retrieving stored weather data and predictions
