#!/bin/bash
nohup jupyter lab --no-browser --allow-root --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''&
nohup watch -n 1 /opt/crispy-doom/screenshot_sync.py &
set -e
trap ctrl_c INT
function ctrl_c() {
  exit 0
}
rm /tmp/.X1-lock 2> /dev/null &
/opt/noVNC/utils/launch.sh --vnc localhost:$VNC_PORT --listen $NO_VNC_PORT &
echo -e "$TIGER_VNC_PASSWORD\n$TIGER_VNC_PASSWORD" | vncserver -xstartup /src/startdoom.sh &
wait
