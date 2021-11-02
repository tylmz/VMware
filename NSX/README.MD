**nom.py** is python based NSX-T object mover. 
- requires "pip install requests"

**What it does?**
- it can move objects like groups, services, firewall policies and firewall rules from old NSX-T environment to new NSX-T environment.

**How it works?**
- just run it like "python nom.py" you will get into a menu. 

**What it can move?**
- IP based groups
- TCP UDP services
- Policy Sections (defaults excluded)
- Rules in Policy Sections (defaults excluded)

**What it needs?**
-Needs more capability to move even VM, vnic, port based defined groups.
-Needs capability to move other service types and nested things.

**Development?**
- If needed i will develop this more. This was just a code written in hours to move one of my customer's environment.

I'm always free to get advises.
