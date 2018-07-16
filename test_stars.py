import juliantime
import coordinates
import math
import csv

# Helsinki
longitude = 24.9333
latitude = math.radians(60.16)

J = juliantime.JulianTime(10800)
ST0 = math.radians(J.getSiderealTime(longitude))

print "Julian Time     : " + str(J.JT)
print "Sidereal Time   : " + str(math.degrees(ST0))


with open('minimal.csv', 'rb') as csvfile:
    starreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    ind_row = 0

    for row in starreader:

        ind_row = ind_row + 1
#        print row
        name = row[1]
        RAHours, RAMinutes, RASeconds = row[8:11]
        DecNS, DecDeg, DecArcmin, DecArcsec = row[11:15]

        if len(name) > 0 and ind_row > 1:
            #print str(name) + " " + str(RAHours) + ":" + str(RAMinutes) + "." + str(RASeconds) + " " \
            #    + str(DecNS) + str(DecDeg) + ":" + str(DecArcmin) + "." + str(DecArcsec) + " "

            RA = coordinates.time2deg(float(RAHours), float(RAMinutes), float(RASeconds))

            if DecNS == 'N' :
                Dec = coordinates.arc2deg(float(DecDeg), float(DecArcmin), float(DecArcsec))
            elif DecNS =='S' : 
                Dec = coordinates.arc2deg(-float(DecDeg), -float(DecArcmin), -float(DecArcsec))
            else:
                Dec = 0.0
                
            #print "RA : " + str(RA) + " Dec : " + str(Dec)

            RA = math.radians(RA)
            Dec = math.radians(Dec)
            
            h = ST0 - RA
            a, A = coordinates.equitorialToHorizontal(h, Dec, latitude)

            print str(name) + " - Az/Alt : " + str(math.degrees(A)) + "/" + str(math.degrees(a))
