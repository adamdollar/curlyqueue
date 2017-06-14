#curlyqueue

Simple website checking using curl
Usage: ./curlyqueue.sh inputfile
Inputfile should contain url of each website that you would like to
check on its own line.  It is assumed that the desired return code
is 200. If this is not the case, append the url with >port number.
For example:
www.example.com>404
