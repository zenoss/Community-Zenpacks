#!/bin/bash


makedb () {
printf "Mysql host(localhost) : "
read mysqlhost
printf "Mysql Root pwd: "
read mysqlpwd

[ -z $mysqlhost ] && mysqlhost="localhost"

echo "create db"
mysql -h $mysqlhost -uroot -p$mysqlpwd -e 'create database smsd'
echo "Setting rights"
mysql -h $mysqlhost -uroot -p$mysqlpwd -e "grant all privileges on smsd.* to zenoss@localhost identified by 'zenoss'"
echo "Creating structure"
mysql -h $mysqlhost -uroot -p$mysqlpwd smsd < smsd.sql

}

mysql -uzenoss -pzenoss smsd -e "" 2> /dev/null 
if ! [ $? -eq 0 ]
then
  echo "Database not configured"
  echo "Lets do this right now ..."
  makedb
fi

clear

echo "We will add a new person:"
echo
printf "Name of the person:    : "
read name
printf "Mobile of the person   : "
read number

if [ -z $name ]
then
  echo "No name entered"
  exit 2
fi
if [ -z $number ]  
then
  echo "No number entered"
  exit 2
fi

mysql -hlocalhost -uzenoss -pzenoss smsd -e "INSERT INTO \`support\` (\`Name\`, \`Number\`, \`Oncall\`, \`Switchover\`) VALUES ( '$name', '$number', 0, 0)"
