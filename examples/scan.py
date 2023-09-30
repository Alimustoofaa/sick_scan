import time
from ..sick_scan_tcp import SickScan

# connect to sick
sick_scan = SickScan(
        ip = '192.168.1.110',
        port = 2111
    )

try:
    while True:
        telegram = sick_scan.scan()
        try:
            angles, values = sick_scan.extract_telegram(telegram=telegram)
            x, y = sick_scan.to_cartesian(angles=angles, distances=values)
        except Exception as e:
            print(e)
        time.sleep(0.1)
except KeyboardInterrupt:
    sick_scan.release()