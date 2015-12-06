#!/usr/bin/env bash

PG_HBA="/etc/postgresql/9.1/main/pg_hba.conf"

sudo apt-get update
sudo apt-get -y install python
sudo apt-get -y install python-dev
sudo apt-get -y install libpq-dev
sudo apt-get -y install ncurses-dev
sudo apt-get -y install postgresql-9.1
sudo apt-get -y install pandas
sudo apt-get -y install git
sudo wget https://bootstrap.pypa.io/ez_setup.py -O - | python
sudo easy_install npyscreen
sudo apt-get build-dep -y python-psycopg2
sudo easy_install psycopg2
sudo truncate -s 0 "$PG_HBA"
echo "local    all             all                                  trust" >> "$PG_HBA"
echo "host    all             all             all                     trust" >> "$PG_HBA"
service postgresql restart
git clone https://github.com/megaconle/CS419-cursesUI.git
cd CS419-cursesUI.git
python psqlSampleDB.py