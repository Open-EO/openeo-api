FROM ubuntu:xenial

RUN apt-get update && apt-get install -y git software-properties-common build-essential curl mkdocs python3-pip
RUN pip3 install mkdocs-material

COPY generate_docs.sh /opt/generate_docs.sh
RUN chmod +x /opt/generate_docs.sh
COPY redoc.html /opt/redoc.html

CMD ["/opt/generate_docs.sh"]

# run with docker run -v $PWD:/shared 