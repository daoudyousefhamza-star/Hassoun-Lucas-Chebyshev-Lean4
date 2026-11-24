import sys
import time
import math

sys.set_int_max_str_digits(100000000)

def benchmark_giant_fast():
    print("=" * 80)
    print("🚀 اختبار مبرهنة حسّون بـ زحزحة البتات السريعة (Mersenne Bitwise Shift)")
    print("   M_136279841 = 2^136279841 - 1 (41 مليون رقم)")
    print("=" * 80)
    
    p = 136279841
    print("\n[1] جاري توليد الرقم والقناع الموديلي...")
    M_p = (1 << p) - 1
    m = math.ceil(math.log2(p))
    
    print(f"⚡ عدد خطوات حسّون اللوغاريتمية: {m} خطوة فقط!")
    print("=" * 80)
    
    val = 6
    t_start = time.perf_counter()
    
    for step in range(1, m + 1):
        step_t0 = time.perf_counter()
        
        # 1. التربيع
        sq = val * val
        
        # 2. الاختزال الموديلي الفائق عبر زحزحة البتات بدلاً من القسمة المطولة
        val = (sq & M_p) + (sq >> p)
        if val >= M_p:
            val -= M_p
            
        step_t1 = time.perf_counter() - step_t0
        print(f"  └─ ⚡ الخطوة [{step:2d}/{m}]: تمت زحزحة البتات والتربيع في {step_t1:.2f} ثانية")
        
    t_total = time.perf_counter() - t_start
    print("\n" + "=" * 80)
    print(f"🎉 اكتمل الاختبار بـ زحزحة البتات في: {t_total:.2f} ثانية ({t_total/60:.2f} دقيقة)!")
    print("=" * 80)

if __name__ == "__main__":
    benchmark_giant_fast()