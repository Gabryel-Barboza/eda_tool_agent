from langchain.utilities import SQLDatabase

from src.settings import settings

db = SQLDatabase.from_uri(settings.database_uri)


async def get_db():
    return db


def init_db():
    db.run("""CREATE TABLE IF NOT EXISTS charts(
    uuid VARCHAR(36) PRIMARY KEY,
    graph_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
           """)


async def get_graph_db(graph_id: str):
    return db.run(
        'SELECT graph_json FROM charts WHERE uuid = :graph_id',
        parameters={'graph_id': graph_id},
    )


def insert_graphs_db(graph_id: str, graph_json: str):
    db.run(
        'INSERT INTO charts ("uuid", "graph_json") VALUES (":graph_id", ":graph_json")',
        parameters={'graph_id': graph_id, 'graph_json': graph_json},
    )
