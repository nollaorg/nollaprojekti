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
private_subnet = []

# Route table for public subnets
public_route_table = aws.ec2.RouteTable(
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
        route_table_id=public_route_table.id,
        subnet_id=public_subnet[i].id
    )

nat_eip = aws.ec2.Eip("nat_eip",
                      vpc=True)

# NAT GW for private subnets
nat_gw = aws.ec2.NatGateway("nat_gw",
                            allocation_id=nat_eip.id,
                            subnet_id=public_subnet[0].id,
                            tags={
                                "Name": "NAT GW",
                            },
                            opts=pulumi.ResourceOptions(depends_on=[igw]))


# Route table for private subnets
private_route_table = aws.ec2.RouteTable(
    "ec2-private-route-table",
    vpc_id=vpc.id,
    routes=[
        {
            "cidr_block": "0.0.0.0/0",
            "gateway_id": nat_gw.id
        }
    ]
)


# Creates two private subnets to different AZs and the route table associations for them
for i in range(0, 2):
    ltr = chr(i+97)
    prv_ip = i+10
    private_subnet.append(aws.ec2.Subnet(
        f"ec2-private-subnet-{i}",
        cidr_block=f"10.0.{prv_ip}.0/24",
        availability_zone=f"eu-west-1{ltr}",
        tags={
            "Name": f"nullproject-private-subnet-{i}"
        },
        vpc_id=vpc.id
    ))

    rt_assoc = aws.ec2.RouteTableAssociation(
        f"ec2-private-rta-{i}",
        route_table_id=private_route_table.id,
        subnet_id=private_subnet[i].id
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
                                       "Role": "webfront"
                                   }))

    pulumi.export(f'public_ip_server{i}', server[i].public_ip)
    pulumi.export(f'public_dns_server{i}', server[i].public_dns)
