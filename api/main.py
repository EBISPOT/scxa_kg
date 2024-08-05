from fastapi import FastAPI
from neo4j import GraphDatabase

app = FastAPI()
graph = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))


@app.get("/dataset-by-cell/{cell_id}")
def get_dataset_by_cell(cell_id: str):
    """
    Query Neo4j to get dataset information based on cell ID
    """
    query = (
        f"MATCH (c:Cell {{id: '{cell_id}'}})-[:BELONGS_TO]->(d:Dataset) RETURN d"
    )
    result = graph.run(query).data()

    if result:
        return result[0]['d']

    return {"message": "Dataset not found for the given cell ID"}
