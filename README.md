# EventFlow - Event Management Platform

## Overview

**EventFlow** is a comprehensive web-based event management platform built with Flask and MySQL. It enables users to create, discover, and register for events seamlessly. The application provides a complete solution for event hosting and management with user authentication, event creation, registration tracking, and a responsive user dashboard.

## Features

✨ **Core Features:**
- **User Authentication**: Secure registration and login with Bcrypt password hashing
- **Event Creation**: Host can create events with details (title, description, location, datetime, capacity, banner image/URL)
- **Event Discovery**: Browse public events with full details and availability status
- **Event Registration**: Users can register for events with automatic capacity tracking
- **User Dashboard**: Personal dashboard showing hosted events and registered events
- **File Uploads**: Support for event banner images (PNG, JPG, GIF, WebP - max 5MB)
- **Email Notifications**: Built-in email support (configured for Gmail SMTP)
- **Responsive Design**: Dark-themed UI with purple/pink accents

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask 3.0.3 |
| **Database** | MySQL 8.0 |
| **Authentication** | Flask-Bcrypt |
| **Web Forms** | Flask-WTF |
| **File Handling** | Werkzeug, Pillow |
| **Email** | Flask-Mail |
| **Containerization** | Docker, Docker Compose |
| **Python Version** | 3.11+ |

## Project Structure

```
eventflow/
├── app/
│   ├── routes/              # Flask blueprints
│   │   ├── auth.py         # Registration, login, logout
│   │   ├── events.py       # Event CRUD and registration
│   │   └── dashboard.py    # User dashboard
│   ├── templates/          # HTML templates
│   │   ├── base.html       # Base template with navbar
│   │   ├── auth/           # Auth pages (login, register)
│   │   ├── events/         # Event pages (browse, create, detail, edit)
│   │   └── dashboard/      # Dashboard page
│   ├── static/             # Static assets
│   │   ├── css/main.css    # Styling
│   │   ├── js/main.js      # Frontend scripts
│   │   └── uploads/        # Event banner images
│   ├── models/             # Data models (placeholder)
│   ├── utils/              # Utility functions
│   ├── config.py           # Configuration settings
│   └── __init__.py         # Flask app factory
├── db/
│   └── init.sql            # Database schema and initialization
├── docker-compose.yaml     # Multi-container setup
├── Dockerfile              # Python image configuration
├── requirements.txt        # Python dependencies
└── run.py                  # Application entry point
```

## Prerequisites

### Local Development
- Python 3.11+
- MySQL 8.0+
- pip or conda package manager
- Git

### Azure VM Deployment
- Azure Virtual Machine (Linux - Ubuntu 20.04 or later recommended)
- SSH access to the VM
- Sudo privileges

## Installation & Setup

### Option 1: Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/airo-swaraj/eventflow.git
cd eventflow
```

#### 2. Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the project root:
```bash
cat > .env << EOF
# Flask Configuration
SECRET_KEY=your-secret-key-here-generate-a-random-string

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_USER=eventflow_user
MYSQL_PASSWORD=eventflow_pass
MYSQL_DB=eventflow_db

# Email Configuration (Gmail)
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-gmail@gmail.com
EOF
```

#### 5. Setup MySQL Database
```bash
# Option A: Using MySQL CLI
mysql -u root -p < db/init.sql

# Option B: Using docker-compose (see Docker section)
```

#### 6. Run the Application
```bash
python run.py
```
Access at: `http://localhost:5000`

---

### Option 2: Docker Deployment (Recommended)

#### 1. Prerequisites

**Ensure Docker and Docker Compose are installed:**

**On macOS/Windows:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Includes both Docker and Docker Compose

