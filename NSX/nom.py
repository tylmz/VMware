import json
import requests
import argparse
import os
import re
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


parser = argparse.ArgumentParser(description='Lets Get Started, tyilmaz@vmware.com for questions and help')
parser.add_argument("--groups",action='store_true', help='do some group thing')
parser.add_argument("--services",action='store_true', help='play on services')
parser.add_argument("--rules",action='store_true', help='makes moves great again!')
args = parser.parse_args()

user = 'admin'
password = 'VMware1!VMware1!'
dIP = '192.168.18.14'
sIP = '192.168.18.14'

def mainmenu():
    print()
    print("************tyilmaz**************")
    print("*******NSX-T Object MOVR*********")
    choice = input("""
                      A: Migrate Groups
                      B: Migrate Services
                      C: Migrate Rules
                      Q: Terminate ME!
                      Please enter your choice: """)    
    if choice == "A" or choice == "a":
        groupsmenu()
    elif choice == "B" or choice == "b":
        servicesmenu()
    elif choice == "C" or choice == "c":
        rulemenu()
    elif choice == "Q" or choice == "q":
        print("bye bye")
        quit()
    else:
        print("Düzgün bir seçenek seçin")
        
def groupsmenu():
    print()
    print("************tyilmaz**************")
    print("*******NSX-T Object MOVR*********")
    choice = input("""
                      A: Parse Source Groups
                      B: Migrate Groups
                      P: Main Menu
                      Please enter your choice: """)
    if choice == "A" or choice == "a":
        getgroups()
        print("Group parsing done!")
        groupsmenu()
    elif choice == "B" or choice == "b":
        writegroups()
        print(str(glen) +" Groups migrated to dest NSX Manager")
        groupsmenu()
    elif choice == "P" or choice == "p":
        mainmenu()
    else:
        print("Düzgün bir seçenek seçin")
        
def servicesmenu():
    print()
    print("************tyilmaz**************")
    print("*******NSX-T Object MOVR*********")
    choice = input("""
                      A: Parse Source Services
                      B: Migrate Services
                      P: Main Menu
                      Please enter your choice: """)
    if choice == "A" or choice == "a":
        getservices()
        print("Service Parsing Done")
        servicesmenu()
    elif choice == "B" or choice == "b":
        writeservices()
        print("Services migrated to dest NSX Manager")
        servicesmenu()
    elif choice == "P" or choice == "p":
        mainmenu()
    else:
        print("Düzgün bir seçenek seçin")

def rulemenu():
    print()
    print("************tyilmaz**************")
    print("*******NSX-T Object MOVR*********")
    choice = input("""
                      A: Parse policies
                      B: Parse source rules, Migrate policies
                      C: Migrate Rules to Destination
                      P: Main Menu
                      Please enter your choice: """)
    if choice == "A" or choice == "a":
        getpolicies()
        print("Policy Parsing Done!")
        rulemenu()
    elif choice == "B" or choice == "b":
        exportpolicies()
        print("Rule Parsing Done!")
        rulemenu()
    elif choice == "C" or choice == "c":
        writerules()
        print("Rules have been migrated!")
        rulemenu()
    elif choice == "P" or choice == "p":
        mainmenu()
    else:
        print("Düzgün bir seçenek seçin")
def jsonize():
    res = requests.get(f"https://{sIP}/policy/api/v1/infra/domains/default/security-policies/", verify=False, auth=HTTPBasicAuth(user, password))
    global response
    response = []
    response = res.json()

def createdirectory():
    checkdir = os.path.exists('rules')
    print(checkdir)
    path = os.getcwd()
    print ("The current working directory is %s" % path)
    if checkdir == False:
        try:
            os.mkdir(path+"/rules")
        except OSError:
            print("Cannot create /rules directory")
        else:
            print("Directory Created")
    else:
        print("Directory exists")
    
def getpolicies():
    jsonize()
    global policies
    policies = response["results"]
    #array uzunluğunu hesaplayalım
    global poln
    poln = len(policies)

