#!/bin/bash

echo "Generating documentation for Raspberry Pi implementation"
echo "========================================================"
cd /root/development/morTimmy/raspberrypi/docs/
sphinx-apidoc -o . /root/development/morTimmy/raspberrypi/morTimmy/
make html
cp -R /root/development/morTimmy/raspberrypi/docs/_build/html/* /var/www/morTimmy/raspberrypi
chown nginx:nginx -R /var/www/morTimmy/raspberrypi/*

echo ""
echo "Generating documentation for Arduino implementation"
echo "========================================================"
cd /root/development/morTimmy/arduino/docs/
sphinx-apidoc -o . /root/development/morTimmy/arduino/morTimmy/
make html
cp -R /root/development/morTimmy/arduino/docs/_build/html/* /var/www/morTimmy/arduino
chown nginx:nginx -R /var/www/morTimmy/arduino/*
