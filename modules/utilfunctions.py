import math

def distanceBetween(a, b):
    xa = a[0]
    xb = b[0]
    ya = a[1]
    yb = b[1]

    return math.sqrt(((xa - xb)**2) + ((ya - yb)**2))