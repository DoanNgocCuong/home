
  

netstat -tlnp | grep -E "30011|30012"


nohup python -m http.server 30011 > output.log 2>&1