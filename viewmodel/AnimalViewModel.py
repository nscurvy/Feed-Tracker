from sqlite3 import Connection
from datetime import datetime, date
from typing import Optional


import db.repository.AnimalType as at
from db.repository.AnimalType import AnimalType
import db.repository.AnimalPopulation
from db.repository.AnimalPopulation import AnimalPopulation
import db.repository.AnimalPopulationUpdate as apu
from db.repository.AnimalPopulationUpdate import AnimalPopulationUpdate


class AnimalViewModel:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def update_animal(self, animal_name: str, delta: int, date_of_change: str, reason: Optional[str]):
        animal_name = animal_name.lower()
        date_of_change = datetime.strptime(date_of_change, '%Y-%m-%d').date()
        candidate = at.get_by_name(self.conn, animal_name)
        if candidate is None:
            new_id = at.insert_new(self.conn, animal_name)
            candidate = AnimalType(new_id, animal_name)
        apu.insert_update(conn=self.conn,
                          animal_type_id=candidate.animal_type_id,
                          delta=delta,
                          date_updated=date_of_change,
                          reason=reason)
        self.conn.commit()