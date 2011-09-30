from Tkinter import *
from ttk import *
from functools import partial
from twisted.internet import tksupport, reactor
from logger import Logger
from multiprocessing import Queue
import tkMessageBox
import traceback

class View(object):
    
    def __init__(self,controller):
        self.logger = Logger()
        self.controller = controller
        self.top = Tk()
        self.pages = {}
        self.current = ''
        self.disabledStack = [] 

    def optionView(self):

        tksupport.install(self.top)

        self.top.title('Chat')
        self.top.geometry( '700x700' )

        def callback():
            self.stop()

        self.top.protocol("WM_DELETE_WINDOW", callback)

        optionView = Frame(self.top)
        optionView.pack()

        MyButton = partial(Button, optionView, text='Host a server', command=self.serverView)

        chooseServer = MyButton()
        chooseServer.pack()

        chooseClient = MyButton(text='Connect to a server', command=self.clientView)
        chooseClient.pack()

        
        quitButton = Button(optionView, text='QUIT',command=self.stop)
        quitButton.pack()

        self.pages['optionView'] = optionView
        self.current = 'optionView'

        reactor.run()

    def serverView(self):

        self.pages[self.current].pack_forget()

        serverView = Frame(self.top)
        serverView.pack()

        hostFrame = Frame(serverView)
        hostFrame.pack()

        labelHost = Label(hostFrame, text='Uw IP is: ')
        labelHost.pack()

        entryHost = Entry(hostFrame, width=20)
        entryHost.insert(0,self.controller.getIP())
        entryHost['state'] = 'readonly'
        entryHost.pack()

        inputPort = Frame(serverView)
        inputPort.pack()

        labelPort = Label(inputPort, text='Port:')
        labelPort.pack()

        entryPort = Entry(inputPort,width=20)
        entryPort.insert(0,'55555')
        entryPort.pack()

        def callback(event=''):
            try:
                self.controller.setupServer(port=int(entryPort.get()))
                self.workView()
            except ValueError:
                self.showInfo('Error','Incorrect input, please try again')
            except Exception as detail:
                self.showInfo('Error','A network error has occured, please try again later')
                self.log('Error','Server: %s | %s' % (repr(detail),traceback.format_exc()),'serverView')

        continueButton = Button(serverView, text='Continue', command=callback)
        continueButton.pack()

        entryPort.bind('<Return>',callback)

        buttonQuit = Button(serverView,text='QUIT',command=self.stop)
        buttonQuit.pack()
        
        self.pages['serverView'] = serverView
        self.current = 'serverView'

    def clientView(self):

        self.pages[self.current].pack_forget()

        clientView = Frame(self.top)
        clientView.pack()

        inputHost = Frame(clientView)
        inputHost.pack()

        labelHost = Label(inputHost, text='IP:')
        labelHost.pack()

        entryHost = Entry(inputHost, width=30)
        entryHost.insert(0,'localhost')
        entryHost.pack()

        inputPort = Frame(clientView)
        inputPort.pack()

        labelPort = Label(inputPort, text='Port:')
        labelPort.pack()

        entryPort = Entry(inputPort,width=30)
        entryPort.insert(0,'55555')
        entryPort.pack()

        def callback(event=''):
            try:
                self.controller.setupClient(entryHost.get(),int(entryPort.get()))
                self.waitView()
            except ValueError:
                self.showInfo('Error','Incorrect input, please try again')
            except Exception as detail:
                self.showInfo('Error','A network error has occured, please try again later')
                self.log('Error','Client: %s | %s' % (repr(detail),traceback.format_exc()),'clientView')
                

        continueButton = Button(clientView, text='Continue', command=callback)
        continueButton.pack()

        entryPort.bind('<Return>',callback)

        buttonQuit = Button(clientView,text='QUIT',command=self.stop)
        buttonQuit.pack()

        self.pages['clientView'] = clientView
        self.current = 'clientView'
        
    def waitView(self):
        
        self.pages[self.current].pack_forget()

        if 'waitView' not in self.pages:
            
            waitView = Frame(self.top)
            waitView.pack()

            buttonQuit = Button(waitView,text='QUIT',command=self.stop)
            buttonQuit.pack()

            self.pages['waitView'] = waitView
            self.current = 'waitView'
            
        else:
            
            self.pages['waitView'].pack()
            self.current = 'waitView'

    def workView(self):

        self.pages[self.current].pack_forget()

        if 'workView' not in self.pages:

            workView = Frame(self.top)
            workView.pack(expand=YES,fill=BOTH)

            frameResults = LabelFrame(workView,text='Results')
            frameResults.pack(expand=YES,fill=BOTH)

            framePasswords = LabelFrame(workView,text='Passwords to Recover')
            framePasswords.pack(expand=YES,fill=BOTH)

            frameParameters = LabelFrame(workView,text='Parameters')
            frameParameters.pack(expand=NO,fill=BOTH)

            frameLength = Frame(frameParameters)
            frameLength.pack(expand=NO,fill=BOTH)

            frameBenchLength = Frame(frameParameters)
            frameBenchLength.pack(expand=NO,fill=BOTH)

            frameCharset = Frame(frameParameters)
            frameCharset.pack(expand=NO,fill=BOTH)

            frameHashFunction = Frame(frameParameters)
            frameHashFunction.pack(expand=NO,fill=BOTH)

            frameEnterHash = Frame(frameParameters)
            frameEnterHash.pack(expand=NO,fill=BOTH)

            frameMakeHash = Frame(frameParameters)
            frameMakeHash.pack(expand=NO,fill=BOTH)

            frameBench = LabelFrame(workView,text='Benchmark')
            frameBench.pack(expand=NO,fill=BOTH)

            frameMaxTime = LabelFrame(workView,text='Maximum Run Time')
            frameMaxTime.pack(expand=NO,fill=BOTH)

            frameProgress = LabelFrame(workView,text='Progress')
            frameProgress.pack(expand=NO,fill=BOTH)

            frameWork = LabelFrame(workView,text='Work')
            frameWork.pack(expand=NO,fill=BOTH)

            #outputResults
            resultsLabel = Label(frameResults, text='Recovered Passwords:')
            resultsLabel.pack()
            
            self.listbox = Listbox(frameResults,height=2,width=40)
            self.listbox.pack(expand=YES,fill=BOTH)
            
            #inputPasswords

            labelPasswordList = Label(framePasswords, text='The passwords to search for:\n Either a list of hashes or a samfile')
            labelPasswordList.pack()

            textPasswords = Text(framePasswords, height=2, width=85)
            textPasswords.pack(expand=YES,fill=BOTH)

            labelPasswords = Label(framePasswords, text='Add a password to search for:')
            labelPasswords.pack(side=LEFT)
            
            entryPasswords = Entry(framePasswords, width=50)
            entryPasswords.pack(side=RIGHT,expand=YES,fill=X)
            
            def callback(event=''):
                try:
                    textPasswords.insert(END, entryPasswords.get() + '\n')
                    entryPasswords.delete(0,END)
                    entryPasswords.icursor(0)
                    textPasswords.see(END)
                except Exception as detail:
                    self.showInfo('Error','An unhandled error occured')
                    self.log('Error','Work: %s | %s' % (repr(detail),traceback.format_exc()),'workView')
                    self.reactivateButtons()
                
            
            buttonPasswords = Button(framePasswords, text='add',command=callback)
            buttonPasswords.pack(side=RIGHT)
            
            #inputLength
            labelLength = Label(frameLength, text='Max password length to test ?:')
            labelLength.pack(side=LEFT)

            entryLength = Entry(frameLength,width=4)
            entryLength.insert(0,'4')
            entryLength.pack(side=RIGHT)

            #inputBenchLength
            labelBenchLength = Label(frameBenchLength, text='Password length for benchmark')
            labelBenchLength.pack(side=LEFT)

            entryBenchLength = Entry(frameBenchLength,width=4)
            entryBenchLength.insert(0,'3')
            entryBenchLength.pack(side=RIGHT)
            
            #inputCharset
            labelCharset = Label(frameCharset, text='choose the charset used in the password')
            labelCharset.pack(side=LEFT)
            
            spinCharset = Combobox(frameCharset, values=('numeric','alpha','alphanumeric','printable','ascii'))
            spinCharset.current(0)
            spinCharset.pack(side=RIGHT)

            #inputHash
            labelHashFunction = Label(frameHashFunction, text='choose which hashfunction to use')
            labelHashFunction.pack(side=LEFT)

            hashes = self.controller.getPossibleHashes()
            spinHashFunction = Combobox(frameHashFunction, values=hashes)
            spinHashFunction.current(0)
            spinHashFunction.pack(side=RIGHT)

            #enterHash
            labelHash = Label(frameEnterHash, text='Convert a password to a hash value')
            labelHash.pack(side=LEFT)

            entryHash = Entry(frameEnterHash,width=20)
            entryHash.pack(side=RIGHT)

            #makeHash
            def makeHashCallback(event=''):
                try:
                    self.controller.makeHash(spinHashFunction.get(),entryHash.get())
                except Exception as detail:
                    self.showInfo('Error','An unhandled error occured')
                    self.log('Error','MakeHash: %s | %s' % (repr(detail),traceback.format_exc()),'workView')

            buttonHash = Button(frameMakeHash, text='Hash', command=makeHashCallback)
            buttonHash.pack()

            self.hashValue = Entry(frameMakeHash,text='',state='readonly',width=50)
            self.hashValue.pack(expand=YES,fill=X)
            
            #controlBench

            frameLabelBench = Frame(frameBench)
            frameLabelBench.pack()

            self.hashSpeed = StringVar()
            labelBenchValue = Label(frameLabelBench,textvariable=self.hashSpeed)
            labelBenchValue.pack(side=RIGHT)

            labelBench = Label(frameLabelBench, text='Passwords / Second :')
            labelBench.pack(side=RIGHT)

            frameButtonBench = Frame(frameBench)
            frameButtonBench.pack()

            def callback2(event=''):
                try:
                    self.controller.setParameters(length=int(entryLength.get()),
                                                    benchLength = int(entryBenchLength.get()),
                                                    charset=spinCharset.get(),
                                                    hashFunction=spinHashFunction.get())
                    self.controller.runBenchmark()
                    self.disableButton(buttonBench)
                    self.disableButton(buttonWork)

                except Exception as detail:
                    self.showInfo('Error','An unhandled error occured')
                    self.log('Error','Bench: %s | %s' % (repr(detail),traceback.format_exc()),'workView')
                    self.reactivateButtons()

            buttonBench = Button(frameButtonBench, text='Run benchmark',command=callback2)
            buttonBench.pack()

            #maxTime
            labelMaxTime = Label(frameMaxTime,text='This workload will take an approximate maximum of:')
            labelMaxTime.pack()

            self.maxTimeAsDate = StringVar()
            labelMaxTimeValue = Label(frameMaxTime,textvariable=self.maxTimeAsDate)
            labelMaxTimeValue.pack()

            def maxTimeCallback(event=''):
                try:
                    self.controller.setParameters(length=int(entryLength.get()),
                                                    charset=spinCharset.get(),
                                                    hashFunction=spinHashFunction.get())
                    self.controller.updateMaxTimeAsDate(int(self.hashSpeed.get()))
                except Exception as detail:
                    self.showInfo('Error','An unhandled error occured')
                    self.log('Error','Work: %s | %s' % (repr(detail),traceback.format_exc()),'workView')


            buttonMaxTime = Button(frameMaxTime, text='Update expected time with new parameters',command=maxTimeCallback)
            buttonMaxTime.pack()
            self.disableButton(buttonMaxTime)

            #progress
            self.currentTime = IntVar()
            self.currentTime.set(0)

            self.progressBar = Progressbar(frameProgress,orient=HORIZONTAL,variable=self.currentTime,mode='determinate')
            self.progressBar.pack(expand=NO,fill=X)

            self.currentTimeAsDate = StringVar()
            time = self.controller.secondsToTime(0)
            self.currentTimeAsDate.set(time)

            labelCurrentTime = Label(frameProgress,textvariable=self.currentTimeAsDate)
            labelCurrentTime.pack()
            
            
            #controlWork
            def callback3(event=''):

                try:
                    self.controller.setParameters(length=int(entryLength.get()),
                                                    benchLength = int(entryBenchLength.get()),
                                                    passwords=textPasswords.get(1.0, END),
                                                    charset=spinCharset.get(),
                                                    hashFunction=spinHashFunction.get())
                    self.controller.runWork()
                    self.disableButton(buttonBench)
                    self.disableButton(buttonWork)
                except ValueError as detail:
                    self.showInfo('Error','Incorrect input, please try again')
                    self.log('Warning','Work: %s' % repr(detail),'workView')
                    self.reactivateButtons()
                except Exception as detail:
                    self.showInfo('Error','An unhandled error occured')
                    self.log('Error','Work: %s | %s' % (repr(detail),traceback.format_exc()),'workView')
                    self.reactivateButtons()
                
            buttonWork = Button(frameWork, text='Start guessing',command=callback3)
            buttonWork.pack()

            buttonQuit = Button(workView,text='QUIT',command=self.stop)
            buttonQuit.pack()

            self.pages['workView'] = workView
            self.current = 'workView'
            
        else:

            self.pages['workView'].pack()
            self.current = 'workView'

    def disableButton(self,button):

        button.config(state=DISABLED)
        self.disabledStack.append(button)

    def resetTime(self):

        self.currentTime.set(0)
        time = self.controller.secondsToTime(0)
        self.currentTimeAsDate.set(time)

    def updateTime(self,time):
        """Increment the clock ( string )"""

        self.currentTimeAsDate.set(time)

    def incrementProgress(self,time):
        """Increment progress ( int )"""

        if time > self.progressBar['maximum']:
            self.progressBar['maximum'] = time
        self.currentTime.set(time)


    def reset(self):

        self.currentTime.set(0)

    def setSliderMax(self,value):

        #self.scaleProgress['to'] = value
        self.progressBar['maximum'] = ( value - 1 )
        self.log('Signal','Progressbar max = %ds' % value,'setSliderMax')

    def reactivateButtons(self):

        while len(self.disabledStack) > 0:
            button = self.disabledStack.pop()
            button.config(state=NORMAL)

