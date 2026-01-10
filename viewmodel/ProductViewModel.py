from sqlite3 import Connection
from decimal import Decimal
from datetime import datetime, date
from typing import Optional

from exception import InvalidFieldValueError
import db.repository.Source as Source
import db.repository.Feed as Feed
import db.repository.Unit as Unit
import db.repository.FeedProductUpdate as FeedProductUpdate
import db.repository.FeedProduct as FeedProduct


class ProductViewModel:
    def __init__(self, conn: Connection):
        self.conn = conn

    def _normalize_fields(self, feed: str, animal_type: str, source: str, size: str, unit: str,
                          brand: str, cost: str, update_date: str) -> dict:
        """Take the submitted fields and turn them into useful data types for processing. If the field is
           not valid, the field's value will be set to None."""
        feed = feed.strip().lower() if feed != '' else None
        animal_type = animal_type.strip().lower() if animal_type != '' else None
        source = source.strip().lower() if source != '' else None
        size = Decimal(size.strip()) if size != '' else None
        unit = unit.strip().lower() if unit != '' else None
        brand = brand.strip().lower() if brand != '' else None
        cost = int(Decimal(cost.strip()) * Decimal(100)) if cost != '' else None
        update_date = datetime.strptime(update_date.strip().lower(),
                                        '%Y-%m-%d').date() if update_date != '' else date.today()
        return {'feed': feed,
                'animal_type': animal_type,
                'source': source,
                'size': size,
                'unit': unit,
                'brand': brand,
                'cost': cost,
                'update_date': update_date
                }

    def _raise_invalid(self, args: dict) -> None:
        """Find the first invalid submitted field and raise an exception."""
        for key in args.keys():
            if args[key] is None:
                raise InvalidFieldValueError(field_name=key, field_value=args[key])

    def _product_update(self,
                        feed: Optional[str],
                        animal_type: Optional[str],
                        source: Optional[str],
                        size: Optional[Decimal],
                        unit: Optional[str],
                        brand: Optional[str],
                        cost: Optional[int],
                        update_date: date) -> None:
        """Update the relevant tables with the submitted fields."""
        args = {
            'feed': feed,
            'animal_type': animal_type,
            'source': source,
            'size': size,
            'unit': unit,
            'brand': brand,
            'cost': cost,
            'update_date': update_date
        }
        valid_fields = all(args.values())
        if not valid_fields:
            self._raise_invalid(args)
        source_row = Source.check_or_insert(self.conn, source)
        feed_row = Feed.check_or_insert(self.conn, feed, animal_type)
        unit_row = Unit.get_by_name_and_type(self.conn, unit, 'mass')
        feed_product_row = FeedProduct.get_or_insert(self.conn,
                                                     feed_id=feed_row.feed_id,
                                                     quantity=size,
                                                     unit_id=unit_row.unit_id,
                                                     source_id=source_row.source_id,
                                                     brand_name=brand,
                                                     cost=cost,
                                                     date_updated=update_date)
        if feed_product_row.date_updated != update_date:
            FeedProductUpdate.insert(self.conn, feed_product_row.feed_product_id, new_cost=cost,
                                     date_updated=update_date.isoformat())

    def submit_product_form(self, feed: str, animal_type: str, source: str, size: str, unit: str,
                            brand: str, cost: str, update_date: str):
        normalized_params = self._normalize_fields(feed, animal_type, source, size, unit, brand,
                                                   cost, update_date)
        with self.conn:
            self._product_update(**normalized_params)
