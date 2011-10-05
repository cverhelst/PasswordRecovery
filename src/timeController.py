# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Cameron"
__date__ ="$5-okt-2011 15:25:23$"

class TimeController(object):

    def __init__(self,model,view):
        self.model = model
        self.view = view
        self.maxTime = 0
        self.currentTime = 0
        self.hashSpeed = 0

    def updateCurrentTime(self):
        self.incrementCurrentTime()
        self.view.updateCurrentTime(self.currentTime)
        string = self.timeToString(self.currentTime)
        self.view.updateCurrentTimeString(string)

    def updateMaxTime(self,hashSpeed):
        self.hashSpeed = hashSpeed
        self.view.showSpeed(hashSpeed)
        self.maxTime = self.model.getMaxTime(hashSpeed)
        string = self.timeToString(self.maxTime)
        self.view.updateMaxTime(self.maxTime)
        self.view.updateMaxTimeString(string)
        self.view.updateHashSpeed(hashSpeed)

    def stop(self):
        self.view.reactivateButtons()

    def incrementCurrentTime(self):
        self.currentTime += 1;

    def reset(self):
        self.resetCurrentTime()
        self.resetMaxTime()

    def resetCurrentTime(self):
        self.currentTime = 0
        self.view.updateCurrentTime(self.currentTime)
        string = self.timeToString(self.currentTime)
        self.view.updateCurrentTimeString(string)

    def resetMaxTime(self):
        self.maxTime = 0
        self.view.updateMaxTime(self.maxTime)
        string = self.timeToString(self.maxTime)
        self.view.updateMaxTimeString(string)

    def timeToString(self,seconds):

        min = 60
        hour = min * 60
        day = hour * 24
        year = day * 365
        month = year / 12

        years = seconds / year
        seconds -= years * year
        months = seconds / month
        seconds -= months * month
        days = seconds / day
        seconds -= days * day
        hours = seconds / hour
        seconds -= hours * hour
        minutes = seconds / min
        seconds -= minutes * min

        times = [['year', years], ['month',months], ['day',days],['hour',hours],['minute',minutes],['second',seconds]]
        result = ''
        for pair in times:
            label = pair[0]
            time = pair[1]
            if time > 1:
                result += " %d %s%s" % (time,label,'s')
            elif time > 0 or label == 'second':
                result += " %d %s" % (time,label)

        return result

if __name__ == "__main__":
    print "Hello World"
