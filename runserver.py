#!vir_python/bin/python
# -*- coding: utf8 -*-

from pprzrest import app, socketio, mIvy, mIvyClass, AppConfig

try:
    if not AppConfig.IVY_BUS == "":
        mIvy = mIvyClass("",socketio)
    else:
    	mIvy = mIvyClass("192.168.4.255:2010",socketio)
        #mIvy = mIvyClass((AppConfig.IVY_BUS +":2010"),socketio)
    mIvy = mIvyClass("192.168.4.255:2010",socketio)
    mIvy.init_bus()
    socketio.run(app,host='0.0.0.0')
except KeyboardInterrupt:
    print "Stopping server"
    mIvy.stop_ivy()
    socketio.server.stop()
#socketio.run(app,host='0.0.0.0')

