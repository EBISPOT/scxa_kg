from fastapi import Depends, FastAPI

from .settings import Neo4jConnection, get_neo4j_conn

app = FastAPI()


@app.get("/datasets/cells/{cell_label}")
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
        RETURN distinct n.label as author_annotion, c.label as CL_annotation, ds.title[0] as dataset_title, ds.publication[0] as publication, ds.download_link[0] as h5ad_file 
        """
    )
    result = conn.run_cypher_query(query)

    if result:
        return result

    return {
        "message": f"Dataset not found for the given cell label {cell_label}"
    }


@app.get("/datasets/tissues/{tissue_label}")
def get_dataset_by_tissue(
    tissue_label: str,
    conn: Neo4jConnection = Depends(get_neo4j_conn)
):
    """
    Query Neo4j to get dataset information based on tissue label
    """
    query = (
        f"""
        MATCH (n:Cell_cluster)-[r:tissue]->(t)-[:SUBCLASSOF|part_of*0..]->(:Class {{label: '{tissue_label}'}})
        MATCH (ds)-[:has_source]-(n:Cell_cluster)-[:composed_primarily_of]->(c:Class:Cell)
        RETURN distinct n.label as author_annotion, t.label as tissue, ds.title[0] as dataset_title, ds.publication[0] as publication, ds.download_link[0] as h5ad_file
        """
    )
    result = conn.run_cypher_query(query)

    if result:
        return result

    return {
        "message": f"Dataset not found for the given tissue label {tissue_label}"
    }
