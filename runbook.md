# NATHAN Project Runbook

## Role of NOC Engineer
The NOC (Network Operations Center) engineer is responsible for monitoring systems, responding to alerts, and escalating critical events. The primary objective is to maintain uninterrupted infrastructure operation.

## Alert Prioritization
- **Severity - Critical - P1 - High Priority:** Immediate response required.
- **Severity - High - P2 - Medium Priority:** Resolution waiting time 15 minutes.
- **Severity - Medium - P3 - Low Priority:** Resolution waiting time 30 minutes.
- **Severity - Low - P4 - Lowest Priority:** Ignore the alert.
- **Severity - Any - PU - Unknown Priority:** - This alarm cannot be prioritized based on runbook content


## Alert Descriptions and Escalation

### Alert: CPU Usage Exceeded
- **Severity**: Critical
- **Alert Example**: `CPU usage is consistently over 90% for the last 5 minutes.`
- **Escalation Message**: `@devops - High CPU load on server {server_name}, immediate check required. Risk of application failure.`

### Alert: Network Equipment Error
- **Severity**: High
- **Alert Example**: `Multiple reports of network connectivity issues detected.`
- **Escalation Message**: `@network - Complaints received about network connection problems, possible equipment malfunction. Please check.`

### Alert: Insufficient Disk Space
- **Severity**: High
- **Alert Example**: `Disk space on server {server_name} has reached 85% capacity.`
- **Escalation Message**: `@support - Disk space on server {server_name} is close to critical, cleanup required.`

### Alert: Service Downtime
- **Severity**: Critical
- **Alert Example**: `Service {service_name} is down. Immediate action required.`
- **Escalation Message**: `@service_team - Service {service_name} is unresponsive, immediate intervention required to restore functionality.`

### Alert: Database Error
- **Severity**: Medium
- **Alert Example**: `Database response time has increased beyond acceptable thresholds.`
- **Escalation Message**: `@db_admins - Database response time has exceeded acceptable thresholds, check for potential performance issues.`

### Alert: High Network Load
- **Severity**: Medium
- **Alert Example**: `Network throughput is unusually high, indicating possible DDoS attack.`
- **Escalation Message**: `@security - Unusually high network activity detected, possible DDoS attack. Verification and response needed.`

## Host Exceptions

### Low Priority Hosts
- **Hosts**: `host_a`, `host_b`, `host_c`
- **Action**: Alerts from these hosts are processed with lowest priority (P4).

### High Priority Hosts
- **Hosts**: `host_g`, `host_d`, `host_e`
- **Action**: Immediately respond to alerts from these hosts, regardless of Severity (P1).

