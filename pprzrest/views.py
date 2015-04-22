# -*- coding: utf8 -*-

from gevent import monkey
monkey.patch_all()

from flask import render_template, session, request, redirect, url_for, jsonify, send_file
from flask.ext.socketio import emit

from pprzrest import app,socketio, mLog, SPM, AppConfig, mIvy
import os

@socketio.on('connect', namespace='/PprzOnWeb')
def test_connect():
    print "client connected"
    mLog.debug("Client connected.")
    if not SPM.ProcessOutput is None:
    	emit('StatusMsg', {'data': SPM.ProcessOutput,
    		'link_sts': SPM.get_status("link"),
    		'server_sts': SPM.get_status("server"),
    		'app_server_sts': SPM.get_status("app_server"),
    		'link_arg': SPM.get_process_arg("link"),
    		'server_arg':SPM.get_process_arg("server"),
    		'app_server_arg': SPM.get_process_arg("app_server")
    		 } )

@socketio.on('disconnect', namespace='/PprzOnWeb')
def test_disconnect():
    print('Client disconnected')
    mLog.debug("Client disconnected.")


@socketio.on('get_ac_list', namespace='/PprzOnWeb')
def get_aclist():
    print('AC list request')
    mLog.debug("AC list request.")
    #if not SPM.ProcessOutput is None:
    emit('AC_LIST', {'data': [i.serialize for i in mIvy.AC_LIST]  } )

TrLat = None
TrLon = None
TrAlt = None
@socketio.on('SetTracker', namespace='/PprzOnWeb')
def set_tracker(Data):
    print('set_tracker')
    TrackerId = int(Data['TrackerId'])
    AcId = int(Data['AcId'])

    global TrLat    
    TrLat = Data['Lat']
    global TrLon
    TrLon = Data['Lon']
    print "Lat type", type(TrLon)
    global TrAlt
    TrAlt = Data['Alt']

    mIvy.set_tracker( TrackerId, AcId, TrLat, TrLon, TrAlt )
    mLog.debug("set_tracker")

@socketio.on('StopTracker', namespace='/PprzOnWeb')
def stop_tracker():
    print('Stop tracking..')  

    mIvy.stop_tracker()
    mLog.debug("stop_tracker")

@socketio.on('GetTrackersAc', namespace='/PprzOnWeb')
def get_tracker_ac(Data):
    print('GetTrackersAc')
    if not Data['TrackerId'] is None:
        TrackerId = int(Data['TrackerId'])
        print "TrackerId:", TrackerId
        AcId = mIvy.get_tracked_ACID(TrackerId)
        global TrLat
        global TrLon
        global TrAlt
        emit('TRACKERS_AC', {'AcId': AcId, 'Lat':TrLat, 'Lon':TrLon, 'Alt':TrAlt  } )

@socketio.on('TurnTracker', namespace='/PprzOnWeb')
def turn_tracker(Data):
    print('TurnTracker')
    if not Data['Axis'] is None:
        TurnAxis = int(Data['Axis'])
        print TurnAxis
        TurnDirection = int(Data['Value'])
        print TurnDirection
        mIvy.turn_tracker_axis(TurnAxis, TurnDirection)

@socketio.on('SetZero', namespace='/PprzOnWeb')
def set_tracker_zero():
    print('SetZero')
    mIvy.set_tracker_zero()

@app.route('/pprzrest/api/v1.0/run', methods = ['POST'])
def run_agent():    
    agent_name = request.form.get('agent', "")
    variable = request.form.get('inputvar', "")
    #print "agent:", agent_name
    #print "variable",variable
    if agent_name == "link":
    	
    	RunStr = AppConfig.PAPARAZZI_PATH + AppConfig.LINK_PATH + variable
    	SPM.start_process("link", RunStr)
   	
    if agent_name == "server":

    	RunStr = AppConfig.PAPARAZZI_PATH + AppConfig.SERVER_PATH + variable 	
    	SPM.start_process("server", RunStr)
    	
    if agent_name == "app_server":
    	
    	RunStr = AppConfig.PAPARAZZI_PATH + AppConfig.APP_SERVER_PATH + variable    	
    	SPM.start_process("app_server", RunStr)

    return jsonify( { 'STATUS': 'OK' } ), 200

#stop
@app.route('/pprzrest/api/v1.0/stop', methods = ['POST'])
def stop_agent():
    agent_name = request.form.get('agent', "")
    if agent_name == "link":
    	SPM.stop_process("link")
    if agent_name == "server":
    	SPM.stop_process("server")
    if agent_name == "app_server":
    	SPM.stop_process("app_server")

    return jsonify( { 'STATUS': 'OK' } ), 200

@app.route('/mfile', methods = ['GET'])
def get_file():
    mFile = request.form.get('file_path', None)
    mLog.debug("Client file request: %s", mFile)
    if mFile is None:
        return jsonify( { 'ERROR': 'No file name in request.' } ), 400
    return send_file(mFile)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trackers')
def trackers():
    return render_template('trackers.html')

@app.route('/system')
def show_system_page():
    return render_template('system.html')

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    os.system("/sbin/poweroff")
    return "Shutting down.. Please do not remove power untill all leds are turned off.. "

