# SSH into EC2 Instance

## Table of Contents

- [Introduction](#introduction)
- [SSH for Mac & Linux Users](#ssh-for-mac--linux-users)
- [SSH for Microsoft Windows Users](#ssh-for-microsoft-windows-users)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

Welcome to this comprehensive guide on how to SSH (Secure Shell) into an Amazon EC2 (Elastic Compute Cloud) instance. Whether you're new to cloud computing or an experienced user, this document will assist you in securely connecting to your EC2 instance from various operating systems. We'll go through the necessary steps for both Mac & Linux and Microsoft Windows users. This guide aims to provide clear, step-by-step instructions to make your experience smooth and hassle-free.

## SSH for Mac & Linux Users

### 1. Open Terminal

Start by opening your Terminal application.

### 2. Locate .pem Key

Navigate to the directory where your `.pem` key file is stored.

### 3. Update Permissions

Run the following command to update permissions for your key:

```bash
chmod 400 keypair_filename
```

Example:

```bash
chmod 400 ec2_connect.pem
```

### 4. Connect to EC2 Instance

Use the following command to SSH into your EC2 instance:

- Syntax: 

```bash
ssh -i keypair_filename UserName@public_IP_Address
```

- Replace `UserName` with the appropriate user name based on your AMI:
- Amazon Linux AMI: `ec2-user`
- Ubuntu AMI: `ubuntu`
- OPENVPN AMI: `root`
- Example: 

```bash
ssh -i ec2_connect.pem ec2-user@54.172.93.175
```

- After entering the command, type `yes` and press Enter to log in.

## SSH for Microsoft Windows Users

### 1. Download Putty and Puttygen

Download both Putty and Puttygen from [here](https://www.chiark.greenend.org.uk/~sgtatham/putty/releases/0.74.html).

### 2. Convert .pem to .ppk

- Open Puttygen.
- Click `Load` to import your `.pem` file.
- Once loaded successfully, click on `Save Private Key`.
- Choose a name for your key (e.g., `keypairname.ppk`) and save it.

### 3. Connect to EC2 Instance

- Open Putty.
- In the Host Name field, enter your instance's public IP address.
- Go to `Connection` > `SSH` > `Auth`. Click `Browse` to select your `.ppk` file.
- Click `Open` to initiate the connection.
- Depending on your AMI, enter the username (`ec2-user`, `ubuntu`, or `root`) and hit Enter.

## Conclusion

This guide has walked you through the steps to securely SSH into an EC2 instance from both Mac & Linux and Windows environments. By following these instructions, you should now be able to successfully access your EC2 instances. Remember, security is paramount when dealing with cloud resources, so ensure your keys are kept safe and permissions are correctly set.

## References

- [Connect to your Linux instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-to-linux-instance.html)
- [Putty and Puttygen official website](https://www.puttygen.com/download-putty)

---

*Thank you for following this guide. We hope it has been helpful in your journey with Amazon EC2.*