import math

def flow_to_speed(flow):
    """
    Converts traffic flow (vehicles/hour) to estimated speed (km/h)
    using a parabolic approximation.
    """
    a = -1.4648375
    b = 93.75
    c = -flow

    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return 0  # no real solution

    sqrt_disc = math.sqrt(discriminant)
    speed1 = (-b + sqrt_disc) / (2 * a)
    speed2 = (-b - sqrt_disc) / (2 * a)

    if flow <= 1500:
        speed = max(speed1, speed2)
    else:
        speed = min(speed1, speed2)

    return min(speed, 60)  # Apply speed limit

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two lat/lon points (in km)
    """
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
