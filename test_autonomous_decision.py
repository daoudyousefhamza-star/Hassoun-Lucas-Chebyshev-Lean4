import sys
import time
import math

sys.set_int_max_str_digits(100000000)

def is_small_prime(n):
    """التحقق من أن الأس p أولي"""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def llt_autonomous_check(p):
    """
    تنفيذ فحص لوكاس-ليهمر المستقل تماماً باستخدام زحزحة البتات
    """
    if p == 2:
        return 0, True
    
    Mp = (1 << p) - 1
    s = 4
    
    # تنفيذ p - 2 تكرار كامل
    for _ in range(p - 2):
        sq = s * s - 2
        s = (sq & Mp) + (sq >> p)
        while s >= Mp:
            s -= Mp
        if s == Mp:
            s = 0
            
    is_prime = (s == 0)
    return s, is_prime

def run_continuous_scanner(max_p=130):
    print("=" * 110)
    print(f"🔬 الماسح الشامل المستقل لاختبار كل أعداد ميرسين المتتالية من p=2 حتى p={max_p}")
    print("   الخوارزمية تفحص كل عدد على حدة وتتخذ القرار الرياضي بنفسها 100%")
    print("=" * 110)
    
    primes_to_test = [p for p in range(2, max_p + 1) if is_small_prime(p)]
    
    print(f"{'الأس p':<6} | {'عدد الأرقام':<12} | {'زمن الفحص':<14} | {'قرار الخوارزمية التلقائي':<25} | {'قيمة الباقي s النهائي'}")
    print("-" * 110)
    
    primes_found = []
    composites_found = []
    
    t_start_all = time.perf_counter()
    
    for p in primes_to_test:
        num_digits = int(p * 0.30102999566) + 1
        
        t0 = time.perf_counter()
        residue, is_prime = llt_autonomous_check(p)
        dt = time.perf_counter() - t0
        
        time_str = f"{dt*1000:.3f} ms"
        
        if is_prime:
            primes_found.append(p)
            decision_str = "👑 أولي (PRIME) ✅"
            res_str = "0 (باقي صفري تام)"
        else:
            composites_found.append(p)
            decision_str = "❌ مركب (COMPOSITE)"
            res_str = str(residue)
            if len(res_str) > 25:
                res_str = res_str[:12] + "..." + res_str[-10:]
                
        print(f"M_{p:<4} | {num_digits:<12,} | {time_str:<14} | {decision_str:<25} | {res_str}")
        
    t_total_all = time.perf_counter() - t_start_all
    
    print("=" * 110)
    print("📊 الإحصائية الشاملة لنتائج الفحص المستقل:")
    print(f"🔹 إجمالي الأعداد التي تم مسحها: {len(primes_to_test)} عدداً")
    print(f"👑 أعداد ميرسين الأولية المكتشفة تلقائياً ({len(primes_found)} أعداد):")
    print(f"   {['M_' + str(p) for p in primes_found]}")
    print(f"\n❌ أعداد ميرسين المركبة التي تم كشفها ورفضها ({len(composites_found)} عدداً):")
    print(f"   {['M_' + str(p) for p in composites_found]}")
    print(f"\n⏱️ استغرق مسح وفحص جميع الأعداد بالكامل: {t_total_all:.4f} ثانية فقط!")
    print("=" * 110)

if __name__ == "__main__":
    run_continuous_scanner(max_p=130)