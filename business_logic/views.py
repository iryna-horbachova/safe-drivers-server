from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import Driver
from routes.models import Route, DesignatedRoute
from users.serializers import DriverSerializer
from routes.serializers import DesignatedRouteSerializer

from enum import Enum
import math


class Criterias(Enum):
    HEALTH_STATE = 1
    DISTANCE = 2
    PAY_FOR_KM = 3
    AVERAGE_SPEED = 4
    EXPERIENCE = 5


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def assign_driver_to_a_route(request, route_pk):

    """
    Optimization criterias:
    Health state, Distance to the location, Pay for km, Average speed
    Criteria coeficients: ranging
    Method of rationing: min/max
    """

    priorities = request.data['priorities']
    print(request.data)
    print(request.data['priorities'])

    # Forming a sample of drivers
    route_id = route_pk
    route = Route.objects.filter(id=route_id)[0]
    drivers = list(Driver.objects.filter(manager__user_id=request.user.id)
                   .filter(car_type=route.load_type)
                   .filter(car_max_load__gte=route.load_quantity))
    designated_routes = list(DesignatedRoute.objects.all())
    print('filtered drivers in the beginning')
    print(drivers)

    for droute in designated_routes:
        if droute.driver in drivers:
            drivers.remove(droute.driver)
        if droute.route.id == route_id:
            return Response({'error': "The route is already in progress", 'driver': None})

    print('drivers after route filtration')
    print(drivers)

    if not drivers:
        return Response({'error': "There are no drivers available at the moment", 'driver': None})

    if len(drivers) == 1:
        return Response({'driver': DriverSerializer(drivers[0]).data, 'error': None})

    # Checking Paretto
    drivers_to_remove = []

    for i in range(0, len(drivers) - 1):
        is_removed = False
        for j in range(i+1, len(drivers)):
            if not is_removed:
                if (drivers[i].health_state < drivers[j].health_state
                    and round(route.start_location.distance(drivers[i].current_location) * 100) >
                    round(route.start_location.distance(drivers[j].current_location) * 100)
                        and drivers[i].pay_for_km > drivers[j].pay_for_km
                        and drivers[i].average_speed_per_hour < drivers[j].average_speed_per_hour
                        and drivers[i].experience < drivers[j].experience):
                    is_removed = True
                    drivers_to_remove.append(drivers[i].user.id)
    print('remove')
    print(drivers_to_remove)
    for id in drivers_to_remove:
        drivers = list(filter(lambda driver: driver.user.id != id, drivers))

    print('drivers left')
    print(drivers)
    if len(drivers) == 1:
        return Response({'driver': DriverSerializer(drivers[0]).data, 'error': None})

    # Coefiicients

    criteria_count = 5
    coeff1 = 5 / 15
    coeff2 = 4 / 15
    coeff3 = 3 / 15
    coeff4 = 2 / 15
    coeff5 = 1 / 15
    coeffs = [coeff1, coeff2, coeff3, coeff4, coeff5]

    # Forming minmax for rationing

    min_health_state = 10
    max_health_state = 0
    min_average_speed = math.inf
    max_average_speed = 0
    min_pay_for_km = math.inf
    max_pay_for_km = 0
    min_distance = math.inf
    max_distance = 0
    min_experience = math.inf
    max_experience = 0

    for driver in drivers:
        distance = round(route.start_location.distance(driver.current_location) * 100)
        if driver.health_state  > max_health_state:
            max_health_state = driver.health_state
        elif driver.health_state < min_health_state:
            min_health_state = driver.health_state
        if driver.average_speed_per_hour > max_average_speed:
            max_average_speed = driver.average_speed_per_hour
        elif driver.average_speed_per_hour < min_average_speed:
            min_average_speed = driver.average_speed_per_hour
        if driver.pay_for_km > max_pay_for_km:
            max_pay_for_km = driver.pay_for_km
        elif driver.pay_for_km < min_pay_for_km:
            min_pay_for_km = driver.pay_for_km
        if distance > max_distance:
            max_distance = distance
        elif distance < min_distance:
            min_distance = distance
        if driver.experience > max_experience:
            max_experience = driver.experience
        elif driver.experience < min_experience:
            min_experience = driver.experience

    # Implemenation of the Algorithm
    # with value rationing

    driver_weights = {}

    for driver in drivers:
        distance = round(route.start_location.distance(driver.current_location) * 100)

        health_weight = coeffs[priorities.index(Criterias.HEALTH_STATE.value)] * \
                  ((driver.health_state - min_health_state) / ((max_health_state - min_health_state) if (max_health_state - min_health_state) else 1))
        distance_weight = coeffs[priorities.index(Criterias.DISTANCE.value)] * \
                          ((max_distance - distance) / (max_distance - min_distance))
        pay_for_km_weight = coeffs[priorities.index(Criterias.PAY_FOR_KM.value)] * \
                          ((max_pay_for_km - driver.pay_for_km) / (max_pay_for_km - min_pay_for_km))
        average_speed_weight = coeffs[priorities.index(Criterias.AVERAGE_SPEED.value)] * \
                  ((driver.average_speed_per_hour - min_average_speed) / (max_average_speed - min_average_speed))
        experience_weight = coeffs[priorities.index(Criterias.EXPERIENCE.value)] * \
                  ((driver.experience - min_experience) / (max_experience - min_experience))

        weight = health_weight + distance_weight + pay_for_km_weight + average_speed_weight + experience_weight
        driver_weights[driver] = weight

    sorted_weights = {k: v for k, v in sorted(driver_weights.items(), key=lambda item: item[1])}
    print('sorted weights')
    print(sorted_weights)
    assigned_driver = list(sorted_weights.keys())[-1]

    serializer = DriverSerializer(assigned_driver)
    return Response({'driver': serializer.data, 'error': None})


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def designate_route(request):
    user_id = request.data['driver_id']
    route_id = request.data['route_id']

    driver = Driver.objects.filter(user_id=user_id)[0]
    route = Route.objects.filter(id=route_id)[0]

    d_route = DesignatedRoute.objects.create(route=route, driver=driver, status="N")

    return Response(DesignatedRouteSerializer(d_route).data)


