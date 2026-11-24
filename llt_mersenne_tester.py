import time
import sys

# رفع حد تحويل الأرقام الضخمة في بايثون
sys.set_int_max_str_digits(100_000_000)

def bitwise_mersenne_reduction(sq, p, Mp):
    """
    اختزال مودولو ميرسين السريع جداً بالعمليات البتية
    """
    while sq >= Mp:
        sq = (sq & Mp) + (sq >> p)
    return 0 if sq == Mp else sq

def fast_lucas_lehmer_test(p):
    """
    اختبار لوكاس-ليهمر (LLT) القاطع مع إظهار التقدم
    """
    if p == 2:
        return True
    
    Mp = (1 << p) - 1
    s = 4
    t0 = time.time()
    digits = int(p * 0.3010299956639812) + 1
    total_steps = p - 2
    
    print(f"=========================================================")
    print(f"      HASSOUN LUCAS-LEHMER PRIMALITY PROVER")
    print(f"=========================================================")
    print(f"الأس المفحوص (p)       : {p}")
    print(f"عدد الأرقام العشرية    : {digits:,} رقم عشري")
    print(f"عدد الخطوات المطلوبة   : {total_steps:,} خطوة")
    print(f"---------------------------------------------------------")
    
    report_step = max(1, total_steps // 10)
    
    try:
        for k in range(1, total_steps + 1):
            sq = s * s - 2
            s = bitwise_mersenne_reduction(sq, p, Mp)
            
            if k % report_step == 0 or k == total_steps:
                pct = (k / total_steps) * 100
                elapsed = time.time() - t0
                spd = k / elapsed if elapsed > 0 else 0
                print(f"  [Progress {pct:5.1f}%] الخطوة: {k:,} / {total_steps:,} | السرعة: {spd:,.0f} خطوة/ث | الوقت: {elapsed:.2f}ث")
                
        is_prime = (s == 0)
        elapsed = time.time() - t0
        
        print(f"---------------------------------------------------------")
        print(f"الوقت الإجمالي : {elapsed:.4f} ثانية")
        if is_prime:
            print(f"🏆 نتيجة جازمة: M_{p} عدد أولي مؤكد 100%! (s_{total_steps} = 0)")
        else:
            print(f"❌ نتيجة جازمة: M_{p} عدد مركب (s_{total_steps} != 0)")
        print(f"=========================================================\n")
        return is_prime

    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف الفحص بواسطة المستخدم بنجاح.")
        print("=========================================================\n")
        return None

if __name__ == "__main__":
    print("🚀 بدء سلسلة إثبات أولية أعداد ميرسين القياسية...\n")
    
    # قائمة بالأعداد القياسية لاختبار أوليتها المباشرة
    benchmark_primes = [
        31,     # M_31 (10 أرقام)
        127,    # M_127 (39 رقم)
        521,    # M_521 (157 رقم)
        2203,   # M_2203 (664 رقم)
        4253,   # M_4253 (1,281 رقم)
        9689,   # M_9689 (2,917 رقم)
        19937,  # M_19937 (6,002 رقم عشري)
    ]
    
    for p_val in benchmark_primes:
        res = fast_lucas_lehmer_test(p_val)
        if res is None:
            break