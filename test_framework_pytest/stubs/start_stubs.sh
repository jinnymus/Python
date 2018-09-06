#!/usr/bin/env bash

/app/gmlc/server_gmlc.py /app/gmlc false &
/app/sodmtd-server/server_sodmtd.py /app/sodmtd-server &
/app/sos-server/server_sos.py /app/sos-server &
