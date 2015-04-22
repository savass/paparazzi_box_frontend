#Simple monitoring tool to watch agents
import time
from threading import Thread
import fcntl
import os

from mProcessHolder import ProcessHolder

class SimProcMon:

    ProcessDemonThread = None
    RunProcessDeamon = True
    ProcessList = []
    ProcessOutput = ""

    def __init__(self, Logger, SocketIo=None):
    	self.mLog = Logger
    	self.SocketIo = SocketIo
    	self.mLog.debug("New SimProcMon class created.")


    def inform_clients(self):
    	self.mLog.debug("Informing clients..")
    	self.SocketIo.emit('StatusMsg',{'data': self.ProcessOutput,
    		'link_sts': self.get_status("link"),
    		'server_sts': self.get_status("server"),
    		'app_server_sts': self.get_status("app_server"),
    		'link_arg': self.get_process_arg("link"),
    		'server_arg':self.get_process_arg("server"),
    		'app_server_arg': self.get_process_arg("app_server")},namespace='/PprzOnWeb')
    
    def get_status(self, ProcessName):    	
    	for mProcess in self.ProcessList:
    		if mProcess.ProcName == ProcessName:
    			return mProcess.ProcessRunning
    	return False
    
    
    def stop_process(self, ProcessName):
          
        for mProcess in self.ProcessList:
        	if mProcess.ProcName == ProcessName:
        		mProcess.RunProcess = False
        		if not mProcess.ProcessAgent is None:
        			mProcess.ProcessAgent.kill()
        			mProcess.ProcessAgent = None
        			self.mLog.info("%s agent terminated.", mProcess.ProcName)
        			#remove from ProcessList
        			self.ProcessList.remove(mProcess)
        			self.ProcessOutput = self.ProcessOutput + mProcess.ProcName + " agent terminated."+ "<br />" 
        			self.inform_clients()
        			return
        		else:
        			self.mLog.error("%s process agent is None.", mProcess.ProcName)
    
    
    def start_process(self, ProcessName, RunStr):
        #need to check if process already started.
        if self.get_status(ProcessName):
        	self.mLog.error("%s is already started.", ProcessName)
        	return
        nPH = ProcessHolder(ProcessName, RunStr, True)
        nPH.run()
        #append the process to process list
        self.ProcessList.append(nPH)
        self.mLog.info("Trying to start %s agent.", ProcessName)
    
    def process_deamon(self):
        self.mLog.info("Process monitor started.")
        while self.RunProcessDeamon:
            time.sleep(0.5)
            for mProcess in self.ProcessList:
                #first need to check if process is running or not.
                
                if mProcess.RunProcess and not mProcess.ProcessAgent is None:
                    #print "mProcess ", mProcess.ProcessRunning
                    fd = mProcess.ProcessAgent.stdout.fileno()
                    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                    try:
                        AppOut = mProcess.ProcessAgent.stdout.read()
                        if AppOut:
                            self.ProcessOutput = self.ProcessOutput + "<br />".join(AppOut.split("\n"))
                            self.inform_clients()
                    except:
                        pass
                if not mProcess.ProcessRunning:
                    #give some time to process
                    self.mLog.info("%s seems to be fresh started. Waiting..", mProcess.ProcName)
                    time.sleep(1.5)

                if not mProcess.ProcessAgent.poll() is None:
                    #process error    <span class="myClass">test</span>        	
                    self.ProcessOutput = self.ProcessOutput  + '<span class="MonError">' + mProcess.ProcName + ' stopped.</span> <br />'
                    
                    if mProcess.RunProcess and mProcess.ProcessRunning:
                        mProcess.run()
                        self.ProcessOutput = self.ProcessOutput  + '<span class="MonOutput">' +  mProcess.ProcName + ' restarted. </span> <br />'
                        self.mLog.info("%s.ProcessAgent.poll() is None > ProcessRunning.", mProcess.ProcName)
                        self.inform_clients()
                    else:
                        self.mLog.info("%s.ProcessAgent.poll() is None > startup failed!", mProcess.ProcName)
                        self.ProcessList.remove(mProcess) 
                        self.inform_clients()
                        continue
                #seems like process started successfully
                if not mProcess.ProcessRunning:
                	mProcess.ProcessRunning = True
                	self.ProcessOutput = self.ProcessOutput  + '<span class="MonOutput">' +  mProcess.ProcName + ' agent started.. </span> <br />'
                	self.mLog.info("%s agent started.", mProcess.ProcName)
                	self.inform_clients()
            #print len(ProcessList)
        self.mLog.info("Process monitor stopped.")
    
    def get_process_arg(self,ProcessName):
        for mProcess in self.ProcessList:
            if mProcess.ProcName == ProcessName:
            	return mProcess.ProcArg
        return None


    def run_process_mon_deamon(self):
        if self.ProcessDemonThread is None:
            self.ProcessDemonThread = Thread(target=self.process_deamon)
            self.ProcessDemonThread.daemon = True
            self.ProcessDemonThread.start()
        else:
            self.mLog.error("Process monitor deamon already stared!")    