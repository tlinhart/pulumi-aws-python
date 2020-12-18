import pulumi
import pulumi_aws as aws


config = pulumi.Config()

ami = aws.get_ami(
    owners=['099720109477'],
    filters=[
        aws.GetAmiFilterArgs(
            name='name',
            values=['ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*']
        )
    ],
    most_recent=True
)

secgrp = aws.ec2.SecurityGroup(
    'web-secgrp',
    description='Enable HTTP access on port 5000',
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=5000,
            to_port=5000,
            cidr_blocks=['0.0.0.0/0']
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol='-1',
            from_port=0,
            to_port=0,
            cidr_blocks=['0.0.0.0/0']
        )
    ]
)

user_data = f"""\
#!/bin/bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
echo {config.require("ghcr-token")} | \
  docker login ghcr.io -u tlinhart --password-stdin
docker run --name hello-world -d -p 5000:5000 \
  ghcr.io/tlinhart/pulumi-aws-python
"""

server = aws.ec2.Instance(
    'web-server',
    instance_type='t2.nano',
    ami=ami.id,
    vpc_security_group_ids=[secgrp.id],
    key_name='aws-ec2-tlinhart-eu-central-1',
    user_data=user_data
)

pulumi.export('public_ip', server.public_ip)
pulumi.export('public_dns', server.public_dns)
