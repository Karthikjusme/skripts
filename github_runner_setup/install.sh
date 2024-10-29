sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
sudo usermod -aG docker ec2-user 

# install docker-compose
curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

curl -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

#aws eks --region ap-south-1 update-kubeconfig --name eka-prod
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

sudo yum install -y git

# https://github.com/organizations/eka-care/settings/actions/runners/new

#mkdir actions-runner && cd actions-runner

#curl -o actions-runner-linux-x64-2.320.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.320.0/actions-runner-linux-x64-2.320.0.tar.gz
#tar xzf ./actions-runner-linux-x64-2.320.0.tar.gz
#sudo ./bin/installdependencies.sh 
#sudo yum install libicu -y
#./config.sh --url <github-url> --token <token> --unattended --replace

#nohup ./run.sh > ~/runner.log >2&1