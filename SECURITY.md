# Security Policy

## Privacy & Data Protection

This tool is designed with privacy in mind:

### What This Tool Does NOT Extract

- ❌ Social Security Numbers (SSNs)
- ❌ Credit card numbers
- ❌ Bank account information
- ❌ Medical records
- ❌ Other highly sensitive PII

### What This Tool DOES Extract

- ✅ School names
- ✅ CEEB codes
- ✅ Student IDs (non-SSN institutional identifiers)

## Best Practices for Institutional Use

### FERPA Compliance

When using this tool in educational institutions:

1. **Access Control**: Limit access to authorized personnel only
2. **Audit Logs**: Maintain logs of who accesses student data
3. **Secure Storage**: Store extracted data in encrypted databases
4. **Data Retention**: Follow institutional policies for data retention
5. **Secure Transmission**: Use encrypted channels (HTTPS, SFTP) for data transfer

### Recommended Security Measures

```python
# Example: Secure file handling
import os
from pathlib import Path

# Set restrictive file permissions
def secure_save(data, filepath):
    # Write file
    with open(filepath, 'w') as f:
        f.write(data)
    
    # Set read/write for owner only (600)
    os.chmod(filepath, 0o600)
```

### Environment Setup

1. **Run in isolated environment**: Use virtual machines or containers
2. **Network isolation**: Process sensitive data on isolated networks
3. **Access logging**: Enable system-level access logging
4. **Regular audits**: Review access logs regularly

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public GitHub issue
2. Contact the maintainer directly
3. Provide detailed information about the vulnerability
4. Allow reasonable time for response before disclosure

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Updates

Security updates will be released as needed. Users should:

- Keep dependencies up to date
- Monitor GitHub releases for security patches
- Review changelogs for security-related updates

## Compliance Resources

- [FERPA Regulations](https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Data Privacy Best Practices](https://www.educause.edu/focus-areas-and-initiatives/policy-and-security/cybersecurity-program/resources/information-security-guide)

## Disclaimer

This tool is provided as-is. Organizations using this tool are responsible for:

- Ensuring compliance with applicable laws and regulations
- Implementing appropriate security controls
- Training staff on proper data handling
- Maintaining secure systems and networks

---

Last Updated: December 2024
