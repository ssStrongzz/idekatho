import os

import requests

import json

import time

import subprocess

import asyncio

import aiohttp

import threading

import psutil

import crypto

import platform

import uuid 

import hashlib

import sqlite3

import shutil

from colorama import init, Fore, Style

from datetime import datetime

from pystyle import *
from pystyle import Colors, Colorate, Write

from licensing.models import *
from licensing.methods import Key, Helpers

# Initialize colorama

init()

RSAPubKey = "<RSAKeyValue><Modulus>3wyUhdgm+VGJrPFLZRBMObDNzaV+xHoca2eixW3H8j41EM9ssmPoID11sFfKcDfAlu8+hxp2ZhrdfjK+u96qYBjxm0BxwUqYZi6GInANqhOuM+iLmR8jytwqeM+emxqw8fpyETzq6vQSg8XM8wcGfUYPfMSZ4bFxEv4aMyq2LIc65Ei16zEbGPWGaEhyV1Lyxius7E2mp3dscmLRd7Z7YJP14DMc0lwiyDJD1xBd5uRn3ZLgePxDpDC0SVPhsJOEzWDDNz2nzgb07YOzdDmmmc6luAcahAa9EMWJq65z8bYxwOvwl8C5HSp76rlzwP0LCFrkhcqyb3WRPR0yoB2THw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"# ENTER RSAKEY
auth = "WyI5MTUyNjk5OSIsImU1aXhvWDhTQm1TNWJQMFNMS2VZSGJXZk10bzFLVXNvOUtjRU5KYzgiXQ==" ## AUTHKEY WITH ACTIVATE !

SERVER_LINKS_FILE = "/storage/emulated/0/Download/server_links.txt"

ACCOUNTS_FILE = "/storage/emulated/0/Download/accounts.txt"

CONFIG_FILE = "/storage/emulated/0/Download/config.json"

webhook_url = None

device_name = None

interval = None

stop_webhook_thread = False

webhook_thread = None


package_statuses = {}

username_cache = {}

CACHE_FILE = "/storage/emulated/0/Download/username_cache.json"

cache_save_interval = 600  # Save the cache every 10 minutes

stop_event = threading.Event()
# Function to print the header

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')



def print_header():

    logo = """

     ░▒▓██████▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓████████▓▒░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
                                                           
    """

    credit = """
    [+] made by idnohw tamvan | tools ver 0.2 [BETA]
    """

    credit2 = """
    [!] Please tell me the bugs on #bug-report! <3
            
            
    """
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(logo)))
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(credit)))
    print(Colorate.Horizontal(Colors.yellow_to_red, Center.XCenter(credit2)))





def create_dynamic_menu(options):

    # Determine the maximum width needed for the menu

    max_option_length = max(len(option) + 2 for option in options)  # +2 for number and dot

    

    # Create dynamic menu box

    #top_border = f"{Fore.LIGHTCYAN_EX}╔{'═' * (max_option_length + 4)}╗"

    #bottom_border = f"╚{'═' * (max_option_length + 4)}╝{Style.RESET_ALL}"

    menu_content = [f"{Fore.WHITE}[ {i+1} ] {option.ljust(max_option_length)}" 

                    for i, option in enumerate(options)]

    

    # Print the menu

    #print(top_border)
    print(Fore.CYAN + "[>] Command list -> \n")

    for line in menu_content:

        print(line)

    #print(bottom_border)
    
def update_status_table(package_statuses):
    clear_screen()
    print_header()

    # Calculate the maximum width required for each column
    max_username_width = max(len(info['Username']) for info in package_statuses.values())
    max_status_width = max(len(info['Status']) for info in package_statuses.values())
    max_datetime_width = len(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Define minimum widths to ensure columns are not too narrow
    min_username_width = 12
    min_status_width = 8
    min_datetime_width = 20

    # Set column widths based on the maximum or minimum required, with additional padding
    datetime_width = max(max_datetime_width, min_datetime_width) + 2  # Added padding
    username_width = max(max_username_width, min_username_width) + 2  # Added padding
    status_width = max(max_status_width, min_status_width) + 2  # Added padding

    # Calculate the total width of the table including separators and borders
    total_width = datetime_width + 2 + username_width + 2 + status_width + 2 + 3  # Extra space for separators and border symbols

    # Create the top and bottom borders with '+' and '-' symbols
    top_border = Fore.CYAN + "+" + "-" * (total_width - 2) + "+"
    bottom_border = Fore.CYAN + f"+{'-' * (total_width - 2)}+" + Style.RESET_ALL

    # Create a formatted string for each package status
    data_lines = []
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for info in package_statuses.values():
        line = f"{current_datetime.ljust(datetime_width)} | {info['Username'].ljust(username_width)} | {info['Status'].ljust(status_width)}"
        data_lines.append(f"| {line.ljust(total_width + 5)} |")  # Adjust width to fit within the borders

    # Print the table
    print(top_border)
    for line in data_lines:
        print(line)
    print(bottom_border)

def auto_save_cache():

    while not stop_event.is_set():  # Use the stop_event to check if thread should stop

        time.sleep(cache_save_interval)

        save_cache()

        print(Fore.GREEN + "<1>" + Style.RESET_ALL)



def verify_cookie(cookie_value):

    try:

        # Set the headers with the cookie

        headers = {

            'Cookie': f'.ROBLOSECURITY={cookie_value}',

            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',

            'Referer': 'https://www.roblox.com/',

            'Origin': 'https://www.roblox.com',

            'Accept-Language': 'en-US,en;q=0.9',

            'Accept-Encoding': 'gzip, deflate, br',

            'Connection': 'keep-alive'

        }



        # Introduce a small delay to mimic a more natural request pattern

        time.sleep(1)



        # Make a GET request to the authentication endpoint

        response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)



        if response.status_code == 200:

            # The user is authenticated

            return True

        elif response.status_code == 401:

            # Unauthorized, the cookie is invalid

            print(Fore.RED + "[x] Maybe check the cookie? Failed." + Style.RESET_ALL)

            return False

        else:

            # Some other error occurred

            print(Fore.RED + f"[!] You must check the cookie i think!" + Style.RESET_ALL)

            return False



    except Exception as e:

        print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)

        return False

        

