from diagrams import Diagram, Cluster
from diagrams.aws.network import VPC, InternetGateway, NATGateway, PublicSubnet, PrivateSubnet, RouteTable
from diagrams.aws.general import User
from diagrams.aws.network import VPCRouter

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

