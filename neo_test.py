from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "test1234"

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("RETURN 'Connection Successful' AS message")
    print(result.single()["message"])
