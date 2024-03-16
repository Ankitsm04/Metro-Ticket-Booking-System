import streamlit as st
import qrcode
from io import BytesIO


class MetroStation:
    def __init__(self, name):
        self.name = name
        self.connections = {}  # Dictionary to store connected stations and their edge information

    def add_connection(self, station, distance, fare):
        self.connections[station] = {'distance': distance, 'fare': fare}


class MetroNetwork:
    def __init__(self):
        self.stations = {}

    def add_station(self, station_name):
        if station_name not in self.stations:
            self.stations[station_name] = MetroStation(station_name)

    def add_connection(self, station1_name, station2_name, distance, fare):
        self.add_station(station1_name)
        self.add_station(station2_name)
        self.stations[station1_name].add_connection(station2_name, distance, fare)
        self.stations[station2_name].add_connection(station1_name, distance, fare)

    def calculate_fare_and_distance(self, source, destination):
        if source == destination:
            return "Same Station selected", None, None
        route = self.find_route(source, destination)
        if route:
            total_distance = sum(
                self.stations[route[i]].connections[route[i + 1]]['distance'] for i in range(len(route) - 1))
            total_fare = sum(
                self.stations[route[i]].connections[route[i + 1]]['fare'] for i in range(len(route) - 1))
            return total_fare, total_distance, route
        else:
            return None, None, None

    def find_route(self, start_station, end_station):
        visited = set()
        queue = [[start_station]]

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end_station:
                return path
            if node not in visited:
                for neighbor in self.stations[node].connections.keys():
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
            visited.add(node)
        return None


metro = MetroNetwork()

# Add stations for the Purple Line
purple_line_stations = ['Mysore Road', 'Deepanjali Nagar', 'Attiguppe', 'Vijayanagar', 'Magadi Road', 'Hosahalli',
                        'Nayandahalli', 'Peenya Industry', 'Peenya']

for station in purple_line_stations:
    metro.add_station(station)

# Add connections with distance and fare for the Purple Line
purple_line_connections = [
    ('Mysore Road', 'Deepanjali Nagar', 5, 10),
    ('Deepanjali Nagar', 'Attiguppe', 3, 5),
    ('Deepanjali Nagar', 'Vijayanagar', 4, 8),
    ('Vijayanagar', 'Magadi Road', 3, 6),
    ('Magadi Road', 'Hosahalli', 2, 4),
    ('Hosahalli', 'Nayandahalli', 3, 6),
    ('Nayandahalli', 'Peenya Industry', 4, 8),
    ('Peenya Industry', 'Peenya', 3, 6),
]

for connection in purple_line_connections:
    metro.add_connection(*connection)

# Add stations for the Green Line
green_line_stations = ['Nagasandra', 'Dasarahalli', 'Jalahalli', 'Peenya Industry', 'Peenya', 'Goraguntepalya',
                       'Yeshwantpur', 'Sandal Soap Factory', 'Mahalakshmi', 'Rajajinagar', 'Kuvempu Road',
                       'Srirampura', 'Sampige Road', 'Kempegowda Interchange', 'Chickpete', 'K R Market',
                       'National College', 'Lalbagh', 'South End Circle', 'Jayanagar', 'R V Road Interchange',
                       'Banashankari', 'JP Nagar', 'Puttenahalli', 'Anjanapura Cross Road']

for station in green_line_stations:
    metro.add_station(station)

# Add connections with distance and fare for the Green Line
green_line_connections = [
    ('Nagasandra', 'Dasarahalli', 2, 5),
    ('Dasarahalli', 'Jalahalli', 2, 5),
    ('Jalahalli', 'Peenya Industry', 3, 5),
    ('Peenya Industry', 'Peenya', 2, 5),
    ('Peenya', 'Goraguntepalya', 3, 5),
    ('Goraguntepalya', 'Yeshwantpur', 3, 5),
    ('Yeshwantpur', 'Sandal Soap Factory', 3, 5),
    ('Sandal Soap Factory', 'Mahalakshmi', 3, 5),
    ('Mahalakshmi', 'Rajajinagar', 2, 5),
    ('Rajajinagar', 'Kuvempu Road', 2, 5),
    ('Kuvempu Road', 'Srirampura', 2, 5),
    ('Srirampura', 'Sampige Road', 2, 5),
    ('Sampige Road', 'Kempegowda Interchange', 3, 5),
    ('Kempegowda Interchange', 'Chickpete', 3, 5),
    ('Chickpete', 'K R Market', 2, 5),
    ('K R Market', 'National College', 2, 5),
    ('National College', 'Lalbagh', 2, 5),
    ('Lalbagh', 'South End Circle', 3, 5),
    ('South End Circle', 'Jayanagar', 2, 5),
    ('Jayanagar', 'R V Road Interchange', 2, 5),
    ('R V Road Interchange', 'Banashankari', 3, 5),
    ('Banashankari', 'JP Nagar', 3, 5),
    ('JP Nagar', 'Puttenahalli', 3, 5),
    ('Puttenahalli', 'Anjanapura Cross Road', 2, 5),
]

for connection in green_line_connections:
    metro.add_connection(*connection)

# Streamlit UI
st.title('Namma Metro Ticket Booking System')
st.image("namma-metro-map.jpg", caption="Namma Metro", use_column_width=True)
line = st.radio("Select Line:", ('Purple Line', 'Green Line'))

if line == 'Purple Line':
    stations = purple_line_stations
else:
    stations = green_line_stations

source = st.selectbox('Select Source Station:', stations)
destination = st.selectbox('Select Destination Station:', stations)
book_ticket = st.selectbox("Do you want to book ticket?", ('Yes', 'No'))

if st.button('Calculate Fare and Distance'):
    if source and destination:
        if line == 'Purple Line':
            fare, distance, route = metro.calculate_fare_and_distance(source, destination)
        else:
            fare, distance, route = metro.calculate_fare_and_distance(source, destination)
        if fare is not None and distance is not None:
            if isinstance(fare, str):
                st.error(fare)
            else:
                st.success(f'Fare: Rs. {fare} | Distance: {distance} km')
                if book_ticket == 'Yes':
                    # Generate QR Code
                    qr_code_data = f'Ticket: From {source} to {destination}\nFare: Rs. {fare}\nDistance: {distance} km'
                    qr_code = qrcode.make(qr_code_data)

                    # Convert QR Code to bytes-like object
                    buffer = BytesIO()
                    qr_code.save(buffer, format='PNG')
                    qr_code_bytes = buffer.getvalue()

                    # Display QR Code
                    st.image(qr_code_bytes, caption='QR Code', use_column_width=True)
                    st.write("Ticket booked successfully!")
                else:
                    st.write("Thank you for using our service!")
        else:
            st.error('No route found. Please select valid source and destination stations.')
    else:
        st.warning('Please select both source and destination stations.')
