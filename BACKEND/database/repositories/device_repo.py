from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models.device import Device
from database.models.heart_rate_data import HeartRateData
from sqlalchemy import Subquery, func

def get_last_connection_devices_sq(session: Session) -> Subquery:
    # Subquery to get the most recent HR data for each device
    hr_data_sq = (
        session.query(HeartRateData.device_id, func.max(HeartRateData.timestamp).label('latest_timestamp'))
        .group_by(HeartRateData.device_id)
        .subquery()
    )
    return hr_data_sq

def get_device_by_id(session: Session, device_id: str) -> Device | None:
    return session.query(Device).filter(Device.id == device_id).first()