# Sick Scan LMS1xx, LMS5xxx

This code provides a comprehensive interface for interacting with a SICK LIDAR sensor with TCP connection, enabling users to configure parameters, retrieve scan data, and perform data processing tasks. It is a valuable tool for applications that require interfacing with LIDAR sensors for environmental sensing, mapping, and other related tasks.

## Install

```shell
git clone https://github.com/Alimustoofaa/sick_scan.git
cd sick_scan
pip3 install .
```

## Features

* Connect to TCP

  ```
  sick_scan = SickScan(
          ip = '192.168.1.110',
          port = 2111
      )
  ```
* Setting Ip Address
  The method will handle the necessary communication and configuration Ip Address, including rebooting the device to save permanent and changed will be active after rebooting the device

  ```python
  new_ip = '192.168.1.110'
  sick_scan.set_ip_addres(
          ip = new_ip
      )
  ```
* Setting Start Stop Angle

  The method will handle the necessary communication with the sensor to configure the specified start and stop angles for data acquisition.

  ```python
  start_angle = 20
  stop_angle = 135

  sick_scan.set_start_stop_angle(
          start_angle = start_angle,
          stop_angle = stop_angle
      )
  ```
* Scan

  The method will return the scan data as a string in the `telegram` variable.

  ```python
  telegram = sick_scan.scan()
  ```

  example output:

  ```
  RA LMDscandata 1 1 153D067 0 0 1FA7 1FAA 939EF3A6 939F9752 0 0 7 0 0 1388 168 0 1 DIST1 3F800000 00000000 FFF92230 1388 21D 55 51 44 46 4F 4E 40 4B 4E 4A 54 54 54 52 5A 5C 60 58 5E 59 62 5E 64 53 59 5A 56 5F 64 60 61 65 6B 6D 6C 69 69 73 6F 7A 7F 81 85 7F 7E 83 83 8F 8B 99 A1 A1 AD A3 AD AA B6 CF F2 10F 114 115 117 112 10D 114 115 113 116 11C 106 112 10E 111 114 113 115 115 10C 10F 10D 123 10C 113 10F 10F 142 21A 5DF 5E3 5C9 5CF 5D2 5D4 5D2 5D1 5DD 5DF 56A 468 3C2 35D 356 37E 382 377 304 25E 264 276 27F 0 0 0 0 0 3 3 3 3 27D 3 3 0 0 16C 158 158 153 14D 14C 14E 146 142 13D 13C 13C 13B 137 13E 132 13C 142 13C 13C 14B 14F 14C 146 137 13F 136 25F 21F 1C0 110 102 100 EB E4 EC EF F8 F3 F4 F8 FA ED F6 118 15A 414 4C8 4BD 4BA 4C8 4BA 4BF 4AA 4A7 4A0 4A0 49A 45C 3 3 337 340 345 3E4 432 442 434 435 437 43D 42F 41F 42A 3F3 3D8 425 42A 430 42A 422 404 3F7 42D 432 42F 434 439 43B 434 431 42E 41D 423 424 414 403 416 41A 426 449 42B 42C 42E 42E 435 432 42C 42A 42F 428 436 42B 431 431 42C 42F 433 439 434 430 43A 43F 433 44B 440 43D 441 442 448 43E 442 44F 449 458 451 453 45B 452 45D 45C 45A 46C 46D 46D 471 483 47E 47C 47E 485 482 491 495 4A1 494 4A1 4A0 4B6 4AE 4B7 4BE 4C3 4C5 4CB 4E0 4DC 4DF 4EB 4ED 4F9 507 503 50C 50B 527 523 520 541 549 541 541 53B 54A 556 562 56A 54B 49F 2A8 1A6 131 132 146 13F 147 167 1DB 5CB 60C 62D 646 646 660 67E 686 697 6B7 6D3 6F5 700 6F9 706 797 BDD BC6 BAE B96 B8D B7D B70 B93 BB3 BEA C13 C3E C67 C9B CCB CFD D2B D94 DC0 C6
  ```
* Extract Output telegram

  ```
  angles, values = sick_scan.extract_telegram(telegram=telegram)
  ```

  **Inspecting telegram**

  - LMS111

  ```
  DIST1 3F800000 00000000 B71B0 1388 47 4EE 
        \------/                        \-/
     scaling factor              first measurement
  ```

  - LMS511

  ```
  DIST1 40000000 00000000 AAE60 1388 3D 288
        \------/                        \-/
     scaling factor              first measurement
  ```

  **Parsing Telegram**

  * Split the telegram string into tokens, using space as the separator.
  * Check that it is the expected command type and command
  * Check that there are 0 encoder payload blocks
  * Check that there is exactly 1 16-bit channel block
  * Check that it is a 'DIST1' block
  * Determine the scaling factor used (1x or 2x)
  * Parse the start angle and angle step, and scale them to degrees
  * Parse the value count
  * Grab the appropriate number of value tokens that follow, discard the rest ** Parse each value, and scale it by the scaling factor
  * Calculate the angles corresponding to each measured value (`start_angle + step * n`)

**Reference:**

- [https://cdn.sick.com/media/docs/7/27/927/technical_information_telegram_listing_ranging_sensors_lms1xx_lms5xx_tim2xx_tim5xx_tim7xx_lms1000_mrs1000_mrs6000_nav310_ld_oem15xx_ld_lrs36xx_lms4000_en_im0045927.pdf]()
- [https://stackoverflow.com/questions/76586507/difference-in-range-of-values-between-lms111-and-lms511-sensors-for-millimeter-m]()
