# Installing Docker on Amazon EC2 (Amazon Linux 2)

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installing Docker CE](#installing-docker-ce)
   - [Step 1: Connect to Your EC2 Instance](#step-1-connect-to-your-ec2-instance)
   - [Step 2: Update Your Instance](#step-2-update-your-instance)
   - [Step 3: Install Docker](#step-3-install-docker)
   - [Step 4: Start and Enable Docker](#step-4-start-and-enable-docker)
   - [Step 5: Add Your User to the Docker Group](#step-5-add-your-user-to-the-docker-group)
   - [Step 6: Verify Docker Installation](#step-6-verify-docker-installation)
   - [Step 7: Install Docker Compose](#step-7-install-docker-compose)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

This guide provides step-by-step instructions for installing Docker and Docker Compose on an Amazon EC2 instance running Amazon Linux 2. Docker is a popular containerization tool that allows developers to package applications into containers—standardized executable components combining application source code with the operating system (OS) libraries and dependencies required to run that code in any environment.

## Prerequisites

- An Amazon EC2 instance running Amazon Linux 2.
- SSH access to your EC2 instance.

## Installing Docker CE

### Step 1: Connect to Your EC2 Instance

First, you need to SSH into your EC2 instance. Use the following command, replacing `your-key.pem` with your actual key file and `your-instance-ip` with the public IP address or DNS name of your EC2 instance:

```sh
ssh -i /path/to/your-key.pem ec2-user@your-instance-ip
```

### Step 2: Update Your Instance

Before installing any packages, it's a good idea to update your package database to ensure you get the latest versions of the software:

```sh
sudo yum update -y
```

### Step 3: Install Docker

Amazon Linux 2 has Docker available in its repositories. You can install it using the following command:

```sh
sudo yum install -y docker
```

### Step 4: Start and Enable Docker

Once Docker is installed, you'll want to start the Docker service and enable it to start on boot:

```sh
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 5: Add Your User to the Docker Group

To run Docker commands without prefixing them with `sudo`, add your user to the Docker group:

```sh
sudo usermod -aG docker $(whoami)
```

Log out and log back in so that your group membership is re-evaluated.

### Step 6: Verify Docker Installation

To verify that Docker has been installed correctly, run the Hello World Docker image:

```sh
docker run hello-world
```

### Step 7: Install Docker Compose

Docker Compose is not included in the default Amazon Linux 2 repositories, so you will need to install it manually:

1. **Download the Docker Compose binary:**

```sh
wget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)
```

The expression `$(uname -s)-$(uname -m)` used in shell commands is a combination of two commands encapsulated in `$(...)`, which is a command substitution syntax in Unix-like operating systems. This syntax allows the output of a command to replace the command itself in a command line. Let's break down the two parts:

1. **`uname -s`**: This command returns the kernel name of the operating system. For example, on Linux, it would return `Linux`, and on macOS, it would return `Darwin`.

2. **`uname -m`**: This command returns the machine hardware name, indicating the architecture of your system. For instance, it could return `x86_64` for a 64-bit architecture or `arm64` for an ARM 64-bit architecture.

When you combine these with a hyphen (`-`) in between, like `$(uname -s)-$(uname -m)`, it dynamically generates a string that identifies your operating system and its architecture. For example, on a 64-bit Linux machine, the output would be `Linux-x86_64`.

This output is used in URLs or file paths to download or reference files that are specific to your system's operating system and architecture. In the context of downloading Docker Compose, this ensures that you retrieve the version of Docker Compose compiled for your specific system type, ensuring compatibility and proper operation.

So, when you see a command like:

```sh
wget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)
```

It dynamically constructs a URL that points to the appropriate Docker Compose binary for your system. For a 64-bit Linux system, the constructed URL would end in `docker-compose-Linux-x86_64`, targeting the correct binary for download.

2. **Make the binary executable:**

```sh
sudo chmod +x docker-compose-$(uname -s)-$(uname -m)
```

3. **Move the binary to a directory in your PATH:**

```sh
sudo mv docker-compose-$(uname -s)-$(uname -m) /usr/local/bin/docker-compose
```

4. **Verify the installation:**

```sh
docker-compose --version
```

## Conclusion

You have now successfully installed Docker and Docker Compose on your Amazon EC2 instance running Amazon Linux 2. You can now proceed to use Docker to containerize and manage your applications.

## References

- [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Compose GitHub Releases](https://github.com/docker/compose/releases)
- [How to install Docker on Amazon Linux 2](https://www.cyberciti.biz/faq/how-to-install-docker-on-amazon-linux-2/)