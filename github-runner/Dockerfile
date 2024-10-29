FROM ghcr.io/actions/actions-runner:latest

RUN sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN sudo chmod +x /usr/local/bin/docker-compose

RUN sudo apt-get update
RUN sudo apt-get install make

RUN sudo curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN sudo unzip awscliv2.zip
RUN sudo ./aws/install