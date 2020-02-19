import paramiko
import argparse
import time
import socket
import sys

parser = argparse.ArgumentParser(description='Lets Get Started, tyilmaz@vmware.com for questions and help')
parser.add_argument("--hostname",action='store_true', help='gather hostnames')
parser.add_argument("--niclist",action='store_true', help='gather NIC info')
parser.add_argument("--adapters",action='store_true', help='gather HBA info')
parser.add_argument("--device",action='store_true', help='gather storage device info')
parser.add_argument('--cmd', action='store_true', help='Use this to execute custom command')
args = parser.parse_args()
cmdlet = []
hostlist = []

class Infra_connect:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        
    
    def get_hosts():
        try:
        ##  ssh.connect(hostname="ankvc.datamarket.com",#str(input('vCenter Address :')),
        ##            username="root",#str(input('Username :')),
        ##            password="VMware1!")#str(input('Password :')))
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
                del hostlist[-1]
                return hostlist
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
                return rem_host()
            else:
                return True

            
if args.hostname:
                cmdlet = {'touch "/vmfs/volumes/NFS10/`hostname`.txt"'}
elif args.niclist:
                cmdlet = {'esxcli network nic list > "/vmfs/volumes/NFS10/niclist.`hostname`.txt"'}
elif args.adapters:
                cmdlet = {'esxcli storage core adapter list > "/vmfs/volumes/NFS10/adapter.`hostname`.txt"'}
elif args.device:
                cmdlet = {'esxcli storage core device list > "/vmfs/volumes/NFS10/coredevice.`hostname`.txt"'}
elif args.cmd:
                print('Please enter a command to execute on ESXi Shell')
                inputcmd = str(input('Command to execute :'))
                correction = False
                while correction == False:
                    print('Please check if you have entered correct command')
                    correction = input('Are you sure to execute : '+inputcmd+' (Y/N):')
                    if correction == "Y":
                        inputcmd = inputcmd+' >> "/vmfs/volumes/NFS/custom.txt"'
                        correction = True
                    else:
                        sys.exit('Bye Bye')
                cmdlet = ['echo "`hostname`" >> "/vmfs/volumes/NFS/custom.txt" ',
                          'echo "\n" >> "/vmfs/volumes/NFS/custom.txt" ',
                          inputcmd,
                          'echo "\n" >> "/vmfs/volumes/NFS/custom.txt" ',
                          ]
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
#Infra_connect.get_hosts()
hostlist = Infra_connect.get_hosts()
rem_host=rem_host()
if rem_host == True:
    sys.exit("Please open all SSH ports")
print(hostlist)
   
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
