connection=$(nmcli -g name,type connection  show  --active | awk -F: '/ethernet|wireless/ { print $1 }')
nmcli con mod "$connection" ipv4.dns "{{ ansible_default_ipv4.address }}"
nmcli con down "$connection" && nmcli con up "$connection"
nmcli con mod "$connection" ipv4.ignore-auto-dns no
