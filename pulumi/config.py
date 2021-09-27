size = "t3.micro"
project_name = "nullproject"
user_data = """
#!/bin/bash
echo "Hello, Jakesti!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""
# Define the number of webfronts. Every second one goes to the public subnet b.
webfront_count = 6
