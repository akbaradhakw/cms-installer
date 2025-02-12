import streamlit as st
from wordpress_installer import WordPressInstaller, WordPressServerConfig
from ghost_installer import GhostInstaller, GhostServerConfig

def main():
    st.title("🚀 CMS Auto-Installer")

    # Sidebar for CMS selection
    cms_options = ["WordPress", "Ghost CMS"]
    selected_cms = st.sidebar.selectbox("Select CMS", cms_options)

    # Shared configuration inputs
    with st.form("cms_installer"):
        # Server Connection Details
        st.header("🔐 Server Connection")
        col1, col2 = st.columns(2)
        with col1:
            ip = st.text_input("Server IP", "192.168.1.100")
            username = st.text_input("SSH Username", "root")
        with col2:
            password = st.text_input("SSH Password", type="password")
            if selected_cms == "WordPress":
                server_type = st.selectbox("Web Server", ["apache2", "nginx"])

        # Installation Details
        st.header("⚙️ Installation Configuration")
        col3, col4 = st.columns(2)
        with col3:
            port = st.number_input("Web Server Port", min_value=1, max_value=65535, value=8082)
            if selected_cms == "WordPress":
                install_path = st.text_input("Installation Path", "/var/www/html/cms")
            else:  # Ghost CMS
                install_path = st.text_input("Installation Path", "/var/www/html/cms")
                web_url = st.text_input("Website URL", "http://localhost:2368")

        # CMS Specific Configurations
        with col4:
            if selected_cms == "WordPress":
                wp_versions = ["latest", "6.2", "6.1", "6.0", "5.9"]
                version = st.selectbox("WordPress Version", wp_versions)
                db_name = st.text_input("Database Name", "wordpress_db")
                db_user = st.text_input("Database Username", "wp_user")
                db_password = st.text_input("Database Password", type="password")
            else:  # Ghost CMS
                ghost_versions = ["latest"]
                version = st.selectbox("Ghost Version", ghost_versions)
                db_name = st.text_input("Database Name", "ghost_db")
                db_user = st.text_input("Database Username", "ghost_user")
                db_password = st.text_input("Database Password", type="password")

        # Submit Button
        submitted = st.form_submit_button("🚀 Install CMS")

        if submitted:
            try:
                if selected_cms == "WordPress":
                    config = WordPressServerConfig(
                        ip, username, password, 
                        version, 
                        install_path, port, server_type, 
                        db_name, db_user, db_password
                    )
                    installer = WordPressInstaller(config)
                else:
                    config = GhostServerConfig(
                        ip, username, password, 
                        install_path, port, 
                        db_name, db_user, db_password, web_url
                    )
                    installer = GhostInstaller(config)

                if installer.connect():

                    # CMS-specific installation steps
                    if selected_cms == "WordPress":
                        installer.install_mariadb()
                        installer.configure_database()
                        installer.configure_webserver()
                        installer.setup_php()
                        installer.install_wordpress()
                        installer.create_wp_config()
                        installer.setup_firewall()
                    else:
                        installer.install_docker()  
                        installer.install_ghost()

                    st.success(f"🎉 {selected_cms} successfully installed on port {port}!")

            except Exception as e:
                st.error(f"❌ Installation failed: {e}")

if __name__ == "__main__":
    main()