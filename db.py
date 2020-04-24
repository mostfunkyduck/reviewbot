import psycopg2
import logging

class PGDriver:
    def __init__(self, **kwargs):
        self.conn = psycopg2.connect("dbname='postgres' user='postgres' host='postgres' password='yaakov'")
        logging.info("connection established to database")

    def store_review(self, **kwargs):
        reviewtext=kwargs["reviewtext"]
        self.execute_query(f"INSERT INTO reviews VALUES('{reviewtext}');")

    def retrieve_reviews(self, **kwargs):
        return self.execute_query(f'SELECT reviewtext FROM reviews;', True)

    def execute_query(self, query, returnresults=False):
        cursor = self.conn.cursor()
        logging.debug( str(self.conn.get_dsn_parameters()))
        cursor.execute(query)
        logging.debug(str(cursor))
        if returnresults and cursor.rowcount > 0:
            record = cursor.fetchall()
            return record
