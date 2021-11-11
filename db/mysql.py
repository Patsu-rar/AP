from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, Query, Session


class MySQL:
    def __init__(self, user, password, host, port, db_name):
        conn_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        self.__engine = create_engine(conn_string)
        self.__engine.connect()
        self.__db_name = db_name
        self.__session: Session = sessionmaker(bind=self.__engine)()

        self.__metadata = MetaData(bind=self.__engine)
        self.__metadata.reflect(bind=self.__engine)

    @property
    def session(self):
        return self.__session

    @property
    def metadata(self):
        return self.__metadata

    @property
    def query(self):
        return self.session.query

    @property
    def tables(self):
        return self.metadata.tables

    def select(self, table_model, where=None):
        table_obj = table_model.__table__
        if where is None:
            res = self.query(table_obj).all()
        else:
            res = list(self.query(table_obj).filter(where).all())

        return [dict(zip(table_obj.columns.keys(), row)) for row in res]

    def insert(self, table_model, **values):
        row = table_model(**values)
        self.session.add(row)
        self.session.commit()

    def update(self, table_model, id, **new_values):
        table_obj: Table = table_model.__table__
        stmt = table_obj.update().where(table_obj.columns[0] == id).values(**new_values)
        self.session.execute(stmt)
        self.session.commit()

    def delete(self, table_model, id):
        table_obj: Table = self.tables.get(table_model.__tablename__)
        del_obj = table_obj.delete(table_obj.columns[0] == id)
        self.session.execute(del_obj)
        self.session.commit()

    def check_if_record_in_db(self, table_model, id):
        table_obj: Table = table_model.__table__
        exists = self.session.query(table_obj).filter(table_obj.columns[0] == id).all()
        return True if exists else False

    def truncate(self, table_model):
        table_name = table_model.__name__
        self.session.execute("SET FOREIGN_KEY_CHECKS=0;")
        self.session.execute(f"truncate table {self.__db_name}.{table_name};")
        self.session.execute("SET FOREIGN_KEY_CHECKS=1;")
        self.session.commit()

    def __del__(self):
        self.session.close()