def exportpolicies():
    ###policy sectionları alalım ve rules klasörü altına yazalım (içerikle beraber)
    createdirectory()
    for i in range(1, poln-1):
        polname = policies[i]["display_name"]
        polcat = policies[i]["category"]
        #replace blank or other preventing characters with "-" (this characters block creating paths)
        recus = re.sub('[ /()]', '-', polname)
        print(polname)
        print(polcat)
#        res = requests.get(f"https://{sIP}/policy/api/v1/infra/domains/default/security-policies/{polname}/rules", verify=False, auth=HTTPBasicAuth(user, password))
        #for test purposes only
        res = requests.get(f"https://{sIP}/policy/api/v1/infra/domains/default/security-policies/{recus}/rules", verify=False, auth=HTTPBasicAuth(user, password))
        response = res.json()
        with open(f"rules/{recus}.rule", "w") as outfile:
            json.dump(response, outfile)
        outfile.close()
        pjson = {
        "resource_type": "SecurityPolicy",
        "id": polname,
        "display_name": polname,
        "category": polcat,
        "stateful": "true",
        "tcp_strict": "false",
        "locked": "false",
        "scope": [
            "ANY"
        ],
        "_protection": "NOT_PROTECTED",
        "_revision": 0
        }        
        pdata = json.dumps(pjson)
        url = f"https://{dIP}/policy/api/v1/infra/domains/default/security-policies/{recus}"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        resp = requests.patch(url, data=pdata, headers=headers, verify=False, auth=HTTPBasicAuth(user, password))
        #write logs to policylogs.txt file (policyname, category, response).
        with open(f"policylogs.txt", "a") as policylogs:
            policylogs.write(polname)
            policylogs.write("\t")
            policylogs.write(polcat)
            policylogs.write("\t")
            policylogs.write(str(resp))
            policylogs.write("\n")
        policylogs.close()
        print(resp)        
        i=i+1

def getgroups():
    res = requests.get(f"https://{sIP}/policy/api/v1/infra/domains/default/groups/", verify=False, auth=HTTPBasicAuth(user, password))
    global response
    global glen
    global groups
    response = res.json()
    groups = response["results"]
    cursor = response["cursor"]
    result_count = response["result_count"]
    print("Current cursor number: ",cursor)
    print("Total NSX-T Groups number :", result_count)
    glen = len(groups)
    print(groups)
    while glen < result_count:
        try:
            pagires = requests.get(f"https://{sIP}/policy/api/v1/infra/domains/default/groups/?cursor={cursor}", verify=False, auth=HTTPBasicAuth(user, password))
            response = pagires.json()
            nextpage = response["results"]
            groups.extend(nextpage)
            cursor = response["cursor"]
            print(glen, "Groups has been parsed")
        except (IndexError, KeyError):
            print("All Groups has been parsed")
        glen = len(groups)
    print(groups)
    print(glen)

    
def writegroups():
    getgroups()
    for gn in range(0, glen):
        groupname = groups[gn]["display_name"]
        print(groupname)
        try:
            ipset = groups[gn]["expression"][0]["ip_addresses"]
        except IndexError:
            print("Hatalı Index")
            ipset = None
        gjson = {
            "expression": [
                {
                    "ip_addresses": ipset,
                    "resource_type": "IPAddressExpression",
                    "_protection": "NOT_PROTECTED"
                }
            ],
            "extended_expression": [],
            "reference": "false",
            "resource_type": "Group",
            "display_name": groupname,
            "_revision": 0
        }
        if ipset != None:
            gdata = json.dumps(gjson)
        else:
            gdata = gjson.pop("expression")
            gdata = json.dumps(gjson)
        url = f"https://{dIP}/policy/api/v1/infra/domains/default/groups/{groupname}"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        resp = requests.patch(url, data=gdata, headers=headers, verify=False, auth=HTTPBasicAuth(user, password))
        print(resp)
        gn = gn+1

