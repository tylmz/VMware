#!/bin/sh

read -p "Location to save output? [Default: /tmp/buffer.txt]:" out;
if [[ "$out" == "" ]]
        then
        out="/tmp/buffer.txt";
fi

function overw()
{
if [ -f $out ]
        then
        read -p "$out file exists are you sure to owerwrite it? (yes/no) :" input
          case $input in
                ("yes")
                rm -f $out
                echo "$out overwrited"
                ;;
                ("no")
                echo "ok, exiting sir"
                exit 1
                break;;
                     *)
                echo 'Please type "yes" or "no"'
                overw
                ;;
          esac
fi
}
overw;
grabt="";
echo "" >> $out;
echo "" >> $out;
grabt="Stats Captured From: `hostname` at `date` "> /dev/null;
echo "$grabt" >> $out;
echo "" >> $out;
echo "" >> $out;
echo "";
echo "";
echo "Network stats are collected and ready to view";
echo "---------------------------";
echo "Please Pick a VM name to show or Simply press enter for all Stats";
echo "For individual vNICs enter exact pattern to match ex: VMNAME.ethX";
echo "Mail me if you have questions: tyilmaz@vmware.com";
echo "`date` innet";
echo "---------------------------";
echo "";
echo "";
for i in `vsish -e ls /net/portsets/ | cut -c 1- | sed 's:/.*::'`;
        do for p in `vsish -e ls /net/portsets/$i/ports | cut -c 1- | sed 's:/.*::'`;
                do vsish -e cat /net/portsets/$i/ports/$p/status | grep "clientName" >> $out; vsish -e cat /net/portsets/$i/ports/$p/stats | egrep -E "droppedTx|droppedRx" >> $out;
                vsish -e cat /net/portsets/$i/ports/$p/vmxnet3/rxSummary 2>/dev/null  | egrep -E "running out of buffers|1st ring size|2nd ring size|of times the 1st ring is full|of times the 2nd ring is full" >> $out;
                echo "---------------------------" >> $out;
        done
done;
until [ "$queryVM" == "exit" ]
do
    read -p "Which VM stats to grab? [Default: ALL stats || Type "Exit" or "exit" to quit session] :" queryVM
        if [[ "$queryVM" != "" ]]
           then
                if [[ "$queryVM" == "Exit" ]] || [[ "$queryVM" == "exit" ]]
                    then
                        break
                                        else
                                        echo "$grabt" >> /tmp/"${queryVM}".txt;
                                        echo "" >> /tmp/"${queryVM}".txt;
                fi

        fi
                        case $queryVM in
                                [$queryVM]* )
                                                egrep -EiA7 "${queryVM}" $out >> /tmp/"${queryVM}".txt
                                                less /tmp/"${queryVM}".txt
                                                ;;
                                          * )
                                                less $out
                                                break;;
                        esac
if [[ "$queryVM" == "" ]] || [[ "$queryVM" == "Exit" ]] || [[ "$queryVM" == "exit" ]]; then echo "These files are created : "$out""; else echo "These files are created : "$out" and "/tmp/"${queryVM}".txt""; fi
done
