import simplejson
with open("jsons/SUAScord.json","r")as f:
    data = simplejson.load(f)
#print(data)
#for item in data['waypoints']:
#    print(item)
def waypoints(lat_long):
    # looks for 'latitude' 'longitude' 'altitude'
    items = []
    if lat_long == 'altitude': #altitude is in feet needs meters
        x = len(data['waypoints'])
        #print("there are " + str(x) + " waypoints")
        i = 0

        while i < x:
            #print(str((data['waypoints'][i][lat_long])/3.281))
            items.append((data['waypoints'][i][lat_long])/3.281)
            i = i + 1
        #print("End of the " + str(len(items)) + " " + lat_long + " list")
        return items
    else:
        x = len(data['waypoints'])
        #print("there are " + str(x) + " waypoints")
        i = 0

        while i < x:
            #print(data['waypoints'][i][lat_long])
            items.append(data['waypoints'][i][lat_long])
            i = i + 1
        #print("End of the " + str(len(items)) + " " + lat_long + " list")
        return items

def boundary(lat_long):
    items = []
    #print(data['flyZones'][0]['boundaryPoints'])
    x = len(data['flyZones'][0]['boundaryPoints'])
    #print("there are " + str(x) + " boundaryPoints")
    i = 0

    while i < x:
        #print(data['flyZones'][0]['boundaryPoints'][i][lat_long])
        items.append(data['flyZones'][0]['boundaryPoints'][i][lat_long])
        i = i + 1
    #print("End of the " + str(len(items)) + " " + lat_long + " list")
    return items

def grid_points(lat_long):
    items = []
    x = len(data['searchGridPoints'])
    #print("there are " + str(x) + " searchGridPoints")
    i = 0

    while i < x:
        #print(data['searchGridPoints'][i][lat_long])
        items.append(data['searchGridPoints'][i][lat_long])
        i = i + 1
    #print("End of the " + str(len(items)) + " " + lat_long + " list")
    return items

def lost_comms(lat_long):
    #print(data['lostCommsPos'])
    x = len(data['lostCommsPos'])
    #print("there are " + str(x) + " lostCommsPos")
    i = 0


    #print(data['lostCommsPos'][lat_long])
    items = data['lostCommsPos'][lat_long]
    i = i + 1
    #print("End of the " + str(len(items)) + " " + lat_long + " list")
    return items

def air_drop_boundary(lat_long):
    items = []
    x = len(data['airDropBoundaryPoints'])
    #print("there are " + str(x) + " airDropBoundaryPoints")
    i = 0

    while i < x:
        #print(data['airDropBoundaryPoints'][i][lat_long])
        items.append(data['airDropBoundaryPoints'][i][lat_long])
        i = i + 1
    #print("End of the " + str(len(items)) + " " + lat_long + " list")
    return items

def stationaryObstacles(lat_long_radius_height):

    items = []
    x = len(data['stationaryObstacles'])
    #print("there are " + str(x) + " stationaryObstacles for " + str(lat_long_radius_height))
    i = 0
    if lat_long_radius_height.lower() == 'radius':
        while i < x:
            #print(data['stationaryObstacles'][i][lat_long_radius_height])
            g = data['stationaryObstacles'][i][lat_long_radius_height]
            y = float(g/3.281)+1 #adding one meter so that the boundry
            #print(str(y) + " meters " + str(i))

            items.append(y)
            #print(str(items[i]))
            i = i + 1
    elif lat_long_radius_height.lower() == 'height':
        while i < x:
            #print(data['stationaryObstacles'][i][lat_long_radius_height])
            g = data['stationaryObstacles'][i][lat_long_radius_height]
            y = float(g/3.281)+1
            #print(str(y) + " meters " + str(i))

            items.append(y)
            #print(str(items[i]))
            i = i + 1
    else:

            while i < x:
                #print(data['stationaryObstacles'][i][lat_long_radius_height])
                items.append((data['stationaryObstacles'][i][lat_long_radius_height]))
                i = i + 1



    #print("End of the " + str(len(items)) + " " + lat_long_radius_height + " list")
    return items
def air_drop(lat_long):
    items = []
    x = len(data['airDropPos'])
    i = 0
    #print('Airdrop Position')
    #print(data['airDropPos'][lat_long])
    items.append(data['airDropPos'][lat_long])
    i = i + 1
    #print("End of the " + str(len(items)) + " " + lat_long + " list")
    return items
def home(lat_long):
    x = len(data['lostCommsPos'])
    i = 0
    #print(data['lostCommsPos'][lat_long])
    items = data['lostCommsPos'][lat_long]
    i = i + 1
    #print("End of the " + str(len(items)) + " " + lat_long + " list")
    return items
def UGV_drive(lat_long):
    items = []
    x = len(data['ugvDrivePos'])
    i = 0
    #print('UGV Drive')
    #print(data['ugvDrivePos'][lat_long])
    items.append(data['ugvDrivePos'][lat_long])
    i = i + 1
    #print("End of the " + str(len(items)) + " " + lat_long + " list")
    return items

#waypoints('altitude')
#waypoints('latitude')
#waypoints('longitude')
#grid_points('latitude')
#grid_points('longitude')
#boundary('latitude')
#boundary('longitude')
#lost_comms('longitude')
#lost_comms('latitude')
#air_drop_boundary('latitude')
#air_drop_boundary('longitude')
#stationaryObstacles('latitude')
#stationaryObstacles('height')
#air_drop('latitude')
#air_drop('longitude')
#UGV_drive('latitude')
#UGV_drive('longitude')
#home('latitude')

