import streamlit as st
import paramiko
from dataclasses import dataclass

@dataclass
class GhostServerConfig:
    ip: str
    username: str
    password: str
    install_path: str
    port: int
    db_name: str
    db_user: str
    db_password: str
    web_url: str
class GhostInstaller:
    def __init__(self, config: GhostServerConfig):
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

    def install_docker(self):
        """Install docker and its dependencies."""
        st.write("🗃️ Installing Docker...")
        docker_command = """
        apt-get update
        apt-get install -y docker docker-compose
        systemctl enable docker
        systemctl start docker
        """
        self._run_command(docker_command)
    
    def install_ghost(self):
        """Install Ghost using docker-compose."""
        st.write("🗃️ Installing Ghost using docker-compose...")

        compose_content = f"""
        version: '3.1'

        services:

        ghost:
            image: ghost:5-alpine
            restart: always
            ports:
            - {self.config.port}:2368
            environment:
            # see https://ghost.org/docs/config/#configuration-options
            database__client: mysql
            database__connection__host: db
            database__connection__user: {self.config.db_user}
            database__connection__password: {self.config.db_password}
            database__connection__database: {self.config.db_name}
            # this url value is just an example, and is likely wrong for your environment!
            url: {self.config.web_url}
            # contrary to the default mentioned in the linked documentation, this image defaults to NODE_ENV=production (so development mode needs to be explicitly specified if desired)
            #NODE_ENV: development
            volumes:
            - ghost:/var/lib/ghost/content

        db:
            image: mysql:8.0
            restart: always
            environment:
            MYSQL_ROOT_PASSWORD: {self.config.db_password}
            volumes:
            - db:/var/lib/mysql

        volumes:
        ghost:
        db:
        """

        # Buat file docker-compose.yml di server
        commands = [
            f"mkdir -p {self.config.install_path}",
            f'echo "{compose_content}" > {self.config.install_path}/docker-compose.yml',
            f"cd {self.config.install_path} && docker-compose up -d"
        ]

        for cmd in commands:
            self._run_command(cmd)
        
        st.success("✅ Ghost installed successfully with docker-compose!")
        self._run_command(ghost_commands)