# JMeter GUI Structure Visualization

When you open the generated JMX file in JMeter 5.5, here's how it would appear in the Test Plan tree:

```
Test Plan
├── User Defined Variables
│   ├── P_base_url = https://api.example.com
│   ├── P_api_key = your-api-key
│   ├── P_delay = 5000
│   └── transaction_prefix = API_TEST_
│
├── Login CSV Data (CSV Data Set Config)
├── User Creation CSV Data (CSV Data Set Config)
├── Product Search CSV Data (CSV Data Set Config)
│
├── Sample API Collection (Thread Group)
│   ├── Number of Threads: 1
│   ├── Ramp-up Period: 1
│   └── Loop Count: 1
│   │
│   ├── ${transaction_prefix}Login (HTTP Request)
│   │   ├── HTTP Headers (HTTP Header Manager)
│   │   │   └── Content-Type: application/json
│   │   ├── Constant Timer (5000ms)
│   │   ├── Response Assertion (Check for 200)
│   │   └── Extract Auth Token (Regular Expression Extractor)
│   │
│   ├── ${transaction_prefix}Get User Profile (HTTP Request)
│   │   ├── HTTP Headers (HTTP Header Manager)
│   │   │   └── Authorization: Bearer ${C_auth_token}
│   │   ├── Constant Timer (5000ms)
│   │   └── Response Assertion (Check for 200)
│   │
│   ├── ${transaction_prefix}Create User (HTTP Request)
│   │   ├── HTTP Headers (HTTP Header Manager)
│   │   │   ├── Content-Type: application/json
│   │   │   └── Authorization: Bearer ${C_auth_token}
│   │   ├── Constant Timer (5000ms)
│   │   └── Response Assertion (Check for 200)
│   │
│   └── ${transaction_prefix}Search Products (HTTP Request)
│       ├── HTTP Headers (HTTP Header Manager)
│       │   └── Authorization: Bearer ${C_auth_token}
│       ├── Constant Timer (5000ms)
│       └── Response Assertion (Check for 200)
│
├── Sample API Collection_CSV_dummy (Thread Group)
│   ├── Create Login CSV (BeanShell PreProcessor)
│   ├── Create User Creation CSV (BeanShell PreProcessor)
│   ├── Create Product Search CSV (BeanShell PreProcessor)
│   └── Dummy Request (HTTP Request)
│
└── View Results Tree (Listener)

## Visual Representation in JMeter GUI:

### Left Panel (Test Plan Tree):
- Icons: Each element has its specific icon
  - Thread Groups: Running person icon
  - HTTP Requests: Globe/world icon
  - CSV Data Set: File icon
  - Timers: Clock icon
  - Assertions: Checkmark icon
  - Extractors: Magnifying glass icon

### Right Panel (Element Configuration):
When clicking on each element, you'll see:

1. **HTTP Request Sampler:**
   - Server Name: ${P_base_url}
   - Path: /api/v1/login
   - Method: POST
   - Body Data: JSON with parameterized values

2. **CSV Data Set Config:**
   - Filename: login_data.csv
   - File Encoding: UTF-8
   - Variable Names: P_username,P_password
   - Delimiter: ,
   - Ignore first line: True

3. **Regular Expression Extractor:**
   - Reference Name: C_auth_token
   - Regular Expression: "accessToken":"(.+?)","refreshToken"
   - Template: $1$
   - Default Value: NOT_FOUND

4. **Thread Group Settings:**
   - Number of Threads: 1
   - Ramp-up Period: 1
   - Loop Count: 1

### Color Coding:
- Green elements: Enabled
- Gray elements: Disabled
- Red highlights: Errors or missing configurations

### Execution Flow:
1. User Defined Variables load first
2. CSV files are read
3. Dummy thread group runs to create CSV files
4. Main thread group executes:
   - Login → Extract token
   - Use token for subsequent requests
5. Results appear in View Results Tree