This folder contains **helper functions** that can be reused across the app.

✅ **Best Practices:**

- Functions in this folder should be **pure functions** (i.e., given the same input, they return the same output).
- **No UI logic should be here!**
- Keep functions **small** and **modular**—each file should contain only one type of utility.
- Name files based on **what they do**, like `formatDate.js`, `validateEmail.js`, etc.

---

## **📌 Example File Structure**

```
/utils
  ├── formatDate.js
  ├── validateEmail.js
  ├── debounce.js
  ├── generateUUID.js
  ├── localStorageHelper.js
```

---

## **📜 Example Utility Functions**

Here are some **commonly used utilities** you might store in `/utils/`.

### **📌 `formatDate.js` – Format Dates**

```js
export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};
```

✅ **Example Usage:**

```js
import { formatDate } from '../utils/formatDate';

console.log(formatDate('2024-02-10')); // Output: "Feb 10, 2024"
```

---

### **📌 `validateEmail.js` – Email Validation**

```js
export const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};
```

✅ **Example Usage:**

```js
import { validateEmail } from '../utils/validateEmail';

console.log(validateEmail('test@example.com')); // true
console.log(validateEmail('invalid-email')); // false
```

---

### **📌 `debounce.js` – Optimize Input Handling**

Useful for **search boxes** or any event that fires too often.

```js
export const debounce = (func, delay = 300) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
};
```

✅ **Example Usage:**

```js
import { debounce } from '../utils/debounce';

const handleSearch = debounce((query) => {
  console.log('Searching for:', query);
}, 500);
```

---

### **📌 `generateUUID.js` – Unique ID Generator**

```js
export const generateUUID = () => {
  return crypto.randomUUID();
};
```

✅ **Example Usage:**

```js
import { generateUUID } from '../utils/generateUUID';

console.log(generateUUID()); // "a1b2c3d4-e5f6-7890-ghij-klmnopqrstuv"
```

---

### **📌 `localStorageHelper.js` – Manage Local Storage**

```js
export const saveToLocalStorage = (key, value) => {
  localStorage.setItem(key, JSON.stringify(value));
};

export const getFromLocalStorage = (key) => {
  const data = localStorage.getItem(key);
  return data ? JSON.parse(data) : null;
};

export const removeFromLocalStorage = (key) => {
  localStorage.removeItem(key);
};
```

✅ **Example Usage:**

```js
import {
  saveToLocalStorage,
  getFromLocalStorage,
} from '../utils/localStorageHelper';

saveToLocalStorage('user', { name: 'John Doe', loggedIn: true });

const user = getFromLocalStorage('user');
console.log(user.name); // "John Doe"
```

---

## **🛑 What NOT to Do in `/utils/`**

🚫 **Do NOT place API calls here.** Use `/services/` instead.  
🚫 **Do NOT include UI-related functions.** Keep this strictly for data manipulation.  
🚫 **Do NOT make functions too specific.** They should be **reusable across the app**.

---
