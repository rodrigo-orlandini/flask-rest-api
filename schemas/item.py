from marsh import marshmallow
from models.item import ItemModel
from models.store import StoreModel

class ItemSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        model = ItemModel
        load_only: ("store",)
        dump_only: ("id",)
        load_instance = True
        include_fk = True