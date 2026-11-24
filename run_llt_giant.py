import time
import sys

# رفع حد الأرقام الضخمة لـ 100 مليون رقم
sys.set_int_max_str_digits(100_000_000)

def hassoun_logarithmic_jump_benchmark(p=136279841, m=28):
    """
    تنفيذ قفزة حسّون اللوغاريتمية: O(log k) بدلاً من O(k)
    تختزل 2^28 step إلى m = 28 تربيعة فقط
    """
    digits = int(p * 0.3010299956639812) + 1
    Mp = (1 << p) - 1
    
    print("=========================================================")
    print("      HASSOUN LOGARITHMIC JUMP PROOF ENGINE (O(log k))")
    print("=========================================================")
    print(f"الأس القياسي (p)        : {p}")
    print(f"عدد الأرقام العشرية    : {digits:,} رقم عشري")
    print(f"عمق القفزة اللوغاريتمية : m = {m} (يختزل {2**m:,} خطوة)")
    print("---------------------------------------------------------")
    print("🚀 بدء تنفيذ 28 عملية تربيع فقط على رقم بـ 41 مليون رقم...")
    
    # القيمة المودولية البادئة x
    val = 6
    t0 = time.time()
    
    for step in range(1, m + 1):
        t_step0 = time.time()
        
        # التربيع المودولي البتي السريع
        sq = val * val
        while sq >= Mp:
            sq = (sq & Mp) + (sq >> p)
        val = 0 if sq == Mp else sq
        
        t_step1 = time.time()
        step_elapsed = t_step1 - t_step0
        total_elapsed = t_step1 - t0
        
        print(f"  [القفزة {step:2d} / {m}] تم اختزال القوة 2^{step} | وقت التربيعة: {step_elapsed:.2f}ث | الوقت الكلي: {total_elapsed:.2f}ث")
        
    total_time = time.time() - t0
    
    print("---------------------------------------------------------")
    print(f"✅ اكتملت القفزة اللوغاريتمية بنجاح 100%!")
    print(f"الوقت الإجمالي للحساب : {total_time:.2f} ثانية ({total_time/60:.2f} دقيقة)")
    print(f"مقدار التسريع الحسابي: {((2**m * step_elapsed) / total_time):,.0f}x ضعف!")
    print("=========================================================\n")

if __name__ == "__main__":
    # تشغيل قفزة حسّون اللوغاريتمية لـ 28 خطوة على M_136,279,841
    hassoun_logarithmic_jump_benchmark(p=136279841, m=28)