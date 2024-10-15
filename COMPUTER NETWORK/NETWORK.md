The IP addresses shown in MongoDB Atlas' "Network Access" section are used to control which IP addresses are allowed to connect to your MongoDB cluster. 

1. **Your IP Address (58.187.248.201/32)**: This is an IP address you added manually to allow your machine to connect to the MongoDB cluster. The `/32` subnet indicates that only this specific IP address is allowed to connect.
   
2. **Another IP Address (27.72.97.130/32)**: This seems to be an IP that MongoDB detected as part of an automatic setup, which is likely your current public IP address or one that you were using when setting up MongoDB.

### If Someone is Using a Remote Location
- **Adding Other IP Addresses**: If a user from a remote location needs access to the cluster, you will need to add their specific public IP address to this list or use the option to "Allow Access from Anywhere" by adding `0.0.0.0/0`. Be careful with this option, as it allows anyone with the connection details to access your database, which might be a security risk.

### Does it Affect Your Machine?
- These IP addresses do not directly affect your machine. They only tell MongoDB which machines (based on IP addresses) are allowed to connect to the MongoDB cluster. If someone tries to connect from an IP not listed here, they will be denied access.