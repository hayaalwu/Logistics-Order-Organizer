import math

# Store the coordinates of all stops
Stop_coordinates = {
    "Warehouse": (26.43, 50.10),
    "A": (26.39, 50.19),
    "B": (26.45, 50.05),
    "C": (26.30, 50.21),
    "D": (26.51, 50.04),
    "H": (26.40, 50.08)
}

# Calculate the distance between two stops
def get_distance(point1, point2):

    lat_diff = point1[0] - point2[0]
    lon_diff = point1[1] - point2[1]

    return math.sqrt(lat_diff**2 + lon_diff**2)


# Generate a route using the nearest neighbor approach
def generate_route(stops):

    unvisited_stops = list(set(stops))
    route = ["Warehouse"]
    current_stop = "Warehouse"

    # Visit the nearest unvisited stop
    while unvisited_stops:
        next_stop = min(
            unvisited_stops,
            key=lambda stop: get_distance(
                Stop_coordinates[current_stop],
                Stop_coordinates[stop]
            )
        )

        route.append(next_stop)
        unvisited_stops.remove(next_stop)
        current_stop = next_stop

    # Return to the warehouse
    route.append("Warehouse")

    return route