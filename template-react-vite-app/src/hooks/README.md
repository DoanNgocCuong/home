# Hooks Folder

This folder contains custom React hooks.

✅ **Best Practices:**

Hooks should always start with use (e.g.,` useAuth.js, useFetch.js`).
Keep logic reusable across multiple components.
Avoid putting API calls here—use /services/ for that.

Example:

```js
import { useState, useEffect } from 'react';

export function useFetch(url) {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then(setData);
  }, [url]);

  return data;
}
```
