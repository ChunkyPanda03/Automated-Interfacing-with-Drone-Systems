from sympy import Line, Point, Circle, Point3D, Line3D, geometry,intersection, Segment, Equivalent
import json_to_py
wps = json_to_py.waypoints
geob = json_to_py.boundary
so = json_to_py.stationaryObstacles

geo = geometry
def wpline3d():
    lines3d = []
    num = len(geob('latitude'))
    numpoints = num - 1
    for i in range(numpoints):
        p1 = Point3D(wps('latitude')[i],wps('altitude')[i],wps('longitude')[i])
        p2 = Point3D(wps('latitude')[i+1],wps('altitude')[i+1],wps('longitude')[i+1])
        lines3d.append(Line3D(p1,p2))
        #print('3d line ' + str(i) + " created")
    return lines3d
def wpline():
    num = len(wps('latitude'))
    numpoints = num - 1
    lines = []
    for i in range(numpoints):
        x = Point((wps('latitude')[i])*1e7, (wps('longitude')[i])*1e7)
        y = Point((wps('latitude')[(i + 1)])*1e7, (wps('longitude')[(i + 1)])*1e7)
        #Interval(wps('latitude')[i],wps('latitude')[(i + 1)])
        lines.append(Segment(x, y))
        #print('line ' + str(i) + " created")
    return lines
def geoline():
    lines = []
    num = len(geob('latitude'))
    numpoints = num - 1
    #print(str(len(wps('latitude'))))
    #print(str(len(wps('latitude'))))
    for i in range(numpoints):
        x = Point(geob('latitude')[i], geob('longitude')[i])
        #print("p1 " + str(x))
        y = Point(geob('latitude')[(i+1)], geob('longitude')[(i+1)])
        #print("p2 " + str(y))
        #Interval()
        Line(x,y)
        lines.append(Line(x, y))
        #print('geoline ' + str(i) + " created")
    return lines
def circle():
    circles = []
    num = len(so('latitude'))
    for i in range(num):
        p = Point((so('latitude')[i])*1e7,(so('longitude')[i])*1e7)
        c=Circle(Point(p),so('radius')[i])
        circles.append(c)
        #print(str(c))
        #print(Circle(Point(p),so('radius')[i]))
    return circles
def intersection_check():
    c = circle()
    cnum = int(len(c))
    #print(str(cnum))
    line = wpline()
    numline = int(len(line))
    #print(str(numline))
    intersects = []
    I_circle= []
    I_line = []
    numv = (cnum-1) * (numline)
    for i in range(cnum):
        for b in range(numline):
            point_of_I = intersection(line[b],c[i])
            print(str(int((((i+b)+(10 * i))*100)/numv)) + '%')
            if point_of_I != []:
                intersects.append(point_of_I)
                I_circle.append((c[i]))
                I_line.append(b)


    #print(intersects)
    #print(intersects[0][1])
    I_circle_num = int(len(I_circle))

    for i in range(I_circle_num):

        c = c[i].center
        l1 = Line(intersects[i][0],c)
        l2 = Line (c,intersects[i][0])
        #print(str(l1))
        #print(str(l2))
        print(wps('longitude')[I_line[i]])
        deg1 = l1.smallest_angle_between(l2)
        if (wps('longitude')[I_line[i]])*1e7 < (wps('longitude')[I_line[i]+1])*1e7:
            deg1 = -1 * (deg1)
            print('coming from bellow')
        elif (wps('longitude')[I_line[i]])*1e7 > (wps('longitude')[I_line[i]+1])*1e7:
            print('coming from above')
        elif wps('latitude')[I_line[i]] < wps('latitude')[I_line[i]+1]:
            deg1 = -1 * (deg1)
            print("coming from left... interesting didn't think that would happen")
        elif wps('latitude')[I_line[i]] > wps('latitude')[I_line[i] + 1]:
            print("coming from right... interesting didn't think that would happen")
        print(deg1)
        return deg1
intersection_check()
#wpline()
#circle()