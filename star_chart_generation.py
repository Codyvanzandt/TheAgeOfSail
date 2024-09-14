import numpy

star_positions = {
    0: [
        ("Betelgeuse", 5, 120),
        ("Arcturus", 10, 60),
        ("Sirius", 20, 180),
        ("Vega", 30, 240),
        ("Polaris", 40, 0),
        ("Rigel", 15, 300),
        ("Deneb", 25, 30),
        ("Altair", 35, 150),
    ],
    5: [
        ("Betelgeuse", 10, 125),
        ("Arcturus", 15, 65),
        ("Sirius", 25, 185),
        ("Vega", 35, 245),
        ("Polaris", 45, 5),
        ("Rigel", 20, 305),
        ("Deneb", 30, 35),
        ("Altair", 40, 155),
    ],
    10: [
        ("Betelgeuse", 15, 130),
        ("Arcturus", 20, 70),
        ("Sirius", 30, 190),
        ("Vega", 40, 250),
        ("Polaris", 50, 10),
        ("Rigel", 25, 310),
        ("Deneb", 35, 40),
        ("Altair", 45, 160),
    ],
    15: [
        ("Betelgeuse", 20, 135),
        ("Arcturus", 25, 75),
        ("Sirius", 35, 195),
        ("Vega", 45, 255),
        ("Polaris", 55, 15),
        ("Rigel", 30, 315),
        ("Deneb", 40, 45),
        ("Altair", 50, 165),
    ],
    20: [
        ("Betelgeuse", 25, 140),
        ("Arcturus", 30, 80),
        ("Sirius", 40, 200),
        ("Vega", 50, 260),
        ("Polaris", 60, 20),
        ("Rigel", 35, 320),
        ("Deneb", 45, 50),
        ("Altair", 55, 170),
    ],
    25: [
        ("Betelgeuse", 30, 145),
        ("Arcturus", 35, 85),
        ("Sirius", 45, 205),
        ("Vega", 55, 265),
        ("Polaris", 65, 25),
        ("Rigel", 40, 325),
        ("Deneb", 50, 55),
        ("Altair", 60, 175),
    ],
    30: [
        ("Betelgeuse", 35, 150),
        ("Arcturus", 40, 90),
        ("Sirius", 50, 210),
        ("Vega", 60, 270),
        ("Polaris", 70, 30),
        ("Rigel", 45, 330),
        ("Deneb", 55, 60),
        ("Altair", 65, 180),
    ],
    35: [
        ("Betelgeuse", 40, 155),
        ("Arcturus", 45, 95),
        ("Sirius", 55, 215),
        ("Vega", 65, 275),
        ("Polaris", 75, 35),
        ("Rigel", 50, 335),
        ("Deneb", 60, 65),
        ("Altair", 70, 185),
    ],
    40: [
        ("Betelgeuse", 45, 160),
        ("Arcturus", 50, 100),
        ("Sirius", 60, 220),
        ("Vega", 70, 280),
        ("Polaris", 80, 40),
        ("Rigel", 55, 340),
        ("Deneb", 65, 70),
        ("Altair", 75, 190),
    ],
    45: [
        ("Betelgeuse", 50, 165),
        ("Arcturus", 55, 105),
        ("Sirius", 65, 225),
        ("Vega", 75, 285),
        ("Polaris", 85, 45),
        ("Rigel", 60, 345),
        ("Deneb", 70, 75),
        ("Altair", 80, 195),
    ],
    50: [
        ("Betelgeuse", 55, 170),
        ("Arcturus", 60, 110),
        ("Sirius", 70, 230),
        ("Vega", 80, 290),
        ("Polaris", 90, 50),
        ("Rigel", 65, 350),
        ("Deneb", 75, 80),
        ("Altair", 85, 200),
    ],
    55: [
        ("Betelgeuse", 60, 175),
        ("Arcturus", 65, 115),
        ("Sirius", 75, 235),
        ("Vega", 85, 295),
        ("Polaris", 90, 55),
        ("Rigel", 70, 355),
        ("Deneb", 80, 85),
        ("Altair", 85, 205),
    ],
    60: [
        ("Betelgeuse", 65, 180),
        ("Arcturus", 70, 120),
        ("Sirius", 80, 240),
        ("Vega", 90, 300),
        ("Polaris", 90, 60),
        ("Rigel", 75, 0),
        ("Deneb", 85, 90),
        ("Altair", 85, 210),
    ],
    65: [
        ("Betelgeuse", 70, 185),
        ("Arcturus", 75, 125),
        ("Sirius", 85, 245),
        ("Vega", 90, 305),
        ("Polaris", 90, 65),
        ("Rigel", 80, 5),
        ("Deneb", 90, 95),
        ("Altair", 85, 215),
    ],
    70: [
        ("Betelgeuse", 75, 190),
        ("Arcturus", 80, 130),
        ("Sirius", 90, 250),
        ("Vega", 90, 310),
        ("Polaris", 90, 70),
        ("Rigel", 85, 10),
        ("Deneb", 90, 100),
        ("Altair", 85, 220),
    ],
    75: [
        ("Betelgeuse", 80, 195),
        ("Arcturus", 85, 135),
        ("Sirius", 90, 255),
        ("Vega", 90, 315),
        ("Polaris", 90, 75),
        ("Rigel", 90, 15),
        ("Deneb", 90, 105),
        ("Altair", 85, 225),
    ],
    80: [
        ("Betelgeuse", 85, 200),
        ("Arcturus", 90, 140),
        ("Sirius", 90, 260),
        ("Vega", 90, 320),
        ("Polaris", 90, 80),
        ("Rigel", 90, 20),
        ("Deneb", 90, 110),
        ("Altair", 85, 230),
    ],
    85: [
        ("Betelgeuse", 90, 205),
        ("Arcturus", 90, 145),
        ("Sirius", 90, 265),
        ("Vega", 90, 325),
        ("Polaris", 90, 85),
        ("Rigel", 90, 25),
        ("Deneb", 90, 115),
        ("Altair", 85, 235),
    ],
    90: [
        ("Betelgeuse", 90, 210),
        ("Arcturus", 90, 150),
        ("Sirius", 90, 270),
        ("Vega", 90, 330),
        ("Polaris", 90, 90),
        ("Rigel", 90, 30),
        ("Deneb", 90, 120),
        ("Altair", 85, 240),
    ],
}


