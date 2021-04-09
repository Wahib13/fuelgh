FROM python:3.9-buster
RUN useradd -ms /bin/bash app_runner
USER app_runner

ENV PYTHONBUFFERED=1
ENV PATH "$PATH:/home/app_runner/.local/bin"

WORKDIR /home/app_runner/code

COPY fuelgh/requirements/ /home/app_runner/code/
RUN pip install -r prod.txt
COPY . /home/app_runner/code/
USER root
RUN chown -R app_runner:app_runner fuelgh/