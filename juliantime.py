import time

class JulianTime:
    def __init__ (self, UTCOffsetSeconds):
        self.UTCOffsetSeconds = UTCOffsetSeconds
        self.setFromCurrentTime()

    @staticmethod
    def computeJulianDay(year, month, day):
        A = int(year/100.0)
        B = int(A/4.0)
        C = int(2.0-A+B)
        E = int(365.25*(year + 4716.0))
        F = int(30.6001*(month+1))
        
        return C + day + E + F - 1524.5
        
    def setFromUTCTime(self, year, month, day, hour, minute, second):
        str = "%4d-%02d-%02d-%02d:%02d:%02d" % (year, month, day, hour, minute, second)       
        
        self.POSIXTime = time.mktime(time.strptime(str, "%Y-%m-%d-%H:%M:%S"))
        self.structTime = time.localtime(self.POSIXTime)
        self.computeJulianTime()
        
    def setFromLocalTime(self, year, month, day, hour, minute, second):
        str = "%4d-%02d-%02d-%02d:%02d:%02d" % (year, month, day, hour, minute, second)

        self.POSIXTime = time.mktime(time.strptime(str, "%Y-%m-%d-%H:%M:%S")) - self.UTCOffsetSeconds
        self.structTime = time.localtime(self.POSIXTime)
        self.computeJulianTime()
        
    def addDeltaTime(self, hours, minutes, seconds):
        self.POSIXTime = self.POSIXTime + hours * 3600 + minutes * 60 + seconds
        self.structTime = time.localtime(self.POSIXTime)
        self.computeJulianTime()

    def setFromCurrentTime(self):
        
        self.structTime = time.localtime()
        self.POSIXTime = time.mktime(self.structTime) - self.UTCOffsetSeconds
        self.structTime = time.localtime(self.POSIXTime)
        self.POSIXTime = time.mktime(self.structTime)
        self.computeJulianTime()
        
    def computeJulianTime(self):

        print "POSIX Time : " + str(self.POSIXTime)
        st = self.structTime

        day = st.tm_mday
        if st.tm_mon < 3:
            year = st.tm_year - 1
            month = st.tm_mon + 12            
        else:
            year = st.tm_year
            month = st.tm_mon
        
        self.JD = self.computeJulianDay(year, month, day)
        self.JT = self.JD + st.tm_hour/24.0 + st.tm_min/(24.0*60.0) + st.tm_sec/(24.0*60.0*60.0)
        
            
    def getLocalTime(self):
        return self.POSIXTime + self.UTCOffsetSeconds

    def getUTCTime(self):
        return self.POSIXTime

    def getJulianDatetime(self):
        return self.JT

    def getJulianDay(self):
        return self.JD

    def getSiderealTime(self, longitude):
        JDref  = math.ceil(self.computeJulianDay(2000, 1, 1))

        tfac = (self.JD - JDref) / 36525.0
        LST = 100.46061837 + 36000.770053608 * tfac + 0.000387933 * tfac * tfac + 1.00273790935 * (self.JT - self.JD) * 360.0 + longitude
        
        return LST
    
