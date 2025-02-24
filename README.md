# CMS INSTALLER

Simple CMS installer for your VPS.

## Supported Distributions

| Distro  | Status |
|---------|--------|
| `Debian` | ✅ |

## Features
- Automatic installation of WordPress and Ghost CMS
- Configures necessary dependencies
- Secure setup with minimal effort

## Requirements
- A Debian-based VPS
- Root or sudo access
- Minimum 1GB RAM (Recommended 2GB+ for Ghost CMS)

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
4. Follow the on-screen instructions to choose between WordPress and Ghost CMS.

## CMS Details

### WordPress
- Installs Apache, MySQL, PHP (LAMP Stack)
- Configures a new database for WordPress
- Sets up a WordPress installation automatically

### Ghost CMS
- Installs whole cms using Docker

## Usage
After installation, visit your server's IP or domain to access the CMS.
- WordPress: `http://yourdomain.com/wp-admin`
- Ghost: `http://yourdomain.com`

## License
This project is licensed under the MIT License.

## Contributing
Feel free to contribute by submitting issues or pull requests!


