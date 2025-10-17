# SIEM Server

A lightweight, flexible SIEM (Security Information and Event Management) server that receives and displays syslog messages over UDP or TCP protocols.

## 🚀 Features

- **Dual Protocol Support**: Supports both UDP and TCP protocols
- **Multi-threaded TCP**: Handles multiple simultaneous TCP client connections
- **Command-line Interface**: Easy-to-use CLI with argument validation
- **Real-time Monitoring**: Displays syslog messages with source IP addresses
- **Flexible Port Configuration**: Configurable port binding with validation
- **Comprehensive Help**: Built-in help system with usage examples
- **Error Handling**: Robust error handling and graceful shutdown

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## 🛠️ Installation

1. Clone or download the project:
   ```bash
   git clone <repository-url>
   cd siem_server
   ```

2. No additional installation required - uses Python standard library only.

## 🔧 Usage

### Basic Syntax
```bash
python server.py --protocol <PROTOCOL> [--port <PORT>] [--help]
```

### Required Arguments
- `--protocol`, `-p`: Protocol to use (`udp` or `tcp`)

### Optional Arguments
- `--port`: Port number to bind to (default: 5140)
- `--help`, `-h`: Show help message and exit

### Examples

#### Start UDP Server (Default Port)
```bash
python server.py --protocol udp
```

#### Start TCP Server with Custom Port
```bash
python server.py --protocol tcp --port 9999
```

#### Start Server on Standard Syslog Port (Requires Root)
```bash
sudo python server.py --protocol udp --port 514
```

#### Using Short Arguments
```bash
python server.py -p tcp --port 8080
```

#### Get Help
```bash
python server.py --help
```

## 📄 License

This project is open source. Please check the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues, questions, or contributions, please create an issue in the project repository.

---

**Note**: This is a basic SIEM server designed for development, testing, and learning purposes. For production environments, consider additional security measures and monitoring capabilities.