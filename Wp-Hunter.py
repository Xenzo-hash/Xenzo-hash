import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
import sys

# Banner for wp-hunter
banner = r"""
██╗    ██╗██████╗       ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██║    ██║██╔══██╗      ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
██║ █╗ ██║██████╔╝█████╗███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██║███╗██║██╔═══╝ ╚════╝██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
╚███╔███╔╝██║           ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝           ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
"""

# WordPress Color Codes
COLOR_BLUE = "\033[94m"   # WordPress Blue
COLOR_LIGHT_GRAY = "\033[97m"  # Light Gray
COLOR_DARK_GRAY = "\033[90m"    # Dark Gray
COLOR_RESET = "\033[0m"   # Reset color

def print_banner():
    print(COLOR_BLUE + banner + COLOR_RESET)

def print_help():
    """Display help information."""
    help_text = f"""
{COLOR_DARK_GRAY}Usage: wp-hunter [options]{COLOR_RESET}

{COLOR_LIGHT_GRAY}Options:
  --h, --help                      Show this help message and exit
  --url <URL>                      Specify the target WordPress site URL
  --username <USERNAME>            Specify the username for brute force login
  --password-file <FILE>           Specify the path to the password file
  --threads <NUMBER>               Specify the number of threads for brute force login

{COLOR_DARK_GRAY}Description:
  wp-hunter is a tool for scanning WordPress sites to detect the version,
  enumerate plugins, themes, and users, and perform brute force login attempts.

{COLOR_LIGHT_GRAY}Features:
  - **WordPress Version Detection**: Automatically detects and displays the version of the target WordPress site.
  - **Plugin Enumeration**: Lists all installed plugins along with their versions.
  - **Theme Enumeration**: Lists all installed themes along with their versions.
  - **User  Enumeration**: Retrieves and displays all registered users on the WordPress site.
  - **Brute Force Login**: Attempts to log in using a list of passwords for a specified username, utilizing multi-threading for speed.

{COLOR_DARK_GRAY}Examples:
  wp-hunter --url http://example.com --username admin --password-file passwords.txt --threads 10
  wp-hunter --h
{COLOR_RESET}
"""
    print(help_text)

def get_wordpress_version(url):
    """Detect WordPress version."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        if meta_generator:
            version = meta_generator.get('content')
            print(f"{COLOR_LIGHT_GRAY}[+] WordPress Version: {version}{COLOR_RESET}")
        else:
            print(f"{COLOR_DARK_GRAY}[-] WordPress version not found.{COLOR_RESET}")
    else:
        print(f"{COLOR_DARK_GRAY}[-] Unable to access {url}{COLOR_RESET}")

def enumerate_plugins(url):
    """Enumerate installed plugins."""
    response = requests.get(url + "/wp-json/wp/v2/plugins")
    if response.status_code == 200:
        plugins = response.json()
        print(f"{COLOR_LIGHT_GRAY}[+] Installed Plugins:{COLOR_RESET}")
        for plugin in plugins:
            print(f"   - {plugin['name']}: {plugin['version']}")
    else:
        print(f"{COLOR_DARK_GRAY}[-] Unable to enumerate plugins.{COLOR_RESET}")

def enumerate_themes(url):
    """Enumerate installed themes."""
    response = requests.get(url + "/wp-json/wp/v2/themes")
    if response.status_code == 200:
        themes = response.json()
        print(f"{COLOR_LIGHT_GRAY}[+] Installed Themes:{COLOR_RESET}")
        for theme in themes:
            print(f"   - {theme['name']}: {theme['version']}")
    else:
        print(f"{COLOR_DARK_GRAY}[-] Unable to enumerate themes.{COLOR_RESET}")

def enumerate_users(url):
    """Enumerate registered users."""
    response = requests.get(url + "/wp-json/wp/v2/users")
    if response.status_code == 200:
        users = response.json()
        print(f"{COLOR_LIGHT_GRAY}[+] Registered Users:{COLOR_RESET}")
        for user in users:
            print(f"   - {user['name']}: {user['slug']}")
    else:
        print(f"{COLOR_DARK_GRAY}[-] Unable to enumerate users.{COLOR_RESET}")

def brute_force_login(url, username, password_file, threads):
    """Perform brute force login attempts."""
    # Implement brute force login logic here
    pass

def main():
    if len(sys.argv) == 1:
        print_banner()
        print_help()
        sys.exit(0)

    if sys.argv[1] in ['-h', '--help']:
        print_banner()
        print_help()
        sys.exit(0)

    # Parse command-line arguments
    url = username = password_file = threads = None
    for arg in sys.argv[1:]:
        if arg.startswith('--url='):
            url = arg.split('=')[1]
        elif arg.startswith('--username='):
            username = arg.split('=')[1]
        elif arg.startswith('--password-file='):
            password_file = arg.split('=')[1]
        elif arg.startswith('--threads='):
            threads = int(arg.split('=')[1])

    if url:
        get_wordpress_version(url)
        enumerate_plugins(url)
        enumerate_themes(url)
        enumerate_users(url)
        if username and password_file and threads:
            brute_force_login(url, username, password_file, threads)

if __name__ == "__main__":
    main()
