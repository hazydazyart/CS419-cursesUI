#!/usr/bin/env bash

PG_HBA="/etc/postgresql/9.1/main/pg_hba.conf"

sudo apt-get update
sudo apt-get -y install python
sudo apt-get -y install python-dev
sudo apt-get -y install vim
sudo apt-get -y install libpq-dev
sudo apt-get -y install ncurses-dev
sudo apt-get -y install postgresql-9.1
sudo apt-get -y install pandas
sudo apt-get -y install git
sudo wget https://bootstrap.pypa.io/ez_setup.py -O - | python
sudo easy_install -y npyscreen
sudo apt-get build-dep -y python-psycopg2
sudo easy_install -y psycopg2
echo "host    all             all             all                     trust" >> "$PG_HBA"
service postgresql restart
sudo apt-get -y install mysql-server
sudo apt-get -y install python-mysqldb