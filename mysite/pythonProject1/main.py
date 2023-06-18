from geopy.geocoders import Nominatim
def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd

crd = geocoding("청주시 흥덕구")
print(crd['lat'])
print(crd['lng'])