# Creating Diagrams as Code using Python

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Install Homebrew](#step-1-install-homebrew)
  - [Step 2: Install Graphviz](#step-2-install-graphviz)
  - [Step 3: Create a Python Virtual Environment](#step-3-create-a-python-virtual-environment)
  - [Step 4: Install Python Packages](#step-4-install-python-packages)
- [Creating the VPC Diagram](#creating-the-vpc-diagram)
  - [Step 1: Save the Python Script](#step-1-save-the-python-script)
  - [Step 2: Run the Script](#step-2-run-the-script)
- [Project Structure](#project-structure)
- [Conclusion](#conclusion)
- [References](#references)

## Introduction

This project demonstrates how to create a visual representation of an AWS vpc_architecture using the `diagrams` Python library. The architecture includes two Availability Zones, public and private subnets, an Internet Gateway, and NAT Gateways, based on a given AWS CloudFormation template.

## Prerequisites

- Python 3 installed on your system.
- `pip` package manager installed.
- Homebrew (for installing Graphviz on macOS).

## Setup Instructions

### Step 1: Install Homebrew

Homebrew is a package manager for macOS that simplifies the installation of software.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Graphviz

Graphviz is a necessary dependency for the `diagrams` library.

```bash
brew install graphviz
```

### Step 3: Create a Python Virtual Environment

1. Navigate to your project directory or create a new one:

```bash
mkdir vpc-diagram
cd vpc-diagram
```

2. Create a virtual environment:

```bash
python3 -m venv myenv
```

3. Activate the virtual environment:

```bash
source myenv/bin/activate
```

### Step 4: Install Python Packages

Install the necessary Python packages, including `diagrams`.

```bash
pip install diagrams
```

## Creating the VPC Diagram

### Step 1: Save the Python Script

Create a file named `vpc_diagram.py` and add the following script:

```python
from diagrams import Diagram, Cluster
from diagrams.aws.network import VPC, InternetGateway, NATGateway, PublicSubnet, PrivateSubnet, RouteTable
from diagrams.aws.general import User

with Diagram("VPC Architecture", show=False):
    user = User("User")
    
    with Cluster("VPC (10.0.0.0/16)"):
        igw = InternetGateway("Internet Gateway")

        with Cluster("Availability Zone 1"):
            pub_subnet_az1 = PublicSubnet("Public Subnet 1\n(10.0.0.0/18)")
            priv_subnet_az1 = PrivateSubnet("Private Subnet 1\n(10.0.128.0/18)")
            nat_gw_az1 = NATGateway("NAT Gateway 1")

            pub_route_table_az1 = RouteTable("Public Route Table 1")
            priv_route_table_az1 = RouteTable("Private Route Table 1")

        with Cluster("Availability Zone 2"):
            pub_subnet_az2 = PublicSubnet("Public Subnet 2\n(10.0.64.0/18)")
            priv_subnet_az2 = PrivateSubnet("Private Subnet 2\n(10.0.192.0/18)")
            nat_gw_az2 = NATGateway("NAT Gateway 2")

            pub_route_table_az2 = RouteTable("Public Route Table 2")
            priv_route_table_az2 = RouteTable("Private Route Table 2")

        # Internet Gateway and Public Subnets
        igw >> pub_route_table_az1 >> pub_subnet_az1
        igw >> pub_route_table_az2 >> pub_subnet_az2

        # NAT Gateways and Private Subnets
        pub_subnet_az1 >> nat_gw_az1 >> priv_route_table_az1 >> priv_subnet_az1
        pub_subnet_az2 >> nat_gw_az2 >> priv_route_table_az2 >> priv_subnet_az2

        # User Internet Access
        user >> igw
```

### Step 2: Run the Script

Run the script to generate the VPC diagram.

```bash
python vpc_diagram.py
```

This will generate a PNG file named `vpc_architecture.png` in your project directory, depicting the vpc_architecture.

## Project Structure

```
vpc-diagram/
├── myenv/                  # Python virtual environment
├── vpc_diagram.py          # Python script to generate the VPC diagram
├── vpc_architecture.png    # Generated VPC Architecture diagram
└── README.md               # Project README file
```

## Conclusion

This project demonstrates how to use the `diagrams` Python library to create a visual representation of an AWS VPC Architecture based on a CloudFormation template. By following the setup instructions and running the provided script, you can generate a diagram that helps visualize the infrastructure setup.

## References

- [Diagrams Documentation](https://diagrams.mingrammer.com/)
- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/index.html)
- [Graphviz Documentation](https://graphviz.org/documentation/)
- [Homebrew Documentation](https://docs.brew.sh/)