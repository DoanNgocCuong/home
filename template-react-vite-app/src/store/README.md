# Store Folder

This folder manages global state with Redux or Context API.

✅ **Best Practices:**

- Keep each feature’s state in a separate file (e.g., `authSlice.js`).
- Store configuration (`store.js`) should only combine reducers.
- If using Context API, create a context/ folder instead.
  Example:

/store
├── store.js
├── authSlice.js
├── userSlice.js
