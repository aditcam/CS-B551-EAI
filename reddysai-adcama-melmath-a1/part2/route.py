#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Sai Prajwal Reddy: reddysai@iu.edu, Aditya Camarushy: adcama@iu.edu, Melissa Rochelle Mathias: melmath@iu.edu 
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
from os import stat
import sys
# importing math library for calculating the distance
from math import pi,sin,cos,tanh,atan2,sqrt

# from part1.solver2021 import successors

class State:
    def __init__(self,source,destination,distance,speed_lt,highway):
        self.source = source
        self.destination = destination
        self.distance = distance
        self.distance_to_state = []
        self.speed_lt = speed_lt
        self.speed_lt_to_state = []
        self.highway = highway
        self.path_to_state = []
        self.move = (destination,str(highway + " for " + distance + " miles"))
        self.g = 0
        self.h = 0
        self.f = 0 

    def set_f(self):
        self.f = self.g + self.h

    def __contains__(self,other):
        for x in other:
            if x.destination == self.destination and x.source == self.source and x.f < self.f:
                return True
        return False 

    def __eq__(self,other):
        return self.f>other.f and self.destination == other.destination and self.source == other.source

#Calculating the delivery time and giving the final answer.
def final_res(state):
    goal_state = state 
    route_taken = goal_state.path_to_state
    total_segments = len(route_taken)
    total_distance = sum(list(goal_state.distance_to_state))
    total_hours = sum([float(goal_state.distance_to_state[x])/float(goal_state.speed_lt_to_state[x]) for x in range(total_segments)])
    total_delivery_hours = 0
    for i in range(total_segments):
        p = 0
        if goal_state.speed_lt_to_state[i] >= 50:
            p = tanh(goal_state.distance_to_state[i]/1000)
            if i == 0:
                t_road = goal_state.distance_to_state[i]/goal_state.speed_lt_to_state[i]
                total_delivery_hours += t_road + 2 * p * t_road
            else :
                t_road = goal_state.distance_to_state[i]/goal_state.speed_lt_to_state[i]
                t_trip = sum(list(goal_state.distance_to_state[x]/goal_state.speed_lt_to_state[x] for x in range(i)))
                total_delivery_hours += t_road + 2 * p * ( t_road + t_trip )
        else:
            total_delivery_hours+= goal_state.distance_to_state[i]/goal_state.speed_lt_to_state[i]
   
    return {"total-segments" : total_segments,
    "total-miles" : total_distance,
    "total-hours" : total_hours,
    "total-delivery-hours" : total_delivery_hours,
    "route-taken" : route_taken}

# Heuristic Functions
def heuristic(cost,city,end_city,cities,total_distance,g,h_,max_speed,d,state):
    #calculates the heuristic for distance as a cost function
    def heuristic_distance(city,end_city,cities,total_distance,g,state):
        if city in cities.keys():
            h = distance_calculator(city,end_city,cities)
        else:
            if h_ != 0:
                h = h_ - g
            else: 
                return 0 # In case you start from a junction for some reason 
        return h

    #calculates the heuristic for segment as a cost function
    def heuristic_segment():
        h = 1
        return h

    #calculates the heuristic for time as a cost function
    def heuristic_time(city,end_city,cities,max_speed,g,d,state):
        if city in cities.keys():
            h = distance_calculator(city,end_city,cities)/max_speed
        else:
            # print('Distance')
            h = (total_distance-d)/max_speed
        return h

    #calculates the heuristic for delivery as a cost function
    def heuristic_delivery(city,end_city,cities,max_speed,g,d,state):
        d = final_res(state)
        # print(d)
        return d["total-delivery-hours"]

    #Checking the cost to know which heuristic to calculate based on the type of cost
    if cost == 'distance':
        return heuristic_distance(city,end_city,cities,total_distance,g,state)
    elif cost == 'time':
        return heuristic_time(city,end_city,cities,max_speed,g,d,state)
    elif cost == 'segments':
        return heuristic_segment()
    elif cost == 'delivery':
        return heuristic_delivery(city,end_city,cities,max_speed,g,d,state)

# Function to calculate the distance using latitude and longitude
# Referenced from 'https://www.mathworks.com/matlabcentral/answers/519457-how-to-calculate-the-euclidean-distance-beetwen-all-points-of-latitude-longitude-pairs'
def distance_calculator(start_city,end_city,cities):
    if start_city in cities.keys():
        latitude1,longitude1 = float(cities[start_city][0]),float(cities[start_city][1])
        latitude2,longitude2 = float(cities[end_city][0]),float(cities[end_city][1])
    lat_diff = (latitude2 * pi/180) - (latitude1 * pi/180)
    long_diff = (longitude2 * pi/180) - (longitude1 * pi/180)
    a = sin((lat_diff/2)) ** 2 + cos(latitude1) * cos(latitude2) * sin(long_diff/2) ** 2
    b = 2 * atan2(sqrt(abs(a)),sqrt(abs(1-a)))
    return(6371 * b * 0.62137119)

# Successors function
def successors(city,routes,visited_places):
    successor_states = []
    for key,value in routes.items():
        if city == key[0] and key[1] not in visited_places:
            successor_states.append(State(key[0],key[1],routes[key]["distance"],routes[key]["speed_lt"],routes[key]["highway"]))
    return successor_states

#To check if we have reached the goal(destination)
def is_goal(state,end):
    return state.destination == end