def get_svg_coords(altitude, azimuth, origin_x=250, origin_y=300):
    rho = compute_rho(altitude)
    degrees_anticlockwise = -azimuth
    radians = numpy.deg2rad(degrees_anticlockwise)
    x = rho * numpy.cos(radians) + origin_x
    y = rho * numpy.sin(radians) + origin_y
    return round(x), round(y)


def compute_rho(altitude):
    return 220 - (220 - 55) / 90 * altitude


def interpolate_curve(start, end, control_factor=-1.25, num_points=19):
    """
    Interpolate a curve between two points using a quadratic Bézier curve with evenly spaced points.

    :param start: Tuple (x, y) representing the start point.
    :param end: Tuple (x, y) representing the end point.
    :param control_factor: Factor to control how far the curve extends (0 to 1).
    :param num_points: Number of points to generate on the curve.
    :return: List of (x, y) tuples representing the interpolated curve with evenly spaced points.
    """
    start = numpy.array(start)
    end = numpy.array(end)

    # Calculate control point
    midpoint = (start + end) / 2
    vector = end - start
    perpendicular = numpy.array([-vector[1], vector[0]])
    perpendicular = perpendicular / numpy.linalg.norm(perpendicular)
    control_point = midpoint + perpendicular * control_factor * numpy.linalg.norm(
        vector
    )

    def bezier_point(t):
        return (1 - t) ** 2 * start + 2 * (1 - t) * t * control_point + t**2 * end

    # Generate initial points
    t_values = numpy.linspace(0, 1, 1000)
    initial_points = numpy.array([bezier_point(t) for t in t_values])

    # Calculate cumulative chord lengths
    chord_lengths = numpy.cumsum(
        numpy.sqrt(numpy.sum(numpy.diff(initial_points, axis=0) ** 2, axis=1))
    )
    chord_lengths = numpy.insert(chord_lengths, 0, 0)  # Add starting point

    # Normalize chord lengths
    chord_lengths /= chord_lengths[-1]

    # Generate evenly spaced points
    even_t_values = numpy.linspace(0, 1, num_points)
    interpolator = numpy.interp(even_t_values, chord_lengths, t_values)

    even_points = [bezier_point(t) for t in interpolator]

    return [tuple(round(x) for x in point) for point in even_points]


def generate_star_path(start_alt_az, end_alt_az, control_factor=0.5):
    start_xy = get_svg_coords(start_alt_az[0], start_alt_az[1])
    end_xy = get_svg_coords(end_alt_az[0], end_alt_az[1])
    return interpolate_curve(
        start_xy, end_xy, control_factor=control_factor, num_points=19
    )


star_paths = {
    "Betelgeuse": generate_star_path((10, 300), (45, 135), control_factor=-1),
    "Arcturus": generate_star_path((88, 15), (81, 132), control_factor=3.2),
    "Sirius": generate_star_path((17, 50), (7, 235), control_factor=-0.5),
    "Vega": generate_star_path((22, 100), (68, 245), control_factor=-1.8),
    "Pollux": generate_star_path((5, 91), (5, 220), control_factor=0.5),
    "Rigel": generate_star_path((60, 192), (3, 345), control_factor=0.8),
    "Deneb": generate_star_path((50, 70), (83, 230), control_factor=2),
    "Altair": generate_star_path((2, 125), (7, 355), control_factor=0.1),
}

star_paths = [dict(zip(star_paths.keys(), path)) for path in zip(*star_paths.values())]


import os
from jinja2 import Template

# Read the Jinja template from a local file
with open("star_chart_2.jinja", "r") as file:
    template_str = file.read()

# Create a Jinja template object
template = Template(template_str)


for latitude, stars in zip(range(0, 95, 5), star_paths):
    svg_content = template.render(latitude=latitude, stars=list(stars.items()))

    # Generate the output filename using the item's name
    filename = f"./star_charts/star_chart_{latitude}_latitude.svg"

    # Save the SVG to a local file
    with open(filename, "w") as file:
        file.write(svg_content)

print("SVGs generated successfully!")
