from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table

metadata = MetaData()

Users = Table(
    'Users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True,),
    Column('email', String, nullable=False),
    Column('display_name', String),
    Column('password', String),
    Column('is_PM', Boolean, default=False),
)
