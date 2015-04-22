
# -*- coding: utf8 -*-
from ivy.std_api import *
import os
import logging

logging.getLogger('Ivy').setLevel(logging.ERROR)

#from pprzrest import mLog





SocketIo = None

class mAC:
    AcName = None
    TrackAcId = None

    def __init__(self, AcId, AcName):
        self.AcId = AcId
        self.AcName = AcName

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       #TODO groupname olacak asagidaki
       return {
           'AcId' : self.AcId,
           'AcName': self.AcName
       }


class mIvyClass:
    IVYAPPNAME = 'PPRZweb'
    ProcessId = None
    ReqId = 0
    SocketIo = None
    mIvyBus = None
    AC_LIST = []

    def __init__(self, mIvyBus, SocketIoIn):
        self.SocketIo = SocketIoIn
        self.mIvyBus = mIvyBus
        self.ProcessId = os.getpid()

    def on_connection_change(self, agent, event):
        print "ConChanged"
        #mLog.debug("Connection changed!")
    
    def on_die(self, agent, id):
        #mLog.debug("Stopping ivybus agent..")
        IvyStop()
        #mLog.debug("Connection changed!")

    def check_ac_list(self, AcId, AcName):
        for ac in self.AC_LIST:
            if ac.AcId == AcId:
                return
        NewAc = mAC(AcId, AcName)
        
        self.AC_LIST.append(NewAc)
        print "New AC added. ", AcId, " ", AcName
        self.SocketIo.emit('AC_LIST', {'data': [i.serialize for i in AC_LIST]  } )

    def on_tracker_gps_param_changed(self, *args):
       #Log.debug("on_tracker_gps_param_changed")
        TrLat = args[5]
        TrLon = args[6]
        TrAlt = args[9]
        print "Tracker Pos=" , TrLat, " ", TrLon, " ", TrAlt 
        self.SocketIo.emit( 'TR_STATUS', { 'TrLat': TrLat, 'TrLon':TrLon , 'TrAlt':TrAlt } ,namespace='/PprzOnWeb' )

    def on_aircrafts(self, *args):        
        print "on_aircrafts"
        for x in args:
            print x
        self.ReqId = self.ReqId + 1

        IvySendMsg(self.IVYAPPNAME + str(self.ProcessId) + str(self.ReqId) + " CONFIG_REQ " + args[2])

    def on_config(self, *args):
        print "on_config"
        check_ac_list(int(args[2]), args[8])

    
    @property
    def get_tracked_ACID (self, TrackerID):
        for ac in self.AC_LIST:
            if ac.AcId == TrackerID:
                return ac.TrackAcId
        return None

    @property
    def set_tracker(self, TrackerID, AcID, TrLat, TrLon, TrAlt):
        for ac in self.AC_LIST:
            if ac.AcId == TrackerID:
                ac.TrackAcId = AcID
        
        IvySendMsg(IVYAPPNAME + " SET_ANT_TR " + str(TrackerID) + " " + str(AcID) + " " + str(TrLat) + " " + str(TrLon) + " " + str(TrAlt) )

    @property
    def stop_tracker(self):    
    IvySendMsg(self.IVYAPPNAME + " STOP_ANT_TR")


    @property
    def stop_tracker(self):
        IvySendMsg(self.IVYAPPNAME + " STOP_ANT_TR")

    @property
    def turn_tracker_axis(self, Axis , Direction):
        IvySendMsg( self.IVYAPPNAME + " TURN_ANT_TRACKER " + str(Axis) + " " + str(Direction) )

    @property
    def turn_tracker_axis(self, Axis , Direction):
        IvySendMsg( self.IVYAPPNAME + " TURN_ANT_TRACKER " + str(Axis) + " " + str(Direction) )


    @property
    def set_tracker_zero(self):
        IvySendMsg( self.IVYAPPNAME + " ANT_TRACKER_SET_ZERO")

    @property
    def init_bus(self):
        NewAc = mAC(255, "BBB_Tracker")    
        self.AC_LIST.append(NewAc)
        sisreadymsg = "%s is ready" % self.IVYAPPNAME

        # initialising the bus
        IvyInit(self.IVYAPPNAME,            # application name for Ivy
                sisreadymsg ,          # ready message
                1,                     # parameter ignored
                on_connection_change,  # handler called on connection/deconnection
                on_die                 # handler called when a die msg is received 
                )
        IvyStart(self.mIvyBus)

        IvyBindMsg(on_tracker_gps_param_changed, "ground TRACKER_GPS (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*)")
        IvyBindMsg(on_config, "(\\S*) ground CONFIG (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*) (\\S*)")
        IvyBindMsg(on_aircrafts, "(\\S*) ground AIRCRAFTS (\\S*)")
        IvySendMsg(self.IVYAPPNAME + str(self.ProcessId) + str(self.ReqId) +" AIRCRAFTS_REQ")
















if __name__ == '__main__':
    mIvy = mIvyClass("",None)
    mIvy.init_bus()

    

