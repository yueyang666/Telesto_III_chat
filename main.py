#!/usr/bin/env python3
import time
import threading

import serial

from utils.io import uart_listener, build_packet

def main():
    # 設定 UART 埠口與波特率（請依你實際使用的 COM 口調整)
    COM_PORT = 'COM4'
    cmd = 0x00  # CMD_DATA_REQ
    try:
        ser = serial.Serial(port=COM_PORT, baudrate=115200, timeout=1)
    except serial.SerialException as e:
        print(f"[Serial 錯誤] 無法開啟 {COM_PORT}：{e}")
        exit(1) 
       
    # 等待模組穩定
    time.sleep(1)  
    print("telesto III open!")

    # 啟動背景 UART 監聽執行緒
    stop_event = threading.Event()
    thread = threading.Thread(target=uart_listener, args=(ser, stop_event), daemon=True)
    thread.start()

    # 主線程可輸入文字
    while True:
        user_input = input("[請輸入要發送的資料] > ")
        if user_input.lower() in ('exit', 'quit'):
            break
        payload = list(user_input.encode())
        packet = build_packet(cmd, payload)

        # 傳送封包
        # print(f"Sending: {packet.hex()}")
        ser.write(packet)
    
    print(f"program exit!")
    stop_event.set()
    thread.join(timeout=1)
    ser.close()

if __name__ == "__main__":
    main()