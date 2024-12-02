#!/bin/bash

#MEMozki dev
IPTABLES="/sbin/iptables"
IP6TABLES="/sbin/ip6tables"
IPSET="/sbin/ipset"
SYSCTL="/sbin/sysctl"
SSHPORT="22"
TCP_PORTS="80,443"
LOG_LIMIT="-m limit --limit 2/min --limit-burst 5"
BANNED_IP_FILE="/etc/iptables/banned_ips.txt"
cat <<EOF > /etc/sysctl.conf
net.ipv4.ip_forward=0
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv4.conf.all.secure_redirects=1
net.ipv4.conf.default.secure_redirects=1
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv4.icmp_ignore_bogus_error_responses=1
net.ipv4.tcp_syncookies=1
net.ipv4.tcp_timestamps=1
net.ipv4.tcp_max_syn_backlog=4096
net.ipv4.tcp_synack_retries=2
net.ipv4.conf.all.log_martians=1
net.ipv4.ip_local_port_range=1024 65000
net.ipv4.tcp_fin_timeout=15
net.ipv4.tcp_keepalive_time=300
EOF
"$SYSCTL" -p
"$IPSET" create blacklist hash:net maxelem 1000000 timeout 3600
"$IPSET" create whitelist hash:net maxelem 1000000 timeout 0
"$IPTABLES" -P INPUT DROP
"$IPTABLES" -P FORWARD DROP
"$IPTABLES" -P OUTPUT ACCEPT
"$IPTABLES" -F
"$IPTABLES" -X
"$IPTABLES" -t nat -F
"$IPTABLES" -t nat -X
"$IPTABLES" -N LOGGING
"$IPTABLES" -A LOGGING -m limit --limit 2/min --limit-burst 5 -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
"$IPTABLES" -A LOGGING -j DROP
"$IPTABLES" -A INPUT -i lo -j ACCEPT
"$IPTABLES" -A OUTPUT -o lo -j ACCEPT
"$IPTABLES" -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
"$IPTABLES" -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
"$IPTABLES" -A INPUT -m set --match-set blacklist src -j DROP
"$IPTABLES" -A FORWARD -m set --match-set blacklist src -j DROP
"$IPTABLES" -A INPUT -p tcp -m multiport --dports $TCP_PORTS -m state --state NEW -j ACCEPT
"$IPTABLES" -A INPUT -p tcp --dport "$SSHPORT" -m state --state NEW -j ACCEPT
"$IPTABLES" -A INPUT -p tcp --dport "$SSHPORT" -m recent --set --name SSH --rsource
"$IPTABLES" -A INPUT -p tcp --dport "$SSHPORT" -m recent --update --seconds 60 --hitcount 4 --name SSH --rsource -j DROP
"$IPTABLES" -A INPUT -p tcp -m connlimit --connlimit-above 10 --connlimit-mask 32 -j DROP
"$IPTABLES" -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s --limit-burst 1 -j ACCEPT
"$IPTABLES" -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT
"$IPTABLES" -A INPUT -f -j LOGGING
"$IPTABLES" -A INPUT -j LOGGING
"$IPTABLES" -A FORWARD -j LOGGING
if [ -f "$BANNED_IP_FILE" ]; then
    while IFS= read -r ip; do
        "$IPSET" add blacklist "$ip"
    done < "$BANNED_IP_FILE"
fi
apt-get install fail2ban -y
cat <<EOF > /etc/fail2ban/jail.local
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
action = iptables[name=SSH, port=ssh, protocol=tcp]
backend = auto
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
EOF
systemctl restart fail2ban
"$IPTABLES" -A INPUT -p udp --dport 53 -j ACCEPT
"$IPTABLES" -A OUTPUT -p udp --dport 53 -j ACCEPT
"$IP6TABLES" -P INPUT DROP
"$IP6TABLES" -P FORWARD DROP
"$IP6TABLES" -P OUTPUT ACCEPT
"$IP6TABLES" -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
"$IP6TABLES" -A INPUT -i lo -j ACCEPT
"$IP6TABLES" -A INPUT -p tcp --dport "$SSHPORT" -j ACCEPT
"$IP6TABLES" -A INPUT -p tcp --dport 80 -j ACCEPT
"$IP6TABLES" -A INPUT -p tcp --dport 443 -j ACCEPT
"$IP6TABLES" -A INPUT -j LOGGING
"$IP6TABLES" -A FORWARD -j LOGGING