import sys
import math
import time
import socket
import struct

class SickScan:
    def __init__(
            self,
            ip: str,
            port: int,
        ) -> None:
        self.ip = ip
        self.port = port
        self.connect()

    def connect(self) -> None:
        self.socket_sick = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.socket_sick.connect((self.ip, self.port))

    def release(self) -> None:
        self.socket_sick.close()

    @staticmethod
    def int_2hex(decimal_number) -> str:
        return hex(int(decimal_number * 10000))[2:].upper()
    
    @staticmethod
    def int_2hexstring(decimal_number) -> str:
        return hex(decimal_number)[2:].upper()
    
    @staticmethod
    def hex_to_meters(i) -> list[float]:
        i = [int(x,16)/1000 for x in i ]
        return i
    
    @staticmethod
    def uint32(i):
        i = struct.unpack('>i', bytes.fromhex(i))[0]
        return i

    @staticmethod
    def remove_outprov(data: str) -> str:
        data = data.replace('\x02','')
        data = data.replace('\x03','')
        return data
    
    @staticmethod
    def to_cartesian(
            distances: list[float], 
            angles: list[float]
        ) -> tuple[list[float], list[float]]:
        x = list(map(lambda r, t: r * math.cos(math.radians(t)), distances, angles))
        y = list(map(lambda r, t: r * math.sin(math.radians(t)), distances, angles))
        return x, y

    def send_socket(
            self,
            message : str,
            buffer : int
        ) -> str:
        try:
            message = f'\x02{message}\x03'.encode()
            self.socket_sick.send(message)
        except ConnectionAbortedError:
            self.connect()
            time.sleep(0.1)
        finally:
            message = f'\x02{message}\x03'.encode()
            self.socket_sick.send(message)

        data = self.socket_sick.recv(buffer)
        data = data.decode()
        data = self.remove_outprov(data=data)
        return data

    def set_ip_addres(
            self,
            ip: str
        ) -> None:
        # login auth
        data = self.send_socket(
            message = "sMN SetAccessMode 03 F4724744",
            buffer = 128
        )
        print(data)

        hex_ip =  " ".join([
                    self.int_2hexstring(int(i)) for i in ip.split('.')
                ])
        data = self.send_socket(
            message = f"sWN EIIpAddr {hex_ip}",
            buffer = 128
        )
        print('Set IpAddr : ',data)
        
        # reboot device
        data = self.send_socket(
            message = "sMN mSCreboot",
            buffer = 128
        )
        print('Reboot : ',data)
        sys.exit('Reboot Device')
        

    def set_start_stop_angle(
            self,
            start_angle : int,
            stop_angle : int
        ) -> None:

        # login auth
        data = self.send_socket(
            message = "sMN SetAccessMode 03 F4724744",
            buffer = 128
        )
        print(data)
        # set angle
        hex_start_angle = self.int_2hex(start_angle)
        hex_stop_angle = self.int_2hex(stop_angle)
        data = self.send_socket(
            message = f"sWN LMPoutputRange 1 1388 {hex_start_angle} {hex_stop_angle}",
            buffer = 1024
        )
        print('Set angle : ',data)

        # disconnect and connect
        self.release(); time.sleep(0.1); self.connect()

    def extract_telegram(
            self,
            telegram: str
        ) -> tuple[list[float], list[float]]:
        tokens = telegram.split()
        # header = tokens[:18]
        sections = tokens[18:]

        scale_factor = 1 if sections[3] == '3F800000' else 2
        try:
            start_angle = self.uint32(sections[5])/10000.0
        except ValueError:
            start_angle = int(sections[5], 16)/10000.0
        angle_step = int(sections[6], 16) / 10000.0
        value_count = int(sections[7], 16)   
        values = list(map(lambda x: (int(x, 16) * scale_factor)/1000.0, sections[8:8+value_count]))
        distances =  self.hex_to_meters(list(sections[8:8+value_count]))
        angles = [start_angle + angle_step * n for n in range(value_count)]
        return angles, values

    def scan(
            self,
        ) -> str:
        data = self.send_socket(
            message = 'sRN LMDscandata',
            buffer = 10240
        )
        return data
