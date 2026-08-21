PRAGMA foreign_keys = ON;
PRAGMA journal_mode = DELETE;

CREATE TABLE buses (
    bus_id INTEGER PRIMARY KEY,
    bus_name TEXT NOT NULL,
    base_kv REAL NOT NULL,
    bus_type TEXT NOT NULL,
    mw_load REAL NOT NULL,
    mvar_load REAL NOT NULL,
    area INTEGER NOT NULL,
    sub_area REAL,
    zone REAL,
    latitude REAL,
    longitude REAL
);

CREATE TABLE generators (
    generator_uid TEXT PRIMARY KEY,
    bus_id INTEGER NOT NULL REFERENCES buses(bus_id),
    generator_id TEXT NOT NULL,
    unit_group TEXT,
    unit_type TEXT NOT NULL,
    category TEXT NOT NULL,
    fuel TEXT NOT NULL,
    initial_mw REAL,
    initial_mvar REAL
);

CREATE TABLE generator_constraints (
    generator_uid TEXT PRIMARY KEY REFERENCES generators(generator_uid),
    pmax_mw REAL,
    pmin_mw REAL,
    qmax_mvar REAL,
    qmin_mvar REAL,
    min_down_time_hr REAL,
    min_up_time_hr REAL,
    ramp_rate_mw_per_min REAL,
    cold_start_time_hr REAL,
    warm_start_time_hr REAL,
    hot_start_time_hr REAL,
    forced_outage_rate REAL,
    mean_time_to_failure_hr REAL,
    mean_time_to_repair_hr REAL,
    scheduled_maintenance_weeks REAL
);

CREATE TABLE generator_costs (
    generator_uid TEXT PRIMARY KEY REFERENCES generators(generator_uid),
    fuel_price_usd_per_mmbtu REAL,
    nonfuel_start_cost_usd REAL,
    nonfuel_shutdown_cost_usd REAL,
    variable_om_source_value REAL,
    output_fraction_0 REAL,
    output_fraction_1 REAL,
    output_fraction_2 REAL,
    output_fraction_3 REAL,
    average_heat_rate_0 REAL,
    incremental_heat_rate_1 REAL,
    incremental_heat_rate_2 REAL,
    incremental_heat_rate_3 REAL
);

CREATE TABLE branches (
    branch_uid TEXT PRIMARY KEY,
    from_bus_id INTEGER NOT NULL REFERENCES buses(bus_id),
    to_bus_id INTEGER NOT NULL REFERENCES buses(bus_id),
    resistance_pu REAL NOT NULL,
    reactance_pu REAL NOT NULL,
    susceptance_pu REAL NOT NULL,
    continuous_rating_mva REAL,
    long_term_emergency_rating_mva REAL,
    short_term_emergency_rating_mva REAL,
    permanent_outage_rate REAL,
    outage_duration_hr REAL,
    transformer_ratio REAL,
    transient_outage_rate REAL,
    length_miles_source_value REAL
);

CREATE TABLE reserve_products (
    reserve_product TEXT PRIMARY KEY,
    timeframe_sec REAL,
    static_requirement_mw REAL,
    eligible_regions TEXT,
    eligible_device_categories TEXT,
    eligible_device_subcategories TEXT,
    direction TEXT
);

CREATE TABLE load_timeseries_da (
    timestamp TEXT NOT NULL,
    period INTEGER NOT NULL,
    region INTEGER NOT NULL,
    load_mw REAL NOT NULL,
    PRIMARY KEY (timestamp, region)
);

CREATE TABLE renewable_availability_da (
    timestamp TEXT NOT NULL,
    period INTEGER NOT NULL,
    generator_uid TEXT NOT NULL REFERENCES generators(generator_uid),
    resource_type TEXT NOT NULL CHECK (resource_type IN ('WIND', 'PV')),
    available_mw REAL NOT NULL,
    PRIMARY KEY (timestamp, generator_uid)
);

CREATE TABLE reserve_requirements_da (
    timestamp TEXT NOT NULL,
    period INTEGER NOT NULL,
    reserve_product TEXT NOT NULL REFERENCES reserve_products(reserve_product),
    requirement_mw REAL NOT NULL,
    PRIMARY KEY (timestamp, reserve_product)
);

CREATE TABLE dispatch_da (
    timestamp TEXT NOT NULL,
    generator_uid TEXT NOT NULL REFERENCES generators(generator_uid),
    generation_mw REAL NOT NULL,
    committed INTEGER NOT NULL CHECK (committed IN (0, 1)),
    production_cost_value REAL NOT NULL,
    transmission_scenario TEXT NOT NULL CHECK (transmission_scenario = 'allTX'),
    PRIMARY KEY (timestamp, generator_uid, transmission_scenario)
);

CREATE INDEX idx_generators_fuel ON generators(fuel);
CREATE INDEX idx_generators_bus ON generators(bus_id);
CREATE INDEX idx_constraints_pmax ON generator_constraints(pmax_mw);
CREATE INDEX idx_branches_from_to ON branches(from_bus_id, to_bus_id);
CREATE INDEX idx_load_time ON load_timeseries_da(timestamp);
CREATE INDEX idx_renewable_time_type ON renewable_availability_da(timestamp, resource_type);
CREATE INDEX idx_dispatch_generator_time ON dispatch_da(generator_uid, timestamp);
CREATE INDEX idx_dispatch_time_generation ON dispatch_da(timestamp, generation_mw DESC);
