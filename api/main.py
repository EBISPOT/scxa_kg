from fastapi import Depends, FastAPI

from .settings import Neo4jConnection, get_neo4j_conn

app = FastAPI()


@app.get("/dataset-by-cell/{cell_label}")
def get_dataset_by_cell(
    cell_label: str,
    conn: Neo4jConnection = Depends(get_neo4j_conn)
):
    """
    Query Neo4j to get dataset information based on cell ID
    """
    query = (
        f"""
        MATCH (c)-[:SUBCLASSOF*0..]->(d) WHERE d.label = '{cell_label}'
        MATCH p=(ds)-[:has_source]-(n:Cell_cluster)-[:composed_primarily_of]->(c:Class:Cell) 
        RETURN distinct n.label as author_annotion, c.label as CL_annotation, ds.download_link[0], ds.title[0], ds.publication[0]
        """
    )
    result = conn.run_cypher_query(query)

    if result:
        return result

    return {"message": "Dataset not found for the given cell ID"}
