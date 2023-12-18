import messages_lib
import pymavlink.dialects.v20.common
import time
import json_to_py
d1 = messages_lib.drone(device="udp:127.0.0.1:14551", source_system=1)
if d1.connect_test(40) == True:
    def send_it():
       # d1.wp_clear_all()
    #d1.home_set(alt=0,frame='MAV_FRAME_GLOBAL_RELATIVE_ALT',lat=json_to_py.lost_comms('latitude'),long=json_to_py.lost_comms('longitude'),seq=0,current_item=0)
        #d1.wp_set_takeoff(0,'MAV_FRAME_GLOBAL_RELATIVE_ALT')
        #d1.wp_set_wp('MAV_FRAME_GLOBAL_RELATIVE_ALT',alt=json_to_py.waypoints('altitude'),lat=json_to_py.waypoints('latitude'),long=json_to_py.waypoints('longitude'),seq=1,accept_radius=1)
        #d1.send_wp()
    #
    #x = input("WPS GOOD?")
        d1.fence_clear_all()
        d1.fence_poly_inclusion('MAV_FRAME_GLOBAL_RELATIVE_ALT', lat=json_to_py.boundary('latitude'),long=json_to_py.boundary('longitude'))
        d1.fence_circle_exclusion(radius=json_to_py.stationaryObstacles('radius'),lat=json_to_py.stationaryObstacles('latitude'),long=json_to_py.stationaryObstacles('longitude'))
        d1.fence_send()
    send_it()
    print(d1.con.wait_heartbeat(blocking=False))
