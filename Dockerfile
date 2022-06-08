FROM python:3.8-buster

ENV WORKDIR /app
WORKDIR ${WORKDIR}

RUN apt-get update
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y curl apt-transport-https wget awscli libopencv-dev && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn

COPY /package.json ${WORKDIR}
COPY /yarn.lock ${WORKDIR}
RUN yarn install


COPY /src ${WORKDIR}/src

# COPY /requirements.txt ${WORKDIR}
# RUN pip install -r ${WORKDIR}/requirements.txt

RUN pip install autopep8 flake8 pytest pytest-mock pytest-freezegun boto3 opencv-python