**On Linux/Azure VM:**
- Follow the installation steps in [Azure VM Configuration](#azure-vm-configuration) section

#### 2. Clone Repository
```bash
git clone https://github.com/airo-swaraj/eventflow.git
cd eventflow
```

#### 3. Create Environment File
```bash
cat > .env << EOF
SECRET_KEY=your-secure-random-key
MYSQL_HOST=db
MYSQL_USER=eventflow_user
MYSQL_PASSWORD=eventflow_pass
MYSQL_DB=eventflow_db
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-gmail@gmail.com
EOF
```

#### 4. Build and Run with Docker Compose
```bash
# Build images
docker-compose build

# Start services (runs in background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Clean up (remove volumes too)
docker-compose down -v
```

#### 5. Verify Services
```bash
# Check running containers
docker ps

# Check application logs
docker-compose logs web

# Check database health
docker-compose logs db
```

---

## Azure VM Configuration

### 1. Azure Virtual Machine Requirements

**VM Configuration:**
- **Operating System**: Ubuntu 20.04 LTS or later
- **Size**: Standard_B2s (2 vCPU, 4 GB RAM) or higher
- **Storage**: At least 30 GB disk space
- **SSH Access**: Enabled with public key authentication
- **Public IP**: Required for accessing the application

> Note: Create the VM using Azure Portal or Azure CLI according to your organization's process

### 2. Network Security Group (NSG) - Required Ports

**Ports to Open:**

| Port | Service | Protocol | Purpose |
|------|---------|----------|---------|
| 22 | SSH | TCP | Remote access |
| 5000 | Flask Web | TCP | EventFlow application |
| 3306 | MySQL | TCP | Database (internal only) |

#### Using Azure Portal:
1. Go to Virtual Machine → Networking
2. Click "Add inbound port rule"
3. Add rules:

**Rule 1: HTTP (Flask App)**
```
Protocol: TCP
Port: 5000
Priority: 100
Name: Allow-EventFlow
```

**Rule 2: SSH**
```
Protocol: TCP
Port: 22
Priority: 101
Name: Allow-SSH
```

### 3. Install Required Software on Azure VM

#### 1. Git Installation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Git
sudo apt install -y git

# Verify installation
git --version

# Configure Git (optional but recommended)
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

#### 2. Docker Installation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add current user to docker group (avoid using sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

### 4. Deploy EventFlow on Azure VM

```bash
# SSH into the VM (use public IP from Azure Portal)
ssh -i ~/.ssh/id_rsa azureuser@<PUBLIC_IP>

# Clone the repository
git clone https://github.com/airo-swaraj/eventflow.git
cd eventflow

# Create .env file with your configuration
nano .env  # Add your configuration (see .env.example)

# Build and start containers
docker-compose up -d

# Verify services are running
docker ps

# Check application logs
docker-compose logs -f web
```

---

## Accessing the Application

### Local Development
```
http://localhost:5000
```

### Azure VM Deployment
```
http://<AZURE_VM_PUBLIC_IP>:5000
```

**Example:**
```
http://20.119.52.45:5000
```

### First Steps:
1. **Home Page**: `http://<IP>:5000/`
2. **Register**: Click "Get Started" → Create new account
3. **Login**: Enter credentials
4. **Browse Events**: Visit `/events` to see public events
5. **Create Event**: Click "Create Event" (logged in users only)
6. **Dashboard**: View hosted and registered events at `/dashboard`

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Events Table
```sql
CREATE TABLE events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    capacity INT NOT NULL,
    registered_count INT DEFAULT 0,
    banner_url VARCHAR(500),
    banner_image VARCHAR(255),
    is_public BOOLEAN DEFAULT TRUE,
    host_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Registrations Table
```sql
CREATE TABLE registrations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_registration (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
```

---

## Configuration Details

### Application Config (`app/config.py`)

**File Upload Settings:**
- Max file size: 5MB
- Allowed extensions: png, jpg, jpeg, gif, webp
- Upload folder: `app/static/uploads/`

**Database:**
- Connection timeout: Default MySQL settings
- Cursor type: DictCursor (returns results as dictionaries)

**Email:**
- SMTP Server: smtp.gmail.com
- Port: 587
- Use TLS: Yes

---

## Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs web

# Rebuild images
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Database connection failed:**
```bash
# Ensure MySQL is healthy
docker-compose logs db

# Check if database is initialized
docker-compose exec db mysql -u root -p -e "SHOW DATABASES;"
```

**Permission denied on uploads:**
```bash
# Fix upload folder permissions
docker-compose exec web chmod -R 777 /app/app/static/uploads
```

### Network Issues

**Cannot reach application on Azure VM:**
```bash
# Check if port 5000 is listening
netstat -tulpn | grep 5000

# Check NSG rules
az network nsg rule list --resource-group myResourceGroup --nsg-name eventflow-vmNSG

# Check firewall on VM
sudo ufw status
sudo ufw allow 5000/tcp
```

### Database Issues

**Reset database:**
```bash
docker-compose down -v
docker-compose up -d
# Wait for MySQL to initialize, then rebuild
```

---

## Environment Variables Reference

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | `generate-random-key` | Flask session encryption key |
| `MYSQL_HOST` | Yes | `db` (Docker) / `localhost` (Local) | MySQL server hostname |
| `MYSQL_USER` | Yes | `eventflow_user` | MySQL username |
| `MYSQL_PASSWORD` | Yes | `eventflow_pass` | MySQL password |
| `MYSQL_DB` | Yes | `eventflow_db` | Database name |
| `MAIL_USERNAME` | No | `your-email@gmail.com` | Gmail account for sending emails |
| `MAIL_PASSWORD` | No | `app-password` | Gmail app-specific password |
| `MAIL_DEFAULT_SENDER` | No | `noreply@eventflow.com` | Default sender email |

---

## Performance Considerations

- **Database Indexing**: Add indexes on `username`, `email`, and `host_id` for faster queries
- **Session Storage**: Currently uses Flask default (memory). For production, use Redis/Memcached
- **File Storage**: For scale, use Azure Blob Storage instead of local filesystem
- **Caching**: Implement Redis for event listing caches

---

## Security Recommendations

1. ✅ Change all default credentials in `.env`
2. ✅ Use strong `SECRET_KEY` (minimum 32 characters)
3. ✅ Generate Gmail app-specific password (not regular password)
4. ✅ Use HTTPS in production (add SSL certificate)
5. ✅ Restrict database access (limit 3306 to internal only)
6. ✅ Regular backups of MySQL data
7. ✅ Use managed MySQL service (Azure Database for MySQL) in production

---

## Useful Commands

```bash
# Build and start containers
docker-compose up -d --build

# View all running containers
docker ps -a

# Execute command in container
docker-compose exec web python -c "print('test')"

# View application logs in real-time
docker-compose logs -f web

# Stop and remove all containers
docker-compose down

# Remove images too
docker-compose down --rmi all

# Connect to MySQL in container
docker-compose exec db mysql -u eventflow_user -p eventflow_db

# Access Flask shell
docker-compose exec web flask shell
```

---

## Support & Documentation

- **Framework**: [Flask Documentation](https://flask.palletsprojects.com/)
- **Database**: [MySQL Documentation](https://dev.mysql.com/doc/)
- **Docker**: [Docker Documentation](https://docs.docker.com/)
- **Azure**: [Azure VM Documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/)

---

## License

This project is open source and available under the MIT License.

---

## Contributors

Created for EventFlow - Event Management Platform

**Last Updated**: May 2026
