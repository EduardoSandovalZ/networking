from pymongo import MongoClient

# Conectarse a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['NetScanBUAP']
collection = db['fcc']

# Consultar todos los documentos en la colección
result = collection.find()

# Contar el número de documentos
num_documentos = collection.count_documents({})

# Mostrar los resultados y el contador
print(f"Base de datos: {db.name}")
print(f"Colección: {collection.name}")
print(f"Número total de documentos en la colección: {num_documentos}")


"""
for document in result:
    print(document)
"""

