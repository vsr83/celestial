import juliantime
import math

class ConvergenceError(Exception):
    def __init__(self, message, error, tol, maxit):
        self.message = message
        self.error   = error
        self.maxit   = maxit
        self.tol     = tol

class Orbit:
    def __init__(self, params):
        
        self.a_0     = params['a_0']
        self.e_0     = params['e_0']
        self.i_0     = params['i_0']
        self.Omega_0 = params['Omega_0']
        self.pl_0    = params['pl_0']
        self.L_0     = params['L_0']

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
    def solveNaturalAnomaly(E, e):
        xu = (math.cos(E) - e)/(1 - e * math.cos(E))
        yu = math.sqrt(1 - e*e)*math.sin(E)/(1 - e*math.cos(E))
        
        return math.atan2(yu, xu)

    def computeParameters(self, JT):
        T = (JT - 2451545.0) / 36525.0
        
        self.a      = self.a_0 + self.a_delta * T
        self.e      = self.e_0 + self.e_delta * T
        self.i      = math.radians(self.i_0     + self.i_delta * T)
        self.Omega  = math.radians(self.Omega_0 + self.Omega_delta * T)
        self.pl     = math.radians(self.pl_0    + self.pl_delta * T)
        self.L      = math.radians(self.L_0     + (JT - 2451545.0) * self.L_delta)
        
    def computePosition(self):
        self.M = self.L - self.pl
        self.E = self.solveEccentricAnomaly(self.M, self.e, 1e-9, 20)
        self.f = self.solveNaturalAnomaly(self.E, self.e)
        
        self.omega = self.pl - self.Omega

        self.r = self.a * (1.0 - self.e * math.cos(self.E))
        
        # Heliocentric Ecliptic Cartesian coordinates:
        self.x_ec = self.r * math.cos(self.Omega) * math.cos(self.omega + self.f) \
                  - self.r * math.sin(self.Omega) * math.sin(self.omega + self.f) * math.cos(self.i)
        self.y_ec = self.r * math.sin(self.Omega) * math.cos(self.omega + self.f) \
                  + self.r * math.cos(self.Omega) * math.sin(self.omega + self.f) * math.cos(self.i)
        self.z_ec = self.r * math.sin(self.omega + self.f) * math.sin(self.i)

        # Heliocentric Ecliptic Spherical coordinates (Longitude and Latitude):
        self.alpha = math.atan2(self.y_ec, self.x_ec) 
        self.delta = math.atan(self.z_ec / math.sqrt(self.y_ec * self.y_ec + self.x_ec * self.x_ec))

        if self.alpha < 0:
            self.alpha = self.alpha + 2 * math.pi
        if self.delta < 0:
            self.delta = self.delta + 2 * math.pi
            
                    
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
                                   
