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
The application follows a three-layer architecture to ensure separation of concerns:

- **Presentation Layer**  
  Handles API endpoints and client requests.

- **Business Logic Layer**  
  Contains domain models and business rules.  
  A **Facade** pattern is used to simplify communication with the Presentation layer.

- **Persistence Layer**  
  Responsible for storing and retrieving data from the database (implemented in later phases).

This design improves maintainability, scalability, and clarity.

### 📐 UML Package Diagram
<img width="366" height="353" alt="image" src="https://github.com/user-attachments/assets/73237c23-a736-41f3-8d83-d72c95d216cf" />


---

## 🧠 Business Logic — Core Entities

### 👤 User Entity
#### 📖 Explanation
Represents application users. Users can be regular users or administrators and are able to manage their profiles.

**Key Responsibilities:**
- Register
- Update profile
- Delete account
- Own places
- Write reviews

### 🏠 Place Entity
#### 📖 Explanation
Represents properties listed by users. Each place belongs to one user and can include multiple amenities.

**Key Responsibilities:**
- Create, update, delete places
- Associate amenities
- Receive reviews

### ⭐ Review Entity
#### 📖 Explanation
Represents feedback provided by users on places they have visited.

**Key Responsibilities:**
- Create, update, delete reviews
- Link users with places

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
- Core entities (**User**, **Place**, **Review**, **Amenity**)
- Their attributes and methods
- Relationships between entities

**Relationship Summary:**
- One **User** owns many **Place**
- One **User** writes many **Review**
- One **Place** has many **Review**
- **Place** and **Amenity** have a many-to-many relationship

### 📐 UML Class Diagram
<img width="524" height="502" alt="image" src="https://github.com/user-attachments/assets/38056a1e-93f1-487d-a21d-b9e3c3e6eaf8" />

---

## 🔄 Sequence Diagrams (API Interactions)
Sequence diagrams show how requests move across the system:  
**Client → Presentation → Business Logic → Persistence**

### 👤 User Registration
#### 📖 Explanation
This sequence shows how a new user is registered:
1. Client sends registration request
2. API validates input
3. Business Logic creates the user
4. Persistence layer stores the user
5. Success response is returned

#### 📐 Sequence Diagram
<img width="525" height="496" alt="image" src="https://github.com/user-attachments/assets/fc35b927-7100-4c6b-bfc7-861469547377" />

---

### 🏠 Place Creation
#### 📖 Explanation
This sequence demonstrates how a user creates a new place:
1. Authenticated user sends create request
2. Ownership and data are validated
3. Place is stored in persistence
4. Confirmation is returned

#### 📐 Sequence Diagram
<img width="525" height="496" alt="image" src="https://github.com/user-attachments/assets/4cef88bc-9b3e-42a1-b800-53cb300f4718" />

---

### ⭐ Review Submission
#### 📖 Explanation
This sequence illustrates how a user submits a review:
1. User sends review request
2. System validates user and place
3. Review is created and saved
4. Response confirms submission

#### 📐 Sequence Diagram
<img width="525" height="453" alt="image" src="https://github.com/user-attachments/assets/d96413b3-f0eb-40f2-888e-616eb61079ee" />

---

### 📋 List Places
#### 📖 Explanation
This sequence shows how a list of places is retrieved:
1. Client requests list of places
2. Business Logic fetches data
3. Persistence returns stored places
4. API sends the list to the client

#### 📐 Sequence Diagram
<img width="525" height="453" alt="image" src="https://github.com/user-attachments/assets/695209b6-89eb-4bd2-bd68-7154c67d166d" />

---

## 📂 Repository Structure
```text
holbertonschool-hbnb/
└── part1/
    ├── README.md
    └── diagrams/
        ├── package_diagram.png
        ├── class_diagram.png
        ├── sequence_user_registration.png
        ├── sequence_place_creation.png
        ├── sequence_review_submission.png
        └── sequence_list_places.png
