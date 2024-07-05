from app import app, db
from server.models import Customer, Item, Review


class TestSerialization:
    '''models in models.py'''

    def test_customer_is_serializable(self):
        '''customer is serializable'''
        with app.app_context():
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()
            r = Review(comment='great!', customer=c)
            db.session.add(r)
            db.session.commit()
            customer_dict = c.to_dict()

            assert 'id' in customer_dict
            assert customer_dict['name'] == 'Phil'
            assert 'reviews' in customer_dict
            assert isinstance(customer_dict['reviews'], list)
            for review in customer_dict['reviews']:
                assert 'customer' not in review
                assert 'item' in review

    def test_item_is_serializable(self):
        '''item is serializable'''
        with app.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()
            r = Review(comment='great!', item=i)
            db.session.add(r)
            db.session.commit()

            item_dict = i.to_dict()
            assert 'id' in item_dict
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert 'reviews' in item_dict
            assert isinstance(item_dict['reviews'], list)
            for review in item_dict['reviews']:
                assert 'item' not in review
                assert 'customer' in review

    def test_review_is_serializable(self):
        '''review is serializable'''
        with app.app_context():
            c = Customer(name='Phil')
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            review_dict = r.to_dict()
            assert 'id' in review_dict
            assert 'customer' in review_dict
            assert 'item' in review_dict
            assert review_dict['comment'] == 'great!'
            assert 'reviews' not in review_dict['customer']
            assert 'reviews' not in review_dict['item']

            # Verify customer and item are correctly serialized in the review
            customer_in_review = review_dict['customer']
            item_in_review = review_dict['item']
            assert 'id' in customer_in_review
            assert 'name' in customer_in_review
            assert 'id' in item_in_review
            assert 'name' in item_in_review
            assert 'price' in item_in_review
