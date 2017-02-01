#!/bin/bash

# Get the list of network interfaces
network_interfaces=(`ifconfig -l`)

for i in "${network_interfaces[@]}"
do
	if [[ $i == en* ]]
	then
		interface_ip=`ifconfig $i | grep "inet " | awk '{print $2}'`
		
		if [[ ! -z "$interface_ip" && "$interface_ip" != "" ]]
		then
			hostname=`host $interface_ip | awk '{print $5}' | awk -F. '{print $1}'`
			if [[ $hostname != *NXDOMAIN* ]]
			then
				scutil --set HostName $hostname
				scutil --set ComputerName $hostname
				scutil --set LocalHostName $hostname
			fi
		fi
	fi
done
