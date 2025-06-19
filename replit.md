# Overview

This is a security-focused Streamlit application designed to demonstrate prompt injection detection and input sanitization techniques. The application appears to be a calendar reminder system with built-in security measures to protect against malicious inputs and unauthorized access attempts.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web application framework
- **UI Components**: Single-page application with session state management
- **Port Configuration**: Runs on port 5000 with headless server configuration
- **Deployment**: Configured for autoscale deployment on Replit

## Backend Architecture
- **Runtime**: Python 3.11
- **Application Server**: Streamlit's built-in server
- **Session Management**: Streamlit's session state for maintaining user data
- **Security Layer**: Custom input validation and sanitization functions

# Key Components

## Security Components
1. **Prompt Injection Detection**: Regular expression-based pattern matching to identify dangerous inputs
2. **Input Sanitization**: Clean and validate user inputs before processing
3. **Red Team Logging**: Session-based logging system for security events
4. **Calendar Validation**: Verify events against an official instructor calendar

## Core Functions
- `is_malicious_input()`: Detects potentially harmful input patterns
- `sanitize_input()`: Cleans and validates user input
- `validate_event_date()`: Cross-references events with official calendar
- `log_red_team()`: Records security incidents (function referenced but not implemented in current codebase)

## Data Structures
- **INSTRUCTOR_CALENDAR**: Hardcoded dictionary containing official events and dates
- **DANGEROUS_PATTERNS**: List of regex patterns for detecting malicious inputs
- **Session State**: Browser session storage for red team logs

# Data Flow

1. **User Input Reception**: Streamlit captures user input through web interface
2. **Security Screening**: Input passes through malicious pattern detection
3. **Input Sanitization**: Clean input or return error message for suspicious content
4. **Calendar Validation**: Verify event dates against official calendar
5. **Session Logging**: Security events logged to session state
6. **Response Generation**: Return sanitized data or security warning to user

# External Dependencies

## Core Dependencies
- **Streamlit (>=1.46.0)**: Web application framework for Python
- **Standard Library**: re, datetime, json modules for core functionality

## System Dependencies
- **Python 3.11**: Runtime environment
- **Nix Package Manager**: For system-level dependency management (stable-24_05 channel)

# Deployment Strategy

## Replit Configuration
- **Deployment Target**: Autoscale deployment for automatic scaling
- **Workflow Management**: Parallel task execution with shell commands
- **Port Configuration**: Fixed port 5000 for consistent access
- **Server Settings**: Headless mode with bind to all interfaces (0.0.0.0)

## Development Environment
- **Module System**: Python 3.11 module configuration
- **Package Management**: UV lock file for dependency resolution
- **Configuration Management**: TOML-based project and server configuration

# Changelog

```
Changelog:
- June 19, 2025. Initial setup
```

# User Preferences

```
Preferred communication style: Simple, everyday language.
```

## Architecture Decisions

### Security-First Design
**Problem**: Need to protect against prompt injection attacks and malicious input
**Solution**: Multi-layered security approach with pattern detection, input sanitization, and event validation
**Rationale**: Prevents common attack vectors while maintaining usability

### Streamlit Framework Choice
**Problem**: Need rapid prototyping for security demonstration
**Solution**: Streamlit for quick web interface development
**Pros**: Fast development, built-in session management, easy deployment
**Cons**: Limited customization compared to full web frameworks

### Hardcoded Calendar Data
**Problem**: Need official event reference for validation
**Solution**: In-memory dictionary with predefined events
**Rationale**: Simple demonstration approach, would connect to real database in production

### Session-Based Logging
**Problem**: Need to track security events during user session
**Solution**: Streamlit session state for temporary log storage
**Limitations**: Data lost on session end, not persistent across restarts