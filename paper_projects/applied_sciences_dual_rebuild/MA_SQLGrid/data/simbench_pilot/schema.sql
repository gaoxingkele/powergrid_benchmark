PRAGMA foreign_keys = ON;

CREATE TABLE networks (
    network_code TEXT PRIMARY KEY,
    source_dataset TEXT NOT NULL,
    scenario INTEGER NOT NULL,
    voltage_scope TEXT NOT NULL,
    settlement_type TEXT NOT NULL,
    switch_representation TEXT NOT NULL,
    base_power_mva REAL NOT NULL
);

CREATE TABLE voltage_levels (
    network_code TEXT NOT NULL,
    voltage_level_code INTEGER NOT NULL,
    nominal_kv REAL NOT NULL,
    bus_count INTEGER NOT NULL,
    PRIMARY KEY (network_code, voltage_level_code, nominal_kv),
    FOREIGN KEY (network_code) REFERENCES networks(network_code)
);

CREATE TABLE buses (
    bus_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    nominal_kv REAL NOT NULL,
    bus_type TEXT,
    subnet TEXT,
    substation TEXT,
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    min_voltage_pu REAL,
    max_voltage_pu REAL,
    FOREIGN KEY (network_code) REFERENCES networks(network_code)
);

CREATE TABLE lines (
    line_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    from_bus_id INTEGER NOT NULL,
    to_bus_id INTEGER NOT NULL,
    standard_type TEXT,
    length_km REAL NOT NULL,
    resistance_ohm_per_km REAL,
    reactance_ohm_per_km REAL,
    max_current_ka REAL,
    max_loading_percent REAL,
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (from_bus_id) REFERENCES buses(bus_id),
    FOREIGN KEY (to_bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE transformers (
    transformer_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    hv_bus_id INTEGER NOT NULL,
    lv_bus_id INTEGER NOT NULL,
    rated_power_mva REAL NOT NULL,
    hv_nominal_kv REAL NOT NULL,
    lv_nominal_kv REAL NOT NULL,
    vector_group TEXT,
    tap_position INTEGER,
    on_load_tap_changer INTEGER CHECK (on_load_tap_changer IN (0, 1)),
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (hv_bus_id) REFERENCES buses(bus_id),
    FOREIGN KEY (lv_bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE loads (
    load_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    bus_id INTEGER NOT NULL,
    active_power_mw REAL NOT NULL,
    reactive_power_mvar REAL NOT NULL,
    maximum_active_power_mw REAL,
    minimum_active_power_mw REAL,
    profile TEXT,
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE generators (
    generator_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    bus_id INTEGER NOT NULL,
    active_power_mw REAL NOT NULL,
    reactive_power_mvar REAL NOT NULL,
    rated_power_mva REAL,
    maximum_active_power_mw REAL,
    minimum_active_power_mw REAL,
    generator_type TEXT,
    physical_type TEXT,
    profile TEXT,
    controllable INTEGER CHECK (controllable IN (0, 1)),
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE switches (
    switch_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT,
    bus_id INTEGER NOT NULL,
    element_id INTEGER NOT NULL,
    element_type TEXT NOT NULL,
    switch_type TEXT,
    closed INTEGER NOT NULL CHECK (closed IN (0, 1)),
    voltage_level_code INTEGER,
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id)
);

CREATE INDEX idx_lines_from_bus ON lines(from_bus_id);
CREATE INDEX idx_lines_to_bus ON lines(to_bus_id);
CREATE INDEX idx_loads_bus ON loads(bus_id);
CREATE INDEX idx_generators_bus ON generators(bus_id);
CREATE INDEX idx_switches_bus ON switches(bus_id);
