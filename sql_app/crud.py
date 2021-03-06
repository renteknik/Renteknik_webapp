# CRUD: CREATE READ UPDATE DELETE

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select
from collections import defaultdict

from . import models, schemas

# Add the provided values to the arc meta data table
def create_panpower_metadata(db: Session, panpower_meta_data: schemas.PanpowerMetaData):
    panpower_meta_data = panpower_meta_data.dict()
    # print(arc_meta_data)
    # print(db)
    db_measurement = models.PanpowerMetaData(**panpower_meta_data)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the Pan42 table.
def create_pan42(db: Session, measurements: schemas.Pan42DictCover):
    measurements = measurements.dict()
    for measurement in measurements:
        measure = measurements[measurement]
        for val in measure:
            # print(f"val = {val}")
            db_measurement = models.Panpower42Measurement(**val)
            db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the panpower pulse table.
def create_panpulse(db: Session, measurements: schemas.PanpowerPulseDictCover):
    measurements = measurements.dict()
    for measurement in measurements:
        measure = measurements[measurement]
        for val in measure:
            # print(f"val = {val}")
            db_measurement = models.PanpowerPulseMeasurement(**val)
            db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the panpower 10/12 table.
def create_panpower(db: Session, measurements: schemas.PanPowerDictCover):
    measurements = measurements.dict()
    for measurement in measurements:
        measure = measurements[measurement]
        for val in measure:
            # print(f"val = {type(val['measurement_time'])},\n")
            db_measurement = models.Panpower1012Measurement(**val)
            db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the arc meta data table
def create_arc_metadata(db: Session, arc_meta_data: schemas.ArcMetaData):
    arc_meta_data = arc_meta_data.dict()
    # print(arc_meta_data)
    # print(db)
    db_measurement = models.ArcMetaData(**arc_meta_data)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the arc key table
def create_arc_keytable(db: Session, arc_key_values: schemas.ArcKeyTable = None, arc_key_dict: dict = None):
    if(arc_key_values):
        arc_key_values = arc_key_values.dict()
    elif(arc_key_dict):
        arc_key_values = arc_key_dict
    # print(arc_key_values)
    # print(db)
    db_measurement = models.ArcKeyTable(**arc_key_values)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)


# Add the provided values to the arc meter table
def create_arc_metertable(db: Session, arc_meter_values: schemas.ArcMeterTable):
    arc_meter_values = arc_meter_values.dict()
    # print(arc_meter_values)
    # print(db)
    db_measurement = models.ArcMeterTable(**arc_meter_values)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)



# Get the metadata from panpower metadata database
def get_panpowermetadata_sitename(db: Session, site_name: str):
    return db.query(models.PanpowerMetaData).filter(models.PanpowerMetaData.site_name == site_name).first()


# Get the given client name from panpower1012
def get_panpower1012_client(db: Session, client_name: str):
    return db.query(models.Panpower1012Measurement).filter(models.Panpower1012Measurement.client == client_name).first()


# Get data from panpower1012 based on client name
def get_panpower1012_client_data(db: Session, client_name: str):
    return db.query(models.Panpower1012Measurement).filter(models.Panpower1012Measurement.client == client_name).all()


# Get the given client name from pan42
def get_pan42_client(db: Session, client_name: str):
    return db.query(models.Panpower42Measurement).filter(models.Panpower42Measurement.client == client_name).first()


# Get data from pan42 based on client name
def get_pan42_client_data(db: Session, client_name: str):
    return db.query(models.Panpower42Measurement).filter(models.Panpower42Measurement.client == client_name).all()


# Get the given client name from pan42
def get_panpowerpulse_client(db: Session, client_name: str):
    return db.query(models.PanpowerPulseMeasurement).filter(models.PanpowerPulseMeasurement.client == client_name).first()


# Get data from panpower pulse based on client name
def get_panpowerpulse_client_data(db: Session, client_name: str):
    return db.query(models.PanpowerPulseMeasurement).filter(models.PanpowerPulseMeasurement.client == client_name).all()


# Get access and refresh token for the given client name
def get_arc_keys_clientname(db: Session, client_name: str):
    return db.query(models.ArcKeyTable).filter(models.ArcKeyTable.client_name == client_name).first()


# Get data from Arc meta data table based on the leed id
def get_arc_metadata_leedid(db: Session, leed_id: str):
    return db.query(models.ArcMetaData).filter(models.ArcMetaData.leed_id == leed_id).first()


# Get data from arc meter table based on the meter_id
def get_arc_meter_data_meter_id(db: Session, meter_id: str):
    return db.query(models.ArcMeterTable).filter(models.ArcMeterTable.meter_id == meter_id).first()

# # Get the given leed id from panpower1012
# def get_arc_leed_data(db: Session, leed_id: str):
#     return db.query(models.ArcMetaData).filter(models.ArcMetaData.leed_id == leed_id).first()


