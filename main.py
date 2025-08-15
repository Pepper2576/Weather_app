from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from api import fetch_weather
from db.querys import add_weather_data
from dotenv import load_dotenv
import os

load_dotenv()

hostName = os.getenv("HOST", "localhost")
portNumber = int(os.getenv("PORT", "8080"))
number_of_requests = 0

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<!DOCTYPE html><html><head><title>My Server</title></head><body>')
        self.wfile.write(b'<h1>Hello, World!</h1>')
        self.wfile.write(b'</body></html>')
        print(f"GET request received at {self.path}")
    
if __name__ == "__main__":
    webServer = HTTPServer((hostName, portNumber), MyServer)
    print(f"Server started at http://{hostName}:{portNumber}")
    
    weather_data = fetch_weather(-1.179443426, 52.831503918)  # longitude, latitude
    print(f"Weather data: {weather_data}")
    add_weather_data(weather_data['time'], weather_data['temperature'])
    number_of_requests += 1
    print(f"Number of requests: {number_of_requests}")
    
    try:
        while True:
            time.sleep(43200)  # Sleep for 12 hours 
            print("Running daily task...")
            
            # Fetch weather data using the imported function
            weather_data = fetch_weather(-1.179443426, 52.831503918)  # longitude, latitude
            add_weather_data(weather_data['time'], weather_data['temperature'])  # Adjust based on your weather_data structure
            print(f"Weather data added to database: {weather_data}")
            
            number_of_requests += 1
            print(f"Number of requests: {number_of_requests}")
    except KeyboardInterrupt:
        print("Server stopped")
        webServer.server_close()