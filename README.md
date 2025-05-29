# Stoculus

Stoculus is a sophisticated financial data processing and streaming platform designed to handle real-time and historical market data, with a particular focus on equity markets and options.

## Project Overview

This project provides a robust framework for:
- Real-time market data streaming
- Historical data processing
- Data reading and processing for various financial instruments
- Scheduler-based data management
- Middleware for data transformation and processing

## Project Structure

```
.
├── configuration/     # Configuration management
├── data_meta/        # Data metadata and schema definitions
├── live_stream/      # Real-time data streaming components
│   ├── theta_data/   # Theta data specific implementations
│   └── response_handlers/  # Response processing handlers
├── middleware/       # Data processing middleware
├── path/            # Path management utilities
├── reader/          # Data reading components
│   ├── equity/      # Equity-specific readers
│   └── tests/       # Reader test suite
├── request/         # Request handling components
├── sandbox/         # Testing and development environment
├── scheduler/       # Task scheduling system
└── utils/           # Utility functions and helpers
```

## Core Components

### Data Reading System
The reader module (`reader/`) provides a flexible framework for reading different types of financial data:
- Stream readers for real-time data
- Time-based data readers for historical data
- Factory pattern implementation for reader creation

### Live Streaming
The live streaming system (`live_stream/`) handles real-time market data:
- Theta data integration
- Response handling
- Listener and requester implementations

### Data Domains
The system supports multiple data domains:
- Equity markets
- Options
- Different price types (Traded, Quote, EOD)

## System Design and Architecture

### Data Flow Architecture
The system implements a robust data pipeline architecture:

1. **Data Ingestion Layer**
   - WebSocket-based real-time data streaming from Theta Data
   - Support for both stock and options data streams
   - Asynchronous processing using asyncio

2. **Message Processing Pipeline**
   - Format Handler: Standardizes incoming data formats
   - Kafka Integration: Implements message queuing for reliable data processing
   - Topic-based message routing (e.g., `{root}_stream_{date}`)

3. **Data Storage and Retrieval**
   - Hierarchical file system organization
   - Domain-based path management
   - Support for multiple data types (CSV, JSON)
   - Configurable file encoding and delimiter settings

### Kafka Integration
The system uses Apache Kafka for message queuing and data distribution:
- Producer implementation for publishing market data
- Topic-based message routing
- JSON serialization for message format
- Default configuration on localhost:9092
- Automatic topic generation based on instrument and date

### Configuration Management
The system implements a flexible configuration system:
- JSON-based configuration files
- Environment-aware configuration loading
- Support for multiple operating systems (MacOS, Windows)
- Domain-specific configuration for different data types
- Path management for data storage

### Data Processing Components
1. **Stream Listeners**
   - ThetaStockStreamListener: Handles equity market data
   - ThetaOptionStreamListener: Processes options market data
   - Asynchronous WebSocket connections

2. **Data Readers**
   - Time-based data streaming
   - Domain-specific readers (Stock, Options)
   - Configurable file formats and parsing options

3. **Response Handlers**
   - Format standardization
   - Kafka message publishing
   - TCP communication support

### Error Handling and Status Management
- Comprehensive status tracking (ReadingStatus, ReaderStatus)
- Error state management
- Connection state monitoring
- Data validation and integrity checks

## Status Management

The system implements several status enums for managing different states:
- `ReadingStatus`: Tracks data reading states (DONE, ONGOING, INACTIVATE)
- `ReaderStatus`: Manages reader states (OPEN, CLOSED, ERROR)

## Getting Started

### Prerequisites
- Python 3.x
- Required dependencies (to be listed in requirements.txt)

### Installation
1. Clone the repository
2. Install dependencies
3. Configure the environment

## Development

### Testing
The project includes comprehensive test suites:
- Unit tests in respective test directories
- Integration tests for core components

### Sandbox Environment
A dedicated sandbox environment is provided for testing and development purposes.

## Contributing

Please read the contribution guidelines before submitting pull requests.

## License

[License information to be added]

## Contact

[Contact information to be added] 