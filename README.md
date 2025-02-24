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

1. Clone the repository:
   ```sh
   git clone https://github.com/yourrepo/cms-installer.git
   cd cms-installer
   ```
2. Make the script executable:
   ```sh
   chmod +x install.sh
   ```
3. Run the installer:
   ```sh
   sudo ./install.sh
   ```
4. Follow the on-screen instructions to select and install WordPress or Ghost CMS.

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

## Uninstallation
To remove the CMS, run:
```sh
sudo ./uninstall.sh
```

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License.

## Author
Your Name - [yourwebsite.com](https://yourwebsite.com)

