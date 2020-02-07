This script needs to ingest a file which consists RDM naa. numbers i'll share an example view of file which is disk.list
Here i used sed to extract 1 line at each iteration. So script basically starts from 1 and counts to end of list, that i have naa.IDs in disk.list file.

#!/bin/sh
 
currentNum=$(/bin/esxcli storage core device list | egrep -Ei "Reserved: true" | wc -l)
echo "Currently $currentNum disks set as Perennially Reserved"
NUM=1
dNUM=`cat disk.list | wc -l`
while [ $NUM -le $dNUM ]
do
naa=$(sed -n "$NUM,1p" disk.list)
esxcli storage core device setconfig -d "$naa" --perennially-reserved=true
echo "Iteration number: $NUM"
echo "$naa set as perennially-reserved going for next one"
NUM=`expr $NUM + 1`
done
 
lastNum=$(/bin/esxcli storage core device list | egrep -Ei "Reserved: true" | wc -l)
echo "Currently $lastNum disks set as Perennially Reserved";
exit
