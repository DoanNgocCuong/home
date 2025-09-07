# Pages Folder

This folder contains **route-level pages** like Home, Dashboard, and Login.

✅ **Best Practices:**

- Each page should have **its own folder** if it has sub-components.
- Pages should **only contain layout and logic**, not reusable components.
- Import UI components from `/components/` instead of defining them here.

Example structure:
/pages
├── Home/
│ ├── Home.jsx
│ ├── Home.module.css
├── Dashboard/
│ ├── Dashboard.jsx