def state_tour(start,end,city_lat_long,road_segments):
    visited_states = {}
    for x in road_segments.keys():
        if '&' not in x[0]:
            visited_states[x[0].split(',')[-1][1:]] = 0
    print(len(visited_states))
    us_states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New_Hampshire','New_Jersey','New_Mexico','New_York','North_Carolina','North_Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode_Island','South_Carolina','South_Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West_Virginia','Wisconsin','Wyoming']
    to_delete = []
    for key in visited_states.keys():
        if key not in us_states:
            to_delete.append(key)
    for key in to_delete:
        del visited_states[key]
    print(len(visited_states))
    print(len(us_states))
    res = [x for x in visited_states.keys()]
    res.sort()
    print(res)

def get_route(start, end, cost):
   
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
   
    # return {"total-segments" : len(route_taken),
    #         "total-miles" : 51.,
    #         "total-hours" : 1.07949,
    #         "total-delivery-hours" : 1.1364,
    #         "route-taken" : route_taken}

    #Reading the 'city-gps.txt' which has the latitude and longitude for cities.
    city_lat_long = {}
    with open(r'city-gps.txt') as gps:
        for line in gps.readlines():
            city,lat,long = line.strip().split(' ')
            city_lat_long[city] = (lat,long)

    #Reading the 'road-segments.txt' which has various details such as start city,end city, distance in miles, speed limit in mph and highway name.
    road_segments = {}
    with open(r'road-segments.txt') as segments:
        for line in segments.readlines():
            source,destination,distance,speed_lt,highway = line.strip().split(' ')
            road_segments[(source,destination)] = {"distance":distance,"speed_lt":speed_lt,"highway":highway}
            road_segments[(destination,source)] = {"distance":distance,"speed_lt":speed_lt,"highway":highway}

    # Computing displacement between start and end using lat & long.
    total_distance = distance_calculator(start,end,city_lat_long)
    #Getting the global maximum speed limit in the file.
    road_values = road_segments.values()
    max_speed = max([i['speed_lt'] for i in road_values])
    max_speed = int(max_speed)
    pq = []
    #Keeping the track of all the visited places.
    visited_list = []
    visited_places = [start]

    #Giving the initial values for g and h.
    for state in successors(start,road_segments,visited_places):
        state.path_to_state = [state.move]
        if cost == 'distance':
            state.g = float(state.distance)
            d = float(state.distance)
            state.h = heuristic("distance",start,end,city_lat_long,total_distance,state.g,0,max_speed,d,state)
        elif cost == 'time':
            state.g = 0
            d = float(state.distance)
            state.h = heuristic("time",start,end,city_lat_long,total_distance,state.g,0,max_speed,d,state)
        elif cost == 'segments':
            state.g = 0
            d = float(state.distance)
            state.h = 1
        elif cost == 'delivery':
            state.g = 0
            d = float(state.distance)
            state.h = 0
        elif cost == 'statetour':
            return state_tour(start,end,city_lat_long,road_segments)
        state.speed_lt_to_state = [float(state.speed_lt)]
        state.distance_to_state = [float(state.distance)]
        # print("Path",state.path_to_state,"\nSource",state.source,"\nDestination",state.destination,"\nG",state.g,"\nH",state.h)
        state.set_f()
        visited_places.append(state.destination)
        pq.append(state)
    pq.sort(key=lambda x:x.f)

    # print(pq)

    #Checking if we reached the goal(destination state)
    if is_goal(pq[0],end):
        return final_res(pq[0])
       
    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
   
    # return {"total-segments" : len(route_taken),
    #         "total-miles" : 51.,
    #         "total-hours" : 1.07949,
    #         "total-delivery-hours" : 1.1364,
    #         "route-taken" : route_taken}

    #Getting the route after calculating the f-score which is equal to g-score and h-score.
    while pq:
        exploration_state = pq.pop(0)
        if is_goal(exploration_state,end):
            return final_res(exploration_state)

        successor_states = successors(exploration_state.destination,road_segments,visited_places)
        visited_places.append(exploration_state.destination)
        # print(len(successor_states))
        for state in successor_states:

            state.path_to_state = exploration_state.path_to_state + [state.move]
            state.speed_lt_to_state = exploration_state.speed_lt_to_state + [float(state.speed_lt)]
            state.distance_to_state = exploration_state.distance_to_state + [float(state.distance)]
            if cost == 'distance':
                state.g = exploration_state.g + float(state.distance)
            elif cost == 'time':
                #print("Time")
                d += float(state.distance)
                state.g = exploration_state.g + (float(state.distance)/float(state.speed_lt))
            elif cost == 'segments':    
                state.g = exploration_state.g + 1
            elif cost == 'delivery':
                d += float(state.distance)
                state.g = exploration_state.g + (float(state.distance)/float(state.speed_lt))
            state.h = heuristic(cost,start,end,city_lat_long,total_distance,state.g,exploration_state.h,max_speed,d,state)
            state.set_f()
            visited_places.append(state.destination)
            # print("Path to State:{} Move:{} g:{} h:{} f:{}".format(state.path_to_state,state.move,state.g,state.h,state.f))

        for state in successor_states:
            if state in pq:
                continue
            elif state in visited_list:
                continue
            else :
                pq.append(state)

        pq.sort(key=lambda x:x.f)
        visited_list.append(exploration_state)


# Please don't modify anything below this line
#
if __name__ == "__main__":

    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery","statetour"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
