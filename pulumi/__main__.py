"""
Author: Robert Vesterinen
Description:
This script will create a basic 3-tier web stack with network resources
- EC2 instances
- VPC
- Private and public subnets
- Security groups etc.
"""

import pulumi
import pulumi_aws as aws
from config import *

# Retrieve the latest AMI
ami = aws.ec2.get_ami(most_recent=True,
                      owners=["137112412989"],
                      filters=[aws.GetAmiFilterArgs(name="name", values=["amzn-ami-hvm-*"])])

vpc = aws.ec2.Vpc(
    "nullproject-vpc",
    cidr_block="10.0.0.0/16"
)

group = aws.ec2.SecurityGroup('test-web-sg',
                              description='Enable HTTP access',
                              vpc_id=vpc.id,
                              ingress=[aws.ec2.SecurityGroupIngressArgs(
                                  protocol='tcp',
                                  from_port=80,
                                  to_port=80,
                                  cidr_blocks=['0.0.0.0/0'],
                              )])

# Internet gateway for internet access
igw = aws.ec2.InternetGateway(
    "ec2-igw",
    vpc_id=vpc.id,
)

public_subnet = []

# Route table for public subnets
route_table = aws.ec2.RouteTable(
    "ec2-public-route-table",
    vpc_id=vpc.id,
    routes=[
        {
            "cidr_block": "0.0.0.0/0",
            "gateway_id": igw.id
        }
    ]
)

# Creates two public subnets to different AZs and the route table associations for them
for i in range(0, 2):
    ltr = chr(i+97)
    public_subnet.append(aws.ec2.Subnet(
        f"ec2-public-subnet-{i}",
        cidr_block=f"10.0.{i}.0/24",
        availability_zone=f"eu-west-1{ltr}",
        tags={
            "Name": f"nullproject-public-subnet-{i}"
        },
        vpc_id=vpc.id
    ))

    rt_assoc = aws.ec2.RouteTableAssociation(
        f"ec2-rta-{i}",
        route_table_id=route_table.id,
        subnet_id=public_subnet[i].id
    )


server = []

# Creates webfronts to each of the public subnets
for i in range(0, webfront_count):
    # Add every second webfront server to the other subnet
    if i % 2 == 0:
        to_subnet = 0
    else:
        to_subnet = 1
    server.append(aws.ec2.Instance(f'webfront-{i}',
                                   instance_type=size,
                                   vpc_security_group_ids=[group.id],
                                   user_data=user_data,
                                   subnet_id=public_subnet[to_subnet].id,
                                   ami=ami.id,
                                   tags={
                                       "Name": f"webfront-{i}",
                                   }))

    pulumi.export(f'public_ip_server{i}', server[i].public_ip)
    pulumi.export(f'public_dns_server{i}', server[i].public_dns)
