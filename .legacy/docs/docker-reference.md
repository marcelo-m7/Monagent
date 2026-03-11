# Docker Quick Reference

## Building

```bash
# Build the image
docker build -t monagent:latest .

# Build with no cache
docker build --no-cache -t monagent:latest .

# Build with specific tag
docker build -t monagent:v1.0.0 .
```

## Running

```bash
# Run with environment file
docker run -d --name monagent-api -p 8000:8000 --env-file .env monagent:latest

# Run with individual environment variables
docker run -d --name monagent-api -p 8000:8000 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_ANON_KEY=your-key \
  -e SUPABASE_SERVICE_ROLE_KEY=your-service-key \
  -e SUPABASE_SCHEMA=monagent \
  monagent:latest

# Run interactively (for debugging)
docker run -it --rm -p 8000:8000 --env-file .env monagent:latest sh
```

## Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View logs
docker logs monagent-api

# Follow logs
docker logs -f monagent-api

# Stop container
docker stop monagent-api

# Start container
docker start monagent-api

# Restart container
docker restart monagent-api

# Remove container
docker rm monagent-api

# Remove container (force)
docker rm -f monagent-api
```

## Health & Inspection

```bash
# Check container health
docker inspect --format='{{json .State.Health}}' monagent-api | jq

# Execute command in running container
docker exec -it monagent-api sh

# Check container stats
docker stats monagent-api

# View container processes
docker top monagent-api
```

## Docker Compose

```bash
# Start services
docker-compose up -d

# Start and rebuild
docker-compose up -d --build

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove, and remove volumes
docker-compose down -v

# View service status
docker-compose ps

# Restart a service
docker-compose restart monagent

# Scale service (run multiple instances)
docker-compose up -d --scale monagent=3
```

## Cleanup

```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune

# Remove all (including volumes)
docker system prune -a --volumes
```

## Production Tips

```bash
# Export environment variables from .env
set -a && source .env && set +a  # Linux/Mac
# Then use in docker run commands

# Check available memory for container
docker run --memory=512m --memory-swap=512m ...

# Set CPU limits
docker run --cpus="1.5" ...

# Run with restart policy
docker run --restart=unless-stopped ...

# Check image size
docker images monagent
```

## Debugging

```bash
# Run with debug output
docker-compose up

# Check Dockerfile syntax
docker build --check -t monagent:latest .

# Inspect image layers
docker history monagent:latest

# Test health check manually
docker exec monagent-api python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read())"
```
