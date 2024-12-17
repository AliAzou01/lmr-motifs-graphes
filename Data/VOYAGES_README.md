# Cargo voyages

## Content

The file contains 99069 voyages from 1556 cargo vessels in 2022. 

## Fields

- id: This is a unique identifier for each voyage.
- mmsi: This is the Maritime Mobile Service Identity (MMSI) number of the vessel that made the voyage. The MMSI is a unique number assigned to each vessel for identification purposes. Unlike the IMO, the MMSI of a vessel may change during the lifetime of the vessel.
- imo: This is the International Maritime Organization (IMO) number of the vessel. The IMO number is a unique number assigned to each vessel for identification purposes.
- departure_date: This is the date and time when the vessel departed from its origin.
- arrival_date: This is the date and time when the vessel arrived at its destination.
- departure_port and arrival_port: These are the ports from which the vessel departed and to which it arrived, respectively.
- departure_date and arrival_date: These are the dates and times when the vessel departed from its origin and arrived at its destination, respectively.
- berth_date and unberth_date: These are the dates and times when the vessel was berthed at its origin and destination, respectively.
- eosp_date: EOSP stands for End Of Sea Passage; i.e. when the vessel enters the vicinity of a port but is not yet berthed. t may be - for instance - in a waiting zone.
- total_distance: This is the total distance of the voyage in nautical miles. 
- number_of_positions: the number of AIS positions reported during the voyage. 
- avg_distance_between_two_positions: This is the average distance between two consecutive AIS positions reported during the voyage. 
- max_distance_between_two_positions: This is the maximum distance between two consecutive AIS positions reported during the voyage. 
- path_file: This is the file name of the path file. The path file contains the AIS positions reported during the voyage (on demand).
- ais_static_messages: may contains static information about the vessel, transmitted within the AIS message.
- waiting_areas: may contains the waiting areas the vessel was in during the voyage.

### Ais static messages

- eta: stands for Estimated Time of Arrival. It's the estimated date and time when the vessel is expected to arrive at its destination.
- destination: the port or location where the vessel is expected to arrive.
- draught: the depth of water from the waterline to the bottom of the vessel.
- timestamp: the timestamp of the AIS message.
