import json
import re
from collections import Counter

paths = Counter()
ips = Counter()
total = 0

with open("/app/data/access.log") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total += 1
        
        # Extract IP address
        ip = line.split()[0]
        ips[ip] += 1
        
        # Extract path from request
        m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
        if m:
            paths[m.group(1)] += 1

# Create clients array
clients = [{"ip": ip, "request_count": count} for ip, count in ips.items()]

# Create popular_pages array (top 10)
popular_pages = [{"path": path, "hit_count": count} for path, count in paths.most_common(10)]

with open("/app/report.json", "w") as out:
    json.dump(
        {
            "total_requests": total,
            "clients": clients,
            "popular_pages": popular_pages,
        },
        out,
    )
print("wrote /app/report.json")
