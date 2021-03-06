
from FlyPyApi import Connection, RouteCollection, Airport

import math
import random
import datetime
import pytz
from collections import deque

class Trip:
    def __init__(self):
        self.startPort = ''
        self.endPort = ''
        self.stepPorts = ''
        self.flightPlan = {}

    def connectionSearch(self, start, end):
        listPort = Airport(IATA=start).all_out()
        finList = []; item = None
        iterate = deque(listPort.connectionSet)

        if listPort.search(end):
            print("direkt")
            return [end]

        go = True
        i = 0
        while go:
            p = Airport(IATA=iterate[i]).all_out().search(end)
            if p:
                if item is not None: finList.append(item)
                finList.append(iterate[i])
                return finList
            if i == (len(iterate)-1):
                if len(listPort.connectionSet) == 0:
                    print("no route found")
                    go = False
                    return []
                item = listPort.connectionSet.pop()
                iterate = list(Airport(IATA=item).all_out().connectionSet)
                i = 0
                if len(iterate) == 0:
                    item = listPort.connectionSet.pop()
                    iterate = list(Airport(IATA=item).all_out().connectionSet)
                continue
            i += 1

    def connectionSearch2(self, start, end):
        popList = Airport(IATA=start).all_out()

        if end in popList.connectionSet:
            return [start]
        search = True

        used = [];p_list = []; visited = []; used_pop = []; p =''
        while search:
            port = popList.connectionSet.pop()
            if port not in visited:
                port_out = Airport(IATA=port).all_out().connectionSet
            else:
                port_out = []
            if end in port_out:
                res = p_list + [port]
                print(res)
                return res
            used.append(port)
            visited.append(port)
            visited = list(set(visited))
            if len(popList.connectionSet) == 0:
                p = used.pop()
                used_pop.append(p)
                popList = Airport(IATA=p).all_out()
                p_list.append(p)
                if len(used) == 0:
                    popList= Airport(IATA= used_pop.pop()).all_out()


    def getFlightplan(self, start: str, end: str, steps: list):
        self.startPort = Airport(IATA=start)
        self.endPort = Airport(IATA=end)
        self.stepPorts = steps
        flightList = [start]
        if len(steps) == 0:

            con = self.connectionSearch(start,end)
            if con:
                flightList.extend(con)
                flightList.append(end)
            else:
                print("no route was found")
        else:
            a = start
            steps.append(end)
            for i, step in enumerate(steps):
                con = self.connectionSearch(a, step)
                flightList.extend(con)
                flightList.append(step)
                a = step
        flightList = sorted(set(flightList), key=flightList.index)

        for i, s in enumerate(flightList):
            if i != len(flightList) - 1:
                self.flightPlan[i] = Connection(s, flightList[i + 1])


    def getTraveltime(self):
        time = 0; wait_time = 0
        start = ''
        for step in self.flightPlan:
            if start == '':
                start = pytz.timezone(self.flightPlan[step].sourceAirport.tz)
            wait = random.randint(1, 4)
            speed = random.randint(800, 950)
            dist = self.flightPlan[step].distance
            time += dist/speed
            wait_time += wait
        end = pytz.timezone(self.flightPlan[step].destinationAirport.tz)
        start_time = datetime.datetime.now() + datetime.timedelta(hours=-2) # remove dst
        final_time = start.fromutc(start_time + datetime.timedelta(hours=time+wait_time)).astimezone(end)
        self.flightPlan["time"] = {"start_time": start.fromutc(start_time).strftime('%Y-%m-%d %H:%M:%S'),
                                   "end_time": final_time.strftime('%Y-%m-%d %H:%M:%S'),
                                   "total_time":round(time + wait_time,1), "waiting_time": wait_time}

    def getRoundTrip(self, iata: str):
        bigAirports = {"America":"JFK", "Europe":"LHR", "Asia": "PEK",
                       "Australia": "SYD", "Pacific":'HNL', 'Africa':'CPT'} # add pacific, australia and africa
        startPort = Airport(IATA=iata)
        worldtour = {}
        flightList = [iata]
        beginNode = bigAirports[startPort.continent]
        flightList.extend(self.connectionSearch(iata, beginNode))



        if beginNode not in flightList: flightList.append(beginNode)

        for i, s in enumerate(flightList):
            if i != len(flightList) - 1:
                worldtour[i] = Connection(s, flightList[i + 1])
        step = worldtour[len(worldtour)- 1]

        '''
        if step.direction > 0 and step.direction < 180:
            directions = 90
        else:
            directions = 270
            '''
        all_dir = [50, 90, 110, 250, 270, 300]
        directions = random.choice(all_dir)
        all_dir.remove(directions)

        const = 0.8
        notHome = True
        banList = []
        continentList = [startPort.continent]
        all_out = step.destinationAirport.all_out()
        while notHome:
            search = True;
            while search:
                if len(all_out.connectionDict) == 0:
                    banList.append(item[1].sourceAirport.IATA)
                    if len(worldtour) == 1:
                        directions = random.choice(all_dir)
                        all_dir.remove(directions)
                    else:
                        p = worldtour.popitem()
                        step = worldtour[len(worldtour)-1]
                    search = False
                else:
                    item = all_out.connectionDict.popitem()
                if abs(1 - abs(directions - item[1].direction)/180) > const and item[0] not in banList:
                    if item[1].destinationAirport.lat == '':
                        item = all_out.connectionDict.popitem()
                    else:
                        step = item[1]
                        worldtour[len(worldtour)] = step
                        continentList.append(step.destinationAirport.continent)
                        search = False
                banList.append(step.destinationAirport.IATA)
                banList = list(set(banList))
            all_out = step.destinationAirport.all_out()
            dist = 0
            continentList = list(set(continentList))
            for i in worldtour.keys():
                dist += worldtour[i].distance

            print(continentList)
            if len(continentList) > 3 or len(continentList) > 2 and step.destinationAirport.continent == startPort.continent:
                if all_out.search(startPort.IATA):
                    worldtour[len(worldtour)] = Connection(step.destinationAirport.IATA,startPort.IATA)
                else:
                    last = [worldtour[len(worldtour)-1].destinationAirport.IATA]
                    last.extend(self.connectionSearch(last[0], beginNode))#startPort.IATA))#
                    if beginNode == startPort.IATA:
                        last.append(beginNode)
                    else:
                        last.extend(reversed(flightList)) #[startPort.IATA])     # reverse list from begin node and make it a connection
                    last = sorted(set(last), key=last.index)
                    for i, el in enumerate(last):
                        if i < len(last)-1:
                            worldtour[len(worldtour)] = Connection(el, last[i+1])

                notHome = False
            print(step)
        print("done")
        self.flightPlan = worldtour
        print(self)
        print(dist)
        print(directions)

    def getLiteRoundTrip(self, iata: str):
        # start with a random direction
        all_dir = [90, 270]  # [70, 90, 110, 250, 270, 290]
        directions = random.choice(all_dir)
        all_dir.remove(directions)
        const = 0.7
        notHome = True
        banList = []

        startPort = Airport(IATA=iata)
        continentList = [startPort.continent]
        worldtour = {}
        flightList = [iata]

        all_out =startPort.all_out()

        if len(all_out) < 20:
            flightList.append(next((e for e in all_out.connectionSet if len(Airport(IATA=e).all_out())), None))
            beginNode = flightList[-1]
        else:
            beginNode = startPort.IATA
            flightList.append(next((e for e in all_out.connectionSet if abs(1 - abs(directions - Connection(iata,e).direction) / 180) > const), None))

        for i, s in enumerate(flightList):
            if i != len(flightList) - 1:
                worldtour[i] = Connection(s, flightList[i + 1])
        step = worldtour[len(worldtour)- 1]


        all_out = step.destinationAirport.all_out()
        while notHome:
            search = True;
            while search:
                if len(all_out.connectionSet) == 0:
                    banList.append(con.sourceAirport.IATA)
                    if len(worldtour) == 1:
                        directions = random.choice(all_dir)
                        all_dir.remove(directions)
                    else:
                        p = worldtour.popitem()
                        step = worldtour[len(worldtour)-1]
                    search = False
                else:
                    item = all_out.connectionSet.pop()
                    con = Connection(step.destinationAirport.IATA,item)
                if abs(1 - abs(directions - con.direction)/180) > const and item not in banList:
                    if con.destinationAirport.lat == '':
                        item = all_out.connectionSet.pop()
                    else:
                        step = con
                        worldtour[len(worldtour)] = step
                        continentList.append(step.destinationAirport.continent)
                        search = False
                banList.append(step.destinationAirport.IATA)
                banList = list(set(banList))
            all_out = step.destinationAirport.all_out()
            dist = 0
            continentList = list(set(continentList))
            for i in worldtour.keys():
                dist += worldtour[i].distance

            print(continentList)
            if len(continentList) > 3 or len(continentList) > 2 and step.destinationAirport.continent == startPort.continent and dist > 20000:
                if all_out.search(startPort.IATA):
                    worldtour[len(worldtour)] = Connection(step.destinationAirport.IATA,startPort.IATA)
                else:
                    last = [worldtour[len(worldtour)-1].destinationAirport.IATA]
                    last.extend(self.connectionSearch(last[0], beginNode))#startPort.IATA))#
                    if beginNode == startPort.IATA:
                        last.append(beginNode)
                    else:
                        last.extend(reversed(flightList)) #[startPort.IATA])     # reverse list from begin node and make it a connection
                    last = sorted(set(last), key=last.index)
                    for i, el in enumerate(last):
                        if i < len(last)-1:
                            worldtour[len(worldtour)] = Connection(el, last[i+1])

                notHome = False
            #print(step)
        print("done")
        self.flightPlan = worldtour
        print(self)
        print(dist)
        print(directions)



    def getDistance(self, sourceAirport,destination):
        R = 6371000

        coord1 = sourceAirport.getCoords()
        coord2 = destination

        rad1 = math.radians(coord1[0])
        rad2 = math.radians(coord2[0])

        y = math.radians(coord2[0] - coord1[0])
        gam = math.radians(coord2[1] - coord1[1])

        a = math.sin(y / 2) * math.sin(y / 2) + \
            math.cos(rad1) * math.cos(rad2) * \
            math.sin(gam / 2) * math.sin(gam / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round((R * c) / 1000, 2)

    def serialize_to_json(self):
        res_json = {}
        for e in self.flightPlan.keys():
            if e == 'time':
                res_json[e] = self.flightPlan[e]
            else:
                res_json[e] = self.flightPlan[e].serialze_to_json()
        return res_json


    def __str__(self):
        resString = ''
        for e in self.flightPlan.keys():
            resString += '{} \t {} \n'.format(e, self.flightPlan[e])
        return resString


if __name__=="__main__":
    t = Trip()
    import time
    start = time.time()
    t.connectionSearch("DRS","ISC")
    end = time.time()
    print(end - start)
    start2 = time.time()
    t.connectionSearch2("DRS","ISC")
    end2 = time.time()
    print(end2 - start2)


    t.getFlightplan('LAX','DUB',steps=[])
    t.getTraveltime()
    res = t.serialize_to_json()
    #t.getLiteRoundTrip('DRS')
    print(t)
