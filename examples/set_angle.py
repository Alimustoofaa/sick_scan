from ..sick_scan_tcp import SickScan

# connect to sick
sick_scan = SickScan(
        ip = '192.168.1.110',
        port = 2111
    )

start_angle = 20
stop_angle = 135

sick_scan.set_start_stop_angle(
        start_angle = start_angle,
        stop_angle = stop_angle
    )