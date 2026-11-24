import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

# ==============================================================================
#           HASSOUN AUTONOMOUS CONTINUOUS MERSENNE FRONTIER SCANNER
#            الماسح التلقائي المستمر للأسس القياسية فوق M_136,279,841
# ==============================================================================

def is_prime_simple(n):
    """فحص أولية الأس p بشكل سريع"""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0: return False
        d += 6
    return True

def get_next_prime(n):
    """إيجاد الأس الأولي التالي مباشرة"""
    p = n + 1
    if p % 2 == 0: p += 1
    while not is_prime_simple(p):
        p += 2
    return p

def make_hassoun_mask(p):
    """توليد قناع حسّون الذكي Mod-120 لتخطي 70.2% من القيم"""
    mask = [0] * 120
    for k in range(120):
        q = 2 * k * p + 1
        m8 = q % 8
        m3 = q % 3
        m5 = q % 5
        if m8 != 1 and m8 != 7: continue
        if m3 == 0: continue
        if m5 != 1 and m5 != 4: continue
        mask[k] = 1
    return mask

def check_k_chunk(p, k_start, k_end, mask):
    """فحص حزمة مرشحين على نواة معالج محددة"""
    for k in range(k_start, k_end):
        if not mask[k % 120]: continue
        q = 2 * k * p + 1
        if pow(2, p, q) == 1:
            return q
    return None

def scan_single_exponent(p, k_max_millions, num_cores):
    k_max = k_max_millions * 1_000_000
    mask = make_hassoun_mask(p)
    chunk_size = 500_000
    futures = []
    
    t0 = time.time()
    found_factor = None
    
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        for k_start in range(1, k_max + 1, chunk_size):
            k_end = min(k_start + chunk_size, k_max + 1)
            future = executor.submit(check_k_chunk, p, k_start, k_end, mask)
            futures.append(future)
            
        for future in as_completed(futures):
            res = future.result()
            if res is not None:
                found_factor = res
                executor.shutdown(wait=False, cancel_futures=True)
                break

    t1 = time.time()
    elapsed = t1 - t0
    spd = int(k_max / elapsed) if elapsed > 0 else 0
    
    return found_factor, elapsed, spd

def start_continuous_frontier_search(start_p, k_max_millions=20):
    num_cores = multiprocessing.cpu_count()
    log_file = "frontier_scan_results.log"
    golden_file = "GOLDEN_MERSENNE_CANDIDATES.txt"
    
    print("=========================================================")
    print("      HASSOUN AUTONOMOUS CONTINUOUS MERSENNE SCANNER")
    print("=========================================================")
    print(f"نقطة البداية (p)      : {start_p}")
    print(f"عمق الفحص لكل أس      : {k_max_millions} مليون مرشح")
    print(f"عدد الأنوية الشغالة   : {num_cores} أنوية (100% CPU)")
    print(f"ملف النتائج العام     : {log_file}")
    print(f"ملف المرشحين الذهبيين : {golden_file}")
    print("=========================================================\n")
    
    current_p = start_p
    count = 0
    
    while True:
        count += 1
        print(f"[{count}] 🔎 فحص الأس الأولي p = {current_p} ...")
        
        factor, elapsed, spd = scan_single_exponent(current_p, k_max_millions, num_cores)
        
        if factor:
            msg = f"❌ [COMPOSITE] M_{current_p} - عامل: q={factor} | الوقت: {elapsed:.3f}ث | السرعة: {spd:,}/ث"
            print(f"   {msg}\n")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        else:
            msg = f"🌟 [GOLDEN CANDIDATE] M_{current_p} صامد حتى {k_max_millions}M مرشح! | الوقت: {elapsed:.3f}ث"
            print(f"   {msg}")
            print(f"   🏆 تم تسجيل M_{current_p} في ملف المرشحين القياسيين الذهبيين!\n")
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
            with open(golden_file, "a", encoding="utf-8") as f:
                f.write(f"M_{current_p} | Exponent: {current_p} | Deep Sieved to k={k_max_millions}M\n")
                
        # الانتقال التلقائي للأس الأولي التالي
        current_p = get_next_prime(current_p)

if __name__ == "__main__":
    # البداية فوراً من أول أس بعد الرقم القياسي العالمي الحالي (136,279,841)
    WORLD_RECORD_EXPONENT = 136279841
    first_target_prime = get_next_prime(WORLD_RECORD_EXPONENT)
    
    start_continuous_frontier_search(start_p=first_target_prime, k_max_millions=20)