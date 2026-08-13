# E-Commerce Security Test Cases

## TC-01: SQL Injection

### Objective
To verify whether user input is safely handled in database queries.

### Vulnerability
SQL Injection

### Test
Enter unexpected SQL characters in the username/product search input.

### Expected Secure Result
The application should treat the input as normal data and should not allow modification of the database query.

### Result
Vulnerability identified during source-code/SAST analysis.

---

## TC-02: Cross-Site Scripting (XSS)

### Objective
To verify whether user-supplied review/input is safely handled before being displayed.

### Vulnerability
Cross-Site Scripting (XSS)

### Test
Enter HTML/script-like input in the product review field.

### Expected Secure Result
The application should display the input as text instead of executing it as browser code.

### Result
Vulnerability identified during source-code/SAST analysis.

---

## TC-03: File Upload Vulnerability

### Objective
To verify whether uploaded files are properly validated.

### Vulnerability
Unrestricted/Improper File Upload

### Test
Attempt to upload a file with an unexpected file type.

### Expected Secure Result
The application should validate the file type, filename and upload location before accepting the file.

### Result
Vulnerability identified during security analysis.
