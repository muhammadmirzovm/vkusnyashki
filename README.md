# 🍔 Vkusnyashki - Fast Food Menu

**Vkusnyashki** loyihasi — bu real-time fast food menyu veb-ilovasi.  
Frontend HTML, Tailwind CSS va JavaScript bilan yaratilgan, backend esa Django + ASGI (Daphne) orqali real-time yangilanishlarni qo‘llab-quvvatlaydi.

---

## 📌 Xususiyatlar

- ✅ Fast food menu kartalari (burger, pizza, fries, va boshqalar)  
- ✅ Real-time CRUD operatsiyalari (yaratish, tahrirlash, o‘chirish)  
- ✅ `is_available` maydoni bo‘yicha menu filtrlanadi — faqat mavjud ovqatlar ko‘rinadi  
- ✅ Responsive dizayn (desktop, tablet, mobile)  
- ✅ ImageField qo‘llab-quvvatlanadi  
- ✅ SSE orqali real-time update  
- ✅ Admin panel orqali menyuni boshqarish  

---

## ⚙️ Texnologiyalar

- **Backend:** Django 5.2.x  
- **ASGI server:** Daphne  
- **Frontend:** HTML, Tailwind CSS, JavaScript  
- **Database:** SQLite (default, boshqa DB ham ishlaydi)  
- **Images:** Pillow  
- **Package manager / venv:** UV

---

## 🛠️ O‘rnatish UV bilan

1. Loyihani klon qilish:

```bash
git clone <repository-url>
cd vkusnyashki

uv venv create .venv
uv venv activate .venv

uv install -r requirements.txt
uv run python manage.py makemigrations
uv run python manage.py migrate