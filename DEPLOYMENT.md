# Weather App Deployment Guide for Raspberry Pi 4

This guide will help you deploy the Weather App on your Raspberry Pi 4 using Docker and Docker Compose.

## Prerequisites

1. Raspberry Pi 4 with Raspberry Pi OS installed
2. Docker and Docker Compose installed on your Raspberry Pi
3. Internet connection

## Installing Docker on Raspberry Pi

If you haven't installed Docker yet, run these commands:

```bash
# Install Docker
curl -sSL https://get.docker.com | sh

# Add your user to the docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt-get install -y docker-compose

# Reboot to apply changes
sudo reboot
```

## Deployment Steps

### 1. Clone or Copy the Project

Transfer your Weather_app directory to your Raspberry Pi:

```bash
# If using git
git clone <your-repo-url>
cd Weather_app

# Or use scp to copy from your computer
# scp -r Weather_app pi@<raspberry-pi-ip>:~/
```

### 2. Create the .env File

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:

```bash
nano .env
```

Update the following variables:
- `PASSWORD`: Change to a secure password
- `HOST`: Keep as `0.0.0.0` to accept connections from any interface
- `PORT`: Default is `8080`, change if needed
- `DB_HOST`: Keep as `postgres` (this is the Docker service name)
- `DATABASE`: Database name (default: `weather_db`)
- `USER`: Database user (default: `weather_user`)

### 3. Build and Start the Containers

Run the following command to build and start both the database and the weather app:

```bash
docker-compose up -d
```

This command will:
- Pull the PostgreSQL image
- Build your weather app Docker image
- Create the database with the schema from `db/init.sql`
- Start both containers
- Set up automatic restart policies

### 4. Verify the Deployment

Check if the containers are running:

```bash
docker-compose ps
```

You should see two containers:
- `weather_db` (PostgreSQL)
- `weather_app` (Your application)

View the logs:

```bash
# View all logs
docker-compose logs

# View weather app logs only
docker-compose logs weather_app

# Follow logs in real-time
docker-compose logs -f weather_app
```

### 5. Test the Application

Access the web server:

```bash
curl http://localhost:8080
```

Or from another device on your network:
```
http://<raspberry-pi-ip>:8080
```

### 6. Check Database Data

To verify data is being stored in the database:

```bash
# Connect to PostgreSQL container
docker-compose exec postgres psql -U weather_user -d weather_db

# Run a query to see stored data
SELECT * FROM weather_data ORDER BY created_at DESC LIMIT 10;

# Exit psql
\q
```

## Managing the Application

### Stop the Application

```bash
docker-compose stop
```

### Start the Application

```bash
docker-compose start
```

### Restart the Application

```bash
docker-compose restart
```

### Stop and Remove Containers

```bash
docker-compose down
```

### Stop and Remove Everything (Including Data)

**WARNING**: This will delete all stored weather data!

```bash
docker-compose down -v
```

### Update the Application

If you make changes to the code:

```bash
# Rebuild and restart
docker-compose up -d --build
```

### View Resource Usage

```bash
docker stats
```

## Troubleshooting

### Container Won't Start

Check the logs:
```bash
docker-compose logs weather_app
```

### Database Connection Issues

1. Ensure the database container is healthy:
```bash
docker-compose ps
```

2. Check database logs:
```bash
docker-compose logs postgres
```

3. Verify environment variables:
```bash
docker-compose config
```

### Port Already in Use

If port 8080 is already in use, change the `PORT` variable in your `.env` file and restart:

```bash
docker-compose down
docker-compose up -d
```

### Permission Issues

If you encounter permission errors:

```bash
sudo chown -R $USER:$USER .
```

## Automatic Startup on Boot

Docker containers with `restart: unless-stopped` will automatically start when your Raspberry Pi boots up.

To enable Docker to start on boot:

```bash
sudo systemctl enable docker
```

## Backup Database

To backup your weather data:

```bash
docker-compose exec postgres pg_dump -U weather_user weather_db > backup_$(date +%Y%m%d).sql
```

To restore from backup:

```bash
cat backup_20250101.sql | docker-compose exec -T postgres psql -U weather_user -d weather_db
```

## Monitoring

The application fetches weather data every 12 hours. You can monitor this by watching the logs:

```bash
docker-compose logs -f --tail=50 weather_app
```

## Performance Considerations for Raspberry Pi

- The application uses PostgreSQL Alpine image for lower resource usage
- Python slim image keeps the container lightweight
- Data is persisted in Docker volumes for reliability
- Logs directory is mounted for easy access

## Network Access

To access your weather app from outside your local network:
1. Configure port forwarding on your router (forward port 8080 to your Raspberry Pi's IP)
2. Consider setting up a dynamic DNS service
3. For security, consider setting up a reverse proxy with SSL/TLS

## Support

For issues or questions, check the logs first:
```bash
docker-compose logs --tail=100
```
