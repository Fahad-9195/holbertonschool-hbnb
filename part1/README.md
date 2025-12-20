# 🏠 HBnB Evolution — UML Technical Documentation (Part 1)

## 📌 Project Overview
HBnB Evolution is a simplified AirBnB-like application.  
This phase focuses on **technical documentation only**, providing a complete UML-based blueprint to guide the implementation in later parts of the project.

The application supports:
- User management
- Place listing and ownership
- Reviews
- Amenities association

---

## 🎯 Project Objectives
The goal of this phase is to:
- Design a clear layered architecture
- Model the business logic using UML
- Visualize interactions between system components
- Prepare a solid foundation for development

---

## 🧱 System Architecture (Layered Design)

### 📖 Explanation
The application follows a **three-layer architecture** to ensure separation of concerns:

- **Presentation Layer**  
  Handles API endpoints and client requests.

- **Business Logic Layer**  
  Contains domain models and business rules.  
  A **Facade pattern** is used to simplify communication with the Presentation layer.

- **Persistence Layer**  
  Responsible for storing and retrieving data from the database (implemented in later phases).

This design improves maintainability, scalability, and clarity.

### 📐 UML Package Diagram
![High-Level Package Diagram](diagrams/package_diagram.png)

---

## 🧠 Business Logic — Core Entities

### 👤 User Entity
#### 📖 Explanation
Represents application users.  
Users can be regular users or administrators and are able to manage their profiles.

**Key Responsibilities:**
- Register
- Update profile
- Delete account
- Own places
- Write reviews

---

### 🏠 Place Entity
#### 📖 Explanation
Represents properties listed by users.  
Each place belongs to one user and can include multiple amenities.

**Key Responsibilities:**
- Create, update, delete places
- Associate amenities
- Receive reviews

---

### ⭐ Review Entity
#### 📖 Explanation
Represents feedback provided by users on places they have visited.

**Key Responsibilities:**
- Create, update, delete reviews
- Link users with places

---

### 🛎️ Amenity Entity
#### 📖 Explanation
Represents features that can be associated with places (e.g., Wi-Fi, Parking).

**Key Responsibilities:**
- Create, update, delete amenities
- Associate with places

---

## 🧩 Business Logic Class Diagram

### 📖 Explanation
This class diagram illustrates:
- Core entities (`User`, `Place`, `Review`, `Amenity`)
- Their attributes and methods
- Relationships between entities

**Relationship Summary:**
- One `User` owns many `Place`
- One `User` writes many `Review`
- One `Place` has many `Review`
- `Place` and `Amenity` have a many-to-many relationship

### 📐 UML Class Diagram
![Business Logic Class Diagram](diagrams/class_diagram.png)

---

## 🔄 Sequence Diagrams (API Interactions)

Sequence diagrams show how requests move across the system:
**Client → Presentation → Business Logic → Persistence**

---

### 👤 User Registration

#### 📖 Explanation
This sequence shows how a new user is registered:
1. Client sends registration request
2. API validates input
3. Business Logic creates the user
4. Persistence layer stores the user
5. Success response is returned

#### 📐 Sequence Diagram
![User Registration Sequence](diagrams/sequence_user_registration.png)

---

### 🏠 Place Creation

#### 📖 Explanation
This sequence demonstrates how a user creates a new place:
1. Authenticated user sends create request
2. Ownership and data are validated
3. Place is stored in persistence
4. Confirmation is returned

#### 📐 Sequence Diagram
![Place Creation Sequence](diagrams/sequence_place_creation.png)

---

### ⭐ Review Submission

#### 📖 Explanation
This sequence illustrates how a user submits a review:
1. User sends review request
2. System validates user and place
3. Review is created and saved
4. Response confirms submission

#### 📐 Sequence Diagram
![Review Submission Sequence](diagrams/sequence_review_submission.png)

---

### 📋 List Places

#### 📖 Explanation
This sequence shows how a list of places is retrieved:
1. Client requests list of places
2. Business Logic fetches data
3. Persistence returns stored places
4. API sends the list to the client

#### 📐 Sequence Diagram
![List Places Sequence](diagrams/sequence_list_places.png)

---

## 📂 Repository Structure

