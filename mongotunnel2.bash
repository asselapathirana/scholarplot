#!/bin/bash

# Infos about ssh server (tunnel)
SSH_SERVER=<>@<>.pathirana.net # <== IP of your SSH server here
PORT=22 # <== Port of your SSH server here (default is 22)

# Local subnet to use (Local subnet to avoid conflicts)
SUBNET=127.0.1

# Infos about Mongo Atlas Cluster (Prod cluster)
SERV0=cluster<>.<>.mongodb.net

# Check the /etc/hosts file and aask changes if needed
if grep -q $SERV0 "/etc/hosts"; then
	  echo "/etc/hosts is already OK"
  else
      echo "Be sure to have those lines in your /etc/hosts file"
      echo "$SUBNET.1       $SERV0"
      read -p "Press [Enter] when it's in /etc/hosts"
fi;

echo "Connected! Use Ctrl+C to exit."
ssh $SSH_SERVER -p $PORT -N \
	    -L $SUBNET.1:27017:$SERV0:27017 

echo "Disconnected!"
