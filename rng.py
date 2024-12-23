from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import ipaddress

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the IP Range Generator Bot!\n\nCommands:\n/rng <startip> <endip> - Generate IP addresses within the specified range and get them in a text file\n\nDeveloped by @darkboy")

def rng(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text("Please provide both start and end IP addresses.\nUsage: /rng <startip> <endip>")
        return

    start_ip = context.args[0]
    end_ip = context.args[1]
    try:
        ip_list = generate_ip_range(start_ip, end_ip)
        file_name = save_to_file(ip_list)
        update.message.reply_document(document=open(file_name, 'rb'))
    except ValueError as e:
        update.message.reply_text(f"Error: {e}")

def generate_ip_range(start_ip: str, end_ip: str) -> list:
    start = ipaddress.ip_address(start_ip)
    end = ipaddress.ip_address(end_ip)
    if start > end:
        raise ValueError("Start IP must be less than or equal to End IP.")
    
    ip_list = [str(ip) for ip in ipaddress.summarize_address_range(start, end)]
    return ip_list

def save_to_file(ip_list: list) -> str:
    file_name = "ip_range.txt"
    with open(file_name, 'w') as file:
        for ip in ip_list:
            file.write(f"{ip}\n")
    return file_name

def main() -> None:
    updater = Updater("7649478498:AAFIMF5aNn72ybJ2t3EN3HLOA4l4R3SCDew")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rng", rng))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
