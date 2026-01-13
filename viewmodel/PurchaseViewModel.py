from datetime import datetime, date
from decimal import Decimal
from sqlite3 import Connection

from db.repository import AnimalType, Source, Feed, Unit, FeedProductUpdate, FeedProduct, Purchase
from exception import InvalidFieldValueError


class PurchaseViewModel:
    def __init__(self, conn: Connection):
        self.conn = conn

    def _normalize_args(self, purchase_date: str, feed: str, animal_type: str, cost: str, item_size: str, item_unit: str, source: str, brand: str, quantity: str) -> dict:
        purchase_date = datetime.strptime(purchase_date.strip().lower(), '%Y-%m-%d').date() if purchase_date != '' else date.today()
        feed = feed.strip().lower() if feed != '' else None
        animal_type = animal_type.strip().lower() if animal_type != '' else None
        cost = int(Decimal(cost.strip()) * Decimal(100)) if cost != '' else None
        item_size = Decimal(item_size.strip().lower()) if item_size != '' else None
        item_unit = item_unit.strip().lower() if item_unit != '' else None
        source = source.strip().lower() if source != '' else None
        brand = brand.strip().lower() if brand != '' else source
        quantity = int(quantity.strip().lower()) if quantity != '' else 1
        return {
            'purchase_date': purchase_date,
            'feed': feed,
            'animal_type': animal_type,
            'cost': cost,
            'item_size': item_size,
            'item_unit': item_unit,
            'source': source,
            'brand': brand,
            'quantity': quantity
        }

    def _raise_invalid(self, args: dict) -> None:
        for arg in args.keys():
            if not args[arg]:
                raise InvalidFieldValueError(field_name=arg, field_value=args[arg])

    def _submit_purchase(self, args: dict) -> None:
        valid_args = all(args.values())
        if not valid_args:
            self._raise_invalid(args)
        source_row = Source.check_or_insert(self.conn, args['source'])
        feed_row = Feed.check_or_insert(self.conn, args['feed'], args['animal_type'])
        unit_row = Unit.get_by_name_and_type(self.conn, args['item_unit'], 'mass')
        product_row = FeedProduct.get_or_insert(self.conn,
                                                feed_id=feed_row.feed_id,
                                                quantity=args['item_size'],
                                                unit_id=unit_row.unit_id,
                                                source_id=source_row.source_id,
                                                brand_name=args['brand'],
                                                cost=args['cost'],
                                                date_updated=args['purchase_date'])
        if product_row.date_updated != args['purchase_date'] and product_row.cost != args['cost']:
            FeedProductUpdate.insert(feed_product_id=product_row.feed_product_id, new_cost=args['cost'], date_updated=args['purchase_date'])
        Purchase.insert(self.conn, product_row.feed_product_id, args['quantity'], args['purchase_date'])

    def submit_form(self, purchase_date: str, feed: str, animal_type: str, cost: str, item_size: str, item_unit: str, source: str,
                    brand: str, quantity: str) -> None:
        normalized_args = self._normalize_args(purchase_date, feed, animal_type, cost, item_size, item_unit, source, brand, quantity)
        with self.conn:
            self._submit_purchase(normalized_args)

    def get_animal_types(self) -> list[str]:
        result = []
        with self.conn:
            result = AnimalType.get_all(self.conn)
        return [i.name.capitalize() for i in result]
