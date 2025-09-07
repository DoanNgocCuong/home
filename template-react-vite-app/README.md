# **🚀 React + Vite + TypeScript + SWC + Tailwind Template**

A **modern React template** using **Vite**, **TypeScript**, **SWC (Speedy Web Compiler)**, and **Tailwind CSS** with a **best-practice folder structure** for scalable applications.

This template provides:  
✅ **Vite** – Super-fast development & optimized builds.  
✅ **TypeScript** – Type safety for better development experience.  
✅ **SWC** – Lightning-fast TypeScript & JSX compilation (replaces Babel).  
✅ **Tailwind CSS** – Utility-first styling for faster UI development.  
✅ **Feature-Based Folder Structure** – Organized & scalable project structure.

---

## **📌 Features**

✔ **Vite** – Lightning-fast development server.  
✔ **TypeScript** – Strong typing for scalable projects.  
✔ **SWC Compiler** – Faster builds than Babel & `tsc`.  
✔ **Tailwind CSS** – Simple and flexible styling.  
✔ **React Router** – Pre-configured for navigation.  
✔ **Reusable Components** – Organized structure with `/components`.  
✔ **Global State Management** – Easily extendable with Redux or Zustand.  
✔ **Optimized for Performance** – Uses Vite’s modern build system with SWC.

---

## **📂 Folder Structure**

```
/src
  ├── /assets        # Static files (images, icons, fonts, global styles)
  ├── /components    # Reusable UI components (Button, Modal, etc.)
  ├── /features      # Feature-based components (Auth, User, Dashboard)
  ├── /hooks         # Custom React hooks
  ├── /layouts       # Layout components (Navbar, Sidebar, Footer)
  ├── /pages         # Page components (Home, About, Dashboard)
  ├── /routes        # Centralized routing
  ├── /services      # API calls and external services
  ├── /store         # Global state management (Redux, Zustand, or Context)
  ├── /utils         # Utility functions (formatDate, debounce, etc.)
  ├── App.tsx        # Main application component
  ├── main.tsx       # Entry point for ReactDOM
  ├── index.css      # Global styles
  ├── tailwind.config.ts # Tailwind configuration
```

---

## **📦 Installation & Setup**

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/brunnoTripovichy/using-react-vite.git
cd using-react-vite
```

### **2️⃣ Install Dependencies**

```bash
npm install
```

### **3️⃣ Start the Development Server**

```bash
npm run dev
```

Your app will be running at **http://localhost:5173/** 🚀

### **4️⃣ Build for Production**

```bash
npm run build
```

This will generate an optimized production-ready build in the **`/dist`** folder.

---

## **🚀 Why Use SWC Instead of Babel or `tsc`?**

| Feature                | SWC                            | Babel                        | `tsc`                  |
| ---------------------- | ------------------------------ | ---------------------------- | ---------------------- |
| 🚀 **Speed**           | 🔥 **Super fast** (Rust-based) | 🐢 Slower (JavaScript-based) | 🐌 Slowest             |
| 🔄 **Hot Reload**      | ✅ Yes                         | ✅ Yes                       | ❌ No                  |
| 🏗 **Type Checking**    | ❌ No (`tsc --noEmit` needed)  | ❌ No                        | ✅ Yes                 |
| 📦 **Bundle Size**     | ✅ Smaller                     | ❌ Larger                    | ❌ N/A (only compiles) |
| 🔧 **Recommended For** | Performance-focused apps       | Legacy projects              | Type checking only     |

📌 **Note:**  
SWC **does not do type checking**. You still need to run TypeScript’s `tsc --noEmit` for type safety.

---

## **🎨 Styling with Tailwind CSS**

This template includes **Tailwind CSS** for efficient styling.  
✔ Utility-first approach for faster development.  
✔ Easily extendable with custom themes.

🛠 Modify **`tailwind.config.ts`** to customize styles.

---

## **📌 Routing with React Router**

This template includes **React Router** for page navigation.  
Routes are defined in **`/routes/AppRoutes.tsx`**.

Example:

```tsx
import { Routes, Route } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import Home from '../pages/Home';
import About from '../pages/About';

function AppRoutes() {
  return (
    <Routes>
      <Route path='/' element={<MainLayout />}>
        <Route index element={<Home />} />
        <Route path='about' element={<About />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
```

---

## **🛠 State Management (Optional)**

This template supports:  
✅ **Context API** (default)  
✅ **Redux Toolkit** (can be added)  
✅ **Zustand** (lightweight state management alternative)

Modify `/store/` to integrate the state management of your choice.

---

## **🌍 Deployment**

Deploy the app using:

### **Vercel**

```bash
vercel deploy
```

### **Netlify**

```bash
netlify deploy
```

### **GitHub Pages**

```bash
npm run build
npm run deploy
```

---

## **🙌 Contributing**

Want to improve this template? Contributions are welcome!

1. **Fork** this repository.
2. **Create a branch:** `git checkout -b my-new-feature`
3. **Commit changes:** `git commit -m "Add a cool feature"`
4. **Push the branch:** `git push origin my-new-feature`
5. **Open a Pull Request**

---

## **📜 License**

This project is **MIT licensed**. Feel free to use and modify it.

---

## **🚀 Ready to Build?**

This template is designed to help you **quickly start** a scalable React + TypeScript project with Vite & SWC.  
If you found this useful, ⭐ **star the repo** and share it with others!

---

### **📩 Need Help?**

Open an **issue** or reach out on **GitHub Discussions**. Let’s build something awesome together! 🚀
