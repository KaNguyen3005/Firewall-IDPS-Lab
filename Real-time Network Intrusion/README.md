# Lab Realtime Network Intrusion Detection

## 1) Mục tiêu
- Xây dựng mô phỏng **IDS thời gian thực** để phân loại luồng mạng thành `BENIGN` hoặc các loại tấn công phổ biến.
- Tái sử dụng mô hình đã huấn luyện sẵn (Random Forest) và pipeline tiền xử lý để dự đoán ngay khi có flow mới.
- Ghi cảnh báo vào log khi phát hiện bất thường.

## 2) Kiến trúc & thành phần
- `main.py`: nạp model + scaler + label encoder + danh sách feature, nhận dữ liệu flow, chuẩn hóa, dự đoán, in/generate alert.
- `models/`: chứa các artifact đã huấn luyện (`random_forest_best_model.pkl`, `scaler.pkl`, `label_encoder.pkl`, `selected_features.pkl`).
- `alerts.log`: nơi lưu các cảnh báo phát hiện tấn công.
- `notebook/processingAndTrain.ipynb`: notebook cho bước tiền xử lý và huấn luyện.
- `data/README.md`: nguồn dataset dùng cho lab.

## 3) Dữ liệu sử dụng
- Dữ liệu tham khảo: Network Intrusion Dataset trên Kaggle (liên kết trong `data/README.md`).
- Nhóm feature realtime gồm các trường thống kê flow và cờ TCP như:
  - `Destination Port`, `Flow Duration`, `Total Fwd Packets`, `Total Backward Packets`
  - `Flow Bytes/s`, `Flow Packets/s`, `Packet Length Mean`, `Packet Length Std`
  - `SYN Flag Count`, `ACK Flag Count`, `FIN Flag Count`, `RST Flag Count`, `PSH Flag Count`, `URG Flag Count`

## 4) Quy trình realtime
1. Thu thập một flow đầu vào (trong lab dùng dữ liệu giả lập từ `sample_flows`).
2. Chuyển flow thành `DataFrame` và sắp thứ tự cột theo `selected_features.pkl`.
3. Chuẩn hóa dữ liệu bằng `scaler.pkl`.
4. Suy luận bằng `random_forest_best_model.pkl`.
5. Giải mã nhãn bằng `label_encoder.pkl`.
6. Nếu nhãn khác `BENIGN` thì:
   - in cảnh báo dạng: `[ALERT] Suspicious traffic detected: <label>. Destination Port: <port>.`
   - ghi thêm 1 dòng vào `alerts.log`.

## 5) Cách chạy demo
### Cài dependency
```bash
pip install -r requirement.txt
```

### Chạy mô phỏng realtime
```bash
python main.py
```

Mặc định, chương trình đang gọi:
```python
simulate_realtime_flow_loaded(sample_flows["DDoS"])
```
nên kết quả kỳ vọng là cảnh báo DDoS và có thêm bản ghi trong `alerts.log`.

## 6) Kết quả mong đợi
- Nếu flow bình thường (`BENIGN`):
  - Console: `[INFO] Normal traffic detected: BENIGN`
  - Không ghi cảnh báo vào log.
- Nếu flow tấn công (ví dụ `DDoS`, `PortScan`, `Bot`, ...):
  - Console: `[ALERT] Suspicious traffic detected: ...`
  - `alerts.log` được append thêm dòng cảnh báo.

## 7) Đánh giá nhanh
### Ưu điểm
- Pipeline rõ ràng, dễ tích hợp vào hệ thống giám sát.
- Suy luận nhanh do dùng mô hình đã huấn luyện.
- Có cơ chế log cảnh báo để phục vụ SOC/forensics.

### Hạn chế
- Hiện tại mới là mô phỏng với dữ liệu flow tĩnh (`sample_flows`), chưa đọc trực tiếp từ traffic thật (pcap/NetFlow).
- Chưa có ngưỡng độ tin cậy hoặc cơ chế giảm false positive.
- Chưa có dashboard realtime để trực quan hóa cảnh báo.

## 8) Hướng mở rộng
- Kết nối nguồn dữ liệu realtime (Zeek/Suricata/NetFlow collector).
- Bổ sung hàng đợi stream (Kafka/Redis) để xử lý lưu lượng lớn.
- Lưu cảnh báo vào Elasticsearch + hiển thị bằng Kibana/Grafana.
- Định kỳ retrain mô hình với dữ liệu mới để giảm drift.

## 9) Kết luận
Phần Lab Realtime đã hoàn thành mục tiêu cốt lõi: xây dựng được một luồng phát hiện xâm nhập gần thời gian thực dựa trên ML, có khả năng phân loại lưu lượng và phát cảnh báo tự động. Đây là nền tảng tốt để mở rộng thành hệ thống IDS vận hành thực tế.
