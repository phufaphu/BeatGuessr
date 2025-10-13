# BeatGuessr

โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชา **Server-Side Web Development (รหัส 06016418)** คณะเทคโนโลยีสารสนเทศ สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง

---

## ✨ **ฟีเจอร์หลัก (Features)**

- **🎮 เกมเพลย์ทายเพลง:** ทายชื่อเพลงจากคลิปเสียงสั้นๆ ในรูปแบบ Multiple Choice พร้อมระบบจับเวลา 15 วินาที
- **👤 ระบบสมาชิกเต็มรูปแบบ:** สมัครสมาชิก, เข้าสู่ระบบ (ด้วย JWT), และจัดการโปรไฟล์ส่วนตัว
- **📊 ประวัติการเล่นและคะแนน:** สามารถดูประวัติการเล่นเกมย้อนหลังและคะแนนที่ทำได้ในแต่ละรอบที่หน้าโปรไฟล์
- **👑 ระบบจัดการสิทธิ์ผู้ใช้ (User Roles):** แบ่งผู้ใช้งานเป็น **Player** (ผู้เล่นทั่วไป) และ **Content Manager** (ผู้จัดการเนื้อหา) ที่มีความสามารถแตกต่างกันอย่างชัดเจน
- **🎵 ระบบจัดการเนื้อหา (CMS) สำหรับ Content Manager:**
  - สร้าง, แก้ไข, และลบเพลย์ลิสต์
  - เพิ่มเพลงลงในเพลย์ลิสต์ทีละเพลงโดยใช้ลิงก์ YouTube
  - ลบเพลงออกจากเพลย์ลิสต์
- **🚀 Import เพลงจาก YouTube Playlist:**
  - สามารถนำเข้าเพลงจาก YouTube Playlist ทั้งหมดได้โดยอัตโนมัติผ่านระบบ **Background Task** (Celery & Redis)
  - **📡 Real-time Logging:** แสดงผล Log การ Import เพลงแบบสดๆ บนหน้าเว็บผ่าน **WebSockets** (Django Channels)
- **⚙️ ระบบจัดการเบื้องหลังขั้นสูง:** หน้า Admin ของ Django ที่ปรับแต่งมาอย่างดีเพื่อให้ง่ายต่อการจัดการข้อมูลทั้งหมด
- **📱 Responsive Design:** รองรับการแสดงผลอย่างสวยงามบนทุกอุปกรณ์

---

## 🚀 **เทคโนโลยีที่ใช้ (Tech Stack)**

| Category           | Technology                                                                                             |
| :----------------- | :----------------------------------------------------------------------------------------------------- |
| **Backend**        | [Python](https://www.python.org/), [Django](https://www.djangoproject.com/), [Django REST Framework](https://www.django-rest-framework.org/), [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) |
| **Frontend**       | [Svelte / SvelteKit](https://svelte.dev/), [TypeScript](https://www.typescriptlang.org/), [Tailwind CSS](https://tailwindcss.com/) |
| **Background Tasks** | [Celery](https://docs.celeryq.dev/), [Redis](https://redis.io/) (as Broker)                             |
| **Real-time**      | [Django Channels](https://channels.readthedocs.io/) (WebSockets)                                         |
| **Audio Processing** | [yt-dlp](https://github.com/yt-dlp/yt-dlp), [pydub](https://github.com/jiaaro/pydub)                         |
| **Database**       | [PostgreSQL](https://www.postgresql.org/)                                                                              |

---

## 📦 **การติดตั้งและเริ่มต้นใช้งาน (Installation & Setup)**

ทำตามขั้นตอนต่อไปนี้เพื่อรันโปรเจกต์บนเครื่องของคุณ

### **📋 สิ่งที่ต้องมีก่อนติดตั้ง (Prerequisites)**

- **Python** (แนะนำเวอร์ชัน 3.12)
- **Node.js** (เวอร์ชัน 18 ขึ้นไป)
- **FFmpeg:**
  - **macOS:** `brew install ffmpeg`
  - **Windows:** ดาวน์โหลดจาก [FFmpeg Official Site](https://ffmpeg.org/download.html) แล้วเพิ่ม path ไปยัง `bin` folder ใน Environment Variables ของระบบ
- **Redis:**
  - **macOS:** `brew install redis`
  - **Windows:** ดาวน์โหลดและติดตั้ง [Redis on Windows](https://github.com/tporadowski/redis/releases) (แนะนำไฟล์ `.msi`)

### **1. Clone the Repository**

```bash
git clone https://github.com/phufaphu/BeatGuessr.git
cd BeatGuessr
```

### **2. ตั้งค่า Backend**

```bash
# 1. สร้างและเปิดใช้งาน virtual environment
# (Windows)
python -m venv venv
venv\Scripts\activate
# (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# 2. ตั้งค่า Environment Variables
cp .env.example .env
#    จากนั้นเปิดไฟล์ .env ขึ้นมาแล้วแก้ไขค่าต่างๆ ให้ถูกต้อง

# 3. ติดตั้งไลบรารีที่จำเป็น
pip install -r requirements.txt

# 4. เตรียมฐานข้อมูล PostgreSQL
#    - ตรวจสอบให้แน่ใจว่า PostgreSQL server ของคุณทำงานอยู่
#    - สร้างฐานข้อมูล (Database) และ User/Password ให้ตรงกับค่าในไฟล์ .env ของคุณ

# 5. สร้างและอัปเดตตารางในฐานข้อมูล
python manage.py migrate
```

### **3. ตั้งค่า Frontend**

```bash
# 1. เปิด Terminal ใหม่ แล้วเข้าไปที่โฟลเดอร์ frontend
cd frontend

# 2. ติดตั้งไลบรารีที่จำเป็น
# ใช้ npm
npm install

# ใช้ yarn
yarn install

# ใช้ pnpm
pnpm install
```

### **4. รันโปรเจคทั้งหมด (ต้องใช้ 3 Terminal)**

- **Terminal 1: รัน Redis และ Celery Worker**
  - **macOS:**

    ```bash
        # รัน Redis service (ถ้ายังไม่รัน)
        brew services start redis
        source venv/bin/activate
        celery -A config worker -l info
    ```

  - **Windows:**

    ```bash
        # โดยปกติ Redis จะรันเป็น Windows Service โดยอัตโนมัติหลังติดตั้ง
        venv\Scripts\activate
        celery -A config worker -l info -P gevent
    ```

- **Terminal 2: รัน Backend (Django Server)**

    ```bash
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate

    # รัน Django server
    python manage.py runserver
    ```

- **Terminal 3: รัน Frontend (Svelte Server)**

    ```bash
    # เข้าไปที่โฟลเดอร์ Frontend
    cd frontend

    # รัน Svelte dev server
    # ใช้ npm
    npm run dev

    # ใช้ yarn
    yarn dev

    # ใช้ pnpm
    pnpm dev
    
    ```

### **5. เปิดใช้งาน**

- เปิดเบราว์เซอร์แล้วไปที่ **`http://localhost:5173`**

---

## 🖼️ **ภาพหน้าจอ (Screenshot)**

![BeatGuessr Screenshot](/beatguessr-landing.png)
