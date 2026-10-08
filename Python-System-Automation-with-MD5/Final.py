import os
import hashlib
import time
import smtplib
import ssl
from email.message import EmailMessage
import sys
from datetime import datetime


def calculate_checksum(path, block_size=1024):
    fobj = open(path, 'rb')  # File object creation
    hobj = hashlib.md5()
    buffer = fobj.read(block_size)
    while buffer:
        hobj.update(buffer)
        buffer = fobj.read(block_size)
    fobj.close()
    return hobj.hexdigest()


def find_and_delete_duplicates(directory, log_dir):
    checksums = {}
    deleted_files = []
    total_files = 0
    start_time = datetime.now()

    for foldername, subfolders, filenames in os.walk(directory):
        for fname in filenames:
            file_path = os.path.join(foldername, fname)
            if not os.path.isfile(file_path):
                continue
            total_files += 1
            try:
                checksum = calculate_checksum(file_path)
                if checksum in checksums:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                else:
                    checksums[checksum] = file_path
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join(log_dir, f"Log_{timestamp}.txt")

    fobj = open(log_file_path, "w")  # File object creation
    fobj.write("Duplicate File Removal Log\n")
    fobj.write(f"Scanning started at: {start_time}\n")
    fobj.write(f"Total files scanned: {total_files}\n")
    fobj.write(f"Total duplicate files deleted: {len(deleted_files)}\n\n")
    fobj.write("Deleted Files:\n")
    for f in deleted_files:
        fobj.write(f + "\n")
    fobj.close()

    return log_file_path, total_files, len(deleted_files), start_time


def send_log_via_email(log_file_path, recipient_email, sender_email, sender_password,
                       start_time, total_files, duplicate_count):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Duplicate File Removal Report"

    body = f"""
    Duplicate File Removal Operation Report

    Start time: {start_time}
    Total number of files scanned: {total_files}
    Total number of duplicate files found and deleted: {duplicate_count}

    Please find the attached log file for details.
    """
    msg.set_content(body)

    fobj = open(log_file_path, "rb")  # File object creation
    file_data = fobj.read()
    file_name = os.path.basename(log_file_path)
    fobj.close()
    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    context = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    smtp.login(sender_email, sender_password)
    smtp.send_message(msg)
    smtp.quit()

    print("Email sent successfully!")


def main():
    if len(sys.argv) != 5:
        print("Usage: python script.py <TargetDirectory> <TimeInterval(in mins)> <RecipientEmail> <YourEmail>")
        return

    target_dir = sys.argv[1]
    interval = int(sys.argv[2])
    recipient_email = sys.argv[3]
    sender_email = sys.argv[4]
    sender_password = input("Enter the sender email password: ")

    marvellous_dir = "Marvellous"
    if not os.path.exists(marvellous_dir):
        os.mkdir(marvellous_dir)

    while True:
        log_file, total_files, duplicates, start_time = find_and_delete_duplicates(target_dir, marvellous_dir)
        send_log_via_email(log_file, recipient_email, sender_email, sender_password, start_time, total_files, duplicates)
        print(f"Waiting for {interval} minutes before next scan...\n")
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()
