## 2. Sequence Diagrams for API Calls

This section illustrates the interaction flow between the Presentation Layer, Business Logic Layer (Facade), and Persistence Layer for the main API use cases of the HBnB Evolution application.

The purpose of these sequence diagrams is to clearly show how requests are processed step-by-step across the system layers.

## 2.1 User Registration — POST /users
Description

A new user registers by submitting personal information. The system validates the input, checks for duplicate emails, hashes the password, and stores the user.

Flow Summary

Client sends registration request to API.

API validates input and forwards to HBnBFacade.

Facade checks email uniqueness and password rules.

User is saved via the UserRepository.

A success response is returned.

<img width="500" height="500" alt="58ded749-c86d-4b53-a62b-c534221da977" src="https://github.com/user-attachments/assets/77a6ea0f-8cf4-4465-a253-7473102dc12c" />

## 2.2 Place Creation — POST /places
Description

A user creates a new place listing and optionally attaches amenities.

Flow Summary

Client submits place data to API.

API forwards request to Facade.

Facade verifies owner exists and validates fields.

Place is saved and amenities are linked.

Created place is returned.

<img width="500" height="500" alt="f7e0e7d5-76ac-4802-8883-19b0ed5d603f" src="https://github.com/user-attachments/assets/46bda90c-d63f-4323-bbe7-8caeb2bae155" />

## 2.3 Review Submission — POST /places/{id}/reviews
Description

A user submits a review for a specific place.

Flow Summary

Client sends review request.

API passes it to the Facade.

Facade checks that user and place exist and rating is valid.

Review is saved.

Success response is returned.

<img width="500" height="500" alt="1a429375-84f5-4a54-8b52-8006b51483f5" src="https://github.com/user-attachments/assets/00486f2f-e1f4-4258-932b-1bf1eec8e1f8" />

## 2.4 Fetching a List of Places — GET /places
Description

A user requests a list of places using optional filters (price, location, amenities).

Flow Summary

Client sends query request.

API parses and validates filters.

Facade validates filters and queries repository.

Matching places are returned to client.

<img width="500" height="500" alt="c178ca6b-9ef5-44a1-811c-200633204b76" src="https://github.com/user-attachments/assets/7175af0c-d988-4ff3-a0fc-68d10a20ef37" />

## Summary
API Call	Purpose
POST /users	Register a new user
POST /places	Create a new place
POST /places/{id}/reviews	Add a review
GET /places	Retrieve list of places

These sequence diagrams demonstrate a clean separation of responsibilities:

Presentation handles requests and validation.

Business Logic (Facade) applies rules and orchestrates operations.

Persistence manages data storage.


