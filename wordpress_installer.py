import streamlit as st
import paramiko
import requests
from dataclasses import dataclass

@dataclass
class WordPressServerConfig:
    ip: str
    username: str
    password: str
    wp_version: str
    install_path: str
    port: int
    server_type: str
    db_name: str
    db_user: str
    db_password: str

class WordPressInstaller:
    def __init__(self, config: WordPressServerConfig):
        self.config = config
        self.client = None

    def connect(self) -> bool:
        """Establish SSH connection to server."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.config.ip,
                port=22,
                username=self.config.username,
                password=self.config.password,
                timeout=10
            )
            return True
        except Exception as e:
            st.error(f"❌ Failed to connect to server: {e}")
            return False

    def _run_command(self, command: str):
        """Run SSH command and handle output."""
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode().strip(), stderr.read().decode().strip()

    def install_mariadb(self):
        """Install MariaDB and its dependencies."""
        st.write("🗃️ Installing MariaDB...")
        mariadb_commands = """
        apt-get update
        apt-get install -y mariadb-server mariadb-client
        systemctl enable mariadb
        systemctl start mariadb
        """
        self._run_command(mariadb_commands)

    def configure_database(self):
        """Create database for WordPress."""
        st.write("🛠️ Configuring WordPress database...")
        db_commands = f"""
        mysql -u root <<MYSQL_SCRIPT
        CREATE DATABASE IF NOT EXISTS {self.config.db_name};
        CREATE USER IF NOT EXISTS '{self.config.db_user}'@'localhost' IDENTIFIED BY '{self.config.db_password}';
        GRANT ALL PRIVILEGES ON {self.config.db_name}.* TO '{self.config.db_user}'@'localhost';
        FLUSH PRIVILEGES;
        MYSQL_SCRIPT
        """
        self._run_command(db_commands)

    def configure_webserver(self):
        """Configure web server with specified port."""
        st.write("🌐 Configuring web server...")
        if self.config.server_type == "nginx":
            config_nginx = f"""
            server {{
                listen {self.config.port};
                server_name _;
                root {self.config.install_path};
                index index.php index.html index.htm;

                location / {{
                    try_files $uri $uri/ /index.php?$args;
                }}

                location ~ \\.php$ {{
                    include snippets/fastcgi-php.conf;
                    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
                    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                    include fastcgi_params;
                }}
            }}
            """
            self._run_command(f"echo '{config_nginx}' > /etc/nginx/sites-available/wordpress")
            self._run_command("ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/")
            self._run_command("systemctl restart nginx")
        else:  # Apache2
            st.write("🔧 Configuring Apache2...")
            self._run_command(f"sed -i 's/^Listen .*/Listen {self.config.port}/' /etc/apache2/ports.conf")

            config_apache = f"""
            <VirtualHost *:{self.config.port}>
                ServerAdmin webmaster@localhost
                DocumentRoot "{self.config.install_path}"

                <Directory "{self.config.install_path}">
                    Options Indexes FollowSymLinks
                    AllowOverride All
                    Require all granted
                </Directory>

                ErrorLog ${{APACHE_LOG_DIR}}/error.log
                CustomLog ${{APACHE_LOG_DIR}}/access.log combined
            </VirtualHost>
            """
            self._run_command(f"echo '{config_apache}' > /etc/apache2/sites-available/wordpress.conf")
            self._run_command("a2ensite wordpress.conf")
            self._run_command("a2enmod rewrite")
            self._run_command("systemctl restart apache2")

    def setup_firewall(self):
        """Adjust firewall to open specified port."""
        st.write("🛡️ Configuring firewall...")
        self._run_command(f"ufw allow {self.config.port}/tcp")
        self._run_command("ufw --force enable")

    def setup_php(self):
        """Install and configure PHP."""
        st.write("🐘 Installing and configuring PHP...")
        php_commands = """
        apt install php8.2 php8.2-curl php8.2-fpm php8.2-bcmath php8.2-gd php8.2-soap php8.2-zip php8.2-mbstring php8.2-mysqlnd php8.2-mysql php8.2-mysqli php8.2-xml php8.2-intl -y
        """
        self._run_command(php_commands)

        # Configure PHP-FPM for nginx
        if self.config.server_type == "nginx":
            self._run_command("sed -i 's/user = www-data/user = nginx/' /etc/php/8.2/fpm/pool.d/www.conf")
            self._run_command("sed -i 's/group = www-data/group = nginx/' /etc/php/8.2/fpm/pool.d/www.conf")
            self._run_command("systemctl restart php8.2-fpm")

    def install_wordpress(self):
        """Download and install WordPress."""
        st.write("📥 Downloading and installing WordPress...")

        # Ensure WordPress installation directory exists
        self._run_command(f"mkdir -p {self.config.install_path}")

        # Download and extract WordPress
        # Fix: Use correct download URL for specified version
        download_url = (
            "https://wordpress.org/latest.tar.gz" 
            if self.config.wp_version == "latest" 
            else f"https://wordpress.org/wordpress-{self.config.wp_version}.tar.gz"
        )
        
        self._run_command(f"wget {download_url} -O /tmp/wordpress.tar.gz")
        self._run_command(f"tar -xzf /tmp/wordpress.tar.gz -C {self.config.install_path} --strip-components=1")

        # Set permissions
        self._run_command(f"chown -R www-data:www-data {self.config.install_path}")
        self._run_command(f"chmod -R 755 {self.config.install_path}")

    def create_wp_config(self):
        """Create wp-config.php file."""
        st.write("⚙️ Creating wp-config.php...")

        # Generate salt keys
        try:
            response = requests.get("https://api.wordpress.org/secret-key/1.1/salt/")
            salt_keys = response.text.strip() if response.status_code == 200 else """
            define('AUTH_KEY',         'put your unique phrase here');
            define('SECURE_AUTH_KEY',  'put your unique phrase here');
            define('LOGGED_IN_KEY',    'put your unique phrase here');
            define('NONCE_KEY',        'put your unique phrase here');
            define('AUTH_SALT',        'put your unique phrase here');
            define('SECURE_AUTH_SALT', 'put your unique phrase here');
            define('LOGGED_IN_SALT',   'put your unique phrase here');
            define('NONCE_SALT',       'put your unique phrase here');
            """
        except:
            salt_keys = """
            define('AUTH_KEY',         'put your unique phrase here');
            define('SECURE_AUTH_KEY',  'put your unique phrase here');
            define('LOGGED_IN_KEY',    'put your unique phrase here');
            define('NONCE_KEY',        'put your unique phrase here');
            define('AUTH_SALT',        'put your unique phrase here');
            define('SECURE_AUTH_SALT', 'put your unique phrase here');
            define('LOGGED_IN_SALT',   'put your unique phrase here');
            define('NONCE_SALT',       'put your unique phrase here');
            """

        config_content = f"""<?php
define('DB_NAME', '{self.config.db_name}');
define('DB_USER', '{self.config.db_user}');
define('DB_PASSWORD', '{self.config.db_password}');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

{salt_keys}

$table_prefix = 'wp_';

if (!defined('ABSPATH')) {{
    define('ABSPATH', __DIR__ . '/');
}}

require_once ABSPATH . 'wp-settings.php';
"""

        # Create wp-config.php in WordPress installation directory
        config_path = f"{self.config.install_path}/wp-config.php"
        
        # Use command to write the file and set permissions
        self._run_command(f"echo '{config_content}' > {config_path}")
        self._run_command(f"chmod 644 {config_path}")
        
        # Verify file creation
        st.write(f"📄 wp-config.php created at {config_path}")