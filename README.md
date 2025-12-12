# secure-firewall-mcp
FastMCP server for interfacing with the Cisco Secure Firewall API using an AI agent. 

Capable of gathering the following:
- Devices
- HA pairs
- Health alerts
- Audit alerts (need to implement second endpoint)
- Job history
- User

# Software Architecture
![Architecture for Secure Firewall MCP Server](images/architecture.png)

# Prerequisites
- Set service account credentials in `src/creds/.env`
- Configure `fmc_hosts.yaml` 
- If running tests, set `FMC_HOST` variable in `src/creds/.env`

# Deployment
``` bash
sudo docker compose up --build
```