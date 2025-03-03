from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


##### FLIGHTS #####

class SavedFlight(Base):
    __tablename__ = 'saved_flight'
    user_id = Column(String, nullable=False)
    flight_id = Column(String, ForeignKey('flight_info.flight_id'), nullable=False)
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'flight_id'),
    )

class FlightInfo(Base):
    __tablename__ = 'flight_info'
    flight_id = Column(String, primary_key=True)
    total_num_segments = Column(Integer)
    price = Column(String)
    num_users_saved = Column(Integer, default=0)

class FlightSegments(Base):
    __tablename__ = 'flight_segments'
    flight_id = Column(String, ForeignKey('flight_info.flight_id'), nullable=False)
    segment_id = Column(String, ForeignKey('segment_info.segment_id'), nullable=False)
    segment_order = Column(Integer)
    bound = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint('flight_id', 'segment_order', 'bound'),
    )

class SegmentInfo(Base):
    __tablename__ = 'segment_info'
    segment_id = Column(String, primary_key=True)
    airline_code = Column(String)
    flight_code = Column(String)
    departure_date = Column(String)
    departure_time = Column(String)
    arrival_date = Column(String)
    arrival_time = Column(String)
    duration = Column(String)
    departure_airport = Column(String)
    destination_airport = Column(String)
    num_flights_saved = Column(Integer, default=0)


##### ITINERARY #####

class SavedItinerary(Base):
    __tablename__ = 'saved_itinerary'
    user_id = Column(String, nullable=False)
    activity_id = Column(String, ForeignKey('itinerary_info.activity_id'), nullable=False)
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'activity_id'),
    )

class ItineraryInfo(Base):
    __tablename__ = 'itinerary_info'
    city = Column(String)
    activity_id = Column(String, primary_key=True)
    activity_name = Column(String)
    activity_details = Column(String)
    price_amount = Column(String)
    price_currency = Column(String)
    pictures = Column(String)
    num_users_saved = Column(Integer, default=0)