#        currentTime = self.currentTime.get()
#        hashSpeed = self.controller.getHashSpeed(currentTime)
#        self.log('Signal','Updating hashSpeed: currentTime = %d hashSpeed = %d' % (currentTime,hashSpeed),'reactivateButtons')
#        self.showHashSpeed(hashSpeed)

    def showInfo(self,subject,message):
        tkMessageBox.showinfo(subject,message)

    def showHash(self,hash):

        self.hashValue['state'] = 'normal'
        self.hashValue.delete(0,END)
        self.hashValue.insert(0,hash)
        self.hashValue['state'] = 'readonly'

    def showMaxTimeAsDate(self,maxTimeAsDate):

        self.maxTimeAsDate.set(maxTimeAsDate)

    def showHashSpeed(self,hashSpeed):

        self.hashSpeed.set(hashSpeed)
        self.controller.getMaxTimeAsDate(hashSpeed)
            
    def showResults(self,results):

        self.log('Signal','Received results %s...' % repr(results),'showResults')
        for password,hash in results.iteritems():
            self.listbox.insert(END, password.ljust(10,' ') + hash)
            self.listbox.see(END)

    def stop(self):
        try:
            self.controller.stop()
        except Exception as detail:
            self.showInfo('Error','An unhandled error occured')
            self.log('Error','%s | %s' % (repr(detail),traceback.format_exc()),'stop')
            self.reactivateButtons()

    def log(self,level,data,method=''):
        self.logger.log(level,data,method,'View')
