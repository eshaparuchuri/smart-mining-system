def check_alert(data, anomaly):
    if anomaly:
        print(f"🚨 ALERT: Machine {data['machine_id']} anomaly detected!")

    if data["temperature"] > 100:
        print(f"🔥 CRITICAL: Machine {data['machine_id']} overheating!")