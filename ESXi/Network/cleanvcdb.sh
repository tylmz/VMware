This script must be executed in vCenter server with root privileges. It basically stops vpxd, cleans task and event tables then start
vpxd again. 

Verified against vCenter Server Appliance 6.7

#!/bin/bash

function check () {
service-control --status vmware-vpxd | sed -n "1,1p"
return
}
check=$(check)
function cleanup() {
/opt/vmware/vpostgres/current/bin/psql -d VCDB -U postgres << "EOF"
CREATE OR REPLACE FUNCTION event_full_cleanup_p ()
returns void as $$
DECLARE
   event_partition VARCHAR (200);
BEGIN
     TRUNCATE TABLE VPX_EVENT_PARTITION_LOOKUP;
     --Truncate partitions
     FOR part IN 1..92
     LOOP
       event_partition = 'TRUNCATE TABLE VPX_EVENT_' || CAST(part AS TEXT) || ' CASCADE ';
       EXECUTE event_partition;
       event_partition = 'TRUNCATE TABLE VPX_EVENT_ARG_' || CAST(part AS TEXT) || ' CASCADE ';
       EXECUTE event_partition;
       event_partition = 'ANALYZE VPX_EVENT_' || CAST(part AS TEXT);
       EXECUTE event_partition;
       event_partition = 'ANALYZE VPX_EVENT_ARG_' || CAST(part AS TEXT);
       EXECUTE event_partition;
    END LOOP;
    TRUNCATE TABLE VPX_ENTITY_LAST_EVENT;
END
$$language plpgsql;
select event_full_cleanup_p();
EOF
}
echo "Checking if vmware-vpxd running"
echo "current status of vpxd : $check"
if [ "$check" == "Running:" ] 
	then 
	service-control --stop vmware-vpxd
	check=$(check)
	echo "Checking if vmware-vpxd running"
	echo "current status of vpxd : $check"
	if [ "$check" == "Stopped:" ]
		then
		cleanup
		echo "DB cleansed"
	fi
elif [ "$check" == "Stopped:" ] 
	then
	cleanup
	echo "DB cleansed"
fi 
echo "Checking if vmware-vpxd stopped"
check=$(check)
echo "current status of vpxd : $check"
if [ "$check" == "Stopped:" ]
	then 
	service-control --start vmware-vpxd
fi
check=$(check)
echo "current status of vpxd : $check"
