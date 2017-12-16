MSR605 Toolbox
======
**MSR605 Toolbox** is a small piece of code which help using the magnetic card reader/writer MSR605.

## Description
The MSR605 is a magnetic card reader/writer you can acquire for 100$. It's a great machine to work and play with magnetic cards. When I started using it, I noticed a lack in the available software. The manufacturer gives a demo software running only on windows and the others open-source projects are pretty old and incomplete. So I give it a fresh new start in Python. Feel welcome to fork or do some pull requests

## Roadmap
- [x] Reset
- [ ] Read ISO
- [ ] Write ISO
- [ ] Read raw
- [ ] Write raw
- [x] Test communication
- [x] Test ram
- [x] Test sensor
- [x] Turn on all leds
- [x] Turn on red led
- [x] Turn on green led
- [x] Turn on yellow led
- [ ] Set leading zero
- [ ] Check leading zero
- [x] Erase card
- [x] Set BPI
- [x] Set BPC
- [x] Get device model
- [x] Get firmware version
- [x] Set coercitivity

## Useful Documentation
### MSR605
* [MSR605](http://www.triades.net/downloads/MSR605%20Programmer%27s%20Manual.pdf) - Programmer manual for the MSR605.

### ISO7811
* [ISO7811](https://www.magtek.com/content/documentationfiles/d99800004.pdf)- Easy and graphic documentation for the ISO7811.
* [ISO7811 - medium](http://arrowinks.com/digital-ink-industry-insights/magnetic-encoding-standards/) - A bit more detailed documentation for 7811. Still easy to understand.
* [ISO7811 - hard](http://d1.amobbs.com/bbs_upload782111/files_32/ourdev_576472.pdf) - Complete documentation of ISO7811. Harder to understand.

### PL2303
* [PL2303](http://prolificusa.com/pl-2303hx-drivers/) The PL2303 is a Serial-USB Controller built inside the MSR605. You need the PL2303 drivers on your machine to communicate with the MSR605. The drivers are built-in the Linux kernel. 

### Python
* [pySerial](http://pythonhosted.org/pyserial/) - Module to help with communication on serial port.
* [argparse](https://docs.python.org/3/library/argparse.html) - Easy module to have a friendly comme-line interface.

## Similar projects
This project is inspired from others open-source projects.
* [Penturalabs/MSR605](https://github.com/PenturaLabs/MSR605/) - A C/C++ library for interaction with MSR605. updated 4 years ago.
* [ioerror/libmsr](https://github.com/ioerror/libmsr) - Basic C library for MSR. updated 8 years ago.
* [tio/tio](https://github.com/tio/tio) - A simple TTy terminal application.

## Useful software
To help undestand the behavior of the MSR605, I recommand to use the Windows software from the manufacturer. You can install it in a virtual box with a Linux host and use a USB sniffer to see how the software communicate with the MSR605.