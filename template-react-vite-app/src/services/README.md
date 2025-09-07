# Services Folder

This folder handles API requests and external services.

✅ Best Practices:

- Keep API calls separate from components.
- Use one file per feature (e.g., `authService.js, userService.js`).
- Use Axios or Fetch for API calls.

Example API call:

```js
import axios from 'axios';
export const fetchUsers = () => axios.get('/api/users');
```
