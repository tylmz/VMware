import paramiko
import argparse
import time

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--gather", default='all')
parser.add_argument("--hostname")
parser.add_argument("--niclist")
parser.add_argument("--adapters")
parser.add_argument("--device")
args = parser.parse_args()
cmdlet = []
if args.hostname == "hostname":
                cmdlet = {'touch "/vmfs/volumes/NFS10/`hostname`.txt"'}
elif args.niclist == "niclist":
                cmdlet = {'esxcli network nic list > "/vmfs/volumes/NFS10/niclist.`hostname`.txt"'}
elif args.adapters == "adapters":
                cmdlet = {'esxcli storage core adapter list > "/vmfs/volumes/NFS10/adapter.`hostname`.txt"'}
elif args.device == "device":
                cmdlet = {'esxcli storage core device list > "/vmfs/volumes/NFS10/coredevice.`hostname`.txt"'}
else:
            cmdlet = ['echo "`hostname`" >> "/vmfs/volumes/NFS10/environment.txt" ',
                      'echo "\n" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "NIC details for `hostname`" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "\n" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'esxcli network nic list >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "\n" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "HBA details for `hostname`" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "\n" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'esxcli storage core adapter list >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "\n" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "BIOS details `hostname`" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "\n" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'vsish -e get /hardware/bios/biosInfo | egrep -Evi "major|minor|controller" >> "/vmfs/volumes/NFS10/environment.txt"',
                      'echo "\n" >> "/vmfs/volumes/NFS10/environment.txt"'
                      ]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
hostlist = []
hostquery = ['shell \n chsh -s /bin/bash \n /opt/vmware/vpostgres/current/bin/psql -U postgres VCDB -c "select ip_address from vpx_host;" | egrep -Evi "rows|ip|--" > /tmp/hostlist'
             ]

try:
  ssh.connect(hostname="ankvc.datamarket.com",#str(input('vCenter Address :')),
            username="root",#str(input('Username :')),
            password="VMware1!")#str(input('Password :')))
  for query in hostquery:
     stdin, stdout, stderr = ssh.exec_command(query)
     stdin.close()
     print(repr(stdout.read()))
     stdout.close()
     stderr.close()
     time.sleep(1)
        
  with ssh.open_sftp() as sftp, \
    sftp.open('/tmp/hostlist') as f:
    hostlist = [line.strip() for line in f]
    del hostlist[-1]
  ssh.close()
except:
  print("Could not connect to vCenter")
    
uname = "root"
passwd = "VMware1!"  #input("please enter password :")
for hname in hostlist:
        try:
            ssh.connect(hostname=hname, username=uname, password=passwd)
        except:
            print("Can't connect to:",hname)
        for cmd in cmdlet:
            print(cmd)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdin.close()
            #print(repr(stdout.read()))
            #print(repr(stderr.read()))
            stdout.close()
            stderr.close()
            time.sleep(1)
        ssh.close()