def getservices():
    res = requests.get(f"https://{sIP}/policy/api/v1/infra/services", verify=False, auth=HTTPBasicAuth(user, password))
    global response
    global slen
    global services
    response = res.json()
    services = response["results"]
    slen = len(services)
    print(slen)
    
def writeservices():
    getservices()
    for sn in range(0, slen):
        servicename = services[sn]["display_name"]
        issystem = services[sn]["_system_owned"]
        if issystem != True:
            servicename = services[sn]["display_name"]
            serviceentry = services[sn]["service_entries"]
            selen = len(serviceentry)
            for se in range(0, selen):
                try:
                    try:
                        l4_protocol = serviceentry[se]["l4_protocol"]
                    except:
                        print("l4_protocol not found")
                    try:
                        protocol = serviceentry[se]["protocol"]
                    except:
                        print("Protocol is L4")
                    source_ports = serviceentry[se]["source_ports"]
                    destination_ports = serviceentry[se]["destination_ports"]
                    resource_type = serviceentry[se]["resource_type"]
                    display_name = serviceentry[se]["display_name"]
                    print(l4_protocol,source_ports,destination_ports,resource_type,display_name)
                except KeyError:
                    print("key not found")
                servicejson = {
                  "display_name": servicename,
                  "_revision": 0,
                  "service_entries": [
                      {
                          "resource_type": resource_type,
                          "display_name": display_name,
                          "source_ports": source_ports,
                          "destination_ports": destination_ports,
                          "l4_protocol": l4_protocol
                      }
                  ]
                }
                sdata = json.dumps(servicejson)
                url = f"https://{dIP}/policy/api/v1/infra/services/{servicename}"
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                resp = requests.patch(url, data=sdata, headers=headers, verify=False, auth=HTTPBasicAuth(user, password))
                print(resp)
                se = se+1            
        sn = sn+1


#ilk ve sondakileri almamak için 1 ve -1 arasını iterate edelim.
def writerules():
    for i in range(1, poln-1):
        polname = policies[i]["display_name"]
        recus = re.sub('[ /()]', '-', polname)
        # policy içeriklerini tek tek okuyalım
        f = open(f"rules/{recus}.rule", "r")
        data = json.loads(f.read())
        r = data["results"]
        dlenght = len(r)
        #okuyup öğrendiklerimizi yazalım
        for t in range(dlenght):
            ruleid = r[t]["display_name"]
            recusruleid = re.sub('[ /()]', '-', ruleid)
            sgroup = r[t]["source_groups"]
            dgroup = r[t]["destination_groups"]
            services = r[t]["services"]
            revjson = {
            "action": "ALLOW",
            "resource_type": "Rule",
            "id": ruleid,
            "display_name": ruleid,
            "path": f"/infra/domains/default/security-policies/{recus}/rules/{recusruleid}",
            "parent_path": f"/infra/domains/default/security-policies/{recus}",
            "sources_excluded": "false",
            "destinations_excluded": "false",
            "source_groups": sgroup,
            "destination_groups": dgroup,
            "services": services,
            "profiles": [
                    "ANY"
            ],
            "logged": "false",
            "scope": [
                    "ANY"
            ],
            "disabled": "false",
            "direction": "IN_OUT",
            "ip_protocol": "IPV4_IPV6",
            "is_default": "false",
            "_system_owned": "false",
            "_protection": "NOT_PROTECTED",
            "_revision": 0
            }     
            print(ruleid)
            ruledata = json.dumps(revjson)
            url = f"https://{dIP}/policy/api/v1/infra/domains/default/security-policies/{recus}/rules/{recusruleid}"
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            resp = requests.patch(url, data=ruledata, headers=headers, verify=False, auth=HTTPBasicAuth(user, password))
            print(resp)
            t=t+1
        # Closing file
        f.close()
        i=i+1

if args.rules:
    while True:
        rulemenu()
elif args.groups:
    while True:
        groupsmenu()
elif args.services:
    while True:
        servicesmenu()
else:
    while True:
        mainmenu()
