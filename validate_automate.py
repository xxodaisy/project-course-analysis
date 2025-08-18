import pandas as pd

# Load dataset yang udah di-export dari script generator
transactions_df = pd.read_csv("transactions.csv")
redemption_df = pd.read_csv("redemption.csv")
completion_df = pd.read_csv("completion.csv")

# --- Pastikan semua kolom tanggal datetime ---
for df in [redemption_df, completion_df, transactions_df]:
    for col in ["transaction_date", "redemption_date", "enrollment_date", "completion_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

# --- VALIDASI OTOMATIS ---
def validate_timelines(redemption_df, completion_df, transactions_df):
    errors = []
    merged = redemption_df.merge(completion_df, on="transaction_id", suffixes=("_red", "_comp"))
    merged = merged.merge(transactions_df, on="transaction_id", how="left", suffixes=("", "_tx"))

    for idx, row in merged.iterrows():
        t = row["transaction_date"]
        r = row["redemption_date"]
        e = row["enrollment_date"]
        c = row["completion_date"]
        status = row["redemption_status"]
        is_void = row.get("is_void", False)
        discount = row.get("discount_percent", 0)
        final_price = row.get("final_price", 0)

        # Basic: transaction harus selalu ada
        if pd.isna(t):
            errors.append((row["transaction_id"], "Transaction date missing"))
            continue
        
        # Kalau pakai voucher (Used/Expired): redeem_date harus ≥ transaction_date
        if status in ["Used", "Expired"]:
            if pd.isna(r) or r < t:
                errors.append((row["transaction_id"], "Redeem date invalid (before transaction)"))
        
        # Kalau Used: enrollment_date harus ≥ redeem_date
        if status == "Used":
            if pd.isna(e) or e < r:
                errors.append((row["transaction_id"], "Enrollment date invalid (before redeem)"))
        
        # Kalau No Voucher: enrollment_date ≥ transaction_date
        if status is None:
            if pd.isna(e) or e < t:
                errors.append((row["transaction_id"], "Enrollment date invalid for no-voucher"))
        
        # Kalau Completed: completion_date harus ≥ enrollment_date
        if row["completion_status"] == "Completed":
            if pd.isna(c) or c < e:
                errors.append((row["transaction_id"], "Completion date invalid (before enrollment)"))

    if errors:
        print(f" Found {len(errors)} timeline errors:")
        for err in errors[:10]:  # tampilkan 10 pertama
            print(f"- TxID {err[0]}: {err[1]}")
    else:
        print(" All timelines are valid!")
       
       # 2. Konsistensi voucher
        if pd.isna(row["voucher_id"]) and status is not None:
            errors.append((row["transaction_id"], "Voucher status set but no voucher_id"))
        if not pd.isna(row["voucher_id"]) and status is None:
            errors.append((row["transaction_id"], "Voucher_id exists but redemption_status is None"))
        
        # 3. Transaksi void
        if is_void:
            if not pd.isna(e) or not pd.isna(c):
                errors.append((row["transaction_id"], "Void transaction should not have enrollment or completion"))
# Jalankan validasi
validate_timelines(redemption_df, completion_df, transactions_df)
