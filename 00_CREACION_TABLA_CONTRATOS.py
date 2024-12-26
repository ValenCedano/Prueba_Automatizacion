import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('database_contratos.sqlite')
cursor = conn.cursor()

# Eliminar la tabla si ya existe (para sobreescribirla)
cursor.execute('DROP TABLE IF EXISTS contract')

# Creación de la tabla contratos
cursor.execute('''
CREATE TABLE contract (
    commerce_id TEXT,     
    contract_type TEXT,
    commission_value INTEGER,
    successful_requests_start_range INTEGER,
    successful_requests_end_range INTEGER,
    discount_available INTEGER CHECK (discount_available IN (0, 1)),
    unsuccessful_requests_start_range INTEGER,
    unsuccessful_requests_end_range INTEGER,
    discount_value FLOAT,
    iva_value REAL DEFAULT 0.19
);
''')


# Valores de los datos a insertar en la tabla contract
datos_contratos = [
    ('KaSn-4LHo-m6vC-I4PU', 'Fijo', 300, None,None, 0, None, None, None, 0.19),
    ('Vj9W-c4Pm-ja0X-fC1C', 'Variable', 250, 0, 10000, 0, None, None, None, 0.19),
    ('Vj9W-c4Pm-ja0X-fC1C', 'Variable', 200, 10001, 20000, 0, None, None, None, 0.19),
    ('Vj9W-c4Pm-ja0X-fC1C', 'Variable', 170, 20002, None, 0, None, None, None, 0.19),
    ('Rh2k-J1o7-zndZ-cOo8', 'Fijo', 600, None, None, 0, None, None, None, 0.19),
    ('3VYd-4lzT-mTC3-DQN5', 'Variable', 250, 0, 22000, 1, 6001, None, 0.05, 0.19),
    ('3VYd-4lzT-mTC3-DQN5', 'Variable', 130, 22002, None, 1, 6001, None, 0.05, 0.19),
    ('GdEQ-MGb7-LXHa-y6cd', 'Fijo', 300, None, None, 1, 2500, 4500, 0.05, 0.19),
    ('GdEQ-MGb7-LXHa-y6cd', 'Fijo', 300, None, None, 1, 4502, None, 0.08, 0.19)
]

cursor.executemany("INSERT INTO contract VALUES (?,?,?,?,?,?,?,?,?,?)", datos_contratos)

# Confirmar y cerrar la conexión
conn.commit()
conn.close()

print("Datos insertados y tabla creada correctamente.")