def download_file(url, destination, binary=False):

    try:

        response = requests.get(url, stream=True)

        if response.status_code == 200:

            mode = 'wb' if binary else 'w'

            with open(destination, mode) as file:

                if binary:

                    shutil.copyfileobj(response.raw, file)

                else:

                    file.write(response.text)

            return destination

        else:

            return None

    except Exception as e:

        return None



# Function to replace the .ROBLOSECURITY cookie value in Cookies.db using sqlite3

def replace_cookie_value_in_db(db_path, new_cookie_value):

    try:

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()



        # First, check if the .ROBLOSECURITY cookie exists

        cursor.execute("""

            SELECT COUNT(*) FROM cookies WHERE host_key = '.roblox.com' AND name = '.ROBLOSECURITY'

        """)

        cookie_exists = cursor.fetchone()[0]



        if cookie_exists:

            # Update the existing cookie

            cursor.execute("""

                UPDATE cookies

                SET value = ?, last_access_utc = ?, expires_utc = ?

                WHERE host_key = '.roblox.com' AND name = '.ROBLOSECURITY'

            """, (new_cookie_value, int(time.time() * 1000000), 99999999999999999))

        else:

            # Insert the cookie if it doesn't exist

            cursor.execute("""

                INSERT INTO cookies (creation_utc, host_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc)

                VALUES (?, '.roblox.com', '.ROBLOSECURITY', ?, '/', 99999999999999999, 0, 0, ?)

            """, (int(time.time() * 1000000), new_cookie_value, int(time.time() * 1000000)))



        conn.commit()

        conn.close()



    except sqlite3.OperationalError as e:

        print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)

    except Exception as e:

        print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)



