import paramiko
import argparse
import time
import socket
import sys

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--gather", default='all')
parser.add_argument("--hostname")
parser.add_argument("--niclist")
parser.add_argument("--adapters")
parser.add_argument("--device")
args = parser.parse_args()
cmdlet = []


class Infra_connect:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        
    
    def get_hosts():
        try:
            ssh.connect(hostname=vc.hostname,username=vc.username,password=vc.password)
            for query in hostquery:
                print(query)
                stdin, stdout, stderr = ssh.exec_command(query)
                stdin.close()
                print(repr(stdout.read()))
                stdout.close()
                stderr.close()
                time.sleep(1)
                
            with ssh.open_sftp() as sftp, \
                sftp.open('/tmp/hostlist') as f:
                hostlist = [line.strip() for line in f]
                print(hostlist)
                del hostlist[-1]
            ssh.close()
        except:
          print("Could not connect to vCenter")

def checkport(host_ip, port=22):
    try:
        probe_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe_socket.connect((host_ip, port))
    except:
        print(host_ip, "Seems that SSH not enabled or port blocked")
        return False
    else:
        print(host_ip, ": SSH is well dude")
        probe_socket.close()
    return True


def rem_host ():
    for hname in hostlist:
        tresult=checkport(hname, port=22)
        if tresult == False:
            askit=input('SSH is disabled for this host do you want to continue yes/no:')
            if askit == "yes":              
                print("SSH of", hname, "is disabled will not collect data from this host")
                hostlist.remove(hname)
                return False
            else:
                return True


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

hostquery = ['shell \n chsh -s /bin/bash \n /opt/vmware/vpostgres/current/bin/psql -U postgres VCDB -c "select ip_address from vpx_host;" | egrep -Evi "rows|ip|--" > /tmp/hostlist'
             ]

vc = Infra_connect(str(input('vCenter Address :')), str(input('Username :')),str(input('Password :')))
Infra_connect.get_hosts()
hostlist = Infra_connect.get_hosts()
print(hostlist)
rem_host=rem_host()
if rem_host == True:
    sys.exit("Please open all SSH ports")

   
uname = "root"
passwd = "VMware1!"  #input("please enter password :")


for hname in hostlist:
    ssh.connect(hostname=hname, username=uname, password=passwd)
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
