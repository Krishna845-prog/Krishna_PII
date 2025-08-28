import csv
import json
import re
import sys

def mask_phone(p):
    if re.fullmatch(r"\d{10}", p):
        return p[:2] + "XXXXXX" + p[-2:]
    return p

def mask_aadhar(a):
    if re.fullmatch(r"\d{12}", a):
        return a[:4] + "XXXX" + a[-4:]
    return a

def mask_passport(pp):
    if re.fullmatch(r"[A-Z][0-9]{7}", pp):
        return pp[0] + "XXXXXX" + pp[-1]
    return pp

def mask_upi(u):
    parts = u.split("@")
    if len(parts) == 2:
        n, b = parts
        return n[:2] + "XXX@" + b[:2] + "XXX"
    return u

def mask_email(e):
    parts = e.split("@")
    if len(parts) == 2:
        user, dom = parts
        return user[:2] + "XXX@" + dom[0] + "XXX" + dom[-4:]
    return e

def mask_name(n):
    t = n.split()
    if len(t) == 2:
        return t[0][0] + "XXX " + t[1][0] + "XXX"
    elif len(t) == 1:
        return t[0][0] + "XXX"
    return n

def mask_address(a):
    return "[REDACTED]"

def mask_ip(ip):
    return "[REDACTED]"

def mask_generic(v):
    return "[REDACTED]"

cat_a = ["phone", "aadhar", "passport", "upi_id"]  # standalone
cat_b = ["name", "first_name", "last_name", "email", "address", "ip_address"]  # combinatorial
all_pii = cat_a + cat_b + ["customer_id", "pin_code", "kyc_status", "username", "contact", "address_proof", "nationality"]

def contains_pii(d):
    # first check standalone
    for k in cat_a:
        if k in d and d[k]:
            return True
    # now check combined
    count = 0
    for k in cat_b:
        if k in d and d[k]:
            count += 1
    if count >= 2:
        return True
    return False

def redact_record(d):
    newd = dict(d)  # copy lol
    for k in d:
        if k not in all_pii:
            continue
        v = str(d[k])
        if k == "phone":
            newd[k] = mask_phone(v)
        elif k == "aadhar":
            newd[k] = mask_aadhar(v)
        elif k == "passport":
            newd[k] = mask_passport(v)
        elif k == "upi_id":
            newd[k] = mask_upi(v)
        elif k == "email":
            newd[k] = mask_email(v)
        elif k in ["name", "first_name", "last_name"]:
            newd[k] = mask_name(v)
        elif k in ["address", "address_proof"]:
            newd[k] = mask_address(v)
        elif k == "ip_address":
            newd[k] = mask_ip(v)
        else:
            newd[k] = mask_generic(v)
    return newd

def main():
    if len(sys.argv) < 2:
        print("Usage: python ok.py <input_csv_file>")
        sys.exit(1)
    infile = sys.argv[1]
    outfile = "redacted_output_candidate_full_name.csv"
    with open(infile, "r", encoding="utf-8") as f, open(outfile, "w", newline="", encoding="utf-8") as fo:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(fo, fieldnames=["record_id", "redacted_data_json", "is_pii"])
        writer.writeheader()
        for r in reader:
            rec = r["record_id"]
            try:
                d = json.loads(r["data_json"])
            except:
                continue  # skip broken json lol
            pii = contains_pii(d)
            red = redact_record(d) if pii else d
            writer.writerow({
                "record_id": rec,
                "redacted_data_json": json.dumps(red, ensure_ascii=False),
                "is_pii": str(pii)
            })

if __name__ == "__main__":
    main()
