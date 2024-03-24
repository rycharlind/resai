# ResAI Docker

## Docker Compose:
- Start service: `docker-compose up -d postgres`
- Build and start: `docker-compose up postgres --build` - Run this if you make changes to `Dockerfile.postgres`
- Stop service: `docker-compose down postgres`
- Get container id: `docker ps -f name=postgres`
- Shell into container: `docker exec -it 9c7f64c91add bash`

## PostgresSQL Config
See `postgressql.conf` in this dir.