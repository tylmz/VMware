import sshtunnel
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
hostlist = {}
hostquery = {'/opt/vmware/vpostgres/current/bin/psql -U postgres VCDB -c "select ip_address from vpx_host;" | egrep -Evi "rows|ip|--" > /tmp/hostlist',
             }
ssh.connect(hostname=str(input('vCenter Address :')), username=str(input('Username :')), password=str(input('Password :')))
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
cmdlet = {'touch "/vmfs/volumes/NFS10/`hostname`.txt"','esxcli network nic list > "/vmfs/volumes/NFS10/niclist.`hostname`.txt"'}

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

