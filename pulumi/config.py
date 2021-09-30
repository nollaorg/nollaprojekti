size = "t3.micro"
project_name = "nullproject"
user_data = """
#!/bin/bash
echo "Hello, Jakesti!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""
# Define the number of webfronts. Every second one goes to the public subnet b.
webfront_count = 2
ec2_pub_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHRHPj4IFhNr8nCvBeWvAWN437AwANEjyfC7rB+5hkLO8tO+K1DQ5bTFvDEdgL7uj0a2jPjLpnnmEYcSbpunp99nNXmSqBBewOoc0SIi9ie14Z7m+fm3DmqpoTqkfeuuu4YyUvKJJM/+vjuPwABCWoVWhSPGN5pi4vo/GDn1sw4UisW8UuqoRehdTZg6JOD6wIEn+YARmzx5TXVv6Q14sGh5nd+2fH/Tugkd1f14RUCHtTz/nCjJOtWFQc7M5jfN1SJYrfIzUbJTeClwaey87h9LAvW12VVkur2qSJZ3lK0d6C0jdFruuX+JwAtx3GTkSiX8vsTj6dT3KJ/3x7jgGH robban@DESKTOP-FUHKTQG"

