# Routes Folder

This folder manages React Router routes in one place.

✅ Best Practices:

- Use AppRoutes.jsx to define the main routes.
- If you have protected routes, add them to PrivateRoutes.jsx.
- Always use Outlet inside layouts for nested routing.

Example:

```jsx
<Route path='/' element={<MainLayout />}>
  <Route index element={<Home />} />
  <Route path='dashboard' element={<Dashboard />} />
</Route>
```
