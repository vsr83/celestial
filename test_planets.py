import orbit
import juliantime

params_mercury = {'a_0'     : 0.38709893, 'a_delta'     : 0.00000066,   \
                  'e_0'     : 0.20563069, 'e_delta'     : 0.00002527,   \
                  'i_0'     : 7.00487,    'i_delta'     : -23.51/3600.0,  \
                  'Omega_0' : 48.33167,  'Omega_delta' : -446.3/3600.0, \
                  'pl_0'    : 77.45645,  'pl_delta'     : 573.57/3600.0,  \
                  'L_0'     : 252.25084,  'L_delta'     : 4.09233880}

params_venus   = {'a_0'     : 0.72333199, 'a_delta'     : 0.00000092,   \
                  'e_0'     : 0.00677323, 'e_delta'     : -0.00004938,   \
                  'i_0'     : 3.39471,    'i_delta'     : -2.86/3600.0,  \
                  'Omega_0' : 76.68069,   'Omega_delta' : -996.89/3600.0, \
                  'pl_0'    : 131.53298,  'pl_delta'    : -108.80/3600.0,  \
                  'L_0'     : 181.97973,  'L_delta'     : 1.60213047}

params_earth   = {'a_0'     : 1.00000011, 'a_delta'     : -0.00000005,   \
                  'e_0'     : 0.01671022, 'e_delta'     : -0.00003804,   \
                  'i_0'     : 0.00005,    'i_delta'     : -46.94/3600.0,  \
                  'Omega_0' : -11.26064,  'Omega_delta' : -18228.25/3600.0, \
                  'pl_0'    : 102.94719,  'pl_delta'    : 1198.28/3600.0,  \
                  'L_0'     : 100.46436,  'L_delta'     : 0.98560910}

params_mars    = {'a_0'     : 1.52366231, 'a_delta'     : -0.00007221,   \
                  'e_0'     : 0.09341233, 'e_delta'     : 0.00011902,   \
                  'i_0'     : 1.85061,    'i_delta'     : -25.47/3600.0,  \
                  'Omega_0' : 49.57854,   'Omega_delta' : -1020.19/3600.0, \
                  'pl_0'    : 336.04084,  'pl_delta'    : 1560.78/3600.0,  \
                  'L_0'     : 355.45332,  'L_delta'     : 0.52403304}

params_jupiter = {'a_0'     : 5.20336301, 'a_delta'     :  0.00060737,   \
                  'e_0'     : 0.04839266, 'e_delta'     : -0.00012880,   \
                  'i_0'     : 1.30530000, 'i_delta'     : -4.15/3600.0,  \
                  'Omega_0' : 100.55615,  'Omega_delta' : 1217.17/3600.0, \
                  'pl_0'    : 14.75385,   'pl_delta'    : 839.93/3600.0,  \
                  'L_0'     : 34.40438,   'L_delta'     : 0.08308687}

params_saturn   = {'a_0'     : 9.53707032, 'a_delta'     : -0.00301530,   \
                   'e_0'     : 0.05415060, 'e_delta'     : -0.00036762,   \
                   'i_0'     : 2.48446,    'i_delta'     : 6.11/3600.0,  \
                   'Omega_0' : 113.71504,  'Omega_delta' : -1591.05/3600.0, \
                   'pl_0'    : 92.43194,   'pl_delta'    : -1948.89/3600.0, \
                   'L_0'     : 49.94432,   'L_delta'     : 0.03346063}

params_uranus   = {'a_0'     : 19.19126393,'a_delta'     : 0.00152025,   \
                   'e_0'     : 0.04716771, 'e_delta'     : -0.00019150,   \
                   'i_0'     : 0.76986,    'i_delta'     : -2.09/3600.0,  \
                   'Omega_0' : 74.22988,   'Omega_delta' : 1681.40/3600.0, \
                   'pl_0'    : 170.96424,   'pl_delta'   : 1312.56/3600.0, \
                   'L_0'     : 313.23218,   'L_delta'    : 0.01173129}

params_neptune  = {'a_0'     : 30.06896348,'a_delta'     : -0.00125196,   \
                   'e_0'     : 0.00858587, 'e_delta'     : 0.00002514,   \
                   'i_0'     : 1.76917,    'i_delta'     : -3.64/3600.0,  \
                   'Omega_0' : 131.72169,  'Omega_delta' : -151.25/3600.0, \
                   'pl_0'    : 44.97135,   'pl_delta'    : -844.43/3600.0, \
                   'L_0'     : 304.88003,   'L_delta'     : 0.00598106}

orbit_mercury  = orbit.Orbit(params_mercury)
orbit_venus    = orbit.Orbit(params_venus)
orbit_earth    = orbit.Orbit(params_earth)
orbit_mars     = orbit.Orbit(params_mars)
orbit_jupiter  = orbit.Orbit(params_jupiter)
orbit_saturn   = orbit.Orbit(params_saturn)
orbit_uranus   = orbit.Orbit(params_uranus)
orbit_neptune  = orbit.Orbit(params_neptune)

dict_planets = {"Mercury" : orbit_mercury, \
                "Venus"   : orbit_venus,   \
                "Earth"   : orbit_earth,   \
                "Mars"    : orbit_mars,    \
                "Jupiter" : orbit_jupiter, \
                "Saturn"  : orbit_saturn,  \
                "Uranus"  : orbit_uranus,  \
                "Neptune" : orbit_neptune}

#dict_planets = {"Jupiter" : orbit_jupiter}


J = juliantime.JulianTime(-10800)

for planet in dict_planets:
    print(planet + ":")
    
    dict_planets[planet].computeParameters(J.JT)
    dict_planets[planet].computePosition()
#    dict_planets[planet].printInputParameters()
#    dict_planets[planet].printOrbitParameters()
    dict_planets[planet].printCoordinates()    
                                                        
