from pymongo import MongoClient

def copy_collection(source_db, source_collection, dest_db, dest_collection):
    # Conectar a la base de datos de origen
    source_client = MongoClient('mongodb://localhost:27017/')
    source_db = source_client[source_db]
    source_collection = source_db[source_collection]

    # Conectar a la base de datos de destino
    dest_client = MongoClient('mongodb://localhost:27017/')
    dest_db = dest_client[dest_db]
    dest_collection = dest_db[dest_collection]

    # Obtener todos los documentos de la colección de origen
    documents = source_collection.find()

    # Insertar los documentos en la colección de destino
    for doc in documents:
        # Eliminar el campo '_id' antes de insertar
        doc.pop('_id', None)
        dest_collection.insert_one(doc)

    # Obtener el número de documentos copiados
    num_documents_copied = dest_collection.count_documents({})

    print(f"Se copiaron {num_documents_copied} documentos de {source_collection.name} a {dest_collection.name}.")

    # Cerrar las conexiones
    source_client.close()
    dest_client.close()

# Especifica los nombres de las bases de datos y colecciones
source_database = 'Testing'
source_collection = 'testing'
destination_database = 'NetScanBUAP'
destination_collection = 'fcc'

# Llama a la función para copiar la colección
copy_collection(source_database, source_collection, destination_database, destination_collection)