class Statuses(Enum):
    HEALTH_STATE = 1
    DISTANCE = 2
    PAY_FOR_KM = 3
    AVERAGE_SPEED = 4
    EXPERIENCE = 5


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def designate_routes(request):
    all_routes =  list(Route.objects.filter(manager__user_id=request.user.id))
    designated_routes = list(DesignatedRoute.objects.all())
    # Remove routes in progress
    for droute in designated_routes:
        if droute.route in all_routes:
            all_routes.remove(droute.route)

    print("all_routes")
    print(all_routes)
    # Sort routes by priority
    routes = []
    for route in all_routes:
        if route.priority == 'H':
            routes.insert(0, route)
        elif route.priority == 'S':
            routes.append(route)
    for route in all_routes:
        if route.priority == 'L':
            routes.append(route)

    print("sorted routes")
    print(routes)

    # Getting all drivers that currently are not assigned to any of the routes
    drivers = list(Driver.objects.filter(manager__user_id=request.user.id))

    for d_route in designated_routes:
        if d_route.driver in drivers and d_route.status != "F":
            drivers.remove(d_route.driver)

    # Greedy algorithms
    # Iterate through all the routes
    for route in routes:
        print("current route")
        print(route)
        drivers_costs = {}
        # Calculate cost of current route for each driver
        for driver in drivers:
            cost = driver.pay_for_km *\
                            round(route.start_location.distance(driver.current_location) * 100) +\
                            driver.pay_for_km * route.distance
            drivers_costs[driver] = cost

        sorted_costs = {k: v for k, v in sorted(drivers_costs.items(), key=lambda item: item[1])}
        print("sorted costs")
        print(sorted_costs)

        # Assign the first driver who satisfies current route requirements
        for driver, cost in sorted_costs.items():
            if (driver.experience >= route.min_experience
                and driver.car_type == route.load_type
                and driver.car_max_load >= route.load_quantity
                and driver.health_state >= route.min_health):
                drivers.remove(driver)
                d_route = DesignatedRoute.objects.create(route=route, driver=driver, status="N")
                print(d_route)
                break;

    return Response("Routes successfully designated")

