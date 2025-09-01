# ReconX Complete

**ReconX Complete v6.0.0** - A comprehensive Python-only reconnaissance tool for security research and penetration testing.

## What the Tool Does

ReconX Complete is a powerful reconnaissance tool designed to gather intelligence about target domains and web applications. Unlike many reconnaissance tools that rely on external binaries or tools, ReconX Complete performs all operations using pure Python, making it lightweight, portable, and easy to deploy.

### Key Features

- **URL Enumeration**: Discovers common endpoints, API paths, backup files, and sitemaps
- **Subdomain Enumeration**: Finds subdomains using certificate transparency logs and DNS resolution
- **GitHub Reconnaissance**: Searches for sensitive information leaks in GitHub repositories
- **Directory Enumeration**: Brute-forces common directory paths and files
- **Real Results**: Uses live APIs and direct HTTP requests for accurate, up-to-date information
- **Export Capabilities**: Generate professional reports in PDF and Excel formats
- **Interactive Menu**: User-friendly interface for selecting scan types
- **No External Dependencies**: Works with standard Python libraries (plus a few common ones)

### Use Cases

- Security assessments and penetration testing
- Bug bounty hunting
- Web application reconnaissance
- Domain intelligence gathering
- Vulnerability research

## Installation Instructions

### Prerequisites

- Python 3.6 or higher
- Internet connection for API calls and web requests

### Installation Steps

#### Windows Installation

1. **Install Python 3.6+**:
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation: `python --version`

2. **Clone or download the repository**:
   ```cmd
   git clone https://github.com/your-repo/reconx-complete.git
   cd reconx-complete
   ```

3. **Install required Python packages**:
   ```cmd
   pip install requests pandas reportlab beautifulsoup4 urllib3
   ```

   Or using requirements.txt (if available):
   ```cmd
   pip install -r requirements.txt
   ```

4. **Optional: Set up GitHub API token**:
   - Create a GitHub personal access token with public repository access
   - Set environment variable:
     ```cmd
     set GITHUB_TOKEN=your_token_here
     ```
   - Or set permanently in System Properties > Environment Variables

#### Linux Installation

1. **Install Python 3.6+** (if not already installed):
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip

   # CentOS/RHEL/Fedora
   sudo yum install python3 python3-pip  # CentOS/RHEL
   sudo dnf install python3 python3-pip  # Fedora

   # Arch Linux
   sudo pacman -S python python-pip
   ```

2. **Clone or download the repository**:
   ```bash
   git clone https://github.com/your-repo/reconx-complete.git
   cd reconx-complete
   ```

3. **Install required Python packages**:
   ```bash
   pip3 install requests pandas reportlab beautifulsoup4 urllib3
   ```

   Or using requirements.txt (if available):
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Optional: Set up GitHub API token**:
   - Create a GitHub personal access token with public repository access
   - Set environment variable:
     ```bash
     export GITHUB_TOKEN=your_token_here
     ```
   - Add to your shell profile (e.g., `~/.bashrc` or `~/.zshrc`) for persistence:
     ```bash
     echo 'export GITHUB_TOKEN=your_token_here' >> ~/.bashrc
     source ~/.bashrc
     ```

#### macOS Installation

1. **Install Python 3.6+** (if not already installed):
   - Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - Install Python: `brew install python`

2. **Clone or download the repository**:
   ```bash
   git clone https://github.com/your-repo/reconx-complete.git
   cd reconx-complete
   ```

3. **Install required Python packages**:
   ```bash
   pip3 install requests pandas reportlab beautifulsoup4 urllib3
   ```

   Or using requirements.txt (if available):
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Optional: Set up GitHub API token**:
   - Create a GitHub personal access token with public repository access
   - Set environment variable:
     ```bash
     export GITHUB_TOKEN=your_token_here
     ```
   - Add to your shell profile for persistence

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 512MB RAM
- **Storage**: ~50MB for the tool and dependencies
- **Network**: Stable internet connection for API calls

## How to Use It

### Basic Usage

1. **Run the tool**:
   ```bash
   python recon.py
   ```

2. **Enter target information**:
   - Target domain (e.g., `example.com`)
   - Base URL (optional, defaults to `https://target-domain`)

3. **Select scan type**:
   - 1: Full Reconnaissance (complete scan)
   - 2: URL Enumeration only
   - 3: Subdomain Enumeration only
   - 4: GitHub Reconnaissance only
   - 5: Directory Enumeration only

### Command Line Options

The tool currently uses an interactive menu, but you can modify it for command-line usage if needed.

### Example Usage

```bash
$ python recon.py

🎯 Enter target domain (e.g., example.com): example.com
🌐 Enter base URL (press Enter for https://example.com):

🔢 Enter your choice (1-5): 1

🚀 Starting FULL RECONNAISSANCE on example.com...
```

### Output and Results

- **Console Output**: Real-time results displayed during scanning
- **JSON Export**: Save complete results to JSON file
- **PDF Reports**: Professional formatted reports
- **Excel Reports**: Spreadsheet format for data analysis

### Advanced Features

- **Custom Wordlists**: Place a `wordlist.txt` file in the same directory for custom directory enumeration
- **Rate Limiting**: Built-in delays to respect API limits
- **Error Handling**: Robust error handling for network issues
- **Concurrent Scanning**: Multi-threaded directory enumeration for faster results

## Contributions

We welcome contributions to improve ReconX Complete! Here's how you can help:

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Contribution Guidelines

- **Code Style**: Follow PEP 8 Python style guidelines
- **Documentation**: Update README and docstrings for new features
- **Testing**: Test on multiple platforms (Windows, macOS, Linux)
- **Security**: Ensure no sensitive information is committed
- **Licensing**: All contributions must be compatible with the project license

### Areas for Improvement

- Additional reconnaissance modules
- Support for more export formats
- Integration with other security tools
- Performance optimizations
- GUI interface options

### Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include detailed steps to reproduce bugs
- Specify your Python version and operating system
- Attach relevant log files or screenshots

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Check code style
python -m flake8
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

ReconX Complete is intended for educational and authorized security research purposes only. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for any misuse or damage caused by this tool.

## Version History

- **v6.0.0**: Complete rewrite with Python-only methods, enhanced export features
- **v5.x**: Previous versions with external tool dependencies

## contributions:
Aditya Sadamwar [https://github.com/Aditya02-S/Reconx]
Manas Dabhane   [https://github.com/manas1020]
Sanika Gongale  [https://github.com/SanikaG31]
Dipti Bhangde   [https://github.com/diptibangde10]
---
**Author**: Security Research Team

**Version**: 6.0.0
