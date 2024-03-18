import streamlit as st
import qrcode
from io import BytesIO
from heapq import heappush, heappop

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
        fare, path = self.find_shortest_path(source, destination)
        if fare is not None and path is not None:
            total_distance = sum(
                self.stations[path[i]].connections[path[i + 1]]['distance'] for i in range(len(path) - 1))
            return fare, total_distance, path
        else:
            return None, None, None

    def find_shortest_path(self, start_station, end_station):
        priority_queue = [(0, start_station)]  # Tuple: (fare, station)
        shortest_fares = {station: float('inf') for station in self.stations}
        shortest_fares[start_station] = 0
        previous_station = {station: None for station in self.stations}

        while priority_queue:
            current_fare, current_station = heappop(priority_queue)
            if current_station == end_station:
                path = []
                while current_station is not None:
                    path.append(current_station)
                    current_station = previous_station[current_station]
                return current_fare, path[::-1]  # Reverse the path to get it from start to end
            for neighbor, edge_info in self.stations[current_station].connections.items():
                fare_to_neighbor = current_fare + edge_info['fare']
                if fare_to_neighbor < shortest_fares[neighbor]:
                    shortest_fares[neighbor] = fare_to_neighbor
                    previous_station[neighbor] = current_station
                    heappush(priority_queue, (fare_to_neighbor, neighbor))

        return None, None  # No path found


metro = MetroNetwork()

# Add stations for the Purple Line
purple_line_stations = ['Mysore Road', 'Deepanjali Nagar', 'Attiguppe', 'Vijayanagar', 'Magadi Road', 'City Rly Stn',
                        'Majestic', 'Sir M.Vishveshwaraih', 'Vidhana Soudha','Cubbon Park','MG Road','Trinity','Halasuru',
                        'Indiriranagar','Swami Vivekananda Rd','Baiyyapanahalli']

for station in purple_line_stations:
    metro.add_station(station)

# Add connections with distance and fare for the Purple Line
purple_line_connections = [
    ('Mysore Road', 'Deepanjali Nagar', 5, 10),
    ('Deepanjali Nagar', 'Attiguppe', 3, 5),
    ('Deepanjali Nagar', 'Vijayanagar', 4, 8),
    ('Vijayanagar', 'Magadi Road', 3, 6),
    ('Magadi Road', 'City Rly Stn', 2, 4),
    ('City Rly Stn', 'Majestic', 3, 6),
    ('Majestic', 'Sir M.Vishveshwaraih', 4, 8),
    ('Sir M.Vishveshwaraih', 'Vidhana Soudha', 3, 6),
    ('Vidhana Soudha','Cubbon Park',3,6),
    ('Cubbon Park','MG Road',4,8),
    ('MG Road','Trinity',3,6),
    ('Trinity','Halasuru',5,10),
    ('Halasuru','Indiriranagar',4,8),
    ('Indiriranagar','Swami Vivekananda Rd',3,6),
    ('Swami Vivekananda Rd','Baiyyapanahalli',4,8),
]


for connection in purple_line_connections:
    metro.add_connection(*connection)

# Add stations for the Green Line
green_line_stations = ['Nagasandra', 'Dasarahalli', 'Jalahalli', 'Peenya Industry', 'Peenya', 'Goraguntepalya',
                       'Yeshwantpur', 'Sandal Soap Factory', 'Mahalakshmi', 'Rajajinagar', 'Kuvempu Road',
                       'Srirampura', 'Sampige Road', 'Majestic', 'Chickpete', 'K R Market',
                       'National College', 'Lalbagh', 'South End Circle', 'Jayanagar', 'R V Road Interchange',
                       'Banashankari', 'JP Nagar', 'Yelechenahalli']

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
    ('Sampige Road', 'Majestic', 3, 5),
    ('Majestic', 'Chickpete', 3, 5),
    ('Chickpete', 'K R Market', 2, 5),
    ('K R Market', 'National College', 2, 5),
    ('National College', 'Lalbagh', 2, 5),
    ('Lalbagh', 'South End Circle', 3, 5),
    ('South End Circle', 'Jayanagar', 2, 5),
    ('Jayanagar', 'R V Road Interchange', 2, 5),
    ('R V Road Interchange', 'Banashankari', 3, 5),
    ('Banashankari', 'JP Nagar', 3, 5),
    ('JP Nagar', 'Yelechenahalli', 3, 5),
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

