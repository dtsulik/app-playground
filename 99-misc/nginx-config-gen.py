#!/usr/bin/env python3

#
# sample cvs.
# 
# url_start,ip,port,websocket
# user1,127.0.0.1,444,true
# user2,127.0.0.1,555,false

import csv

server_port = 80
config_file = "/etc/nginx/nginx_include.conf"

f = open(config_file, "w")
websocket_config = """
    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }
"""
f.write(websocket_config)

with open('test.cvs') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            server_start_block = f"""
    server {{
        listen {server_port};
"""
            f.write(server_start_block)
            line_count += 1
        # end of column names
        else:
            location_block = f"""
        location ~ ^/{row[0]}[\d]* {{
            proxy_set_header X-Forwarded-Host $host:$server_port;
            proxy_set_header X-Forwarded-Server $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://{row[1]}:{row[2]};
        }}
            """
            location_websocket_block = f"""
        location ~ ^/{row[0]}[\d]* {{
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_pass http://{row[1]}:{row[2]};
        }}
            """
            if("true" in {row[3]}):
                f.write(location_websocket_block)
            else:
                f.write(location_block)

            line_count += 1
        # end of loop

server_end_block = f"""
    }}
"""
f.write(server_end_block)
f.close()
