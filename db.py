import psycopg2
import logging

class Review:
    def __repr__(self):
        return f"{self.key}: {self.author}: {self.text}"

    def __init__(self, **kwargs):
        self.key    = kwargs.get("key")
        self.text   = kwargs["text"]
        self.author = kwargs["author"]


class PGDriver:
    def __init__(self, **kwargs):
        self.conn = psycopg2.connect("dbname='postgres' user='postgres' host='postgres' password='yaakov'")
        logging.info("connection established to database")

    def store_review(self, review):
        self.execute_query(f"INSERT INTO reviews (author, text) VALUES('{review.author}', '{review.text}');")

    def remove_review(self, key):
        if not key:
            raise Exception("you moron, you passed a null key to PGDriver.remove_review()")

        # if there's a problem, we're currently just spitting out the exception
        self.execute_query(f"DELETE FROM reviews WHERE id = '{key}';")

    def retrieve_reviews(self):
        results = self.execute_query(f'SELECT id, text, author FROM reviews;', True)
        logging.debug(f"retrieve_reviews results: {results}")
        for r in results:
            logging.debug(f"retrieve_reviews got record: [{r}]")
            yield Review(
                key=r[0],
                text=r[1],
                author=r[2]
            )

    def execute_query(self, query, returnResults=False):
        ret = None
        cursor = self.conn.cursor()
        cursor.execute(query)

        if returnResults and cursor.rowcount > 0:
            ret = cursor.fetchall()
        cursor.close()

        # forgot to commit initially, weird shit happens when you do that
        self.conn.commit()
        return ret
