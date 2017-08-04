#!/bin/bash

# Parse parameters
if [ -z $1 ] || [ "$1" == "-h" ] ; then
	echo "curlyqueue"
	echo "-----------------------------"
	echo "Simple website checking using curl"
	echo "Usage: ./curlyqueue.sh inputfile"
	echo
	echo "Inputfile should contain url of each website that you would like to"
	echo "check on its own line.  It is assumed that the desired return code"
	echo "is 200. If this is not the case, append the url with >port number."
	echo "For example:"
	echo "www.example.com>404"
	exit 0
fi

ret=0
queue=`cat $1`
for line in $queue ; do
	site=`echo $line | cut -d'>' -f1`
	desired=`echo $line | cut -d'>' -f2`
	if [ "`echo $desired | grep -c '\.'`" == "1" ] ; then
		desired="200"
	fi
	actual=`curl -ILs --connect-timeout 5 $site |  cut -d' ' -f2 | head -1`
	if [ -z $actual ] ; then
		echo "[X] $site (TIMEOUT instead of ${desired})"
		ret=1
	elif [ $actual == $desired ] ; then
		echo "[O] $site (${actual})"
	else
		echo "[X] $site (${actual} instead of ${desired})"
		ret=1
	fi
done

exit $ret