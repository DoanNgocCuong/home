The `/features/` folder is used to organize **self-contained features** of the application. Each feature should have **everything it needs**—components, logic, hooks, API calls, and state management—**in one place**.

This structure is useful for **large-scale applications** because it keeps code modular, scalable, and easier to maintain.

---

## **📌 Why Use a Feature-Based Folder Structure?**

✅ **Keeps related code together** (components, hooks, API, and state).  
✅ **Avoids bloated `/components/` and `/pages/` folders.**  
✅ **Encapsulates each feature** so it can be worked on independently.  
✅ **Scales well for large applications** with multiple teams.

---

## **📂 Recommended Folder Structure for `/features/`**

```
/features
  ├── auth/               # Authentication feature
  │    ├── components/
  │    │    ├── LoginForm.jsx
  │    │    ├── SignupForm.jsx
  │    ├── hooks/
  │    │    ├── useAuth.js
  │    ├── services/
  │    │    ├── authService.js
  │    ├── store/
  │    │    ├── authSlice.js  (if using Redux)
  │    ├── AuthPage.jsx
  │    ├── index.js
  │
  ├── user/               # User profile & settings feature
  │    ├── components/
  │    │    ├── UserProfile.jsx
  │    │    ├── UserSettings.jsx
  │    ├── services/
  │    │    ├── userService.js
  │    ├── store/
  │    │    ├── userSlice.js
  │    ├── UserPage.jsx
  │    ├── index.js
```

---

## **📂 Folder Breakdown & Best Practices**

### **1️⃣ `/features/auth/` – Authentication Feature**

Contains everything related to authentication:  
✅ **Components** (`LoginForm`, `SignupForm`)  
✅ **Hooks** (`useAuth.js`)  
✅ **API Calls** (`authService.js`)  
✅ **State Management** (`authSlice.js` for Redux or `useContext`)

Example **authService.js**:

```js
import axios from 'axios';

const API_URL = 'https://api.example.com/auth';

export const login = async (email, password) => {
  return axios.post(`${API_URL}/login`, { email, password });
};

export const signup = async (userData) => {
  return axios.post(`${API_URL}/signup`, userData);
};
```

Example **useAuth.js** (for authentication logic):

```js
import { useState, useEffect } from 'react';
import { login } from '../services/authService';

export function useAuth() {
  const [user, setUser] = useState(null);

  const loginUser = async (email, password) => {
    const response = await login(email, password);
    setUser(response.data.user);
  };

  return { user, loginUser };
}
```

✅ **Why is this better?**

- Everything related to **authentication is inside `/features/auth/`**.
- If we need to remove or modify authentication, **we only touch this folder**.

---

### **2️⃣ `/features/user/` – User Feature (Profile & Settings)**

This feature includes:  
✅ **User-related components** (`UserProfile.jsx`, `UserSettings.jsx`)  
✅ **API requests** (`userService.js`)  
✅ **Redux state management** (`userSlice.js`)

Example **userService.js**:

```js
import axios from 'axios';

const API_URL = 'https://api.example.com/users';

export const getUserProfile = async (userId) => {
  return axios.get(`${API_URL}/${userId}`);
};
```

Example **UserProfile.jsx**:

```jsx
import { useEffect, useState } from 'react';
import { getUserProfile } from '../services/userService';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    getUserProfile(userId).then((res) => setUser(res.data));
  }, [userId]);

  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>Email: {user.email}</p>
    </div>
  );
}

export default UserProfile;
```

✅ **Why is this better?**

- The user feature **is self-contained**—it doesn’t depend on `/components/`.
- **Easier to manage**—if we change how profiles work, we modify only `/features/user/`.

---

## **🛑 What NOT to Do in `/features/`**

🚫 **Do NOT place global components here.** Keep reusable UI components in `/components/`.  
🚫 **Do NOT put unrelated logic inside features.** Features should be independent.  
🚫 **Do NOT mix multiple features in the same folder.** Keep each feature isolated.

---
