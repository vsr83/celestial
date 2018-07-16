import math

def translateCart(r, dr):
    return [r[0]+dr[0], r[1]+r[1], r[2]+dr[2]]

def diffCart(r, dr):
    return [r[0]-dr[0], r[1]-dr[1], r[2]-dr[2]]


def rotateCartX(r, angle):
    xr = r[0]
    yr = math.cos(angle) * r[1] - math.sin(angle) * r[2]
    zr = math.sin(angle) * r[1] + math.cos(angle) * r[2]
    
    return [xr, yr, zr]

def rotateCartY(r, angle):
    xr = math.cos(angle) * r[0] + math.sin(angle) * r[2]
    yr = r[1]
    zr = -math.sin(angle) * r[0] - math.cos(angle) * r[2]
    
    return [xr, yr, zr]

def rotateCartZ(r, angle):
    xr = math.cos(angle) * r[0] - math.sin(angle) * r[1]
    yr = math.sin(angle) * r[0] + math.cos(angle) * r[1]
    zr = r[2]
    
    return [xr, yr, zr]

def cartToSpherical(r):
    theta = math.atan2(r[1], r[0]) 
    phi = math.atan(r[2] / math.sqrt(r[1]*r[1] + r[0]*r[0]))
    r = math.sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2])

    if theta < 0:
        theta = theta + 2 * math.pi
    if phi < 0:
        phi = phi + 2 * math.pi
    
    return [r, theta, phi]

def equitorialToHorizontal(h, delta, phi):
    a = math.asin(math.cos(h)*math.cos(delta)*math.cos(phi) + math.sin(delta)*math.sin(phi))
    A = math.pi + math.atan2(math.sin(h)*math.cos(delta), math.cos(h)*math.cos(delta)*math.sin(phi) - math.sin(delta)*math.cos(phi))
    return [a, A]
