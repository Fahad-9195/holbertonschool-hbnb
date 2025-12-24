# holbertonschool-hbnb

HBnB Evolution is a simplified AirBnB-like application built using a layered architecture (Presentation → Business Logic → Persistence) and a Facade pattern to unify access to core use-cases.

This repository contains the technical documentation for **Part 1** (UML design) and will later include the implementation parts.

---

## Project Structure

```text
holbertonschool-hbnb/
└── part1/
    ├── README.md
    └── diagrams/
        ├── 0_package_diagram.png
        ├── 1_class_diagram.png
        ├── 2_1_user_registration.png
        ├── 2_2_place_creation.png
        ├── 2_3_review_submission.png
        └── 2_4_fetch_places.png
```
## Part 1: Technical Documentation (UML)
Objectives

Design the high-level architecture (3-layer system).

Define the Business Logic classes (User, Place, Review, Amenity).

Show sequence diagrams for key API calls.

Compile all into a clear documentation guide for implementation.

## 0. High-Level Package Diagram

Goal: Illustrate the three-layer architecture and how layers communicate via the Facade pattern.

Diagram:


Notes:

Presentation Layer: API endpoints, DTO validation, request/response handling.

Business Logic Layer: domain models + rules + HBnBFacade.

Persistence Layer: repositories/DAO + database operations (implemented in Part 3).

The Facade provides a single interface to use-cases and reduces coupling.

## 1. Detailed Class Diagram (Business Logic Layer)

Goal: Model the core entities, attributes, methods, and relationships.

Diagram:


Key Concepts:

Every entity has:

id (UUID4)

created_at

updated_at

Relationships:

User owns many Place

User writes many Review

Place has many Review

Place includes many Amenity (many-to-many)

## 2. Sequence Diagrams (API Calls)

These diagrams show the flow across:
Client → Presentation → HBnBFacade → Persistence → Database

2.1 User Registration — POST /users

Flow Summary:

Validate request DTO.

Check email uniqueness.

Hash password and create user.

Save user and return 201 Created.

If email exists → 409 Conflict.

2.2 Place Creation — POST /places

Flow Summary:

Validate request DTO.

Verify owner exists.

Validate place fields (price, lat, long).

Validate amenities (optional).

Save place + link amenities → 201 Created.

Invalid owner → 404 Not Found.

2.3 Review Submission — POST /places/{id}/reviews

Flow Summary:

Validate request DTO.

Verify user exists.

Verify place exists.

Validate rating (1..5).

Save review → 201 Created.

Invalid rating → 400 Bad Request.

Place not found → 404 Not Found.

2.4 Fetching a List of Places — GET /places

Flow Summary:

Parse and validate query filters.

Facade validates filters.

Repository performs search.

Return 200 OK with list.

Bad filters → 400 Bad Request.

Implementation Notes (Next Parts)

## Part 2 will implement the core logic and API endpoints.

Part 3 will add database persistence and repositories.

Requirements

Use UML notation for diagrams.

Ensure separation of concerns between layers.

Follow clean architecture style:

Controllers are thin

Business rules live in domain layer

Persistence is accessed via repositories
