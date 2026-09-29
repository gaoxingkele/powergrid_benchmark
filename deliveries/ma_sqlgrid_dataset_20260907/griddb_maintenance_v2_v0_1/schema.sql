DROP TABLE IF EXISTS grid_topology;
DROP TABLE IF EXISTS sensor_readings;
DROP TABLE IF EXISTS maintenance_logs;
DROP TABLE IF EXISTS work_orders;
DROP TABLE IF EXISTS technicians;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS asset_types;

CREATE TABLE asset_types (
    asset_type_id INTEGER PRIMARY KEY,
    type_name TEXT NOT NULL,
    voltage_class TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    expected_lifetime_years INTEGER NOT NULL
);

CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY,
    location_name TEXT NOT NULL,
    region TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    criticality TEXT NOT NULL
);

CREATE TABLE assets (
    asset_id INTEGER PRIMARY KEY,
    asset_name TEXT NOT NULL,
    asset_type_id INTEGER NOT NULL REFERENCES asset_types(asset_type_id),
    location_id INTEGER NOT NULL REFERENCES locations(location_id),
    install_date TEXT NOT NULL,
    status TEXT NOT NULL,
    capacity_mw REAL NOT NULL
);

CREATE TABLE technicians (
    technician_id INTEGER PRIMARY KEY,
    technician_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    home_region TEXT NOT NULL,
    active INTEGER NOT NULL
);

CREATE TABLE work_orders (
    work_order_id INTEGER PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    assigned_technician_id INTEGER NOT NULL REFERENCES technicians(technician_id),
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    scheduled_date TEXT NOT NULL,
    completed_date TEXT,
    fault_code TEXT NOT NULL
);

CREATE TABLE maintenance_logs (
    log_id INTEGER PRIMARY KEY,
    work_order_id INTEGER NOT NULL REFERENCES work_orders(work_order_id),
    technician_id INTEGER NOT NULL REFERENCES technicians(technician_id),
    action_type TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT NOT NULL,
    notes TEXT NOT NULL,
    parts_cost REAL NOT NULL
);

CREATE TABLE sensor_readings (
    reading_id INTEGER PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    reading_time TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    reading_value REAL NOT NULL,
    unit TEXT NOT NULL,
    alarm_flag INTEGER NOT NULL
);

CREATE TABLE grid_topology (
    edge_id INTEGER PRIMARY KEY,
    upstream_asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    downstream_asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    connection_type TEXT NOT NULL,
    switch_status TEXT NOT NULL
);
