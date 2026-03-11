# Production Deployment Checklist

## Pre-Deployment

### Environment Setup
- [ ] Create production `.env` file with real values
- [ ] Set `ENV=production`
- [ ] Configure Supabase production URL
- [ ] Set up Supabase service role key (keep secure!)
- [ ] Verify Supabase schema name matches configuration
- [ ] Never commit `.env` file to version control

### Database Setup
- [ ] Run `scripts/lead.sql` in Supabase SQL editor
- [ ] Verify `monagent` schema exists
- [ ] Verify `leads` table created successfully
- [ ] Test unique email constraint
- [ ] Confirm Row Level Security (RLS) is enabled
- [ ] Set up appropriate RLS policies for your use case
- [ ] Create database backups schedule in Supabase

### Security
- [ ] Keep `SUPABASE_SERVICE_ROLE_KEY` secret
- [ ] Use environment variables (never hardcode secrets)
- [ ] Enable HTTPS in production
- [ ] Configure CORS if needed
- [ ] Review and set appropriate rate limits
- [ ] Enable firewall rules if applicable

## Docker Deployment

### Build Process
- [ ] Test Docker build locally: `docker build -t monagent:latest .`
- [ ] Verify image size is reasonable
- [ ] Test container runs: `docker run -d -p 8000:8000 --env-file .env monagent:latest`
- [ ] Test health endpoint: `curl http://localhost:8000/health`
- [ ] Test leads endpoint with sample data

### Container Configuration
- [ ] Configure restart policy (`unless-stopped` or `always`)
- [ ] Set appropriate memory limits
- [ ] Set CPU limits if needed
- [ ] Configure logging driver (json-file, syslog, etc.)
- [ ] Set up log rotation

### Networking
- [ ] Open port 8000 (or your chosen port)
- [ ] Configure reverse proxy (NGINX/Caddy) for HTTPS
- [ ] Set up domain/subdomain DNS
- [ ] Configure SSL certificates (Let's Encrypt)
- [ ] Test external access

## Cloud Platform Deployment

### Railway
- [ ] Install Railway CLI: `npm i -g @railway/cli`
- [ ] Login: `railway login`
- [ ] Initialize project: `railway init`
- [ ] Add environment variables in Railway dashboard
- [ ] Deploy: `railway up`
- [ ] Configure custom domain if needed

### Fly.io
- [ ] Install Fly CLI
- [ ] Login: `fly auth login`
- [ ] Launch: `fly launch`
- [ ] Add secrets: `fly secrets set KEY=value`
- [ ] Deploy: `fly deploy`
- [ ] Configure custom domain if needed

### Render
- [ ] Connect GitHub repository
- [ ] Select "Docker" environment
- [ ] Add all environment variables
- [ ] Configure auto-deploy on push
- [ ] Set up custom domain if needed

### DigitalOcean / AWS / GCP
- [ ] Provision VM/Container instance
- [ ] Install Docker and Docker Compose
- [ ] Clone repository or copy files
- [ ] Set up `.env` file
- [ ] Run with Docker Compose
- [ ] Configure firewall rules
- [ ] Set up monitoring

## Post-Deployment

### Verification
- [ ] Test health endpoint: `curl https://your-domain.com/health`
- [ ] Test API documentation: `https://your-domain.com/docs`
- [ ] Submit test lead via API
- [ ] Verify lead appears in Supabase
- [ ] Test with real UTM parameters
- [ ] Verify IP and user agent capture

### Monitoring
- [ ] Set up application monitoring (Sentry, DataDog, etc.)
- [ ] Configure uptime monitoring (UptimeRobot, Pingdom, etc.)
- [ ] Set up log aggregation (if needed)
- [ ] Configure alerts for downtime
- [ ] Monitor database connection pool
- [ ] Watch for API response times

### Performance
- [ ] Load test the API (use tools like `wrk` or `ab`)
- [ ] Verify 4 Uvicorn workers are running
- [ ] Monitor memory usage under load
- [ ] Check database query performance
- [ ] Optimize slow endpoints if needed

### Backup & Recovery
- [ ] Set up automated database backups
- [ ] Test backup restoration process
- [ ] Document recovery procedures
- [ ] Keep `.env` backup in secure location
- [ ] Version control your deployment configs

## Maintenance

### Regular Tasks
- [ ] Review logs weekly
- [ ] Monitor error rates
- [ ] Check for dependency updates
- [ ] Review and clean old leads (if applicable)
- [ ] Monitor disk usage
- [ ] Check SSL certificate expiration

### Updates
- [ ] Test updates in staging first
- [ ] Build new Docker image
- [ ] Tag with version number
- [ ] Deploy to production
- [ ] Verify health checks pass
- [ ] Monitor for errors after deployment
- [ ] Be ready to rollback if needed

## Rollback Plan

If something goes wrong:
```bash
# Docker Compose
docker-compose down
docker-compose up -d --build

# Or rollback to previous image
docker tag monagent:v1.0.0 monagent:latest
docker-compose up -d
```

## Environment Variables Reference

Required for production:
```env
ENV=production
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxxxx...  # Keep secret!
SUPABASE_SCHEMA=monagent
```

## Support & Troubleshooting

### Common Issues

**Container won't start:**
- Check logs: `docker logs monagent-api`
- Verify environment variables are set
- Check port conflicts: `lsof -i :8000`

**Database connection fails:**
- Verify Supabase URL is correct
- Check API keys are valid
- Ensure schema exists in Supabase
- Verify network connectivity

**Health check fails:**
- Check if app is running: `docker exec monagent-api ps aux`
- Test manually: `curl http://localhost:8000/health`
- Review application logs

**Performance issues:**
- Increase Uvicorn workers
- Check database indexes
- Monitor memory/CPU usage
- Consider horizontal scaling

## Contact

For deployment support:
- Email: marcelo@monynha.com
- GitHub Issues: https://github.com/marcelo-m7/Monagent/issues
