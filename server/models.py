from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship("Review", back_populates="customer");
    
    #varname = association_proxy('relattribute', 'classnamelowercase',
    #                             creator=lambda classnamelowercase_obj: ClassNameTransition(relattributeintransclass=classnamelowercase_obj))
    
    items = association_proxy('reviews', 'item', creator=lambda item_obj: Review(item=item_obj))

    serialize_rules = ('-reviews.customer',);

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship("Review", back_populates="item");

    #varname = association_proxy('relattribute', 'classnamelowercase',
    #                             creator=lambda classnamelowercase_obj: ClassNameTransition(relattributeintransclass=classnamelowercase_obj))
    customers = association_proxy('reviews', 'customer',
                                 creator=lambda customer_obj: Review(customer=customer_obj));
    
    serialize_rules = ('-reviews.item',);

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews";

    id = db.Column(db.Integer, primary_key=True);
    comment = db.Column(db.String);
    
    #db.Column('colname', DataType, db.ForeignKey('dbtablename.colname'));#example only
    #colname = db.Column(DataType, db.ForeignKey('dbtablename.colname'));#example only
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'));
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'));
    
    #varname = db.relationship("ClassName", back_populates="correspondingattribute");#example only
    customer = db.relationship("Customer", back_populates="reviews");
    item = db.relationship("Item", back_populates="reviews");

    serialize_rules = ('-item.reviews', '-customer.reviews');