# # Get the arc keys from arc key table based on the given leed id
# def get_arckey_leedid(db: Session, leed_id: str):
#     return db.query(models.ArcKeyTable).filter(models.ArcKeyTable.leed_id == leed_id).first()


# Get the arc keys from arc key table based on the given leed id
def update_arckeytable_client(db: Session, client_name: str, access_token: str, refresh_token: str, current_time: str):
    db.query(models.ArcKeyTable).filter(models.ArcKeyTable.client_name == client_name).update({models.ArcKeyTable.access_token: access_token, models.ArcKeyTable.refresh_token: refresh_token, models.ArcKeyTable.current_time: current_time}, synchronize_session = False)
    db.commit()
    db.flush()


# Get the arc keys from arc key table based on the given leed id
def update_arcmetadata_leedid(db: Session, leed_id: str, electrical_hierarchy: str, timezone: str, duration_format: str, duration: str):
    db.query(models.ArcMetaData).filter(models.ArcMetaData.leed_id == leed_id).update({models.ArcMetaData.electrical_hierarchy: electrical_hierarchy, models.ArcMetaData.timezone: timezone, models.ArcMetaData.duration_format: duration_format, models.ArcMetaData.duration: duration}, synchronize_session = False)
    db.commit()
    db.flush()



# Get the arc keys from arc key table based on the given leed id
def update_arcmetertable_meterid(db: Session, meter_id:str, leed_id: str, customer_id: str, meter_name: str, meter_type: str, meter_unit: str, renteknik_meter: str, duration_format: str, duration: str):
    db.query(models.ArcMeterTable).filter(models.ArcMeterTable.meter_id == meter_id).update({models.ArcMeterTable.leed_id: leed_id, models.ArcMeterTable.customer_id: customer_id,
                                                                                           models.ArcMeterTable.meter_name: meter_name, models.ArcMeterTable.meter_type: meter_type,
                                                                                           models.ArcMeterTable.meter_unit: meter_unit, models.ArcMeterTable.renteknik_meter: renteknik_meter,
                                                                                           models.ArcMeterTable.duration_format: duration_format, models.ArcMeterTable.duration: duration}, synchronize_session = False)
    db.commit()
    db.flush()




# def query_to_dict(rset):
#     result = defaultdict(list)
#     for obj in rset:
#         instance = inspect(obj)
#         for key, x in instance.attrs.items():
#             result[key].append(x.value)
#     return result

# Getting data for Energystar update from data base
# Monthly data Based on the date and client name
def energy_star_fetch_data(db: Session, client: str, start_date: str, end_date: str):

    # select where method to choose data from the data base
    stmt = select(models.Panpower1012Measurement).where(models.Panpower1012Measurement.client == client, models.Panpower1012Measurement.measurement_time >= start_date,
                                                        models.Panpower1012Measurement.measurement_time < end_date) \
                                                        .group_by(models.Panpower1012Measurement.measurement_time, models.Panpower1012Measurement.device_id)



    result = db.execute(stmt).all()

    # print(result[0])


    # Printing the data output
    for val in result:
        # print(val)
        for values in val:
            print(values.measurement_time)
        # print(user_obj.energy, user_obj.measurement_time, user_obj.client)
        # pass

    # Query filter & method to filter data from database
    values = db.query(models.Panpower1012Measurement).filter(models.Panpower1012Measurement.client == client) \
        .filter((models.Panpower1012Measurement.measurement_time >= start_date) & (models.Panpower1012Measurement.measurement_time < end_date)) \
        .group_by(models.Panpower1012Measurement.measurement_time, models.Panpower1012Measurement.device_id).all()


    # print(type(values[0]))

    db.commit()
    db.flush()
    return values


# Getting data for Energystar update from data base
# Monthly data Based on the date and client name
def energy_star_fetch_pulsedata(db: Session, client: str, start_date: str, end_date: str):

    # select where method to choose data from the data base
    stmt = select(models.PanpowerPulseMeasurement).where(models.PanpowerPulseMeasurement.client == client, models.PanpowerPulseMeasurement.measurement_time > start_date,
                                                        models.PanpowerPulseMeasurement.measurement_time <= end_date).distinct()
    result = pd.read_sql(db.execute(stmt), db.bind)

    result = result.drop_duplicates()

    print(f"====================>> Result \n\n {result}")

    # Printing the data output
    for user_obj in result:
        print(user_obj)
        # print(user_obj.energy, user_obj.measurement_time, user_obj.client)
        # pass

    # Query filter & method to filter data from database
    values = db.query(models.PanpowerPulseMeasurement).filter(models.PanpowerPulseMeasurement.client == client) \
        .filter((models.PanpowerPulseMeasurement.measurement_time > start_date) & (models.PanpowerPulseMeasurement.measurement_time <= end_date)).all()


    db.commit()
    db.flush()
    return values
