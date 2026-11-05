import time 
import random 
import json 
import os 
import winsound 
import ctypes 
import re  
import sys 
import msvcrt 
from datetime import datetime, timedelta  
import platform
import socket
import multiprocessing
import getpass

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.service import Service 
from selenium.common.exceptions import TimeoutException, WebDriverException 

# ========================================== 
# 0. ☕ COFFEE-HUB LEAD-GEN CORE CONFIG 
# ========================================== 
PORT = "9222"  

# Operating hours (24h format) - Aligned with local business hours
WORK_START_HOUR = 7  
WORK_END_HOUR = 19   

# Melbourne Coffee Promotional Copy
reply_text = """☕ MELBOURNE ARTISAN COFFEE | NOVEMBER DROP 🍂
Freshly roasted beans, straight to your door 🚚

🟤 Ethiopian Yirgacheffe (Light Roast) — floral, citrusy, perfect for pour-over
⚫ Melbourne Midnight (Dark Roast) — bold, chocolatey, ideal for espresso

💰 NOVEMBER LOCAL DEALS:
• 250g 👉 $25
• 500g 👉 $45 (+ Free Shipping 🎁)
• 1kg  👉 $80 (+ 1 Free Cold Brew Can 🎁)

🚚 Same-day delivery under 15km Melb CBD
💵 Cash on delivery or PayID

📲 Tele.gram: @MelbCoffeeHub
Or drop your @ below to unlock our Wholesale Menu ☕""" 

# ==========================================
# 1. Fetch Local Hardware Specs (For HUD Telemetry)
# ==========================================
try:
    sys_os = f"{platform.system()} {platform.release()}"
    sys_cpu = platform.processor() or "Unknown CPU"
    if len(sys_cpu) > 15: sys_cpu = sys_cpu[:12] + "..."
    sys_cores = f"{multiprocessing.cpu_count()} Cores"
    sys_user = getpass.getuser()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    sys_ip = s.getsockname()[0]
    s.close()
except:
    sys_os, sys_cpu, sys_cores, sys_user, sys_ip = "Unknown", "Unknown CPU", "N/A", "Admin", "127.0.0.1"

sys_ram = "Unknown"
if platform.system() == "Windows":
    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
        sys_ram = f"{round(memoryStatus.ullTotalPhys / (1024**3), 1)} GB"
    except: pass

def check_force_sleep():
    sleep_triggered = False
    while msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'\x1b': # Esc key
            sleep_triggered = True
    return sleep_triggered

# ========================================== 
# 2. System Boot Panel
# ========================================== 
print("\n" + "="*70) 
print(f"  ☕ MELBOURNE COFFEE LEAD-GEN ENGINE (Port {PORT})") 
print("  ✨ Architecture: Selenium Headless + Anti-Ban Sleep Protocol") 
print("  🕹️ Manual Override: Press [Esc] to Sleep | Press [Enter] to Wake")
print("="*70) 

is_loop_mode = True 
total_target = 500   
batch_size = 100        
wait_min, wait_max = 2.5, 5.0  
override_status = None 

# ========================================== 
# 3. Attach to Chrome (Port forwarding for auth bypass)
# ========================================== 
chrome_options = Options() 
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{PORT}") 
chrome_options.page_load_strategy = 'eager' 
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.set_capability("acceptInsecureCerts", True)

try: 
    print(f"🔧 Attaching to local browser kernel (Port: {PORT})...") 
    service = Service() 
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    print(f"✅ Connection Established! Radar system online.") 
except Exception as e: 
    print(f"\n❌ Connection Failed! Ensure port {PORT} is open.\n")
    exit() 

# ========================================== 
# 4. Main Engine Loop
# ========================================== 
session_sent_count = 0 

# Target Melbourne Suburbs
search_locations = [ 
    "Malvern VIC, Australia", "Northcote VIC, Australia", 
    "Kew VIC, Australia", "Sunshine VIC, Australia", "West Melbourne VIC, Australia" 
] 
location_index = 0 

