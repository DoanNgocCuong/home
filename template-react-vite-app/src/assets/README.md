This folder contains **static files** such as images, icons, fonts, and global styles that are used throughout the app. Keeping these assets in one place helps maintain **organization and reusability**.

---

## **📌 Why Use an `/assets/` Folder?**

✅ **Keeps static files separate** from components and logic.  
✅ **Organized storage** for images, fonts, and global styles.  
✅ **Ensures easy imports** instead of using `/public`.  
✅ **Improves maintainability** by grouping related assets.

---

## **📂 Recommended Folder Structure**

```
/assets
  ├── /images
  │    ├── logo.png
  │    ├── background.jpg
  ├── /icons
  │    ├── home.svg
  │    ├── user.svg
  ├── /fonts
  │    ├── Roboto-Regular.ttf
  ├── /styles
  │    ├── global.css
  │    ├── variables.css
  │    ├── theme.css
```

---

## **📜 What Goes Inside `/assets/`?**

### **📌 `/images/` – Static Images**

- Store **logos, backgrounds, banners, product images, etc.**
- Import images directly instead of referencing from `/public`.

✅ **Example Import in Component:**

```jsx
import logo from '../assets/images/logo.png';

function Header() {
  return <img src={logo} alt='Logo' />;
}
```

🚫 **Avoid placing images in `/public/` unless absolutely necessary**.  
If an image needs to be dynamic (e.g., from a CMS or user upload), **store it in a database instead**.

---

### **📌 `/icons/` – SVG & Icon Files**

- Keep **SVG icons, favicon files, and custom icon sets** here.

✅ **Example Import in Component:**

```jsx
import HomeIcon from '../assets/icons/home.svg';

function Sidebar() {
  return <img src={HomeIcon} alt='Home' />;
}
```

🚀 **Better Practice:** Use an **Icon Component** to dynamically import icons instead of hardcoding them.

```jsx
function Icon({ name }) {
  return <img src={require(`../assets/icons/${name}.svg`)} alt={name} />;
}
```

✅ **Usage:**

```jsx
<Icon name='home' />
```

---

### **📌 `/fonts/` – Custom Fonts**

- Store **custom `.ttf`, `.woff`, `.woff2` font files** here.
- Reference them in **global CSS**.

✅ **Example Import in `global.css`**:

```css
@font-face {
  font-family: 'Roboto';
  src: url('../assets/fonts/Roboto-Regular.ttf') format('truetype');
}
```

🚀 **Better Practice:** If the font is available via Google Fonts, use **CDN links instead** of storing local files.

---

### **📌 `/styles/` – Global Styles & Variables**

- Store **global CSS, Tailwind config, or SCSS variables** here.

✅ **Example Files:**

```
/styles
  ├── global.css
  ├── variables.css
  ├── theme.css
```

✅ **Example Usage in `variables.css`**:

```css
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
}
```

✅ **Example Import in Component:**

```jsx
import '../assets/styles/global.css';
```

🚀 **Better Practice:**

- If using **CSS Modules**, place them inside `/components/`.
- Use `/styles/` only for **global styles** that apply to the entire app.

---

## **🛑 What NOT to Do in `/assets/`**

🚫 **Do NOT store JavaScript or JSX files here.** This folder is only for static files.  
🚫 **Do NOT keep large media files here.** Use a CDN for videos & large images.  
🚫 **Do NOT place components here.** Components should go in `/components/`.
