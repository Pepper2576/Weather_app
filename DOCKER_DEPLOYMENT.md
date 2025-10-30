# Docker Deployment Guide for Raspberry Pi

This guide explains how to deploy the Weather Data Collection Application on a Raspberry Pi using Docker Compose.

## Prerequisites

1. **Raspberry Pi** with Raspberry Pi OS installed
2. **Docker and Docker Compose** installed on the Pi:

   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Add your user to docker group
   sudo usermod -aG docker $USER

   # Install Docker Compose
   sudo apt-get update
   sudo apt-get install docker-compose-plugin
   ```

## Deployment Steps

1. **Copy the application files** to your Raspberry Pi:

   ```bash
   # If using SCP from your development machine:
   scp -r Weather_app/ pi@your-pi-ip:/home/pi/
   ```

2. **Navigate to the application directory**:

   ```bash
   cd /home/pi/Weather_app
   ```

3. **Create environment file** (optional - defaults are set in docker-compose.yaml):

   ```bash
   cp .env.example .env
   # Edit .env if you want to change any settings
   nano .env
   ```

4. **Build and start the application**:

   ```bash
   docker compose up -d
   ```

5. **Check the status**:
   ```bash
   docker compose ps
   docker compose logs -f weather-app
   ```

## Services

The Docker Compose setup includes:

### PostgreSQL Database (`postgres`)

- **Image**: postgres:15-alpine (ARM64 compatible)
- **Port**: 5432
- **Database**: weather_db
- **Username**: weather_user
- **Password**: weather_password
- **Data**: Persisted in Docker volume `postgres_data`

### Weather Application (`weather-app`)

- **Port**: 8080
- **Environment**: Configured for container networking
- **Depends on**: PostgreSQL database
- **Restart**: Automatically restarts unless stopped

## Accessing the Application

- **Web Interface**: http://your-pi-ip:8080
- **Database**: Connect to PostgreSQL on port 5432 if needed

## Management Commands

### View logs:

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f weather-app
docker compose logs -f postgres
```

### Stop the application:

```bash
docker compose down
```

### Update the application:

```bash
# Stop services
docker compose down

# Rebuild and start
docker compose up -d --build
```

### View database data:

```bash
# Connect to PostgreSQL container
docker compose exec postgres psql -U weather_user -d weather_db

# Run SQL queries
SELECT * FROM weather_data ORDER BY date DESC LIMIT 10;
```

## Data Persistence

- **Database data**: Stored in Docker volume `postgres_data`
- **Application logs**: Can be accessed via `docker compose logs`
- **Database initialization**: Handled automatically via `init.sql`

## Troubleshooting

### Check if services are running:

```bash
docker compose ps
```

### Check logs for errors:

```bash
docker compose logs weather-app
docker compose logs postgres
```

### Restart a specific service:

```bash
docker compose restart weather-app
docker compose restart postgres
```

### Clean restart (removes volumes):

```bash
docker compose down -v
docker compose up -d
```

### Check database connection:

```bash
docker compose exec postgres pg_isready -U weather_user -d weather_db
```

## Customization

### Change location coordinates:

Edit `main.py` and modify the latitude/longitude values in the `fetch_weather()` calls.

### Change collection frequency:

Edit `main.py` and modify the `time.sleep(43200)` value (currently 12 hours).

### Database configuration:

Modify the environment variables in `docker-compose.yaml` or create a `.env` file.

## Monitoring

The application logs all activities to the console, which can be viewed with:

```bash
docker compose logs -f weather-app
```

Key log messages include:

- Server startup confirmation
- Weather data fetch results
- Database insertion confirmations
- Request counting and timing

## Performance on Raspberry Pi

This setup is optimized for Raspberry Pi:

- Uses Alpine Linux base images for smaller footprint
- ARM64 compatible images
- Minimal resource usage
- Automatic restart on failure

The application should run smoothly on Raspberry Pi 3B+ or newer models.
