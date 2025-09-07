This folder contains **layout components** that define the **overall structure of different sections of your app**. Layouts typically include elements like **navigation bars, sidebars, footers, and content wrappers**.

---

## **📌 Why Use Layouts?**

✅ **Keeps the UI consistent** across multiple pages.  
✅ **Prevents duplication** of common elements (e.g., Navbar, Sidebar).  
✅ **Supports nested routing** in React Router.  
✅ **Helps separate structure from individual page logic.**

---

## **📂 Folder Structure Example**

```
/layouts
  ├── MainLayout.jsx
  ├── AuthLayout.jsx
  ├── DashboardLayout.jsx
```

---

## **📜 Common Layout Examples**

### **📌 `MainLayout.jsx` – Default Layout (Header, Footer)**

Used for **public pages** like Home, About, and Contact.

```jsx
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function MainLayout() {
  return (
    <div>
      <Navbar />
      <main>
        <Outlet /> {/* Renders the current route's component */}
      </main>
      <Footer />
    </div>
  );
}

export default MainLayout;
```

✅ **Usage in Routes (`AppRoutes.jsx`)**

```jsx
<Routes>
  <Route path='/' element={<MainLayout />}>
    <Route index element={<Home />} />
    <Route path='about' element={<About />} />
    <Route path='contact' element={<Contact />} />
  </Route>
</Routes>
```

---

### **📌 `AuthLayout.jsx` – Layout for Authentication Pages**

Used for **login and signup pages**, without a navbar or footer.

```jsx
import { Outlet } from 'react-router-dom';

function AuthLayout() {
  return (
    <div className='auth-container'>
      <div className='auth-box'>
        <Outlet /> {/* Renders Login or Signup page */}
      </div>
    </div>
  );
}

export default AuthLayout;
```

✅ **Usage in Routes (`AppRoutes.jsx`)**

```jsx
<Routes>
  <Route path='/auth' element={<AuthLayout />}>
    <Route path='login' element={<Login />} />
    <Route path='signup' element={<Signup />} />
  </Route>
</Routes>
```

---

### **📌 `DashboardLayout.jsx` – Layout for Protected Routes**

Used for **authenticated pages**, including a sidebar.

```jsx
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';

function DashboardLayout() {
  return (
    <div className='dashboard-container'>
      <Sidebar />
      <div className='dashboard-content'>
        <Navbar />
        <Outlet />
      </div>
    </div>
  );
}

export default DashboardLayout;
```

✅ **Usage in Routes (`PrivateRoutes.jsx`)**

```jsx
<Routes>
  <Route path='/dashboard' element={<DashboardLayout />}>
    <Route index element={<Dashboard />} />
    <Route path='settings' element={<Settings />} />
  </Route>
</Routes>
```

---

## **🛑 What NOT to Do in `/layouts/`**

🚫 **Do NOT place page-specific logic here.** Layouts should only handle the structure.  
🚫 **Do NOT put global state inside layouts.** Use **Context API or Redux** instead.  
🚫 **Do NOT duplicate layouts in components.** Always **wrap routes inside a layout**.
