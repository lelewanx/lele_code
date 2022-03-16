import socket
import sys

sys.path.extend([".", ".."])
from remote_ssh_command import Remote_SSH_Server


def check_hostname_by_ip(**host):
    name, ip = host.get("hostname"), host.get("ip")
    try:
        hostname, alias, ips = socket.gethostbyaddr(ip)
        print("gethostbyaddr: ", hostname, alias, ips)
        if hostname == name:
            return True
    except socket.error as e:
        print(f"check_hostname_by_ip. {e}")
        return None


def check_ip_by_hostname(**host):
    name, ip = host.get("hostname"), host.get("ip")
    try:
        hostname, alias, ips = socket.gethostbyname_ex(name)
        print("gethostbyname_ex: ", hostname, alias, ips)
        if ip == ips[0]:
            return host
        else:
            print(f"IP changes from {ip} to {ips[0]}.")
            host['ip'] = ips[0]
            return host
    except socket.error as e:
        print(f"check_ip_by_hostname. {e}")
        return None


def check_available_host(**host):
    if bool(check_hostname_by_ip(**host)):
        new_host = check_ip_by_hostname(**host)
        return new_host
    else:
        new_host = check_ip_by_hostname(**host)
        return new_host


def start_ssh_connect(**host):
    rss = Remote_SSH_Server(**host)
    if bool(rss):
        if rss.ssh_open() and rss.sftp_open():
            return rss


def main():
    hostlist = [{
        "ip": "10.239.89.150",
        "hostname": "lele-desktop.sh.intel.com",
        "port": 22,
        "username": "lelle",
        "password": "intel123"
    }, {
        "ip": "10.239.85.94",
        "hostname": "nuc-shanghai.sh.intel.com",
        "port": 22,
        "username": "nuc",
        "password": "intel123"
    }]

    for host in hostlist:
        new_host = check_available_host(**host)
        rss = start_ssh_connect(**new_host)
        if bool(rss):
            cmd = "hostname -A"
            ret = rss.send_ssh_command(cmd)
            print(f"available: {ret}")


if __name__ == '__main__':
    main()
