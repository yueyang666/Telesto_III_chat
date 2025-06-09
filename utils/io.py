import time
import sys

def uart_listener(ser, stop_event):
    """多線程監聽無線電payload"""
    while not stop_event.is_set():
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            parsed = parse_packet(data)
            if parsed['cmd'] == 0x40:
                # print(f"\n[UART 收到]: {data.hex()}")
                pass
            elif parsed['cmd'] == 0x81:
                # 清除目前行，避免干擾使用者輸入
                sys.stdout.write('\r\033[2K')  # 回到行首並清除整行
                sys.stdout.flush()
                # 印出 UART 資料
                msg = parsed['payload'].decode('utf-8', errors='ignore')
                RSSI = parsed['rssi']
                print(f"[UART] {msg}, RSSI: {RSSI}dbm")
                # 重新顯示使用者輸入提示
                sys.stdout.write('[請輸入要發送的資料] > ')
                sys.stdout.flush()
        time.sleep(0.05)

def calculate_checksum(start, cmd, length, payload):
    """計算 checksum，包含 Start, CMD, LEN, PAYLOAD 的 XOR 總和"""
    cs = start ^ cmd ^ length
    for byte in payload:
        cs ^= byte
    return cs

def build_packet(cmd, payload):
    """建立 Telesto-III UART 封包"""
    start = 0x02
    length = len(payload)
    cs = calculate_checksum(start, cmd, length, payload)
    return bytes([start, cmd, length] + payload + [cs])

def parse_packet(data):
    """解析 Telesto 封包，正確處理 RSSI"""
    if len(data) < 5:  # 至少要有 Start, CMD, LEN, RSSI, CS
        return None

    start = data[0]
    cmd = data[1]
    length = data[2]
    payload_and_rssi = data[3:-1]
    cs = data[-1]

    # 驗證 checksum
    if cs != calculate_checksum(start, cmd, length, list(payload_and_rssi)):
        return None

    # 若為 0x81，最後一 byte 是 RSSI
    if cmd == 0x81:
        payload = payload_and_rssi[:-1]
        rssi = payload_and_rssi[-1]
        rssi = rssi - 256
    else:
        payload = payload_and_rssi
        rssi = None

    return {
        'start': start,
        'cmd': cmd,
        'length': length,
        'payload': payload,
        'rssi': rssi,
        'checksum': cs
    }