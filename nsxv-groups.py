import json
import requests
import argparse
import os
import re
import xml.etree.ElementTree as ET
import urllib.request
import xmltodict
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser(description='Lets Get Started, tyilmaz@vmware.com for questions and help')
parser.add_argument("--groups",action='store_true', help='do some group thing')
parser.add_argument("--services",action='store_true', help='play on services')
parser.add_argument("--rules",action='store_true', help='makes moves great again!')
args = parser.parse_args()

user = 'admin'
password = ''
NSXVIP = ''
NSXTIP = ''

def getgroups():
    res = requests.get(f"https://{NSXVIP}/api/2.0/services/securitygroup/scope/globalroot-0", verify=False, auth=HTTPBasicAuth(user, password))
    global response
    global glen
    global groups
    tree = ET.fromstring(res.content)
    limit = len(tree)
    memberlist = {}
    vmlist = {}
    for i in range(limit):
        for child in tree[i].iter('securitygroup'):
            json_sg = ET.tostring(child).decode("utf-8")
            json_sgx = xmltodict.parse(json_sg)
            json_sgl = json.dumps(json_sgx)
            json_sgy = json.loads(json_sgl)
            groupname = json_sgy["securitygroup"]["name"]
            print("\b")
            print(20*"--")
            print("Group Name: ", groupname)
            memberlist.update({'group': groupname})
            #groups having more than one object
            try:
                if type(json_sgy["securitygroup"]["member"]) == list:
                    memberlen = len(json_sgy["securitygroup"]["member"])
                    for t in range(memberlen):              
                        membername = json_sgy["securitygroup"]["member"][t]["name"]
                        membertype = json_sgy["securitygroup"]["member"][t]["type"]["typeName"]
                        t=t+1
                        print("Member Name: ", membername)
                        print("Member Type: ",membertype)
                        vmlist.update({'vmname': membername})
                    memberlist.update({'vms': vmlist})
                    vmlist = {}
                #groups having one object
                elif type(json_sgy["securitygroup"]["member"]) == dict:
                    membername = json_sgy["securitygroup"]["member"]["name"]
                    membertype = json_sgy["securitygroup"]["member"]["type"]["typeName"]
                    print("Member Name: ", membername)
                    print("Member Type: ",membertype)
                    vmlist.update({'vmname': membername})
                    memberlist.update({'vms': vmlist})
                    vmlist = {}
            except (IndexError,KeyError) as error:
                print("***No member here***")
        i=i+1
    print(memberlist)
getgroups()

##def getservices():
##    res = requests.get(f"https://{NSXVIP}/api/2.0/services/securitygroup/scope/globalroot-0", verify=False, auth=HTTPBasicAuth(user, password))
##    global response
##    global glen
##    global groups
##    tree = ET.fromstring(res.content)
##    limit = len(tree)    for i in range(limit):
##    for child in tree[i].iter('securitygroup'):
##        json_sg = ET.tostring(child).decode("utf-8")
##        json_sgx = xmltodict.parse(json_sg)
##        json_sgl = json.dumps(json_sgx)
##        json_sgy = json.loads(json_sgl)
##getservices()
