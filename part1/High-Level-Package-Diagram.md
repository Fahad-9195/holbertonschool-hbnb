## 📐 High-Level Package Diagram

```mermaid
classDiagram
direction TB

class "Presentation Layer (API Services)" as PL {
  APIEndpoints
  Controllers
  ApplicationServices
}

class "Business Logic Layer (Core Models)" as BL {
  HBnBFacade <<Facade>>
  User
  Place
  Review
  Amenity
  BusinessRules
}

class "Persistence Layer (Data Access)" as DAL {
  Repositories
  DAOs
  Database
}

PL --> BL : uses Facade
BL --> DAL : data operations
