-- Initialize the weather database with required table
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the date column for better query performance
CREATE INDEX IF NOT EXISTS idx_weather_data_date ON weather_data(date);

-- Insert a sample record to verify the table is working
-- INSERT INTO weather_data (date, temperature) VALUES (NOW(), 20.5);