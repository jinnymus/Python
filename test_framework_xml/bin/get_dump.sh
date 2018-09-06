#!/bin/sh

port1=$1
port2=$2
port3=$3
pcapfile=$4
duration=$5

tshark -l -i lo -V -Y "((http.request.method == POST or http.request.method == POST or http.response) and ((tcp.port == "$port1") or (tcp.port == "$port2") or (tcp.port == "$port3"))) or http.content_encoding or http.response or http.request or http.request.method or http.response.code or http.content_type or http.file_data" \
-Tek -e http.file_data -e http.request.full_uri -e http.request.method -e http.request.version -e http.response.code -e http.content_type -e http.request.uri -e ip.src_host -e ip.dst_host -e tcp.srcport -e tcp.dstport -e tcp.port -Eseparator=# > $pcapfile &