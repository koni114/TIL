FROM ubuntu:16.04
RUN apt-get update && apt-get install -y vim apache2
COPY index.html /var/www/html/
CMD ["/usr/sbin/apachectl" "-D", "FOREGROUND"]

EXPOSE 80
EXPOSE 8888

LABEL maintainer "Airflow Airflow@Airflow.com"
LABEL title="Test Docker"
LABEL version="0.1"
LABEL description="Docker Test Label"
