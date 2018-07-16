import juliantime
import coordinates
import math

class ConvergenceError(Exception):
    def __init__(self, message, error, tol, maxit):
        self.message = message
        self.error   = error
        self.maxit   = maxit
        self.tol     = tol

# This class implements the computations related to elliptic orbits.        
class Orbit:

    # The orbital elements are expressed as affine functions with respect to the time
    # after the Epoch J2000.0 in terms of Julian centuries:
    def __init__(self, params):

        self.a_0     = params['a_0']       # Semimajor axis
        self.e_0     = params['e_0']       # Eccentricity
        self.i_0     = params['i_0']       # Inclination
        self.Omega_0 = params['Omega_0']   # Longtitude of the ascending node
        self.pl_0    = params['pl_0']      # Longitude of the periapsis
        self.L_0     = params['L_0']       # Mean longitude

        self.a_delta     = params['a_delta']
        self.e_delta     = params['e_delta']
        self.i_delta     = params['i_delta']
        self.Omega_delta = params['Omega_delta']
        self.pl_delta    = params['pl_delta']
        self.L_delta     = params['L_delta']

        
    @staticmethod
    # Solve Kepler's equation with Newton-Raphson iteration:
    # M   Mean anomaly
    # e   Linear eccentricity
    # tol Absolute tolerance
    def solveEccentricAnomaly(M, e, tol, maxit):
        err = tol + 1
        it  = 0

        E = M

        while err > tol:
            it = it + 1
            if it > maxit:
                raise ConvergenceError("Convergence Failed", err, tol, maxit)

            E = E - (E - e*math.sin(E) - M) / (1 - e*math.cos(E))                        
            err = abs(E - e*math.sin(E) - M)
            #print("Iteration " + str(it) + " error " + str(err) + " E " + str(E))            
            
        return E

    @staticmethod
    # Compute the Natural Anomaly from the Eccentric Anomaly
    # E Eccentric anomaly
    # e Linear eccentricity
    def solveNaturalAnomaly(E, e):
        xu = (math.cos(E) - e)/(1 - e * math.cos(E))
        yu = math.sqrt(1 - e*e)*math.sin(E)/(1 - e*math.cos(E))
        
        return math.atan2(yu, xu)

    # Compute orbital elements from the Julian time:
    # JT Julian Time
    def computeParameters(self, JT):
        T = (JT - 2451545.0) / 36525.0
        
        self.a      = self.a_0 + self.a_delta * T
        self.e      = self.e_0 + self.e_delta * T
        self.i      = math.radians(self.i_0     + self.i_delta * T)
        self.Omega  = math.radians(self.Omega_0 + self.Omega_delta * T)
        self.pl     = math.radians(self.pl_0    + self.pl_delta * T)
        self.L      = math.radians(self.L_0     + (JT - 2451545.0) * self.L_delta)


    # Compute anomalies and Heliocentric Ecliptic Coordinates for the planet:
    def computePosition(self):
        # Compute mean, eccentric and natural anomalies
        self.M = self.L - self.pl
        self.E = self.solveEccentricAnomaly(self.M, self.e, 1e-9, 20)
        self.f = self.solveNaturalAnomaly(self.E, self.e)

        # Argument of periapsis
        self.omega = self.pl - self.Omega

        # Distance 
        self.r = self.a * (1.0 - self.e * math.cos(self.E))
        
        # Heliocentric Ecliptic Cartesian coordinates:
        self.r_ec = coordinates.rotateCartZ( \
                    coordinates.rotateCartX( \
                    coordinates.rotateCartZ([self.r, 0, 0], self.omega + self.f), self.i), self.Omega)             

        self.x_ec, self.y_ec, self.z_ec = self.r_ec
        
        # Heliocentric Ecliptic Spherical coordinates (Longitude and Latitude):
        rdummy, self.alpha, self.delta = coordinates.cartToSpherical(self.r_ec)                    
                    
    def printInputParameters(self):
        print("Major axis half  (a)  : " + str(self.a))
        print("Linear eccentri. (e)  : " + str(self.e))
        print("Inclination      (i)  : " + str(self.i)     + " rad " + str(math.degrees(self.i))     + " deg")
        print("Long. Asc. Node  (O)  : " + str(self.Omega) + " rad " + str(math.degrees(self.Omega)) + " deg")
        print("Length of perih. (om) : " + str(self.pl)    + " rad " + str(math.degrees(self.pl))    + " deg")
        print("Mean Longitude   (L)  : " + str(self.L)     + " rad " + str(math.degrees(self.L))     + " deg")

    def printOrbitParameters(self):
        print("Arg. of perih.    (o) : " + str(self.omega) + " rad " + str(math.degrees(self.omega)) + " deg")
        print("Mean anomaly      (M) : " + str(self.M)     + " rad " + str(math.degrees(self.M))     + " deg")
        print("Eccentric anomaly (E) : " + str(self.E)     + " rad " + str(math.degrees(self.E))     + " deg")
        print("Natural anomaly   (f) : " + str(self.f)     + " rad " + str(math.degrees(self.f))     + " deg")
        
    def printCoordinates(self):
        print("x (Hel. Ecliptic)     : " + str(self.x_ec))
        print("y (Hel. Ecliptic)     : " + str(self.y_ec))
        print("z (Hel. Ecliptic)     : " + str(self.z_ec))
        print("lon (Hel. Ecliptic)   : " + str(math.degrees(self.alpha)))
        print("lat (Hel. Ecliptic)   : " + str(math.degrees(self.delta)))
                                   
