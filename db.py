import psycopg2
import logging

class Review:
    def __repr__(self):
        return f"{self.key}: ({self.tag}): {self.text}"

    def __init__(self, **kwargs):
        self.key    = kwargs.get("key")
        self.text   = kwargs["text"]
        self.tag    = kwargs["tag"]


class PGDriver:
    def __init__(self, **kwargs):
        password  = kwargs["password"]
        self.conn = psycopg2.connect(f"dbname='postgres' user='postgres' host='postgres' password='{password}'")
        logging.info("connection established to database")

    def store_review(self, review):
        values = (review.tag, review.text)
        self.execute_query(f"INSERT INTO reviews (tag, text) VALUES(%s, %s);", values)

    def remove_review(self, key):
        if not key:
            raise Exception("you moron, you passed a null key to PGDriver.remove_review()")

        # if there's a problem, we're currently just spitting out the exception
        self.execute_query(f"DELETE FROM reviews WHERE id = %s;", (key))

    def retrieve_reviews(self, tag=None):
        query = "SELECT id, text, tag FROM reviews"
        values = ()
        if tag:
            query = query + f" WHERE tag = %s"
            values = (tag,)
        query = query + ";"
        results = self.execute_query(query, values, True)
        if not results:
            logging.debug(f"retrieve_reviews returning None")
            return None

        for r in results:
            logging.debug(f"retrieve_reviews got record: [{r}]")
            yield Review(
                key=r[0],
                text=r[1],
                tag=r[2]
            )

    def execute_query(self, query, values, returnResults=False):
        ret = None
        cursor = self.conn.cursor()
        logging.debug(f"executing query: [{query}] with values [{values}]")
        cursor.execute(query, values)

        if returnResults and cursor.rowcount > 0:
            ret = cursor.fetchall()
        cursor.close()

        # forgot to commit initially, weird shit happens when you do that
        self.conn.commit()
        logging.debug(f"query completed, returning [{ret}]") 
        return ret
