FROM python:3.11.5-slim-bullseye AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1

ARG bucket_name
ARG access_key_id
ARG access_key
ARG endpoint_url
ARG elster_datenlieferant
ARG elster_hersteller_id
ENV ELSTER_DATENLIEFERANT=$elster_datenlieferant
ENV ELSTER_HERSTELLER_ID=$elster_hersteller_id

WORKDIR /app
RUN echo "Package: *\nPin: release n=bookworm\nPin-Priority: 50\n" >> /etc/apt/preferences && \
    echo "deb http://ftp.debian.org/debian bookworm main" >> /etc/apt/sources.list.d/bookworm.list && \
    apt-get update && \
    apt-get install --no-install-recommends -y -t bookworm pcsc-tools pcscd && \
    apt-get install --no-install-recommends -y procps unzip curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl https://dbs-download.obs.otc.t-systems.com/rds/ca-bundle.pem -o /opt/rds-ca-bundle.pem

# Install debugging tools
# RUN apt-get update && \
#  apt-get install -y vim telnet coreutils less strace lsof rsyslog usbutils && \
#  rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh

COPY ./Pipfile ./Pipfile.lock ./setup.py ./
RUN pip install --upgrade --no-cache-dir pip pipenv && pipenv install --ignore-pipfile

COPY . .

# Get tax office list and ERiC libraries
RUN env ERICA_BUCKET_NAME=$bucket_name AWS_ACCESS_KEY_ID=$access_key_id AWS_SECRET_ACCESS_KEY=$access_key ENDPOINT_URL=$endpoint_url pipenv run python scripts/load_eric_binaries.py download-eric-cert-and-binaries && \
    env ERICA_ENV=testing pipenv run python scripts/create_tax_office_lists.py create

EXPOSE 8000

ENTRYPOINT [ "/entrypoint.sh" ]

######## cron target
FROM base AS cron
RUN apt-get update && apt-get install --no-install-recommends --yes cron procps && rm -rf /var/lib/apt/lists/*
# Set up log forwarding to docker log collector (used by cron jobs)
RUN ln -sf /proc/1/fd/1 /app/cronjob_success_fail_output && \
    ln -sf /proc/1/fd/1 /app/cronjob_not_processed_output
COPY ./cron.d/* /etc/cron.d/
RUN chown root:root /etc/cron.d/* && \
    chmod go-wx /etc/cron.d/* && \
    chmod -x /etc/cron.d/*
CMD ["/usr/sbin/cron", "-f"]
#########

#########
### main target for api and workers
######
FROM base AS erica
CMD [ "python", "-m", "erica" ]
#########