while session_sent_count < total_target: 
    while msvcrt.kbhit(): msvcrt.getch()

    now = datetime.now()
    
    if WORK_START_HOUR <= now.hour < WORK_END_HOUR and override_status == "WAKE": override_status = None
    if (now.hour < WORK_START_HOUR or now.hour >= WORK_END_HOUR) and override_status == "SLEEP": override_status = None

    should_sleep = (now.hour < WORK_START_HOUR or now.hour >= WORK_END_HOUR)
    if override_status == "WAKE": should_sleep = False
    elif override_status == "SLEEP": should_sleep = True
    
    if should_sleep:
        print(f"\n🌙 Sleep protocol triggered. Entering low-power stealth mode...")
        try: driver.get("about:blank") 
        except: pass
            
        if now.hour >= WORK_END_HOUR or override_status == "SLEEP":
            if now.hour >= WORK_END_HOUR or now.hour >= WORK_START_HOUR: target_time = (now + timedelta(days=1)).replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)
            else: target_time = now.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)
        else: target_time = now.replace(hour=WORK_START_HOUR, minute=0, second=0, microsecond=0)
            
        while True:
            current_time = datetime.now()
            if current_time >= target_time:
                override_status = None
                break
                
            time_left = target_time - current_time
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            status_bar = f" ☕ [STANDBY] ⏳ Resuming operations in ▓ {hours:02d}:{minutes:02d}:{seconds:02d} ▓ (Press Enter to wake) "
            print(f"\r{status_bar.ljust(90)}", end="", flush=True)
            
            # HUD Interface Injection (Geek Panel)
            try:
                js_dashboard = f"""
                document.body.style.margin = '0';
                document.body.style.backgroundColor = '#000000'; 
                document.body.style.overflow = 'hidden';
                document.body.style.userSelect = 'none';
                
                if (!document.getElementById('jarvis-ui-container')) {{
                    document.body.innerHTML = `
                    <style>
                        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Consolas', monospace; }}
                        .jarvis-ui {{ position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; background: #000000; display: flex; justify-content: center; align-items: center; }}
                        .anchor-center {{ position: absolute; top: 50%; left: 50%; width: 0; height: 0; z-index: 10; }}
                        .track-ring {{ position: absolute; border-radius: 50%; transform: translate(-50%, -50%); }}
                        @keyframes spinCW {{ 100% {{ transform: translate(-50%, -50%) rotate(360deg); }} }}
                        @keyframes spinCCW {{ 100% {{ transform: translate(-50%, -50%) rotate(-360deg); }} }}
                        @keyframes glowPulse {{ 
                            0%, 100% {{ box-shadow: 0 0 30px rgba(0, 243, 255, 0.4), inset 0 0 20px rgba(0, 243, 255, 0.4); }}
                            50% {{ box-shadow: 0 0 70px rgba(0, 243, 255, 0.8), inset 0 0 40px rgba(0, 243, 255, 0.8); }}
                        }}
                        .arc-outer {{ width: 580px; height: 580px; border: 1px solid rgba(0, 243, 255, 0.1); border-left: 2px solid #00f3ff; border-right: 2px solid #00f3ff; animation: spinCW 40s linear infinite; }}
                        .arc-radar {{ width: 440px; height: 440px; border: 2px dashed rgba(0, 243, 255, 0.5); animation: spinCCW 25s linear infinite; }}
                        .arc-mid {{ width: 330px; height: 330px; border: 15px solid transparent; border-top: 15px solid #00f3ff; border-bottom: 15px solid #00f3ff; box-shadow: 0 0 20px rgba(0, 243, 255, 0.2); animation: spinCW 12s linear infinite; }}
                        .arc-inner {{ width: 220px; height: 220px; border: 3px solid rgba(0, 243, 255, 0.8); box-shadow: inset 0 0 15px #00f3ff; animation: spinCCW 8s linear infinite; }}
                        .arc-core {{ width: 130px; height: 130px; background: transparent; border: 2px solid #00f3ff; animation: glowPulse 3s infinite ease-in-out; }}
                        .time-display-core {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 38px; font-weight: 900; color: #ffffff; letter-spacing: 5px; text-shadow: 0 0 10px #00f3ff, 0 0 25px #00f3ff; z-index: 100; }}
                        .hud-side {{ position: absolute; top: 50%; transform: translateY(-50%); z-index: 20; width: 300px; }}
                        .side-l {{ left: 5%; border-left: 2px solid #00f3ff; padding-left: 20px; }}
                        .side-r {{ right: 5%; border-right: 2px solid #00f3ff; padding-right: 20px; text-align: right; }}
                        .info-row {{ margin-bottom: 25px; padding-bottom: 5px; border-bottom: 1px solid rgba(0, 243, 255, 0.15); }}
                        .info-label {{ font-size: 11px; color: rgba(0, 243, 255, 0.7); font-weight: bold; letter-spacing: 4px; margin-bottom: 6px; }}
                        .info-val {{ font-size: 18px; color: #fff; font-weight: bold; text-shadow: 0 0 8px #00f3ff; text-transform: uppercase; }}
                        .alert-badge {{ position: absolute; bottom: 8%; left: 50%; transform: translateX(-50%); background: rgba(0, 243, 255, 0.1); border: 1px solid #00f3ff; padding: 8px 35px; color: #00f3ff; font-size: 15px; font-weight: 900; letter-spacing: 6px; box-shadow: 0 0 20px rgba(0, 243, 255, 0.3); z-index: 20; text-transform: uppercase; }}
                    </style>
                    <div id="jarvis-ui-container" class="jarvis-ui">
                        <div class="hud-side side-l">
                            <div class="info-row"><div class="info-label">PROTOCOL SYSTEM</div><div class="info-val">LEAD-GEN ACTIVE</div></div>
                            <div class="info-row"><div class="info-label">OS KERNEL</div><div class="info-val">{sys_os}</div></div>
                            <div class="info-row"><div class="info-label">PROCESSOR MAT</div><div class="info-val">{sys_cpu}</div></div>
                        </div>
                        <div class="anchor-center">
                            <div class="track-ring arc-outer"></div>
                            <div class="track-ring arc-radar"></div>
                            <div class="track-ring arc-mid"></div>
                            <div class="track-ring arc-inner"></div>
                            <div class="track-ring arc-core"></div>
                        </div>
                        <div id="jarvis-timer-text" class="time-display-core"></div>
                        <div class="hud-side side-r">
                            <div class="info-row"><div class="info-label">ADMIN OVERRIDE</div><div class="info-val">{sys_user}</div></div>
                            <div class="info-row"><div class="info-label">SECURE UPLINK</div><div class="info-val">{sys_ip}</div></div>
                            <div class="info-row"><div class="info-label">MEMORY ALLOC</div><div class="info-val">{sys_ram}</div></div>
                        </div>
                        <div class="alert-badge">SYSTEM IN STANDBY</div>
                    </div>
                    `;
                }}
                var timeElement = document.getElementById('jarvis-timer-text');
                if (timeElement) {{ timeElement.innerText = '{hours:02d}:{minutes:02d}:{seconds:02d}'; }}
                """
                driver.execute_script(js_dashboard)
            except: pass
            
            wake_triggered = False
            while msvcrt.kbhit():
                key = msvcrt.getch()
                if key in [b'\r', b'\n']: wake_triggered = True
                
            if wake_triggered:
                print("\n\n🚀 Manual override engaged. Radar coming online...\n")
                override_status = "WAKE"
                break
                
            time.sleep(1)
            
        if override_status != "WAKE":
            print(f"\n\n🚀 {WORK_START_HOUR:02d}:00 reached! System waking up, radar ready...\n")
        continue 

    current_batch_urls = [] 
     
    # ------------------------------------------ 
    # [Phase 1: Lock Target Area] 
    # ------------------------------------------ 
    if is_loop_mode: 
        print(f"\n🔄 [PHASE 1] Harvesting traffic... (Press 'Esc' to force sleep)") 
        try: 
            # Simulated local directory URL
            driver.get("https://local-networking-directory.com/maps")  
            time.sleep(2) 
            
            try: 
                current_loc = search_locations[location_index % len(search_locations)] 
                print(f"   📍 Switching Zone: {current_loc}") 
                 
                search_box = WebDriverWait(driver, 5).until( 
                    EC.presence_of_element_located((By.ID, "map-location-inputs")) 
                ) 
                 
                search_box.send_keys(Keys.CONTROL, "a") 
                search_box.send_keys(Keys.BACK_SPACE) 
                driver.execute_script("arguments[0].value = '';", search_box) 
                time.sleep(0.5) 
                 
                search_box.send_keys(current_loc) 
                time.sleep(1.5) 
                 
                search_box.send_keys(Keys.ARROW_DOWN) 
                time.sleep(0.2) 
                search_box.send_keys(Keys.ENTER) 
                time.sleep(2.0) 
                 
                location_index += 1  
            except: pass 
        except: pass 

    # ------------------------------------------ 
    # [Phase 2: Extract Lead Signatures] 
    # ------------------------------------------ 
    try: driver.execute_script("document.body.style.zoom = '0.5'") 
    except: pass 
     
    last_added_time = time.time() 
     
    while len(current_batch_urls) < batch_size: 
        if check_force_sleep():
            print("\n🛑 [MANUAL OVERRIDE] Esc detected! Preparing for sleep...")
            override_status = "SLEEP"
            break
            
        try: 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            time.sleep(0.5) 

            # Target local coffee enthusiast signatures
            elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='local-coffee-lover']") 
            new_added = 0 
            for el in elements: 
                try: 
                    url = el.get_attribute("href") 
                    if url and url not in current_batch_urls: 
                        current_batch_urls.append(url) 
                        new_added += 1 
                except: continue 
             
            print(f"📥 Current Extraction Progress: {len(current_batch_urls)} / {batch_size}", end="\r") 
             
            if new_added > 0: 
                last_added_time = time.time() 

            if time.time() - last_added_time > 35: 
                break  
        except Exception: 
            time.sleep(1) 
            continue 
            
    if override_status == "SLEEP":
        continue 
             
    try: driver.execute_script("document.body.style.zoom = '1.0'") 
    except: pass 
     
    if len(current_batch_urls) == 0: 
        time.sleep(1.0) 
        continue 

    # ------------------------------------------ 
    # [Phase 3: Rapid Dispatch & History Purge] 
    # ------------------------------------------ 
    print(f"\n🚀 [PHASE 3] Initiating dispatch and history purge...") 
     
    for index, url in enumerate(current_batch_urls, start=1): 
        if check_force_sleep():
            override_status = "SLEEP"
            break
            
        try: 
            if index % 20 == 0: 
                driver.get("about:blank") 
                time.sleep(0.5) 

            print(f"🔎 [{index}/{len(current_batch_urls)} | Total Sent: {session_sent_count}] Processing: {url}") 
            driver.set_page_load_timeout(15) 
            driver.get(url) 
             
            try: 
                message_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Message')]"))) 
                driver.execute_script("arguments[0].click();", message_btn) 
            except: continue 

            try: input_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "textarea"))) 
            except: continue 

            # Execute history deletion to prevent shadow-bans
            try: 
                driver.execute_script("window.scrollBy(0, -300);")
                time.sleep(0.5)
                delete_attempts = 0
                while delete_attempts < 5: 
                    trash_xpath = "//span[contains(@class, 'material-icons') and contains(., 'delete')]" 
                    trash_icons = driver.find_elements(By.XPATH, trash_xpath) 
                    if len(trash_icons) == 0: break  
                        
                    try:
                        target_trash = trash_icons[0]
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_trash) 
                        driver.execute_script("arguments[0].click();", target_trash) 
                        time.sleep(1.0) 
                        
                        try:
                            for_both_btn = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'For Both')]")))
                            driver.execute_script("arguments[0].click();", for_both_btn)
                        except: pass
                        delete_attempts += 1
                    except Exception: break
            except Exception: pass 

            # Dispatch Promotion
            try: 
                input_box = driver.find_element(By.TAG_NAME, "textarea") 
                driver.execute_script(""" 
                    var el = arguments[0]; 
                    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set; 
                    nativeInputValueSetter.call(el, arguments[1]); 
                    el.dispatchEvent(new Event('input', { bubbles: true })); 
                """, input_box, reply_text) 
                 
                try: 
                    input_box.send_keys(" ") 
                    input_box.send_keys(Keys.BACK_SPACE) 
                    input_box.send_keys(Keys.ENTER) 
                except: pass 
                 
                session_sent_count += 1 
            except Exception: continue 

            sleep_time = random.uniform(wait_min, wait_max) 
            end_sleep = time.time() + sleep_time
            while time.time() < end_sleep:
                if check_force_sleep():
                    override_status = "SLEEP"
                    break
                time.sleep(0.1)

        except Exception: continue 
            
    if override_status == "SLEEP":
        continue 
             
    if not is_loop_mode: break  

print(f"\n🏆 Mission Accomplished! Total successful dispatches: {session_sent_count}.") 