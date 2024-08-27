# Connecting to an ECS Task using Session Manager Plugin and e1s

This README provides a step-by-step guide for setting up and using the Session Manager plugin to connect to an ECS (Elastic Container Service) Task using the e1s tool on a Mac with an ARM64 architecture.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Session Manager Overview](#session-manager-overview)
- [e1s Overview](#e1s-overview)
- [Installation Steps](#installation-steps)
   - [Step 1: Install the Session Manager Plugin](#step-1-install-the-session-manager-plugin)
   - [Step 2: Install e1s](#step-2-install-e1s)
- [Using e1s with ECS Tasks](#using-e1s-with-ecs-tasks)
   - [Step 1: Connect to an ECS Task Using e1s](#step-1-connect-to-an-ecs-task-using-e1s)
   - [Step 2: Exit the e1s Tool](#step-2-exit-the-e1s-tool)
- [Troubleshooting](#troubleshooting)
- [Support](#support)
- [References](#references)

## Prerequisites

- **AWS CLI**: Ensure you have the AWS CLI installed and configured with the necessary permissions.
- **Homebrew**: Make sure Homebrew is installed on your system. If not, you can install it by running:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Session Manager Overview

**AWS Systems Manager Session Manager** is a fully managed service that allows you to manage your Amazon EC2 instances, on-premises servers, and other AWS resources without the need to open inbound ports, manage SSH keys, or use bastion hosts. It provides a secure and auditable way to access and manage your resources, making it easier to comply with security policies and audit requirements.

## e1s Overview

`e1s` is a terminal application designed to easily browse and manage AWS ECS resources, supporting both Fargate and EC2 ECS launch types. The tool is inspired by `k9s`, providing a user-friendly interface for ECS resource management.

## AWS Credentials and Configuration

`e1s` leverages the default `aws-cli` configuration. It does not store or transmit your access and secret keys. These credentials are used solely to securely connect to the AWS API via the AWS SDK. The default profile and region can be overridden by setting the `AWS_PROFILE` and `AWS_REGION` environment variables, or by using the `--profile` and `--region` options.

## Installation Steps

### Step 1: Install the Session Manager Plugin

The Session Manager Plugin is required to establish a connection to your ECS task. Follow these updated steps to install it:

1. **Download the Session Manager Plugin bundle:**

```bash
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/mac_arm64/sessionmanager-bundle.zip" -o "sessionmanager-bundle.zip"
```

Example output:

```bash
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                Dload  Upload   Total   Spent    Left  Speed
100 3612k  100 3612k    0     0  1702k      0  0:00:02  0:00:02 --:--:-- 1702k
```

2. **Unzip the downloaded bundle:**

```bash
unzip sessionmanager-bundle.zip
```

Example output:

```bash
Archive:  sessionmanager-bundle.zip
    creating: sessionmanager-bundle/
extracting: sessionmanager-bundle/VERSION
    inflating: sessionmanager-bundle/LICENSE
    creating: sessionmanager-bundle/bin/
    inflating: sessionmanager-bundle/bin/session-manager-plugin
    inflating: sessionmanager-bundle/seelog.xml.template
    inflating: sessionmanager-bundle/THIRD-PARTY
    inflating: sessionmanager-bundle/install
    inflating: sessionmanager-bundle/NOTICE
    inflating: sessionmanager-bundle/README.md
    inflating: sessionmanager-bundle/RELEASENOTES.md
```

3. **Run the installation script:**

```bash
sudo ./sessionmanager-bundle/install -i /usr/local/sessionmanagerplugin -b /usr/local/bin/session-manager-plugin
```

You will be prompted to enter your password. After successful installation, you should see:

```bash
Password:
Creating install directories: /usr/local/sessionmanagerplugin/bin
Creating Symlink from /usr/local/sessionmanagerplugin/bin/session-manager-plugin to /usr/local/bin/session-manager-plugin
Installation successful!
```

4. **Verify the installation:**

```bash
session-manager-plugin
```

You should see output similar to:

```bash
The Session Manager plugin was installed successfully. Use the AWS CLI to start a session.
```

### Step 2: Install e1s

The e1s tool helps in simplifying the process of connecting to ECS tasks. Install it using Homebrew:

1. Run the following command to install e1s:

```bash
brew install keidarcy/tap/e1s
```

2. Verify the installation by running:

```bash
e1s --version
```

This should output the version of e1s installed, indicating a successful installation.

## Using e1s with ECS Tasks

### Step 1: Connect to an ECS Task Using e1s

Now that you have the necessary tools installed, you can use `e1s` to browse and manage your ECS tasks. Follow these steps to connect to an ECS task using `e1s`:

1. **Launch e1s with Default Configuration**:

To start `e1s` with your default AWS profile and region, simply run:
```bash
e1s
```

2. **Specify a Custom Profile and Region**:

If you need to use a specific AWS profile and region, you can set them using environment variables:

```bash
AWS_PROFILE=custom-profile AWS_REGION=us-east-2 e1s
```

Alternatively, you can specify them directly as options:

```bash
e1s --profile custom-profile --region us-east-2
```

3. **Browse ECS Resources**:

Once `e1s` is running, you can browse your ECS resources directly from the terminal interface. Use the arrow keys to navigate, and select the desired cluster and task.

4. **Connect to an ECS Task**:

To execute a command on an ECS task (such as opening a shell), navigate to the specific task in the `e1s` interface. Then, specify the shell you want to use (e.g., `/bin/bash` or `/bin/sh`):

```bash
e1s --shell /bin/bash
```

This command can be added directly when launching `e1s`, or you can use the default `/bin/sh` shell.

5. **Advanced Usage**:

You can also configure `e1s` with additional flags for read-only mode, debug output, stopping auto-refresh, and more:

```bash
e1s --readonly --debug --refresh -1 --log-file /tmp/e1s.log --json --theme dracula
```

For instance, the command below runs `e1s` in read-only mode, with debugging enabled, auto-refresh disabled, output in JSON format, and using the Dracula color theme:

```bash
e1s --readonly --debug --refresh -1 --log-file /tmp/e1s.log --json --theme dracula
```

6. **Docker Usage**:

If you prefer to use `e1s` in a Docker container, you can run:

```bash
docker run -it --rm -v $HOME/.aws:/root/.aws ghcr.io/keidarcy/e1s:latest e1s --profile YOUR_PROFILE --region YOUR_REGION
```

By following these steps, you can effectively manage your ECS tasks and resources using the `e1s` terminal application.

### Step 4: Exit the e1s Tool

Once you have finished managing your ECS resources or interacting with your ECS tasks using `e1s`, you can easily exit the tool:

1. **Exit the e1s Interface**:

To exit `e1s`, simply press `Ctrl + C` in the terminal. This will safely terminate the `e1s` session and return you to your standard terminal prompt.

2. **Alternative Method**:

If `Ctrl + C` does not work, you can try typing `exit` and then pressing `Enter`.

This step ensures that you properly close the `e1s` tool after completing your session.

## Troubleshooting

- **Session Manager Plugin Issues**: Ensure that the symbolic link is correctly set up and that the plugin is in your system’s PATH.
- **Permission Errors**: Verify that your AWS CLI is configured with appropriate permissions to connect to ECS tasks.

## Support

If you have any questions or need assistance, you can:
- Open an issue in the GitHub repository
- Contact the course maintainers via email at support@kientree.com
- Join our community Slack channel for real-time help

## References

- [AWS Documentation: Session Manager Plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)
- [Install the Session Manager plugin on macOS](https://docs.aws.amazon.com/systems-manager/latest/userguide/install-plugin-macos-overview.html)
- [e1s GitHub Repository](https://github.com/keiDarcy/e1s)