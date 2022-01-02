#!/bin/bash
rm -rf /tmp
mkdir /tmp
[ -e ~/.vnc/passwd ] || (mkdir -p ~/.vnc && (echo password | tigervncpasswd -f > ~/.vnc/passwd))
printf %s "admin" | tigervncpasswd -f > ~/.vnc/passwd
tigervncserver :1 -geometry 1280x768 -localhost no -passwd ~/.vnc/passwd -xstartup flwm
/bin/sh -c "while sleep 1000; do :; done"
