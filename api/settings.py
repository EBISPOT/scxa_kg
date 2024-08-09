"""
Settings API module
"""
from functools import lru_cache

from neo4j import GraphDatabase, Session
from pydantic import Field
from pydantic_settings import BaseSettings


class Neo4jConnection:
    """
    Neo4j connection class
    """
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """
        Close the connection
        """
        self._driver.close()

    def get_session(self) -> Session:
        """
        Get the session
        """
        return self._driver.session()

    def run_cypher_query(self, query, parameters=None):
        """
        Run a Cypher query
        """
        with self.get_session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]


class Settings(BaseSettings):
    """
    Neo4j connection settings
    """
    neo4j_uri: str = Field(..., env="NEO4J_URI")
    neo4j_user: str = Field(..., env="NEO4J_USER")
    neo4j_password: str = Field(..., env="NEO4J_PASSWORD")


@lru_cache
def get_settings() -> Settings:
    """
    Get the settings from environment variables
    """
    return Settings()


# Initialize the Neo4j connection
@lru_cache
def get_neo4j_conn():
    """
    Get the Neo4j connection
    """
    settings = get_settings()

    neo4j_conn = Neo4jConnection(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )
    return neo4j_conn
