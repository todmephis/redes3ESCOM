import xml.etree.ElementTree as etree
import sys
def parse_xml(filename):
    """Given an XML filename, reads and parses the XML file and passes the 
    the root node of type xml.etree.ElementTree.Element to the get_host_data
    function, which will futher parse the data and return a list of lists
    containing the scan data for a host or hosts."""
    try:
        tree = etree.parse(filename)
    except Exception as error:
        print("[-] A an error occurred. The XML may not be well formed. "
              "Please review the error and try again: {}".format(error))
        exit()
    root = tree.getroot()
    scan_data = get_host_data(root)
    return scan_data
def get_host_data(root):
    """Traverses the xml tree and build lists of scan information
    and returns a list of lists.
    """
    host_data = []
    hosts = root.findall('host')
    for host in hosts:
        addr_info = []

        # Ignore hosts that are not 'up'
        if not host.findall('status')[0].attrib['state'] == 'up':
            continue
        # Get IP address and host info. If no hostname, then ''
        ip_address = host.findall('address')[0].attrib['addr']
        host_name_element = host.findall('hostnames')
        try:
            host_name = host_name_element[0].findall('hostname')[0].attrib['name']
        except IndexError:
            host_name = ''
        
        # If we only want the IP addresses from the scan, stop here
        if True:
            addr_info.extend((ip_address, host_name))
            host_data.append(addr_info)
            continue
        
        # Get the OS information if available, else ''
        try:
            os_element = host.findall('os')
            os_name = os_element[0].findall('osmatch')[0].attrib['name']
        except IndexError:
            os_name = ''
    return host_data
def list_ip_addresses(data):
    """Parses the input data to return only the IP address information"""
    ip_list = [item[0] for item in data]
    sorted_set = sorted(set(ip_list))
    addr_list = [ip for ip in sorted_set]
    return addr_list

try:
    file = open(sys.argv[1],"r") 
except Exception as e:
    print(e)
    exit(-1 )
data = parse_xml(file)
addrs = list_ip_addresses(data)
with open("outputs/hostsfound.list", "w") as f:
    for addr in addrs:
        f.write(addr)
        f.write("\n")
        print("[+]IP {} encontrada en {}".format(addr, sys.argv[1]))
f.close