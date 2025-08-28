# Real-time PII Defense 🚀

## 📌 Problem Statement
Flixkart’s security audit revealed a **critical risk of PII (Personally Identifiable Information) leakage** through unmonitored assets such as:
- API logs
- Background jobs
- 3rd-party integrations

A recent fraud incident traced back to exposed logs highlights the urgent need for a **real-time PII detection and redaction system**.

---

## 🎯 Solution Overview
We developed a **Real-time PII Detector & Redactor** that automatically:
- Detects sensitive data like names, phone numbers, emails, Aadhaar, PAN, passport, UPI IDs, addresses.
- Redacts them in **real-time** before data leaves the system.
- Works in a **multi-layered defense model** for maximum coverage.

---

## 🛡️ Deployment Strategy (Hybrid Model)
Our solution uses a **layered deployment approach** for scalability and low latency:

1. **API Gateway Plugin** – Central enforcement at ingress/egress.  
2. **Sidecar with Sensitive Services** – Protects critical microservices like orders, payments, user profile.  
3. **DaemonSet in Kubernetes** – Runs on every node, ensuring no unmonitored traffic bypasses protection.  
4. **Observability** – Centralized logging & real-time alerts on failures.  

✅ This hybrid model ensures **defense-in-depth** without rewriting services.

---

## ⚙️ How It Works
1. **Input** → CSV/JSON dataset containing logs or API payloads.  
2. **PII Detector** → Scans each record and flags sensitive fields.  
3. **Redactor** → Masks detected PII using consistent patterns (e.g., `raXXX@eXX.com`, `98XXXXXX10`).  
4. **Output** → Stored in a redacted CSV with:
   - `record_id`
   - `redacted_data_json`
   - `is_pii` flag

---

## 📂 Example Output
| record_id | redacted_data_json | is_pii |
|-----------|--------------------|--------|
| 1 | {"customer_id":"[REDACTED]","phone":"98XXXXXX10","order_value":1299} | TRUE |
| 2 | {"name":"RXXX KXXX","email":"raXXX@eXX.com","city":"Mumbai"} | TRUE |
| 3 | {"first_name":"Priya","product":"iPhone 14","category":"Electronics"} | FALSE |
| 4 | {"aadhar":"1234XXX9012","transaction_type":"purchase"} | TRUE |

---

## 🚀 Usage

### 1. Clone the Repo
```bash
git clone https://github.com/Krishna845-prog/Krishna_PII.git
cd Krishna_PII
```
2. Run Detector
```bash
python3 detector_Krishna_Arun_Iyer.py iscp_pii_dataset.csv
```
3. Output

A file named:
```php-template
redacted_output_Krishna_Arun_Iyer.csv
```
redacted_output_<yourname>.csv
will be generated in the same folder.

✅ Key Benefits

1) Scalable → Works at both cluster and service level

2) Low Latency → Gateway ensures minimal performance overhead

3) Cost-Effective → Central enforcement avoids expensive service rewrites

4) Compliant → Audit-ready logs for GDPR & Indian data protection laws

👨‍💻 Authors

Krishna Arun Iyer – PII Detection & Redaction Implementation
