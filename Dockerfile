FROM python:3.7.2-stretch

LABEL maintainer="Aly Sivji <alysivji@gmail.com>" \
      description="Development image for SivDev"

WORKDIR /home/web/

COPY requirements.txt requirements_dev.txt /tmp/

RUN groupadd -g 901 -r sivdev && \
    useradd -g sivdev -r -u 901 sivpack && \
    pip install --no-cache-dir -r /tmp/requirements_dev.txt

EXPOSE 5000

COPY . /home/web

# Switch from root user for security
USER sivpack

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:7000"]
