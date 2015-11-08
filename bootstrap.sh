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
sudo easy_install npyscreen
sudo apt-get build-dep -y python-psycopg2
sudo easy_install psycopg2
sudo truncate -s 0 $PG_HBA
echo "local    all             all					trust" >> "$PG_HBA"
service postgresql restart
debconf-set-selections <<< 'mysql-server mysql-server/root_password password mysql'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password mysql'
sudo apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y python-mysqldb
sudo apt-get install -y python-pip
sudo pip install -U pip
sudo pip install --allow-external mysql-connector-python mysql-connector-python