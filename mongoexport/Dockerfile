FROM ubuntu:20.04
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y wget unzip curl gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | \
      gpg -o /usr/share/keyrings/mongodb-server-4.4.gpg \
      --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-4.4.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" |  tee /etc/apt/sources.list.d/mongodb-org-4.4.list

RUN apt-get update && apt-get install -y mongodb-org
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip
# Clean up the installation
RUN rm -rf aws
COPY genie-export.sh /genie-export.sh
RUN chmod +x /genie-export.sh
RUN touch /genie.json
CMD ["/genie-export.sh"]

