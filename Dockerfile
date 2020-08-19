FROM python:3.7-slim

# Use "RUN adduser -D -g '' newuser" for alpine
RUN adduser --disabled-password --gecos '' social_credit

WORKDIR /srv/social_credit

ENV VIRTUAL_ENV=/srv/social_credit/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install \
    --trusted-host pypi.python.org \
    --disable-pip-version-check \
    -r requirements.txt

COPY src src/
COPY locale locale/
COPY crontab.yaml crontab.yaml

USER social_credit

ENTRYPOINT ["python", "src/main.py"]