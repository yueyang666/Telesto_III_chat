# Telesto_III_chat

`Telesto_III_chat` 是一個以 Python 撰寫的簡易範例程式，用於透過 UART 與 Würth Elektronik 的 **Telesto‑III 無線模組**通訊。  
程式會在背景偵聽模組回傳的封包並解析 RSSI，同時提供互動式介面讓使用者輸入欲傳送的資料。


## 主要功能

- **Telesto‑III 封包建構與解析**  
  `utils/io.py` 提供 `build_packet()` 與 `parse_packet()`，用來產生並解析 UART 封包。

- **背景 UART 監聽**  
  使用 `uart_listener()` 持續讀取模組回傳資料，並顯示 RSSI 強度。

- **簡易互動介面**  
  `main.py` 提供命令列介面，允許使用者即時輸入與模組互動。

## 環境需求 Requirements

- Python 3.7 以上
- `pyserial` 套件
- 與電腦連接的 **Telesto‑III 無線模組**


## 安裝

```bash
# 安裝相依套件
pip install pyserial
````

## 使用方式 Usage

1. 請確保電腦擁有USB to TTL 驅動CH340(若無請到[沁恒微电子](https://www.wch.cn/downloads/ch341ser_exe.html)下載)

2. 將 Telesto‑III 模組連接至電腦，預設使用序列埠 `COM4`
   （如需修改請編輯 `main.py` 中的 `COM_PORT` 變數）

3. 執行主程式：

   ```bash
   python3 main.py
   ```

4. 於提示字元輸入欲發送的文字
   輸入 `exit` 或 `quit` 可離開程式

5. 收到的回應資料將顯示在螢幕，包含解碼後文字與 RSSI 值

## 專案結構

```
Telesto_III_chat/
├── main.py          # 主程式
├── utils/
│   └── io.py        # 封包建構、解析與 UART 監聽
├── doc/
│   └── UM_Telesto-III_2609011x91000 (rev2.13).pdf  # 官方手冊
├── LICENSE          # 授權條款
```

## 參考文件

更完整的 Telesto‑III UART 協議與指令集，請參考：

`doc/UM_Telesto-III_2609011x91000 (rev2.13).pdf`


## 授權

本專案以 [MIT License](./LICENSE) 授權釋出。
