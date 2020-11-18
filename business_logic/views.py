from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import Driver
from routes.models import Route, DesignatedRoute
from users.serializers import DriverSerializer


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def assign_driver_to_a_route(request, route_pk):
    route_id = route_pk
    route = Route.objects.filter(id=route_id)[0]
    drivers = list(Driver.objects.filter(manager__user_id=request.user.id).filter(car_type=route.load_type))
    designated_routes = list(DesignatedRoute.objects.all())

    for droute in designated_routes:
        if droute.driver in drivers:
            drivers.remove(droute.driver)
        if droute.route.id == route_id:
            return Response("The route is already in progress")

    for driver in drivers:
        if driver.car_type != route.load_type:
            drivers.remove(driver)
        if route.load_quantity > driver.car_max_load:
            drivers.remove(driver)

    if not drivers:
        return Response("There are no drivers available at the moment")

    driver_weights = {}

    for driver in drivers:
        weight = 0
        if driver.health_state:
            weight += 0.9 * driver.health_state
        if driver.current_location:
            weight -= 0.1 * round(route.start_location.distance(driver.current_location) * 100)
        weight -= 0.2 * route.distance * driver.pay_for_km
        weight += 0.2 * driver.average_speed_per_hour
        driver_weights[driver] = weight

    sorted_weights = {k: v for k, v in sorted(driver_weights.items(), key=lambda item: item[1])}
    assigned_driver = list(sorted_weights.keys())[-1]
    serializer = DriverSerializer(assigned_driver)
    return Response(serializer.data)