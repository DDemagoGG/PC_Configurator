from repository.connection import Connector

user_connector = Connector(
    username="regular_user",
    password="pswd",
    database_name="NadoPC",
    host="postgres",
    port=5432,
)

admin_connector = Connector(
    username="admin",
    password="pswd",
    database_name="NadoPC",
    host="postgres",
    port=5432,
)

shop_connector = Connector(
    username="shop", password="pswd", database_name="NadoPC", host="postgres", port=5432
)
