-- Create the weather_data table
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the date column for faster queries
CREATE INDEX IF NOT EXISTS idx_weather_date ON weather_data(date);

-- Create an index on created_at for chronological queries
CREATE INDEX IF NOT EXISTS idx_weather_created_at ON weather_data(created_at);
