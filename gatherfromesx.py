import paramiko
import argparse

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--gather", default='all')
parser.add_argument("--hostname")
parser.add_argument("--niclist")
parser.add_argument("--adapters")
parser.add_argument("--device")
args = parser.parse_args()
niclist = args.niclist
print(niclist)
print(args)
cmdlet = {}
if args == "hostname":
                cmdlet = {'touch "/vmfs/volumes/NFS10/`hostname`.txt"'}
elif niclist == "niclist":
                cmdlet = {'esxcli network nic list > "/vmfs/volumes/NFS10/niclist.`hostname`.txt"'}
elif args == "adapters":
                cmdlet = {'esxcli storage core adapter list > "/vmfs/volumes/NFS10/adapter.`hostname`.txt"'}
elif args == "device":
                cmdlet = {'esxcli storage core device list > "/vmfs/volumes/NFS10/coredevice.`hostname`.txt"'}        
else:
            cmdlet = {'touch "/vmfs/volumes/NFS10/`hostname`.txt"',
                      'esxcli network nic list > "/vmfs/volumes/NFS10/niclist.`hostname`.txt"',
                      'esxcli storage core adapter list > "/vmfs/volumes/NFS10/adapter.`hostname`.txt"',
                      'esxcli storage core device list > "/vmfs/volumes/NFS10/coredevice.`hostname`.txt"'
                      }

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
hostlist = {}
hostquery = {'/opt/vmware/vpostgres/current/bin/psql -U postgres VCDB -c "select ip_address from vpx_host;" | egrep -Evi "rows|ip|--" > /tmp/hostlist',
             }
ssh.connect(hostname="istvc.datamarket.com",#str(input('vCenter Address :')),
            username="root",#str(input('Username :')),
            password="VMware1!")#str(input('Password :')))
for query in hostquery:
        stdin, stdout, stderr = ssh.exec_command(query)
        stdin.close()
        print(repr(stdout.read()))
        stdout.close()
        stderr.close()

with ssh.open_sftp() as sftp, \
    sftp.open('/tmp/hostlist') as f:
    hostlist = [line.strip() for line in f]
    del hostlist[-1]
ssh.close()

print(hostlist)
uname = "root"
passwd = "VMware1!"  #input("please enter password :")
#cmdlet = {'touch "/vmfs/volumes/NFS10/`hostname`.txt"','esxcli network nic list > "/vmfs/volumes/NFS10/niclist.`hostname`.txt"'}

for hname in hostlist:
    ssh.connect(hostname=hname, username=uname, password=passwd)
    for cmd in cmdlet:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.close()
        print(repr(stdout.read()))
        print(repr(stderr.read()))
        stdout.close()
        stderr.close()
    ssh.close()
