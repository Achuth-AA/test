# Body Parameters to CSV Data Config Mapping

## How Body Parameters are Handled:

### 1. Original API Request Body:
```json
{
    "username": "testuser",
    "password": "Test@123",
    "email": "test@example.com"
}
```

### 2. Parameterized in JMeter HTTP Request:
```json
{
    "username": "${P_username}",
    "password": "${P_password}",
    "email": "${P_email}"
}
```

### 3. CSV Data Set Config:
- **Filename:** login_data.csv
- **Variable Names:** P_username,P_password,P_email

### 4. CSV File Content:
```csv
P_username,P_password,P_email
testuser,Test@123,test@example.com
user2,Pass@456,user2@example.com
user3,Secret@789,user3@example.com
```

## Complete Flow Example:

### For Create User Endpoint:

**Original Request Body:**
```json
{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "age": 30,
    "isActive": true
}
```

**JMeter HTTP Request Body:**
```json
{
    "firstName": "${P_firstName}",
    "lastName": "${P_lastName}",
    "email": "${P_email}",
    "age": ${P_age},
    "isActive": ${P_isActive}
}
```

**CSV Data Set Config:**
- Variable Names: P_firstName,P_lastName,P_email,P_age,P_isActive

**CSV File (user_creation_data.csv):**
```csv
P_firstName,P_lastName,P_email,P_age,P_isActive
John,Doe,john.doe@example.com,30,true
Jane,Smith,jane.smith@example.com,25,false
Bob,Johnson,bob.j@example.com,35,true
```

## Benefits of this approach:

1. **Data-driven testing**: Run same test with multiple data sets
2. **Easy maintenance**: Update test data without modifying JMX
3. **Parameterization**: All body fields become variables
4. **Reusability**: Same CSV can be used across multiple test runs

## The BeanShellPreProcessor creates these CSV files automatically:

```java
import java.io.*;

String filePath = "user_creation_data.csv";
File csvFile = new File(filePath);
FileWriter writer = new FileWriter(csvFile);

try {
    // Headers matching the variable names
    writer.append("P_firstName,P_lastName,P_email,P_age,P_isActive\n");
    // Sample data row
    writer.append("John,Doe,john.doe@example.com,30,true\n");
    writer.flush();
    writer.close();
} catch (IOException e) {
    log.error("Error writing CSV file: " + e.getMessage());
}
```

This way, every body parameter from the API collection becomes:
1. A placeholder in the HTTP request (${P_paramName})
2. A column in the CSV file
3. A variable that JMeter replaces at runtime