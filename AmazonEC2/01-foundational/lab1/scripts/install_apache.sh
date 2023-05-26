#!/bin/bash

# Switch to root user
sudo su

# Run updates
yum -y update

# Install Apache web server
yum install httpd -y

# Start the web server
systemctl start httpd

# Enable httpd to start on boot
systemctl enable httpd

# Add content to index.html
echo "<html>Welcome to KienTree company home page</html>" > /var/www/html/index.html

# Restart the web server
systemctl restart httpd

echo "Apache server installation, configuration, and content setup complete."
