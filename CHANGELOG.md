# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2025-08-20

### Changed
- **Documentation Consolidated**: Merged PROJECT_SUMMARY.md into comprehensive README.md
- **README Enhanced**: Added complete project overview, metrics, troubleshooting, and development guides
- **Single Source of Truth**: One comprehensive documentation file for all audiences

### Added
- **Comprehensive Troubleshooting**: Detailed solutions for common issues
- **Development Workflow**: Complete guide for contributors
- **Project Metrics**: Quality scores and current status
- **Quick Reference**: Most common commands and help section
- **Architecture Details**: Enhanced technical documentation

## [2.0.0] - 2025-08-20

### Added
- **Environment Variables Support**: Secure configuration with .env files
- **Input Validation**: Protection against malicious inputs and long city names
- **Error Handling**: Comprehensive error handling throughout the application
- **Flash Messages**: Real-time user feedback for all operations
- **Logging System**: Proper logging for debugging and monitoring
- **Modern UI**: Responsive design with CSS styling and mobile support
- **Configuration Management**: Centralized configuration with different environments
- **Testing Framework**: Unit tests with pytest
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment
- **Docker Improvements**: Multi-stage builds, health checks, non-root user
- **Development Tools**: Makefile, batch scripts for Windows, requirements-dev.txt
- **Documentation**: Comprehensive README with setup instructions

### Security Improvements
- **Non-root Docker Container**: Enhanced security posture
- **Environment Variable Configuration**: No more hardcoded secrets
- **Input Sanitization**: Protection against injection attacks
- **Updated Dependencies**: Latest secure versions of all packages
- **Proper Secret Management**: Flask secret key from environment

### Fixed
- **Port Consistency**: Fixed port mismatches between app and documentation  
- **Static Directory**: Created proper static folder for matplotlib plots
- **Database Schema**: Added timestamps to weather data
- **Memory Leaks**: Proper matplotlib figure cleanup
- **API Timeout**: Added timeout handling for weather API requests
- **Error Messages**: Better user-friendly error messages

### Changed
- **Python Version**: Upgraded to Python 3.11
- **Flask Version**: Updated to Flask 3.0.3
- **Database Structure**: Added timestamp column to weather table
- **Project Structure**: Organized files and removed unnecessary duplicates
- **Ansible Playbook**: Improved with proper modules and error handling
- **Vagrant Configuration**: Fixed networking and file paths

### Removed
- **Hardcoded API Keys**: Replaced with environment variables
- **Duplicate Files**: Cleaned up project structure
- **.vagrant Directory**: Removed auto-generated Vagrant files
- **Insecure Configurations**: Replaced with best practices

## [1.0.0] - Original Release

### Initial Features
- Basic Flask weather application
- SQLite database storage
- Matplotlib plotting
- Docker containerization
- Ansible deployment
- Jenkins pipeline
- Vagrant VM setup
