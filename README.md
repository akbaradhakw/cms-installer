# CMS Installer

A simple CMS installer for your VPS, supporting WordPress and Ghost CMS.

## Features
- Automated installation of WordPress and Ghost CMS
- Configuration of necessary dependencies
- Secure and optimized setup
- Easy-to-use installation process

## Prerequisites
- A Debian-based VPS
- Root or sudo access
- Minimum 1GB RAM (2GB+ recommended for Ghost CMS)

## Installation
1. Install python & dependency:
   ```py
   sudo apt install python3 && pip install streamlit paramiko
   ```
2. Clone the repository:
   ```py
   git clone https://github.com/yourrepo/cms-installer.git && cd cms-installer
   ```
3. Run the installer:
   ```py
   python3 -m paramiko run main_installer.py
   ```
5. Open localhost:8501 or yourip:8501 and follow the instruction.

## CMS Installation Details

### WordPress
- Installs and configures LAMP Stack (Apache, MySQL, PHP)
- Sets up a new database and WordPress instance
- Provides a secure initial setup

### Ghost CMS
- Deploys Ghost CMS using Docker
- Sets up a MySQL database container
- Ensures Ghost runs as a Docker container for better manageability

## Accessing Your CMS
After installation, visit your server’s IP or domain:
- **WordPress**: `http://yourdomain.com/wp-admin`
- **Ghost**: `http://yourdomain.com`

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.
[![Contributors](https://contrib.rocks/image?repo=akbaradhakw/cms-installer&max=10)](https://github.com/akbaradhakw/cms-installer/graphs/contributors)

## License
This project is licensed under the MIT License.

## Author
Baryoks - [aryok.me](https://aryok.me)

