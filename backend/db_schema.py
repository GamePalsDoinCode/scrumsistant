from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()

Users = Table(
    'Users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('display_name', String),
    Column('password', String),
)
