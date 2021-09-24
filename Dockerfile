FROM postgres:latest

# install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y install python3.6
#RUN apt-get install postgresql-server-dev-10 gcc python3-dev musl-dev
RUN apt-get install libpq-dev musl musl-dev postgresql-client-10 postgresql-server-dev-10

# Install Requirements
RUN mkdir -p /run_tables
WORKDIR /run_tables
COPY requirements.txt run_tables/requirements.txt
RUN pip3 install -r run_tables/requirements.txt
RUN apt-get install postgresql-server-dev-10


ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres
ENV POSTGRES_PASSWORD=postgres
ENV PGDATA=/var/lib/postgresql/data/some_name/

COPY . /run_tables


# bind mount Postgres volumes for persistent data
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]




