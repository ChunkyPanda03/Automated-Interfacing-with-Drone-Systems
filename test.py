import MCC_DL
import pymavlink.dialects.v20.common
import time
import json_to_py
d1 = MCC_DL.drone(device="udp:localhost:14550", source_system=1,)
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
    input('allset?')
    d1.change_speed("air_speed",15)
    d1.modeset('guided')
    d1.arm_drone(True)
    d1.guided_takeoff_global(0,0,30)
    input('ready for auto?')
    d1.modeset('auto')
    input('rtl?')
    d1.guide_rtl()



    #d1.guided_servo(10, 500)
    #time.sleep(10)
    #d1.guided_servo(10, 1100)
    #d1.change_speed("air_speed",10,-1)
    #d1.wp_set_send_wp('mav_frame_global',0)
    #d1.wp_set_takeoff(100,"MAV_FRAME_GLOBAL_RELATIVE_ALT",seq=0)
    #d1.wp_set_takeoff(100, "mav_frame_global", seq=1)
    #d1.wp_set_send_wp("MAV_FRAME_GLOBAL_RELATIVE_ALT",alt=[100,100],lat=[-35.361548,-35.361548],long=[149.164084,149.164090],seq=1)

    #d1.modeset("guided")
    #d1.arm_drone(True)
    #d1.guided_takeoff_global(0,0,100,0,0)
    #time.sleep(60)
    #d1.modeset("auto")
    #d1.guide_rtl()
    #d1.wp_clear_all()
    #d1.wp_set_wp("MAV_FRAME_GLOBAL_RELATIVE_ALT",alt=json_to_py.waypoints('altitude'),lat=json_to_py.waypoints('latitude'),long=json_to_py.waypoints('longitude'),seq=1)
    #d1.send_wp()











    #pi mavproxy.py --master=/dev/ttyACM0 --out=/dev/ttyUSB0
    #local mavproxy.py --out=udp:localhost:14550
    #servo is 10 min:500 max:1100
