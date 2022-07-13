FROM lambci/lambda:build-python3.8
# FROM python:3.8-buster

RUN pip install --upgrade pip

ENV WORKDIR /app
WORKDIR ${WORKDIR}

RUN yum update -y && yum -y install curl
RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash - && \
    -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo
RUN yum install -y nodejs && npm install -g yarn

COPY /package.json ${WORKDIR}
COPY /yarn.lock ${WORKDIR}
RUN yarn install


COPY /src ${WORKDIR}/src

COPY /requirements.txt ${WORKDIR}
RUN pip install -r ${WORKDIR}/requirements.txt

RUN pip install autopep8 flake8 pytest pytest-mock pytest-freezegun boto3 opencv-python
