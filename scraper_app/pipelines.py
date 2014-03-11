from sqlalchemy.orm import sessionmaker
from models import Template, db_connect, create_table


class WrapBootstrapPipeline(object):
    """Wrapbootstrap pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()

        # Popping out the empty strings
        temp = item.copy()
        for k, v in temp.iteritems():
            if not v:
                item.pop(k)

        deal = Template(**item)

        try:
            session.add(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
