#!/bin/bash

# TODO: Figure out how to get ECM to work here
#       without breaking Windows support

# Currently OSX supports Mass Storage + Serial but *not* RNDIS (at least not 10.12 anyway)
# Windows 10 and Linux seem to support everything
# Windows 8, 7 and below are untested

if [ ! -d /sys/kernel/config/usb_gadget ]; then
        modprobe libcomposite
fi

#if [ -d /sys/kernel/config/usb_gadget/g1 ]; then
#        exit 0
#fi

ID_VENDOR="0x1d6b"
ID_PRODUCT="0x0104"

SERIAL="$(grep Serial /proc/cpuinfo | sed 's/Serial\s*: 0000\(\w*\)/\1/')"
MAC="$(echo ${SERIAL} | sed 's/\(\w\w\)/:\1/g' | cut -b 2-)"
MAC_HOST="12$(echo ${MAC} | cut -b 3-)"
MAC_DEV="02$(echo ${MAC} | cut -b 3-)"

cd /sys/kernel/config/usb_gadget/

mkdir g1
cd g1

echo "0x0200" > bcdUSB
echo "0x02" > bDeviceClass
echo "0x00" > bDeviceSubClass
echo "0x3066" > bcdDevice
echo $ID_VENDOR > idVendor
echo $ID_PRODUCT > idProduct

# Windows extensions to force config

echo "1" > os_desc/use
echo "0xcd" > os_desc/b_vendor_code
echo "MSFT100" > os_desc/qw_sign

mkdir strings/0x409
echo "9112473" > strings/0x409/serialnumber
echo "Pimoroni Ltd." > strings/0x409/manufacturer
echo "PiratePython" > strings/0x409/product

# Config #1 for OSX / Linux

mkdir configs/c.1
mkdir configs/c.1/strings/0x409
echo "CDC 2xACM+Mass Storage+RNDIS" > configs/c.1/strings/0x409/configuration

mkdir functions/acm.GS0
mkdir functions/acm.GS1
mkdir functions/ecm.usb0 # OSX/Linux
mkdir functions/rndis.usb0 # Flippin' Windows
#mkdir functions/mass_storage.piratepython

#echo "/dev/mmcblk0p1" > functions/mass_storage.piratepython/lun.0/file
#echo 0 > functions/mass_storage.piratepython/stall
#echo 0 > functions/mass_storage.piratepython/lun.0/cdrom
#echo 0 > functions/mass_storage.piratepython/lun.0/nofua
#echo 1 > functions/mass_storage.piratepython/lun.0/removable
#echo "PiratePython" > functions/mass_storage.piratepython/lun.0/inquiry_string

echo "RNDIS" > functions/rndis.usb0/os_desc/interface.rndis/compatible_id
echo "5162001" > functions/rndis.usb0/os_desc/interface.rndis/sub_compatible_id

echo $MAC_HOST > functions/rndis.usb0/host_addr
echo $MAC_DEV > functions/rndis.usb0/dev_addr

# Set up the rndis device only first

ln -s functions/rndis.usb0 configs/c.1

# Tell Windows to use config #2

ln -s configs/c.1 os_desc

# Show Windows the RNDIS device with
# bDeviceClass 0x02
# bDeviceSubClass 0x02

echo "20980000.usb" > UDC

# Give it time to install

sleep 5

# Yank it back

#echo "" > UDC

# Sneak in all the extra goodies

#ln -s functions/acm.GS0 configs/c.1
#ln -s functions/acm.GS1 configs/c.1
#ln -s functions/mass_storage.piratepython configs/c.1

# Reset bDeviceClass to 0x00
# This is essential to make it work in Windows 10
# Basically forces it to use device information
# in the descriptors versus assuming a particular class.

echo "0x00" > bDeviceClass

# Re-attach the gadget
#
echo "20980000.usb" > UDC

# BOOM!

ifconfig usb0 up 10.0.99.1
