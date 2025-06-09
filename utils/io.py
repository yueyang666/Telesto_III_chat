import time

def uart_listener(ser, stop_event):
    """多線程監聽無線電payload"""
    while not stop_event.is_set():
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            parsed = parse_packet(data)
            if parsed['cmd'] == 0x40:
                print(f"\n[UART 收到]: {data.hex()}")
            elif parsed['cmd'] == 0x81:
                print(f"\n{parsed['payload'].decode('utf-8', errors='ignore')}")
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
    """簡易解析回應封包，僅供確認用"""
    if len(data) < 4:
        return None
    start = data[0]
    cmd = data[1]
    length = data[2]
    payload = data[3:-1]
    cs = data[-1]
    cs_calc = calculate_checksum(start, cmd, length, list(payload))
    if cs != cs_calc:
        return None
    return {
        'start': start,
        'cmd': cmd,
        'length': length,
        'payload': payload,
        'checksum': cs
    }