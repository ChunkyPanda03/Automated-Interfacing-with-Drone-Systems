from pymavlink import mavutil, mavwp, mavexpression
import time, json
util = mavutil
class drone():
    def __init__(self, device, source_system, source_component = 0):
        self.con = util.mavlink_connection(device=device, source_system=source_system, source_component=source_component)
        self.mavmsg = mavutil.mavlink
        self.wp = mavwp.MAVWPLoader()
        self.msg = self.con.mav.command_long_send
        self.fence = mavwp.MAVFenceLoader(target_system=self.con.target_system,target_component=self.con.target_component)
    def precision_land_mode(self,mode):
        x = mode.lower()
        if x == "disabled":
            return 0
        elif x == "opportunistic":
            return 1
        elif x == "required":
            return 2
        else:
            print("unknown mode")
    def frame_type_to_id(self,frame):
        x = frame.upper()
        if x == "MAV_FRAME_GLOBAL":
            return 0
        elif x == "MAV_FRAME_LOCAL_NED":
            return 1
        elif x == "MAV_FRAME_GLOBAL_RELATIVE_ALT":
            return 3
        else:
            print("unsupported frame type or not yet supported")
    def connect_test(self, timeout = 5):
        try:
            hb = self.con.wait_heartbeat(True, timeout)

        finally:
            if hb == None:
                print("connection failed")
                return False
            else:
                print(hb)
                print("connection success")
                return True

    def arm_drone(self, arm=True):
        if arm == True:
            arm = 1
        elif arm == False:
            arm = 0

        try:
            arming = self.msg(self.con.target_system,
                              self.con.target_component,
                              self.mavmsg.MAV_CMD_COMPONENT_ARM_DISARM,
                              0,  #number of confirmations
                              1,  #force
                              arm,  # 0 = disarm 1 = arm
                              0, 0, 0, 0, 0)
        finally:
            if arming == None:
                print("arming success")
                time.sleep(5)
            if arming != None:
                print("arming failed")
    def modeset(self, mode):
        def mode_to_id():
            variable = mode.lower()
            if variable == "stabilize":
                return 0
            elif variable == "acro":
                return 1
            elif variable == "althold":
                return 2
            elif variable == "auto":
                return 3
            elif variable == "guided":
                return 4
            elif variable == "loiter":
                return 5
            elif variable == "rtl":
                return 6
            elif variable == "circle":
                return 7
            elif variable == "land":
                return 9
            elif variable == "drift":
                return 11
            elif variable == "sport":
                return 13
            elif variable == "flip":
                return 14
            elif variable == "autotune":
                return 15
            elif variable == "poshold":
                return 16
            elif variable == "brake":
                return 17
            elif variable == "throw":
                return 18
            elif variable == "avoid_adsb":
                return 19
            elif variable == "guided_nogps":
                return 20
            elif variable == "smart_rtl":
                return 21
            elif variable == "flowhold":
                return 22
            elif variable == "follow":
                return 23
            elif variable == "zigzag":
                return 24
            elif variable == "systemid":
                return 25
            elif variable == "heli_autorotate":
                return 26
            elif variable == "auto rtl":
                return 27
            else:
                print("invalid input")
            '''f*** you dillon'''
        try:
            mode = self.msg(self.con.target_system,
                            self.con.target_component,
                            self.mavmsg.MAV_CMD_DO_SET_MODE,
                            0,
                            1, #custom mode just leave 1
                            mode_to_id(), #mode number can't be bothered to do smart switch statememnt
                            0,
                            0,
                            0,
                            0,
                            0)
        finally:
            print(mode)
    def fence_poly_inclusion(self,frame='MAV_FRAME_GLOBAL_RELATIVE_ALT', inclusion_group=1, vertex_count=3, lat=[], long=[], current_item=0, autocontinue=0, seq=0):
        wps=len(lat)
        self.con.wait_heartbeat(blocking=True)
        items = []
        for i in range(wps):
            m = self.mavmsg.MAVLink_mission_item_int_message(self.con.target_system,
                                                                 self.con.target_component,
                                                                 seq,
                                                                 self.frame_type_to_id(frame),
                                                                 self.mavmsg.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION,
                                                                 current_item,  # current false:0 true:1
                                                                 autocontinue, #auto cont
                                                                 wps,
                                                                 inclusion_group,
                                                                 0,
                                                                 0,
                                                                 int(lat[i]*1e7),
                                                                 int(long[i]*1e7),
                                                                 0, #alt
                                                                 1) #mission type fence


            self.wp.add(m)
            print("fencepoint " + str(i))

            items.append(m)
            seq += 1
        self.wp.reindex()
    def fence_poly_exclusion(self, frame='MAV_FRAME_GLOBAL_RELATIVE_ALT', lat=[], long=[], current_item=0, autocontinue=0, seq=0):
        wps=len(lat)
        self.con.wait_heartbeat(blocking=True)
        items = []
        for i in range(wps):
            m = self.mavmsg.MAVLink_mission_item_int_message(self.con.target_system,
                                                                 self.con.target_component,
                                                                 seq,
                                                                 self.frame_type_to_id(frame),
                                                                 self.mavmsg.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION,
                                                                 current_item,  # current false:0 true:1
                                                                 autocontinue, #auto cont
                                                                 wps,
                                                                 0,
                                                                 0,
                                                                 0,
                                                                 int(lat[i]*1e7),
                                                                 int(long[i]*1e7),
                                                                 0, #alt
                                                                 1) #mission type fence


            self.wp.add(m)
            print("fencepoint " + str(i))

            items.append(m)
            seq += 1
        self.wp.reindex()

    def fence_circle_exclusion(self, radius, frame='MAV_FRAME_GLOBAL_RELATIVE_ALT', lat=[], long=[], current_item=0, autocontinue=0, seq=0):
        wps=len(lat)
        self.con.wait_heartbeat(blocking=True)

        for i in range(wps):
            m = self.mavmsg.MAVLink_mission_item_int_message(self.con.target_system,
                                                                 self.con.target_component,
                                                                 seq,
                                                                 self.frame_type_to_id(frame),
                                                                 self.mavmsg.MAV_CMD_NAV_FENCE_CIRCLE_EXCLUSION,
                                                                 current_item,  # current false:0 true:1
                                                                 autocontinue, #auto cont
                                                                 float(radius[i]),
                                                                 0,
                                                                 0,
                                                                 0,
                                                                 int(lat[i]*1e7),
                                                                 int(long[i]*1e7),
                                                                 0,
                                                                 1) #mission type fence

            print("fencepoint " + str(i))
            self.wp.add(m)
            seq += 1
        self.wp.reindex()

    def home_set(self, frame, alt=0, use_current=0, lat=0, long=0, yaw=0, current_item=0, autocontinue=0, seq=0):
        print(lat)
        print(long)
        self.msg(self.con.target_system,
                 self.con.target_component,
                 self.mavmsg.MAV_CMD_NAV_TAKEOFF,
                 0,  # nu=mber of confirmations
                 use_current,  # pitch
                 0,  # Empty
                 0,  # Empty
                 yaw,
                 int(lat * 1e7),  # 0 = current lat
                 int(long * 1e7),  # 0 = current long
                 alt)
    def fence_send(self):
        print(str(self.wp.count()) + ' in waypoint count')

        self.con.mav.mission_count_send(
                self.con.target_system,
                self.con.target_component, #this tells there are items waiting to be sent
                self.wp.count(),
                1)

        for i in range(self.wp.count()):

            msg = self.con.recv_match(type=['MISSION_REQUEST'], blocking=True)
            self.con.mav.send(self.wp.wp(msg.seq),force_mavlink1=False)
            print('Sending fence {0}'.format(msg.seq))
        self.wp.clear()
        print("should be sending fence")
    def fence_clear_all(self):
        self.fence.clear()
        print("fences cleared")
    def fence_enable(self, enable="enable"):
        def enable_id():
            x = enable.lower()
            if x == "disable":
                return 0
            elif x == "enable":
                return 1
            elif x == "disable_floor_only":
                return 2
            else:
                print("unknown enable")

        self.msg(self.con.target_system,
                 self.con.target_component,
                 self.mavmsg.MAV_CMD_DO_FENCE_ENABLE,
                 0,
                 enable_id(),  # custom mode just leave 1
                 0,  # mode number can't be bothered to do smart switch statememnt
                 0,
                 0,
                 0,
                 0,
                 0)

    def guided_takeoff_global(self, pitch, yaw, altitude, lat=0, long=0):
        try:
            self.msg(self.con.target_system,
                            self.con.target_component,
                            self.mavmsg.MAV_CMD_NAV_TAKEOFF,
                            0,  #nu=mber of confirmations
                            pitch,  #pitch
                            0,  #Empty
                            0,  #Empty
                            yaw,
                            lat,  # 0 = current lat
                            long,  # 0 = current long
                            altitude)

        finally:
            print("takingoff")

    def change_speed(self, speed_type, speed, throttle=-1):

        def speed_id():
            x = speed_type.lower()
            if x == "air_speed":
                return 0
            elif x == "ground_speed":
                return 1
            elif x == "climb_speed":
                return 2
            elif x == "descent_speed":
                return 3

        self.msg(self.con.target_system,
                 self.con.target_component,
                 self.mavmsg.MAV_CMD_DO_CHANGE_SPEED,
                 0,  # nu=mber of confirmationspoints.append
                 speed_id(),  # pitch
                 speed,  # Empty
                 throttle,  # Empty
                 0,
                 0,  # 0 = current lat
                 0,  # 0 = current long
                 0)
    def guided_takeoff_local(self, pitch=0, yaw=0, Ascend_Rate=5, ypos=0, xpos=0,zpos=0): #this is unsupported don't use
        try:
            takingoff = self.msg(self.con.target_system,
                                 self.con.target_component,
                                 self.mavmsg.MAV_CMD_NAV_TAKEOFF_LOCAL,
                                 0,  # number of confirmations
                                 pitch,  # M/S
                                 0,  # empty
                                 Ascend_Rate,  # M/S
                                 yaw,  # rad
                                 ypos,  # M
                                 xpos,  # M
                                 zpos  # M
                                 )
        finally:



            if takingoff == None:
                print("message valid sent")
            if takingoff != None:
                print("message not valid or not sent")

    def guided_servo(self, instance, pwm):
        self.msg(self.con.target_system,
                                 self.con.target_component,
                                 self.mavmsg.MAV_CMD_DO_SET_SERVO,
                                 0,
                                 instance,
                                 pwm,
                                 0,
                                 0,
                                 0,
                                 0,
                                 0)
    def guided_land_global(self,lat,long,alt, land_mode,yaw=0,abort_alt=0):
        self.msg(self.con.target_system,
                 self.con.target_component,
                 self.mavmsg.MAV_CMD_NAV_LAND,
                 0, print(
                 abort_alt,
                 self.precision_land_mode(str(land_mode)),
                 0, #empty
                 yaw,
                 lat,
                 long,
                 alt))#landing altitude of current frame
    def guide_rtl(self):
        self.msg(self.con.target_system,
                 self.con.target_component,
                 self.mavmsg.MAV_CMD_NAV_RETURN_TO_LAUNCH,
                 0,
                 0,#Empty
                 0,#Empty
                 0,  # empty
                 0,#Empty
                 0,#Empty
                 0,#Empty
                 0) #Emptydialect=2

    def wp_set_wp(self, frame, alt=[], lat=[], long=[],hold=0, current_item=0,autocontinue=0, yaw=0, pass_radius=0, accept_radius=10, seq=1):
        wps = len(lat)
        self.con.wait_heartbeat(blocking=True)
        for i in range(wps):
            self.wp.add(self.mavmsg.MAVLink_mission_item_int_message(self.con.target_system,
                                                                 self.con.target_component,
                                                                 seq,
                                                                 self.frame_type_to_id(frame),
                                                                 mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                                                                 current_item,  # current false:0 true:1
                                                                 autocontinue,
                                                                 hold,
                                                                 accept_radius,
                                                                 pass_radius,
                                                                 yaw,
                                                                 int(lat[i] * 1e7),
                                                                 int(long[i] * 1e7),
                                                                 int(alt[i]),
                                                                 0))
            seq += 1
    def send_wp(self):
        print(str(self.wp.count()) + ' in waypoint count')
        self.con.mav.mission_count_send(
            self.con.target_system,
            self.con.target_component,  # this tells there are items waiting to be sent
            self.wp.count(),
            0)

        for i in range(self.wp.count()):
            msg = self.con.recv_match(type=['MISSION_REQUEST'], blocking=True)
            self.con.mav.send(self.wp.wp(msg.seq))
            #self.con.wait_heartbeat(blocking=True)
            #time.sleep(1)
            print('Sending waypoint {0}'.format(msg.seq))
        self.wp.clear()



    def wp_set_land(self, abort_alt, land_mode, frame, lat, long, alt, yaw="NaN", current_item=0, autocontinue=0, seq=1):





        self.wp.add(self.mavmsg.MAVLink_mission_item_message(self.con.target_system,
                                                             self.con.target_component,
                                                             seq,
                                                             self.frame_type_to_id(frame),
                                                             self.mavmsg.MAV_CMD_NAV_LAND,
                                                             current_item,#current false:0 true:1
                                                             autocontinue,
                                                             abort_alt,
                                                             self.precision_land_mode(land_mode),
                                                             0, #Empty
                                                             yaw,
                                                             lat,
                                                             long,
                                                             self.con.target_component,
                                                             alt))

    def wp_set_takeoff(self, alt, frame, pitch=0, lat=0, long=0, yaw=0, current_item=0, autocontinue=0, seq=0):


        self.wp.add(self.mavmsg.MAVLink_mission_item_message(self.con.target_system,
                                                             self.con.target_component,
                                                             seq,
                                                             self.frame_type_to_id(frame),
                                                             mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                                                             current_item,#current false:0 true:1
                                                             autocontinue,
                                                             pitch,
                                                             0,#Empty
                                                             0, #Empty
                                                             yaw,
                                                             lat,
                                                             long,
                                                             alt))
    def wp_home_set(self, frame, alt=0, use_current=0, lat=0, long=0, yaw=0, current_item=0, autocontinue=0, seq=0):
        print(lat)
        print(long)
        self.wp.add(self.mavmsg.MAVLink_mission_item_message(self.con.target_system,
                                                             self.con.target_component,
                                                             seq,
                                                             self.frame_type_to_id(frame),
                                                             mavutil.mavlink.MAV_CMD_DO_SET_HOME,
                                                             current_item,  # current false:0 true:1
                                                             autocontinue,
                                                             use_current,
                                                             0,  # Empty
                                                             0,  # Empty
                                                             yaw,
                                                             int(lat * 1e7),
                                                             int(long * 1e7),
                                                             alt))
    def wp_clear_all(self):
        self.con.waypoint_clear_all_send()

    def recive_parameter_change(self, source_system=1, source_component=3):
        if self.mavmsg.get_srcSystem() == source_system and self.mavmsg.get_srcComponent() == source_component:
            print("Got message from ground!")
            if self.mavmsg.get_type() is self.mavmsg.MAVLink_param_set_message.name:
                print(
                    f"Set paramter {self.mavmsg.param_id} to '{self.mavmsg.param_value}'. Parameter type is '{self.mavmsg.param_type}'.")
            else:
                print("Bad message")

