# Flask Notes - Docker Compose Application

A simple, containerized note-taking application built with Flask and MySQL, designed for easy deployment on AWS EC2 instances.

## 🚀 Features

- **Simple Note Management**: Create, read, update, and delete notes
- **Containerized Architecture**: Docker Compose setup with Flask web app and MySQL database
- **Persistent Storage**: MySQL data persisted using Docker volumes
- **Health Checks**: Built-in health monitoring for both web and database services
- **Responsive UI**: Clean, modern interface with dark theme
- **Production Ready**: Optimized for deployment on Amazon Linux EC2

## 🏗️ Architecture

```
┌─────────────┐    HTTP     ┌──────────────┐    MySQL     ┌──────────────┐
│   Browser   │ ──────────► │ Flask Web    │ ───────────► │ MySQL DB     │
│             │             │ Container    │              │ Container    │
└─────────────┘             └──────────────┘              └──────────────┘
                                   │                             │
                                   │        Docker Network       │
                                   └─────────────────────────────┘
```

## 📂 Project Structure

```
flask-notes-compose/
├── app/
│   ├── __init__.py          # Python package marker
│   ├── app.py              # Flask application routes
│   ├── db.py               # Database operations
│   ├── static/
│   │   └── styles.css      # Application styles
│   └── templates/
│       └── index.html      # Main HTML template
├── db/
│   └── init/
│       └── 01-init.sql     # Database initialization script
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker services configuration
├── Dockerfile             # Flask app container definition
└── README.md              # This file
```

## ⚙️ Prerequisites

- AWS EC2 instance running Amazon Linux
- SSH access to your EC2 instance
- Security group configured to allow HTTP traffic on port 80

## 🛠️ Installation & Setup

### Step 1: Connect to EC2 and Update System

```bash
# Connect via SSH (replace with your key and instance details)
ssh -i "your-key.pem" ec2-user@your-ec2-ip

# Update the system
sudo yum update -y
```

### Step 2: Install Docker

```bash
# Install Docker
sudo yum install -y docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add ec2-user to docker group
sudo usermod -a -G docker ec2-user

# Apply group changes
newgrp docker

# Verify Docker installation
docker --version
```

### Step 3: Install Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Create symlink for easier access
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 4: Install Git

```bash
sudo yum install -y git
git --version
```

### Step 5: Clone and Setup Project

```bash
# Clone this repository
git clone <repository-url>
cd flask-notes-compose

# Copy environment file and configure
cp .env.example .env

# Edit environment variables (optional)
nano .env
```

### Step 6: Deploy Application

```bash
# Build and start services
docker compose up -d --build

# Check service status
docker compose ps

# View logs (optional)
docker compose logs -f
```

## 🌐 Access Your Application

Once deployed, access your notes application at:
```
http://your-ec2-public-ip
```

## 🔧 Configuration

### Environment Variables

Edit the `.env` file to customize your deployment:

```bash
HOST_PORT=80                    # Port to expose the web application
MYSQL_ROOT_PASSWORD=change_me_root   # MySQL root password
MYSQL_DATABASE=notesdb          # Database name
MYSQL_USER=notesuser           # Database user
MYSQL_PASSWORD=change_me_user   # Database user password
FLASK_ENV=production           # Flask environment
```

### Security Considerations

**Important**: Before deploying to production:

1. Change all default passwords in `.env`
2. Use strong, unique passwords
3. Consider using environment variable injection for sensitive data
4. Configure proper firewall rules
5. Set up SSL/TLS certificates for HTTPS

## 🐳 Docker Services

### Web Service (`web`)
- **Base Image**: Python 3.11 slim
- **Port**: 80
- **Features**: Flask application with health checks
- **Dependencies**: Waits for database to be healthy

### Database Service (`db`)
- **Base Image**: MySQL 8.0
- **Port**: 3306 (internal)
- **Features**: Persistent data storage, health monitoring
- **Volumes**: Named volume for data persistence

## 📊 Database Schema

The application uses a simple `notes` table:

```sql
CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 🔄 Management Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f [service_name]

# Rebuild and restart
docker compose up -d --build

# Check service status
docker compose ps

# Access MySQL directly
docker compose exec db mysql -u notesuser -p notesdb
```

## 🛡️ Health Monitoring

The application includes built-in health checks:

- **Web Service**: HTTP health check on `/healthz` endpoint
- **Database Service**: MySQL ping health check
- **Automatic Restart**: Unhealthy containers are automatically restarted

## 🔍 Troubleshooting

### Common Issues

1. **Port 80 Permission Denied**
   ```bash
   # Check if port 80 is available
   sudo netstat -tulpn | grep :80
   ```

2. **Database Connection Failed**
   ```bash
   # Check database logs
   docker compose logs db
   
   # Verify database is running
   docker compose exec db mysql -u root -p -e "SELECT 1"
   ```

3. **Container Won't Start**
   ```bash
   # Check container logs
   docker compose logs [service_name]
   
   # Rebuild containers
   docker compose down && docker compose up -d --build
   ```

### Logs and Debugging

```bash
# View all service logs
docker compose logs -f

# View specific service logs
docker compose logs -f web
docker compose logs -f db

# Execute commands in running containers
docker compose exec web bash
docker compose exec db mysql -u root -p
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the application logs using the management commands
3. Open an issue in this repository with detailed error information

## 🚀 Deployment Tips

- Ensure your EC2 security group allows inbound traffic on port 80
- Consider using an Application Load Balancer for production deployments
- Set up automated backups for your MySQL data volume
- Monitor resource usage and scale your EC2 instance as needed
- Consider implementing log aggregation for production monitoring
