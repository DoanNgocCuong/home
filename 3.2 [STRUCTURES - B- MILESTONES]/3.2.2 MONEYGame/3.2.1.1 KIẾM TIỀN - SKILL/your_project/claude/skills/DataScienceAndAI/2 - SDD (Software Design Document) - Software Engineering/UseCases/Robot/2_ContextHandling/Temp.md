# TECHNICAL SPECIFICATION: FRIENDSHIP LEVEL UPDATE (OPTION 2)

## 1. Overview

This document details the technical implementation for **Option 2** of the Friendship Level update mechanism. In this approach, the Backend (BE) service calculates and provides the `engage_day` metric, while the AI/Context Service retains the responsibility of applying the business logic to determine and update the user's `friendship_level` based on the received `engage_day`.

This design maintains the AI/Context Service as the single source of truth for the core context state (`friendship_level`), but introduces a dependency on the BE for the primary input metric (`engage_day`).

## 2. Goal, Scope, and User Story

### 2.1 Goal
To establish a reliable, asynchronous API endpoint that allows the Main Backend Service to update a user's `engage_day` metric, triggering the AI/Context Service to recalculate and persist the corresponding `friendship_level`.

### 2.2 Scope
- **In Scope:** Defining the API contract, updating the `friendship_status` data model, and implementing the level calculation logic within the AI/Context Service.
- **Out of Scope:** The internal logic of how the Main Backend Service calculates the `engage_day` (e.g., "70% of todo list completion").

### 2.3 User Story
As a **System Administrator**, I want the **Main Backend Service** to automatically calculate and send the user's `engage_day` to the **AI/Context Service** every night, so that the user's **Friendship Level** is correctly updated based on the new engagement metric, ensuring the next day's Agent Selection is accurate.

## 3. Architecture & Flow

The process involves a scheduled nightly job on the Main Backend Service and a dedicated API endpoint on the AI/Context Service.

### 3.1 Flow Diagram

![Architecture Flow Diagram for Option 2](https://private-us-east-1.manuscdn.com/sessionFile/e6qGLhxx4QzoIGiYLyk7qp/sandbox/iz7sTcuFm4qm6Td28BNSvJ-images_1765245952772_na1fn_L2hvbWUvdWJ1bnR1L29wdGlvbl8yX2FyY2hpdGVjdHVyZQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvZTZxR0xoeHg0UXpvSUdpWUx5azdxcC9zYW5kYm94L2l6N3NUY3VGbTRxbTZUZDI4Qk5TdkotaW1hZ2VzXzE3NjUyNDU5NTI3NzJfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyOXdkR2x2Ymw4eVgyRnlZMmhwZEdWamRIVnlaUS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=oqQ5sTqbZ4-pHyfBKEpPLJGNCuR-j7OUeXSI7foBvMiHtAXpnh6~7iQF9PaEIELZq38gXjtP43DL4bu-MrbErqqW~fUO~CW9go4LmOQ0wbO1VTMyKNFBrd0M25ja5PD1QlBBAWXhiTTnW6UGBsaNnL2qnhbqXMYgGlBm9QDxBDJfpHb3TaNuIvRS46av5q0x1bz9fsR-whasumOdkqenjBX8bImb1XQwLGcxvtCmTeyiuy7D4I7eF6Mib7Sr6gWJKtjTLr6a9jkaJ3zrY61UGiDrLLgaZysUSIJI-M9DFcuXh5lduqb3jDtme4Bz77KQTZy57R3V7DQ0zfThFuQrTQ__)

## 4. API Specification

### 4.1 Endpoint: Update Engage Day

| Property | Value |
| :--- | :--- |
| **Endpoint** | `POST /v1/friendship/update-engage-day` |
| **Mô tả** | Cập nhật `engage_day` cho một danh sách User ID. **BE chỉ gửi những user có thay đổi về `engage_day`**. |
| **Authentication** | API Key/Token (Internal Service Call) |
| **Request Body** | JSON Array |
| **Response** | `200 OK` (JSON) |

### 4.2 Request Body Example

The request body is a list of objects containing the user ID and the newly calculated `engage_day`.

\`\`\`json
[
  {
    "user_id": "user_123",
    "engage_day": 5,
  },
    {
    "user_id": "user_123",
    "engage_day": 7,
  },
{
    "user_id": "user_123",
    "engage_day": 12,
  },
  {
    "user_id": "user_456",
    "engage_day": 14,
  }
]
\`\`\`

### 4.3 Response Body Example (200 OK)

\`\`\`json
{
  "success": true,
  "message": "Engage days and friendship levels updated successfully for 2 users",
  "updated_count": 2,
  "details": [
 ....
  ]
}
\`\`\`

## 5. Data Model

The `friendship_status` table (or equivalent) in the AI/Context Service database must be updated to include the `engage_day` column.

### 5.1 `friendship_status` Table Schema Update

| Column | Type | Description |
| :--- | :--- | :--- |
| `user_id` | `VARCHAR` | Primary Key, User identifier |
| `friendship_score` | `FLOAT` | **(Legacy/Secondary)** Score based on conversation metrics |
| `friendship_level` | `VARCHAR` | **(Primary)** Current friendship phase (PHASE1/2/3) |
| **`engage_day`** | **`INTEGER`** | **NEW:** Number of days the user has completed the engagement criteria. **AI duy trì cột này để đồng bộ với BE và tính toán `friendship_level`**. |
| `topic_metrics` | `JSONB` | Metrics for each topic |
| `updated_at` | `TIMESTAMP` | Last update time |

## 6. Pipeline Modules (AI/Context Service)

### 6.1 Level Calculation Logic

The AI/Context Service will implement the following deterministic logic to calculate `friendship_level` based on the received `engage_day`.

| Engage Day Range | Friendship Level |
| :--- | :--- |
| `engage_day` < 7 | `PHASE1_STRANGER` |
| `7 <= engage_day < 14` | `PHASE2_ACQUAINTANCE` |
| `engage_day >= 14` | `PHASE3_FRIEND` |

### 6.2 Implementation Flow

The API handler will execute the following steps for each user in the request:

1. **Validation:** Validate `user_id` and `engage_day` (must be non-negative integer).
2. **Level Determination:**
   \`\`\`python
   def determine_level(engage_day: int) -> str:
       """
       Logic tính toán friendship_level dựa trên engage_day.
       """
       if engage_day >= 14:
           return "PHASE3_FRIEND"
       elif engage_day >= 7:
           return "PHASE2_ACQUAINTANCE"
       else:
           return "PHASE1_STRANGER"
   \`\`\`
3. **DB Transaction:**
   - Fetch current `friendship_status` for `user_id`.
   - Store `old_level`.
   - **Update `engage_day` with the new value (Đồng bộ với BE).**
   - **Update `friendship_level` using the result of `determine_level(new_engage_day)` (AI tự tính).**
   - Commit transaction.
4. **Response:** Return the status, `old_level`, and `new_level` in the response body.

## 7. Conclusion on Option 2

**Pros:**
- **AI retains control over core context:** The AI/Context Service remains the single source of truth for `friendship_level`, simplifying the Agent Selection Logic.
- **Clear separation of concerns:** BE handles the complex calculation of `engage_day` (based on conversation logs, todo lists, etc.), while AI handles the simple, fixed mapping logic.

**Cons:**
- **Distributed Logic:** The mapping logic (7 days -> Phase 2) exists only in the AI/Context Service. If this mapping needs to change, only the AI service needs to be updated. This is the inherent trade-off of Option 2.
- **Dependency:** The AI service is dependent on the BE service calling the API nightly.
\`\`\`
