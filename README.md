# Logistics Routing Engine

This project simulates constrained last-mile delivery for 40 packages across 3 trucks using a deterministic nearest-neighbor route planner and a fixed speed/time model.

It is implemented in pure Python with no third-party dependencies and is designed to make algorithmic decisions transparent and auditable.

## What it does

- Loads package metadata and a symmetric distance matrix from CSV.
- Applies business constraints during load planning:
- delayed package availability windows
- truck-specific assignment rules
- bundled package delivery groups
- corrected address availability at a specific timestamp (Package 9 at 10:20 AM)
- Builds routes with a greedy nearest-neighbor heuristic.
- Simulates travel time and mileage at 18 MPH.
- Tracks package state as a function of time (`At hub`, `DELAYED`, `En route`, `Delivered`).
- Exposes a CLI to query all packages, a single package, and truck-level mileage summaries at any timestamp.

## Core design

### Data model

- `Package` ([package.py](/Users/Anyone/Desktop/logistics-routing-engine/package.py))
- Immutable source fields: id, address, city, zip, deadline, weight, special notes.
- Mutable simulation fields: status, delivery timestamp, assigned truck.

- `Truck` ([truck.py](/Users/Anyone/Desktop/logistics-routing-engine/truck.py))
- Capacity: 16 packages.
- Speed: 18 MPH.
- Tracks current location, elapsed time (minutes since midnight), mileage, and loaded packages.

- `DistanceTable` ([distance.py](/Users/Anyone/Desktop/logistics-routing-engine/distance.py))
- Address normalization for matching package addresses to matrix entries.
- Handles half-filled triangular matrix by reading `d[i][j]` first, then `d[j][i]` fallback.

- `PackageStore` ([hash_table.py](/Users/Anyone/Desktop/logistics-routing-engine/hash_table.py))
- Separate-chaining hash table with modulo bucketing.
- Included for O(1) average lookup by package ID when needed by extensions.

### Pipeline

1. Read package and distance CSV input ([loader.py](/Users/Anyone/Desktop/logistics-routing-engine/loader.py)).
2. Initialize trucks at staggered starts:
- Truck 1: 8:00 AM
- Truck 2: 9:05 AM
- Truck 3: 10:20 AM
3. Assign packages using constraint-aware loading order:
- delayed arrivals first
- truck-only packages
- bundled groups
- early-deadline packages
- remaining fill strategy
4. Execute routes per truck using nearest-neighbor selection.
5. Return each truck to hub and compute total mileage.
6. Answer time-based status queries through CLI.

## Routing and constraints

The route loop in [main.py](/Users/Anyone/Desktop/logistics-routing-engine/main.py):

- Selects the next stop by minimum distance from current truck location.
- Skips Package 9 until 10:20 AM when its corrected address becomes available.
- Delivers all packages for the current address in one stop.
- Returns truck to hub after assigned set is completed.

Constraint helpers include:

- `available_at_minutes(...)` for delayed depot arrival parsing.
- `is_truck2_only(...)` for truck-specific rules.
- `bundle_ids(...)` for "must be delivered with" groups.
- `correct_package_9(...)` for mid-run data correction.

## Complexity

Let `n` be number of packages loaded onto a truck.

- Nearest-neighbor route construction: `O(n^2)` worst case per truck.
- Delivery status/report generation: `O(P)` where `P` is total package count.
- Distance lookup: `O(1)` average via indexed matrix access.

For this dataset (`P=40`), runtime is effectively instantaneous on local execution.

## Running locally

```bash
python3 main.py
```

Menu options:

- `1`: status of all packages at a provided time
- `2`: status of one package at a provided time
- `3`: truck summaries and total mileage
- `0`: exit

## Verified baseline output (current implementation)

Execution date: March 2, 2026

- Packages loaded: 40
- Total mileage: 118.9 miles
- Deadline misses: 0

Truck breakdown from current run:

- Truck 1: 40.2 miles, return 10:14 AM
- Truck 2: 47.6 miles, return 11:44 AM
- Truck 3: 31.1 miles, return 12:04 PM

## Repository layout

- [main.py](/Users/Anyone/Desktop/logistics-routing-engine/main.py): orchestration, routing, scheduling rules, CLI
- [loader.py](/Users/Anyone/Desktop/logistics-routing-engine/loader.py): CSV ingestion and normalization
- [distance.py](/Users/Anyone/Desktop/logistics-routing-engine/distance.py): distance matrix abstraction
- [truck.py](/Users/Anyone/Desktop/logistics-routing-engine/truck.py): truck simulation primitives
- [package.py](/Users/Anyone/Desktop/logistics-routing-engine/package.py): package entity model
- [hash_table.py](/Users/Anyone/Desktop/logistics-routing-engine/hash_table.py): custom hash table
- `data/`: source datasets (`packages.csv`, `distances.csv`)

## Extension points

- Replace nearest-neighbor with 2-opt or metaheuristics for route quality improvements.
- Add a true event queue for time-dependent state transitions.
- Add unit tests around constraint parsing and deadline verification.
- Track route traces per truck for post-run analytics and visualization.
