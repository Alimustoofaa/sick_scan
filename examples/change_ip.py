from ..sick_scan_tcp import SickScan

# connect to sick
current_ip = '192.168.1.110'
sick_scan = SickScan(
        ip = current_ip,
        port = 2111
    )

# change ip addres
new_ip = '192.168.1.110'
sick_scan.set_ip_addres(
        ip = new_ip
    )