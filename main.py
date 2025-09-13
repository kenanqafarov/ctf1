import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Flaqı ətraf mühit dəyişəni (environment variable) kimi saxlayın
# render.com-da bunu 'Environment' bölməsində etmək tövsiyə olunur
FLAG = os.environ.get("FLAG", "CTF{s3cur3_c0d3_but_n0t_th1s_fl4g}")

@app.route("/")
def index():
    """Əsas səhifə, tətbiqin işlədiyini yoxlamaq üçün."""
    return jsonify({
        "message": "SQL Injection tapşırıq back-end-inə xoş gəldiniz!",
        "challenge_info": "Siz SQL Injection ilə gizli flaqı çıxarmalısınız. '/products' endpoint-ini yoxlayın.",
        "status": "active"
    })

@app.route("/products")
def get_products():
    """
    Simulyasiya edilmiş məhsul siyahısı.
    'category' parametri SQL Injection-a qarşı zəifdir.
    """
    category = request.args.get("category", "")
    
    # Həqiqi bir verilənlər bazası sorğusunu simulyasiya edir
    # İstifadəçinin daxil etdiyi dəyər birbaşa istifadə olunur, bu da zəiflik yaradır
    sql_query_template = "SELECT * FROM products WHERE category = '{}'".format(category)

    # Bu, flaqı gizlətmək üçün xüsusi bir məntiqdir
    # Əgər istifadəçinin sorğusu 'TRUE' (doğru) dəyərini qaytarırsa
    # Və bu dəyərin uzunluğu flaqın uzunluğuna uyğundursa
    # Bu, blind SQL Injection hücumu üçün vacibdir
    if "substring" in category.lower() and "length" in category.lower():
        if "sleep" in category.lower():
            return jsonify({"status": "error", "message": "Zəifliklərdən istifadə edin, amma `sleep` funksiyasından yox"})
        
        # İstifadəçinin sorğusunu bir Python ifadəsi kimi dəyərləndiririk
        # Bu, başqa bir təhlükəsizlik zəifliyidir, lakin tapşırığın məqsədi budur
        try:
            # Həqiqi bir verilənlər bazası cavabını simulyasiya edin
            # Doğru sorğu halında, 'product' tapılır, əks halda yox
            is_match = eval(category.replace('FLAG', f'"{FLAG}"'))
            if is_match:
                # Blind SQL Injection üçün "doğru" cavabı simulyasiya edin
                return jsonify({"status": "success", "message": "Məhsullar tapıldı!", "products": ["Telefon"]})
            else:
                return jsonify({"status": "failure", "message": "Məhsul tapılmadı.", "products": []})
        except:
            return jsonify({"status": "error", "message": "Sorğu xətası."})
            
    # Əgər flaqın hissəsi yoxlanılmırsa, normal cavab verin
    products = {
        "elektronika": ["Laptop", "Telefon", "Planşet"],
        "kitab": ["Roman", "Elmi-Fantastika"]
    }
    
    # Normal məhsul axtarışı
    if category in products:
        return jsonify({
            "status": "success",
            "message": "Məhsullar tapıldı!",
            "products": products[category]
        })
    else:
        return jsonify({
            "status": "failure",
            "message": "Məhsul tapılmadı.",
            "products": []
        })

@app.route("/solve", methods=["POST"])
def solve_challenge():
    """
    İstifadəçinin göndərdiyi flaqı yoxlayır.
    """
    data = request.get_json()
    submission = data.get("flag", "").strip()

    if submission == FLAG:
        return jsonify({"status": "success", "message": "Təbriklər! Doğru flaqı tapdınız!"})
    else:
        return jsonify({"status": "failure", "message": "Səhv flaq. Yenidən cəhd edin."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
