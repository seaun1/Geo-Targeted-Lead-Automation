# 📍 Geo-Targeted Lead Automation Engine

A resilient, headless Chrome automation system designed to extract B2C leads from hyper-local networking directories and funnel them into a Telegram CRM pipeline. 

## 💼 The Business Impact (Why I Built This)
In the sales industry, the most grueling and low-ROI task is top-of-funnel prospecting—manually searching for potential customers and sending cold outreach messages. I built this engine to completely eliminate that "garbage time." 

By deploying this script to run 24/7 autonomously, I transformed a tedious manual grind into a passive lead-generation machine. Now, I simply wake up to a pipeline full of warm replies. It allows me to focus 100% of my human effort on high-value closing and customer service, rather than repetitive data entry.

## 📖 The Architecture Story (End-to-End CRM Pipeline)
This project is **Part 1** of a larger B2B automation pipeline I built to help a Melbourne-based artisan coffee distributor scale their direct-to-consumer (DTC) sales without paying for Facebook/Google Ads.

1. **Lead Generation (This Project):** This Python/Selenium script runs on a dedicated port (`9222`) avoiding fresh browser detection. It navigates local suburb directories, parses profiles, cleans up previous chat histories (to prevent shadow-banning), and sends promotional direct messages.
2. **Order Fulfillment (Part 2):** When a customer replies on Telegram to place an order, a separate `Telethon` asynchronous bot intercepts the chat, parses the delivery address, and instantly pushes the order into a Google Sheet via `gspread` for driver dispatching.

## 🔥 Key Technical Highlights
- **Headless Port-Forwarding (`127.0.0.1:9222`):** Eliminates repetitive logins and captchas by hijacking an already authenticated Chrome instance.
- **Anti-Ban Cleanup Protocols:** Automatically detects and purges old conversation histories (`Delete for Both`) before initiating new contact to maintain account health.
- **Dynamic HUD & Sleep Scheduling:** Includes a custom Javascript injection that overrides the browser window with a real-time terminal HUD displaying hardware telemetry (`CPU`, `RAM`, `IP`). It automatically enters low-power sleep mode outside of configured business hours (19:00 - 07:00) with a hardware keyboard interrupt (`msvcrt`) override.

## 🛠️ Stack
`Python 3` • `Selenium WebDriver` • `JavaScript (DOM Injection)` • `Multiprocessing`
