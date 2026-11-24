import math
from decimal import Decimal, getcontext

# ضبط دقة الحسابات إلى 50 خانة عشرية
getcontext().prec = 50

def fuss_catalan_coeff(n, k):
    """حساب معاملات حسّون-فوس-كاتالان العامة"""
    if k == 0: 
        return Decimal(1)
    comb = math.comb(n * k + 1, k)
    return Decimal(comb) / Decimal(n * k + 1)

def solve_hassoun_system(a_val, b_val, n=5, terms=30):
    a = Decimal(str(a_val))
    b = Decimal(str(b_val))
    
    # 1. حساب نصف قطر التقارب الحرج
    R_n = (Decimal(n - 1)**(n - 1)) / (Decimal(n)**n)
    z = b * (a**(n - 1))
    
    print("=" * 65)
    print(f"🔹 حل معادلة حسّون للدرجة {n}: x - ({b})*x^{n} = {a}")
    print(f"قيمة معامل التوسع z = {z:.6f}")
    print(f"نصف قطر التقارب الحرج R_{n} = {R_n:.6f}")
    
    if abs(z) >= R_n:
        print("❌ تحذير: المعاملات خارج نطاق التقارب! المتسلسلة ستتباعد.")
        return
    else:
        print("✅ المعاملات داخل نطاق التقارب التام (Convergence Zone).")
    
    # 2. حساب المجموع التراكمي لمتسلسلة فوس-كاتالان
    x = Decimal(0)
    for k in range(terms):
        coeff = fuss_catalan_coeff(n, k)
        term = a * coeff * (z**k)
        x += term
        
    print(f"\n🎯 الجذر التحليلي الدقيق x =")
    print(f"{x}")
    
    # 3. حساب مقدار المتبقي للتأكد من الدقة
    residual = x - b * (x**n) - a
    print(f"\n📊 مقدار الخطأ (Residual): {residual:.2e}")
    print("=" * 65 + "\n")

# --- التجارب الرياضية الناجحة ---

# التجربة 1: a = 1.0, b = 0.05 (درجة خامسة)
solve_hassoun_system(a_val=1.0, b_val=0.05, n=5, terms=35)

# التجربة 2: a = 2.0, b = 0.002 (درجة خامسة)
solve_hassoun_system(a_val=2.0, b_val=0.002, n=5, terms=35)