def inject_cookies_and_appstorage():

    # Ensure the Google Drive link is correct

    db_url = "https://github.com/shirooscripts/auto-rj/raw/main/Cookies"  # Keep this as binary

    appstorage_url = "https://raw.githubusercontent.com/shirooscripts/auto-rj/main/appStorage.json"  # Use this for JSON



    # Download the files correctly

    downloaded_db_path = download_file(db_url, "/storage/emulated/0/Download/Cookies.db", binary=True)

    downloaded_appstorage_path = download_file(appstorage_url, "/storage/emulated/0/Download/appStorage.json", binary=False)



    if not downloaded_db_path or not downloaded_appstorage_path:

        return

    

    # Path to cookie.txt file

    cookie_txt_path = os.path.join(os.getcwd(), "/storage/emulated/0/Download/cookie.txt")  # cookie.txt in the same directory as the script

    

    # Check if the cookie.txt file exists

    if not os.path.exists(cookie_txt_path):

        return



    # Read cookies from the cookie.txt file

    with open(cookie_txt_path, "r") as file:

        cookies = [line.strip() for line in file.readlines()]



    # Check if there are cookies to inject

    if not cookies:

        print(Fore.RED + "[!] Make cookie.txt in Download Folder!" + Style.RESET_ALL)

        return



    # Get the Roblox packages

    packages = get_roblox_packages()

    count_packages = count_roblox_processes()

    if len(cookies) > len(packages):

        print(Fore.RED + "[!] You inputed extra cookie than roblox installed." + Style.RESET_ALL)

        time.sleep(2)

        return



    # Inject each cookie and appStorage.json into its corresponding package

    for idx, package_name in enumerate(packages):

        try:

            if idx < len(cookies):

                cookie = cookies[idx]

                

                # Verify the cookie before injection

                if verify_cookie(cookie):

                    print(Fore.GREEN + f"[+] {package_name}: Cookie is valid!." + Style.RESET_ALL)

                else:

                    print(Fore.RED + f"[!] Maybe check the cookie?" + Style.RESET_ALL)

                    continue

                

                # Paths to the destination directories

                destination_db_dir = f"/data/data/{package_name}/app_webview/Default/"

                destination_appstorage_dir = f"/data/data/{package_name}/files/appData/LocalStorage/"



                # Ensure directories exist

                os.makedirs(destination_db_dir, exist_ok=True)

                os.makedirs(destination_appstorage_dir, exist_ok=True)



                # Copy the downloaded Cookies.db to the destination

                destination_db_path = os.path.join(destination_db_dir, "Cookies")

                shutil.copyfile(downloaded_db_path, destination_db_path)



                # Inject the appStorage.json

                destination_appstorage_path = os.path.join(destination_appstorage_dir, "appStorage.json")

                shutil.copyfile(downloaded_appstorage_path, destination_appstorage_path)



                # Replace the cookie value in the database

                replace_cookie_value_in_db(destination_db_path, cookie)



                # Verify the cookie after injection


        except Exception as e:

            print(Fore.RED + f"[x] Error > {package_name}: {e}" + Style.RESET_ALL)
    
    def launch_roblox(package_name, num_packages):

        try:

            subprocess.run(['am', 'start', '-n', f'{package_name}/com.roblox.client.startup.ActivitySplash'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

            time.sleep(15 if num_packages >= 6 else 8)  # Wait depending on the number of packages

        except Exception as e:

            print(f"[x] Error: {e}")

    print(Fore.GREEN + "[+] Auto Login with Cookie are done." + Style.RESET_ALL)

    print(Fore.GREEN + "[>] Refreshing the Username & ID.")

    kill_roblox_processes()

    for pkg in packages:

        launch_roblox(pkg, count_packages)
    
    time.sleep(2)
    
    kill_roblox_processes()

    time.sleep(2)

            

# Function to get Roblox packages

def get_roblox_packages():

    packages = []

    for suffix in ['u', 'v', 'w', 'x', 'y', 'z', 'p', 'q', 'r', 's']:

        package_name = f"com.roblox.clien{suffix}"

        if os.system(f"pm list packages | grep -q '{package_name}'") == 0:

            packages.append(package_name)

    return packages



# Function to capture a screenshot using Android's screencap command

def capture_screenshot():

    screenshot_path = "/data/data/com.termux/files/home/screenshot.png"

    os.system(f"screencap -p {screenshot_path}")

    return screenshot_path



# Function to retrieve system information

def get_system_info():

    cpu_usage = psutil.cpu_percent(interval=1)

    memory_info = psutil.virtual_memory()

    uptime = time.time() - psutil.boot_time()



    system_info = {

        "cpu_usage": cpu_usage,

        "memory_total": memory_info.total,

        "memory_available": memory_info.available,

        "memory_used": memory_info.used,

        "uptime": uptime

    }

    

    return system_info



# Function to load configuration from file

def load_config():

    global webhook_url, device_name, interval

    if os.path.exists(CONFIG_FILE):

        with open(CONFIG_FILE, "r") as file:

            config = json.load(file)

            webhook_url = config.get("webhook_url")

            device_name = config.get("device_name")

            interval = config.get("interval")

    else:

        webhook_url = None

        device_name = None

        interval = None

def delete_files(path, file_names):

    for file_name in file_names:

        file_path = os.path.join(path, file_name)
        
        # Check if the file exists before attempting to delete it
        if os.path.isfile(file_path):

            try:

                os.remove(file_path)

                print(f"File {file_name} removed successfully.")

            except Exception as e:

                print(f"Failed to remove {file_name}: {e}")

        else:

            print(f"File {file_name} does not exist in {path}.")


# Function to save configuration to file

def save_config():

    config = {

        "webhook_url": webhook_url,

        "device_name": device_name,

        "interval": interval

    }

    with open(CONFIG_FILE, "w") as file:

        json.dump(config, file)



def start_webhook_thread():

    global webhook_thread, stop_webhook_thread

    if webhook_thread is None or not webhook_thread.is_alive():

        stop_webhook_thread = False

        webhook_thread = threading.Thread(target=send_webhook)

        webhook_thread.start()

		

def count_roblox_processes():

    count = 0

    for proc in psutil.process_iter(['name']):

        if 'roblox' in proc.info['name'].lower():

            count += 1

    return count

	

def send_webhook():

    global stop_webhook_thread



    while not stop_webhook_thread:

        # Capture a screenshot

        screenshot_path = capture_screenshot()

        def get_roblox_packages(num):

            base_package = "com.roblox.clien"

            suffixes = "uvwxyzpqr"

            packages = [base_package + suffix for suffix in suffixes[:num]]
            
            return "\n".join(packages)

        # Get system information

        system_info = get_system_info()

        process_count = count_roblox_processes()  # Get the number of open Roblox packages

        roblox_process_count = get_roblox_packages(process_count)

        # Prepare the embed data

        embed = {

            "title": f"System Info for {device_name}",

            "color": 15258703,

            "fields": [

                {

                    "name": "Device Name",

                    "value": device_name,

                    "inline": True

                },

                {

                    "name": "CPU Usage",

                    "value": f"{system_info['cpu_usage']}%",

                    "inline": True

                },

                {

                    "name": "Uptime",

                    "value": f"{system_info['uptime'] / 3600:.2f} hours",

                    "inline": True

                },

                {

                    "name": "Open Roblox Packages",

                    "value": f"{roblox_process_count}",

                    "inline": True

                }

            ],

            "image": {

                "url": "attachment://screenshot.png"

            }

        }



        # JSON payload

        payload = {

            "embeds": [embed],

            "username": "Ailox Rejoiner"

        }



        # Sending POST request to the webhook URL with the image as an attachment

        with open(screenshot_path, "rb") as file:

            response = requests.post(

                webhook_url,

                data={"payload_json": json.dumps(payload)},

                files={"file": ("screenshot.png", file)}

            )



        if response.status_code == 204 or response.status_code == 200:

            print(Fore.GREEN + "[+] Webhook Sended Successfully" + Style.RESET_ALL)

        else:

            print(Fore.RED + f"[x] Error: {response.status_code}" + Style.RESET_ALL)



        # Delete the screenshot file silently

        try:

            os.remove(screenshot_path)

        except Exception as e:

            print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)



        # Wait for the specified interval before sending the next webhook

        time.sleep(interval * 60)  



def stop_webhook():

    global stop_webhook_thread

    stop_webhook_thread = True

    stop_event.set()  # Signal the thread to stop

    



# Function to prompt for webhook URL, device name, and interval

def setup_webhook():

    global webhook_url, device_name, interval, stop_webhook_thread



    stop_webhook_thread = True  # Stop any existing webhook thread



    webhook_url = input(Fore.GREEN + "[+] Enter Your Discord URL: " + Style.RESET_ALL)

    device_name = input(Fore.GREEN + "[+] Enter Device Name: " + Style.RESET_ALL) 

    interval = int(input(Fore.GREEN + "[+] Interval of Webhook Sending: " + Style.RESET_ALL))



    save_config()  # Save the configuration



    stop_webhook_thread = False

def fluxus_hwid():

    def launch_roblox(package_name, server_link, num_packages):

        try:

            subprocess.run(['am', 'start', '-n', f'{package_name}/com.roblox.client.startup.ActivitySplash', '-d', server_link], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            

            time.sleep(15 if num_packages >= 6 else 8)  # Wait depending on the number of packages


            subprocess.run(['am', 'start', '-n', f'{package_name}/com.roblox.client.ActivityProtocolLaunch', '-d', server_link], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            time.sleep(20)

        except Exception as e:

            print(f"[x] Error: {e}")

    print(Fore.RED + "[!] Getting all HWID First, Dont touch anything!" + Style.RESET_ALL)

    count_packages = count_roblox_processes()

    avaible_packages = get_roblox_packages()

    for pkg in avaible_packages:

        directory = f"/data/data/{pkg}/app_assets/content/"

        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        if not files:

            print(Fore.YELLOW + f"[!] {pkg}: No HWID Found, Getting HWID first!" + Style.RESET_ALL)

            launch_roblox(pkg, "https://www.roblox.com/games/920587237?privateServerLinkCode=51979231498527920056172713087652", count_packages)
        
        else:

            print(Fore.YELLOW + f"[!] {pkg}: HWID Has been found!" + Style.RESET_ALL)

            continue

    kill_roblox_processes()

    print(Fore.YELLOW + "[!] RE-Checking HWID Again!" + Style.RESET_ALL)

    for pkg in avaible_packages:

        directory = f"/data/data/{pkg}/app_assets/content/"

        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        if not files:

            print(Fore.YELLOW + f"[!] {pkg}: No HWID Found, Getting HWID first!" + Style.RESET_ALL)

            launch_roblox(pkg, "https://www.roblox.com/games/920587237?privateServerLinkCode=51979231498527920056172713087652", count_packages)
        
        else:

            print(Fore.YELLOW + f"[!] {pkg}: HWID Has been found!" + Style.RESET_ALL)

            continue

    hwid = input(Fore.WHITE + "[>] Enter your Main HWID: ")

    for package in avaible_packages:

        directory  = f"/data/data/{package}/app_assets/content/"

        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        for file_name in files:

            file_path = os.path.join(directory, file_name)
            
            if os.path.isfile(file_path):
                # Buka file dalam mode penulisan ('w') untuk menghapus teks lama dan menulis teks baru
                with open(file_path, 'w', encoding='utf-8') as file:

                    file.write(hwid)

                print("[+] HWID Updated to the main HWID.")

            else:

                print("[x] HWID Not Found maybe open roblox manually?")

                time.sleep(2)
    


# Function to check if a Roblox process is running

def is_roblox_running(package_name):

    for proc in psutil.process_iter(['name']):

        if package_name in proc.info['name'].lower():

            return True

    return False



# Function to kill Roblox processes

def kill_roblox_processes():


    package_names = get_roblox_packages()

    for package_name in package_names:


        # Use pkill to kill processes by package name

        os.system(f"pkill -f {package_name}")

    time.sleep(2) 



# Function to kill a specific Roblox process

def kill_roblox_process(package_name):


    # Use pkill to kill process by package name

    os.system(f"pkill -f {package_name}")

    time.sleep(2) 



# Function to launch Roblox

def launch_roblox(package_name, server_link, num_packages, package_statuses):

    try:

        subprocess.run(['am', 'start', '-n', f'{package_name}/com.roblox.client.startup.ActivitySplash', '-d', server_link], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        

        time.sleep(15 if num_packages >= 6 else 8)  # Wait depending on the number of packages


        subprocess.run(['am', 'start', '-n', f'{package_name}/com.roblox.client.ActivityProtocolLaunch', '-d', server_link], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        

        time.sleep(20)

        package_statuses[package_name]["Status"] = Fore.GREEN + "RUNNING" + Style.RESET_ALL

        update_status_table(package_statuses)

    except Exception as e:

        package_statuses[package_name]["Status"] = Fore.RED + f"ERROR" + Style.RESET_ALL

        update_status_table(package_statuses)


        

# Function to format server link

def format_server_link(input_link):

    if 'roblox.com' in input_link:

        return input_link

    elif input_link.isdigit():

        return f'roblox://placeID={input_link}'

    else:

        print(Fore.RED + "[!] What is that game? are you sure avaible on roblox?" + Style.RESET_ALL)

        return None



# Function to save server links to file

def save_server_links(server_links):

    with open(SERVER_LINKS_FILE, "w") as file:

        for package, link in server_links:

            file.write(f"{package},{link}\n")



# Function to load server links from file

def load_server_links():

    server_links = []

    if os.path.exists(SERVER_LINKS_FILE):

        with open(SERVER_LINKS_FILE, "r") as file:

            for line in file:

                package, link = line.strip().split(",", 1)

                server_links.append((package, link))

    return server_links



# Function to save accounts to file

def save_accounts(accounts):

    with open(ACCOUNTS_FILE, "w") as file:

        for package, user_id in accounts:

            file.write(f"{package},{user_id}\n")



# Function to load accounts from file

def load_accounts():

    accounts = []

    if os.path.exists(ACCOUNTS_FILE):

        with open(ACCOUNTS_FILE, "r") as file:

            for line in file:

                package, user_id = line.strip().split(",", 1)

                accounts.append((package, user_id))

    return accounts



# Function to find UserId from file

def find_userid_from_file(file_path):

    try:

        with open(file_path, 'r') as file:

            content = file.read()

            # Debugging information removed to keep console clean



            userid_start = content.find('"UserId":"')

            if userid_start == -1:

                return None



            userid_start += len('"UserId":"')

            userid_end = content.find('"', userid_start)

            if userid_end == -1:

                return None



            userid = content[userid_start:userid_end]

            return userid



    except IOError as e:

        print(f"[x] Error: {e}")

        return None



# Asynchronous function to get user ID from username

async def get_user_id(username):

    url = "https://users.roblox.com/v1/usernames/users"

    payload = {

        "usernames": [username],

        "excludeBannedUsers": True

    }

    headers = {

        "Content-Type": "application/json"

    }



    async with aiohttp.ClientSession() as session:

        async with session.post(url, json=payload, headers=headers) as response:

            data = await response.json()

            if 'data' in data and len(data['data']) > 0:

                return data['data'][0]['id']

    return None

def extract_current_cookie_from_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT value FROM cookies WHERE host_key = '.roblox.com' AND name = '.ROBLOSECURITY'
        """)

        current_cookie = cursor.fetchone()

        conn.close()

        if current_cookie:
            return current_cookie[0]
        else:
            return None

    except sqlite3.OperationalError as e:
        print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)
        return None
    except Exception as e:
        print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)
        return None
    
# Function to get username from user ID

def get_username(user_id):

    retry_attempts = 2

    for attempt in range(retry_attempts):

        try:

            url = f"https://users.roblox.com/v1/users/{user_id}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            username = data.get("name", "Unknown")

            if username != "Unknown":

                username_cache[user_id] = username

                save_username(user_id, username)

                return username

        except requests.exceptions.RequestException as e:

            print(Fore.RED + f"Attempt {attempt + 1} failed for Roblox Users API: {e}" + Style.RESET_ALL)

            time.sleep(2 ** attempt)  # Exponential backoff



    # Fallback to RoProxy API

    for attempt in range(retry_attempts):

        try:

            url = f"https://users.roproxy.com/v1/users/{user_id}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            username = data.get("name", "Unknown")

            if username != "Unknown":

                username_cache[user_id] = username

                save_username(user_id, username)

                return username

        except requests.exceptions.RequestException as e:

            print(Fore.RED + f"Attempt {attempt + 1} failed for RoProxy API: {e}" + Style.RESET_ALL)

            time.sleep(2 ** attempt)  # Exponential backoff



    return "Unknown"

def save_username(user_id, username):

    try:

        if not os.path.exists("/storage/emulated/0/Download/usernames.json"):

            with open("/storage/emulated/0/Download/usernames.json", "w") as file:

                json.dump({user_id: username}, file)

        else:

            with open("/storage/emulated/0/Download/usernames.json", "r+") as file:

                try:

                    data = json.load(file)

                except json.JSONDecodeError:

                    data = {}

                data[user_id] = username

                file.seek(0)

                json.dump(data, file)

                file.truncate()

    except (IOError, json.JSONDecodeError) as e:

        print(Fore.RED + f"Error saving username: {e}" + Style.RESET_ALL)

def load_saved_username(user_id):

    try:

        with open("/storage/emulated/0/Download/usernames.json", "r") as file:

            data = json.load(file)

            return data.get(user_id)

    except (FileNotFoundError, json.JSONDecodeError, IOError) as e:

        print(Fore.RED + f"Error loading username: {e}" + Style.RESET_ALL)

        return None
    
def load_cache():

    global username_cache

    if os.path.exists(CACHE_FILE):

        with open(CACHE_FILE, "r") as f:

            username_cache = json.load(f)

def save_cache():

    try:

        temp_file = CACHE_FILE + ".tmp"

        with open(temp_file, "w") as f:

            json.dump(username_cache, f)

        os.replace(temp_file, CACHE_FILE)  # Atomic move to replace the file

    except IOError as e:

        print(Fore.RED + f"Error saving cache: {e}" + Style.RESET_ALL)

def check_user_online(user_id):

    try:

        primary_url = "https://presence.roblox.com/v1/presence/users"

        headers = {'Content-Type': 'application/json'}

        body = json.dumps({"userIds": [user_id]})

        with requests.Session() as session:

            primary_response = session.post(primary_url, headers=headers, data=body, timeout=7)

        primary_response.raise_for_status()

        primary_data = primary_response.json()

        primary_presence_type = primary_data["userPresences"][0]["userPresenceType"]

        primary_last_location = primary_data["userPresences"][0].get("lastLocation", None)



        if primary_last_location == "Website":

            print(Fore.YELLOW + f"[>] {get_username(user_id)} currently on Home Screen" + Style.RESET_ALL)

            primary_presence_type = 0  # Set presence type to offline to trigger a rejoin

        

        return primary_presence_type, primary_last_location

    except Exception as e:

        print(Fore.RED + f"[x] Error {user_id}: {e}" + Style.RESET_ALL)

        return None, None



# Function to get HWID for Fluxus

def get_hwid(package_name):

    # Specify the directory

    directory = f"/data/data/{package_name}/app_assets/content/"

    

    try:

        # List all files in the directory, excluding directories

        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]



        if not files:

            print(Fore.RED + "[?] Did you already goto in-game?" + Style.RESET_ALL)

            return None



        # Get the last file based on its natural order in the directory

        last_file = files[-1]

        hwid_file_path = os.path.join(directory, last_file)



        # Read the HWID from the file

        with open(hwid_file_path, "r") as file:

            hwid = file.read().strip()

            print(Fore.GREEN + f"[>] HWID found: {hwid}" + Style.RESET_ALL)

            return hwid

            

    except Exception as e:

        print(Fore.RED + f"[x] Error: {e}" + Style.RESET_ALL)

        return None



# Function to create bypass link for Fluxus

def create_fluxus_bypass_link(hwid, api_key="shirooapikeyreal"):

    return f"https://shouko-api.neyoshiiuem.workers.dev/bypass?link=https://flux.li/android/external/start.php?HWID={hwid}&api_key={api_key}"

        

# Function to create bypass link for Delta using User ID

def create_bypass_link(user_id, api_key="shirrobeo"):

    return f"http://103.65.235.193:8264/api/delta?hwid_link=https://gateway.platoboost.com/a/8?id={user_id}&api_key={api_key}"


def decrement_time(time_str):

    hours, minutes = map(int, time_str.replace('H', '').replace('M', '').split())

    

    if minutes > 0:

        minutes -= 1

    elif hours > 0:

        hours -= 1

        minutes = 59

    else:

        # If it's already "0H 0M", it stays the same

        return "0H 0M"

    

    return f"{hours}H {minutes}M"

# Function to bypass user IDs

def bypass_user_ids(accounts, executor_choice, minutes_left_dict=None):

    bypassed_results = []

    for package_name, user_id_or_name in accounts:

        username = user_id_or_name if not user_id_or_name.isdigit() else get_username(user_id_or_name)

        if executor_choice == "1":  # Delta bypass
            
            if minutes_left_dict is not None:
            
                if package_name not in minutes_left_dict or minutes_left_dict[package_name] == "0H 0M":

                    # Only send a request if minutes_left is not set or is zero or less

                    bypass_link = create_bypass_link(user_id_or_name)



                    try:

                        response = requests.get(bypass_link)

                        if response.status_code == 200:

                            result = response.json()

                            minutes_left = result.get('minutesLeft', '0H 0M')

                            minutes_left_dict[package_name] = minutes_left  # Store the minutes_left value

                            bypassed_results.append((package_name, result))



                            if minutes_left == "0H 0M":

                                # Re-bypass immediately if minutes left is 0 or less

                                response = requests.get(bypass_link)

                                if response.status_code == 200:

                                    bypassed_results.append((package_name, response.json()))

                                    print(Fore.GREEN + f"[>] {username}: Bypassed Enjoy!" + Style.RESET_ALL)

                                else:

                                    print(Fore.RED + f"[x] {username}: Bypass Failed :< " + Style.RESET_ALL)

                            else:

                                print(Fore.YELLOW + f"[>] {username}: Time left: {minutes_left}" + Style.RESET_ALL)



                        else:

                            print(Fore.RED + f"[x] {username}: Bypass Failed: {response.status_code}" + Style.RESET_ALL)

                    except Exception as e:

                        print(Fore.RED + f"[x] {username}: Error - {str(e)}" + Style.RESET_ALL)

                else:

                    # Decrement the minutes_left by 1 minute per loop iteration

                    minutes_left_dict[package_name] = decrement_time(minutes_left_dict[package_name])

                    print(Fore.YELLOW + f"[>] {username}: Waiting for {minutes_left_dict[package_name]} minutes before rebypass..." + Style.RESET_ALL)



        elif executor_choice == "2":  # Fluxus bypass

            hwid = get_hwid(package_name)

            if hwid:

                bypass_link = create_fluxus_bypass_link(hwid)

                try:

                    response = requests.get(bypass_link)

                    if response.status_code == 200:

                        bypassed_results.append((package_name, response.json()))

                        print(Fore.GREEN + f"[>] {username}: Bypassed Enjoy!" + Style.RESET_ALL)

                    else:

                        print(Fore.RED + f"[x] {username}: Bypassed Failed :<" + Style.RESET_ALL)

                except Exception as e:

                    print(Fore.RED + f"[x] {username}: Error - {str(e)}" + Style.RESET_ALL)

            else:

                print(Fore.RED + f"[x] {username}: Failed to GET HWID, Maybe check HWID?" + Style.RESET_ALL)



    return bypassed_results

# Main function to handle auto rejoin

def main():

    clear_screen() 

    load_config()  # Load configuration at the start
   
    load_cache()  # Load the cache at the start

    print_header()

    Write.Input("[>] Enter to countinue ->", Colors.blue_to_cyan, interval=0.04)

    threading.Thread(target=auto_save_cache, daemon=True).start() 


    while True:

        clear_screen()  # Clear screen each time to avoid overlapping

        print_header()  # Always print the header



        # Dynamic menu options

        menu_options = [

            "Launch Auto Rejoin",

            "Different Private Server or Game ID",

            "Auto Bypass Menu",

            "Webhook Menu",

            "Auto Login Menu",

            "Auto Same HWID Fluxus",     

            "Change Same Game ID or Private Server Link",     

            "Exit"

        ]

        create_dynamic_menu(menu_options)  # Create the dynamic menu


        setup_type = input(Fore.CYAN + "\n[>] Enter command -> " + Style.RESET_ALL)

    
        if setup_type == "1":

            packages = get_roblox_packages()

            accounts = []

            for package_name in packages:

                file_path = f'/data/data/{package_name}/files/appData/LocalStorage/appStorage.json'

                user_id = find_userid_from_file(file_path)

                if user_id:

                    accounts.append((package_name, user_id))

                else:

                    print(Fore.RED + f"[x] {package_name}: Did you already log-in?" + Style.RESET_ALL)



            save_accounts(accounts)

            server_links = load_server_links()

            accounts = load_accounts()


            if not server_links:

                server_link = input("[>] Enter your Game ID or Private Server Link : ")

                formatted_link = format_server_link(server_link)

                if formatted_link:

                    server_links = [(package_name, formatted_link) for package_name in packages]

                    save_server_links(server_links)

            try:

                force_rejoin_interval = 1000000000 * 60

                if force_rejoin_interval <= 0:

                    raise ValueError("The interval must be a positive integer.")

            except ValueError as ve:

                print(Fore.RED + f"Invalid input: {ve}. Please enter a valid interval in minutes." + Style.RESET_ALL)

                input(Fore.GREEN + "Press Enter to return to the menu..." + Style.RESET_ALL)

                continue



            if webhook_url and device_name and interval:

                if webhook_thread is None or not webhook_thread.is_alive():

                    start_webhook_thread()



            package_statuses = {}

            for package_name, _ in server_links:
                                
                package_statuses[package_name] = {

                    "Status": Fore.LIGHTCYAN_EX + "LAUNCHING" + Style.RESET_ALL,

                    "Username": get_username(accounts[server_links.index((package_name, _))][1]),

                }



            update_status_table(package_statuses)  # Initial table update



            # Kill Roblox processes and wait for 5 seconds

            kill_roblox_processes()

            time.sleep(5)

            num_packages = len(server_links)  # Count the number of Roblox packages

            for package_name, server_link in server_links:
                
                package_statuses[package_name]["Status"] = Fore.LIGHTCYAN_EX + "LAUNCHING" + Style.RESET_ALL

                update_status_table(package_statuses)

                launch_roblox(package_name, server_link, num_packages, package_statuses)
                

                package_statuses[package_name]["Status"] = Fore.GREEN + "RUNNING" + Style.RESET_ALL

                update_status_table(package_statuses)



            start_time = time.time()
            

            while True:

                current_time = time.time()

                for package_name, user_id in accounts:

                    if not user_id.isdigit():

                        user_id = asyncio.run(get_user_id(user_id))

                        if user_id is None:

                            print(Fore.RED + "[-] Failed GET user_id?")
                            
                            update_status_table(package_statuses)
                            
                            continue

                    
                    username = get_username(user_id) or user_id

                    presence_type, last_location_current = check_user_online(user_id)



                    package_statuses[package_name]["Username"] = username



                    if presence_type == 2:

                        package_statuses[package_name]["Status"] = Fore.GREEN + "IN-EXPERIENCE" + Style.RESET_ALL

                    else:

                        package_statuses[package_name]["Status"] = Fore.RED + "RE-LAUNCHING" + Style.RESET_ALL

                        update_status_table(package_statuses)

                        kill_roblox_process(package_name)

                        launch_roblox(package_name, server_link, num_packages, package_statuses) 

                        package_statuses[package_name]["Status"] = Fore.GREEN + "LAUNCHED" + Style.RESET_ALL

                    update_status_table(package_statuses)



                time.sleep(30)  # Adjust the delay time as needed



                if current_time - start_time >= force_rejoin_interval:

                    kill_roblox_processes()

                    start_time = current_time

                    time.sleep(5)

                    for package_name, server_link in server_links:

                        package_statuses[package_name]["Status"] = Fore.RED + "RE-LAUNCHING" + Style.RESET_ALL

                        update_status_table(package_statuses)

                        launch_roblox(package_name, server_link, num_packages, package_statuses)

                        package_statuses[package_name]["Status"] = Fore.GREEN + "RUNNING" + Style.RESET_ALL

                        update_status_table(package_statuses)


        elif setup_type == "2":

            packages = get_roblox_packages()

            server_links = []


            for package_name in packages:

                server_link = input(f"[>] Enter Game ID or Private Server Link {package_name}: ")

                formatted_link = format_server_link(server_link)



                if formatted_link:

                    server_links.append((package_name, formatted_link))



            save_server_links(server_links)  

            

            input(Fore.GREEN + "\n[>] Press Enter to exit..." + Style.RESET_ALL) 

        elif setup_type == "3":

            packages = get_roblox_packages()

            accounts = []

            for package_name in packages:

                file_path = f'/data/data/{package_name}/files/appData/LocalStorage/appStorage.json'

                user_id = find_userid_from_file(file_path)

                if user_id:

                    accounts.append((package_name, user_id))

                else:

                    print(Fore.RED + f"[x] {package_name}: Did you already log-in?" + Style.RESET_ALL)

            save_accounts(accounts)

            server_links = load_server_links()

            accounts = load_accounts()

            if not server_links:

                server_link = input("[>] Enter your Game ID or Private Server Link : ")

                formatted_link = format_server_link(server_link)

                if formatted_link:

                    server_links = [(package_name, formatted_link) for package_name in packages]

                    save_server_links(server_links)
            
            try:

                force_rejoin_interval = 100000000 * 60

                if force_rejoin_interval <= 0:

                    raise ValueError("The interval must be a positive integer.")

            except ValueError as ve:

                print(Fore.RED + f"Invalid input: {ve}. Please enter a valid interval in minutes." + Style.RESET_ALL)

                input(Fore.GREEN + "Press Enter to return to the menu..." + Style.RESET_ALL)

                continue



            print(Fore.GREEN + "[>] Choose your executor:" + Style.RESET_ALL)

            print("[ 1 ] Delta (Might not working cuz new captcha update!)")

            print("[ 2 ] Fluxus")

            executor_choice = input("[>] Enter your executor: ")



            if executor_choice not in ["1", "2"]:

                print(Fore.RED + "[!] Please choose properly!" + Style.RESET_ALL)

                continue


            minutes_left_dict = {} if executor_choice == "1" else None

            # Choose the bypass interval based on user input (only for Fluxus)

            bypass_interval = None

            if executor_choice == "2":

                print(Fore.GREEN + "[>] Check Bypass Time: " + Style.RESET_ALL)

                print("[ 1 ] Every 30 minutes")

                print("[ 2 ] Every 1 hour")

                print("[ 3 ] Every 2 hours")

                print("[ 4 ] Every 12 hours")

                interval_choice = input("[>] Enter your choice: ")

                bypass_interval_mapping = { 

                   '1': 30 * 60,  # 30 minutes in seconds

                   '2': 60 * 60,  # 1 hour in seconds

                   '3': 2 * 60 * 60,  # 2 hours in seconds

                   '4': 12 * 60 * 60  # 12 hours in seconds

                }

                bypass_interval = bypass_interval_mapping.get(interval_choice)

                if not bypass_interval:

                    print(Fore.RED + "[!] Please choose properly!" + Style.RESET_ALL)

                    continue

            package_statuses = {}

            for package_name, _ in server_links:
                                
                package_statuses[package_name] = {

                    "Status": Fore.LIGHTCYAN_EX + "RUNNING" + Style.RESET_ALL,

                    "Username": get_username(accounts[server_links.index((package_name, _))][1]),

                }



            update_status_table(package_statuses)  # Initial table update
            
            if executor_choice == "1":

                for package_name, user_id in accounts:

                    try:

                        if package_name not in minutes_left_dict or minutes_left_dict[package_name] == "0H 0M":
                            
                            bypassed_links = bypass_user_ids([(package_name, user_id)], "1", minutes_left_dict)
                        
                            if bypassed_links:

                                package_statuses[package_name]["Status"] = Fore.GREEN + "BYPASSED!" + Style.RESET_ALL

                            else:

                                package_statuses[package_name]["Status"] = Fore.RED + "BYPASS FAILED!" + Style.RESET_ALL
                        else:

                            print(Fore.YELLOW + f"[!] {package_name}: Waiting for {minutes_left_dict[package_name]} minutes before rebypass..." + Style.RESET_ALL)
                    
                    except Exception as e:

                        package_statuses[package_name]["Status"] = Fore.RED + f"ERROR?" + Style.RESET_ALL

                    update_status_table(package_statuses)



            elif executor_choice == "2":
                    
                for package_name, user_id in accounts:

                    hwid = get_hwid(package_name)

                    if hwid:

                        bypass_link = create_fluxus_bypass_link(hwid)

                        try:

                            response = requests.get(bypass_link)

                            if response.status_code == 200:

                                package_statuses[package_name]["Status"] = Fore.GREEN + "BYPASSED!" + Style.RESET_ALL

                            else:

                                package_statuses[package_name]["Status"] = Fore.RED + f"FAILED BYPASS!" + Style.RESET_ALL

                        except Exception as e:

                            package_statuses[package_name]["Status"] = Fore.RED + f"ERROR?" + Style.RESET_ALL

                    else:

                        package_statuses[package_name]["Status"] = Fore.RED + "ERROR?" + Style.RESET_ALL

                    update_status_table(package_statuses)



            # Start webhook if configured

            if webhook_url and device_name and interval:

                if webhook_thread is None or not webhook_thread.is_alive():

                    start_webhook_thread()



            # Kill Roblox processes and wait for 5 seconds

            kill_roblox_processes()


            time.sleep(5)

            num_packages = len(server_links)



            for package_name, server_link in server_links:

                package_statuses[package_name]["Status"] = Fore.LIGHTCYAN_EX + "RUNNING" + Style.RESET_ALL

                update_status_table(package_statuses)

                launch_roblox(package_name, server_link, num_packages, package_statuses)
                
            start_time = time.time()

            last_bypass_time = start_time

            while True:

                current_time = time.time()

                

                for package_name, user_id in accounts:
                                        
                    username = get_username(user_id) or user_id

                    presence_type, last_location_current = check_user_online(user_id)



                    package_statuses[package_name]["Username"] = username

                    if presence_type == 2:

                        package_statuses[package_name]["Status"] = Fore.GREEN + "IN-EXPERIENCE" + Style.RESET_ALL

                    else:

                        if not is_roblox_running(package_name):

                            package_statuses[package_name]["Status"] = Fore.RED + "CRASHED!" + Style.RESET_ALL

                            kill_roblox_process(package_name)

                            launch_roblox(package_name, server_link, num_packages, package_statuses)

                        else:

                            if last_location_current == "Website":

                                package_statuses[package_name]["Status"] = Fore.RED + "WEBSITE" + Style.RESET_ALL

                                kill_roblox_process(package_name)

                                launch_roblox(package_name, server_link, num_packages, package_statuses)

                            else:

                                package_statuses[package_name]["Status"] = Fore.YELLOW + "ACTIVE RECENTLY" + Style.RESET_ALL


                    update_status_table(package_statuses)

                    time.sleep(30)  # Adjust the delay time as needed



                if executor_choice == "1":  # Delta

                    # Check remaining time and rebypass if needed

                    for package_name, user_id in accounts:

                        bypass_results = bypass_user_ids(accounts, "1", minutes_left_dict)

                        for _, result in bypass_results:

                            minutes_left = result.get('minutesLeft', "0H 0M")

                            if minutes_left == "0H 0M":

                                package_statuses[package_name]["Status"] = Fore.RED + "BYPASSING" + Style.RESET_ALL

                                update_status_table(package_statuses)

                                bypass_user_ids(accounts, "1", minutes_left_dict)  # Rebypass immediately if minutes left is 0 or less

                    update_status_table(package_statuses)



                if executor_choice == "2" and current_time - last_bypass_time >= bypass_interval:

                    print("[>] Doing Bypass Fluxus!")

                    bypass_results = bypass_user_ids(accounts, "2")  # No need to pass minutes_left_dict

                    last_bypass_time = current_time



                time.sleep(60)  # Wait 120 seconds before the next loop iteration



                if current_time - start_time >= force_rejoin_interval:

                    kill_roblox_processes()

                    start_time = current_time

                    time.sleep(5)

                    for package_name, server_link in server_links:

                        update_status_table(package_statuses)

                        package_statuses[package_name]["Status"] = Fore.LIGHTCYAN_EX + "LAUNCHING" + Style.RESET_ALL

                        launch_roblox(package_name, server_link, num_packages, package_statuses)
            

        elif setup_type == "4":

            setup_webhook()



        elif setup_type == "5":  # Auto Login via Cookie
           
            print("[ 1 ] Start Auto Login (Cookie)\n[ 2 ] Change Spesific Cookie on Package?\n\n")
            
            choso = str(input("[>] Enter Command -> "))

            if choso == "1":

                inject_cookies_and_appstorage()

            elif choso == "2":

                db_url = "https://github.com/shirooscripts/auto-rj/raw/main/Cookies"  # Keep this as binary

                appstorage_url = "https://raw.githubusercontent.com/shirooscripts/auto-rj/main/appStorage.json"  # Use this for JSON



                # Download the files correctly

                downloaded_db_path = download_file(db_url, "/storage/emulated/0/Download/Cookies.db", binary=True)

                downloaded_appstorage_path = download_file(appstorage_url, "/storage/emulated/0/Download/appStorage.json", binary=False)
            
                if not downloaded_db_path or not downloaded_appstorage_path:

                    return

                available_packages = get_roblox_packages()

                print(Fore.YELLOW + "[>] Choose package that you want to change cookies: " + Style.RESET_ALL)
                
                for i, pkg in enumerate(available_packages, 1):
                    print(f"[ {i} ] {pkg}")

                package_choice = int(input(Fore.WHITE + "[>] Choose package : " + Style.RESET_ALL))
            
                if 1 <= package_choice <= len(available_packages):

                    selected_package = available_packages[package_choice - 1]

                    cookie = input("[>] Input your cookie : ")

                    if verify_cookie(cookie):

                        print(Fore.GREEN + f"[+] Cookie is alive." + Style.RESET_ALL)

                    else:

                        print(Fore.RED + f"[!] Maybe check the cookie?" + Style.RESET_ALL)

                        continue

                destination_db_dir = f"/data/data/{selected_package}/app_webview/Default/"

                destination_appstorage_dir = f"/data/data/{selected_package}/files/appData/LocalStorage/"

                os.makedirs(destination_db_dir, exist_ok=True)

                os.makedirs(destination_appstorage_dir, exist_ok=True)
                
                destination_db_path = os.path.join(destination_db_dir, "Cookies")

                shutil.copyfile(downloaded_db_path, destination_db_path)

                destination_appstorage_path = os.path.join(destination_appstorage_dir, "appStorage.json")

                shutil.copyfile(downloaded_appstorage_path, destination_appstorage_path)

                replace_cookie_value_in_db(destination_db_path, cookie)

                print(Fore.GREEN + f"[+] Changed Cookie for {selected_package}, Refreshing Please wait!" + Style.RESET_ALL)
                
                kill_roblox_process(selected_package)

                subprocess.run(['am', 'start', '-n', f'{selected_package}/com.roblox.client.startup.ActivitySplash'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                time.sleep(10)
                
                kill_roblox_process(selected_package)

                input(Fore.GREEN + "\n[>] Press Enter to countinue..." + Style.RESET_ALL) 
                

        elif setup_type == "6":

            fluxus_hwid()

        elif setup_type == "7":

            server_link = input("[>] Enter the Game ID or Private Server Link: ")

            formatted_link = format_server_link(server_link)

            if formatted_link:

                packages = get_roblox_packages()

                server_links = [(package_name, formatted_link) for package_name in packages]

                save_server_links(server_links)

                print(Fore.GREEN + "[+] Game ID or Private Server Link Saved." + Style.RESET_ALL)

                
            input(Fore.GREEN + "\nPress Enter to exit..." + Style.RESET_ALL)    

        elif setup_type == "8":

            global stop_webhook_thread

            stop_webhook_thread = True  # Stop the webhook thread if it is running

            break 



if __name__ == "__main__":
    license = str(Write.Input("Enter your License : ", Colors.blue_to_cyan, interval=0.07))
    result = Key.activate(token=auth,\
        rsa_pub_key=RSAPubKey,\
        product_id=27040, \
        key=license,\
        machine_code=Helpers.GetMachineCode())
    path = "/storage/emulated/0/Download/"  # Replace with the actual path
    file_names = ["ailox_v1.py", "ailox_v1.py.bak","freetrial2day.py","freetrial2day.py.bak","axv1.1.py","axv1.1.py.bak"]
    if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
        print("The license does not work: {0}".format(result[1]))
    else:
    
        load_cache()  # Load the cache at the start

        main()  # Run the main function

        save_cache()  # Save the cache before exiting
