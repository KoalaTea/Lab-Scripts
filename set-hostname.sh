#!/bin/bash

# Sets a Mac's hostname based on the PTR record in DNS

# Get the list of network interfaces
network_interfaces=(`ifconfig -l`)

# Interate through the network interfaces
# If the interface has an IP, run host on it
for i in "${network_interfaces[@]}"
do
	if [[ $i == en* ]]
	then
		interface_ip=`ifconfig $i | grep "inet " | awk '{print $2}'`
		
		if [[ ! -z "$interface_ip" && "$interface_ip" != "" ]]
		then
			hostname=`host $interface_ip | awk '{print $5}' | awk -F. '{print $1}'`
			
			# If we have an hostname, set it
			if [[ $hostname != *NXDOMAIN* ]]
			then
				scutil --set HostName $hostname
				scutil --set ComputerName $hostname
				scutil --set LocalHostName $hostname
			fi
		fi
	fi
done
