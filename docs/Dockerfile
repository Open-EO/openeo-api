FROM ubuntu:xenial

RUN apt-get update && apt-get install -y git software-properties-common build-essential curl mkdocs
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && apt-get install -y nodejs

WORKDIR /opt
RUN git clone https://github.com/swagger-api/swagger-ui.git

COPY Docker/generate_docs.sh /opt/generate_docs.sh
RUN chmod +x /opt/generate_docs.sh

CMD ["/opt/generate_docs.sh"]

# run with docker run -v $PWD:/shared 