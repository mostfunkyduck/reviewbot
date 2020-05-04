import psycopg2
import logging

class Tag:
    def __repr__(self):
        return f"{self.name}"

    def __init__(self, **kwargs):
        self.name = kwargs["name"]

class Review:
    def __repr__(self):
        return f"{self.key}: ({self.tag or '<no tags>'}): {self.text}"

    def __init__(self, **kwargs):
        self.key    = kwargs.get("key")
        self.text   = kwargs["text"]
        self.tag    = kwargs.get("tag")


class PGDriver:
    def __init__(self, **kwargs):
        password  = kwargs["password"]
        self.conn = psycopg2.connect(f"dbname='postgres' user='postgres' host='postgres' password='{password}'")
        logging.info("connection established to database")

    def store_review(self, review):
        values = (review.text,)
        self.execute_query(f"INSERT INTO reviews (text) VALUES(%s);", values)

    def retrieve_review(self, key):
        results = self.execute_query(f"SELECT id, text, tag FROM reviews WHERE id = %s", (key,), True)
        if not results:
            logging.debug(f"retrieve_review returning None when querying for review #{key}")
            return None

        if len(results) >  1:
            raise Exception(f"uh, wth? there are multiple results for review ID #{key}, which is supposed to be a primary key!")

        return Review(
            key=results[0][0],
            text=results[0][1],
            tag=results[0][2]
        )

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

    def tag_review(self, **kwargs):
        review = kwargs["review"]
        tag = kwargs["tag"]

        self.execute_query("UPDATE reviews SET tag = %s WHERE id = %s;", (tag.name,review.key,))


    def store_tag(self, tag):
        self.execute_query("INSERT INTO tags (name) VALUES(%s);", (tag.name,))

    def retrieve_tags(self):
        results = self.execute_query("SELECT name FROM tags;", (), True)
        if not results:
            return None
        for result in results:
            yield Tag(name=result[0])

    def retrieve_tag(self, name):
        results = self.execute_query("select name from tags where name = %s", (name,), True)
        if not results:
            return None

        if len(results) > 1:
            raise Exception("hrm, got multiple results when querying for a tag named {name}, which is supposed to be a primary key")

        t = Tag(name=results[0][0])
        return t
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
