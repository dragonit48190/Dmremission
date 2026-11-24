\# Contributing to DM Remission Dashboard



ขอบคุณที่สนใจร่วมพัฒนาโครงการ DM Remission Dashboard



โครงการนี้เปิดให้ผู้สนใจนำไปศึกษา ใช้งาน Fork แก้ไข และพัฒนาต่อยอดได้ภายใต้ MIT License



\## วิธีร่วมพัฒนา



1\. Fork Repository นี้ไปยัง GitHub Account ของคุณ

2\. Clone Repository ที่ Fork แล้วลงเครื่อง

3\. สร้าง Branch ใหม่สำหรับงานที่ต้องการพัฒนา

4\. แก้ไขและทดสอบระบบ

5\. Commit การเปลี่ยนแปลง

6\. Push Branch ขึ้น GitHub

7\. ส่ง Pull Request กลับมายัง Repository ต้นฉบับ



ตัวอย่าง:



```powershell

git checkout -b feature/my-feature

```



หลังแก้ไข:



```powershell

git add .

git commit -m "Add my feature"

git push origin feature/my-feature

```



จากนั้นสร้าง Pull Request ผ่าน GitHub



\## แนวทางการพัฒนา



กรุณารักษาแนวทางต่อไปนี้:



\- ไม่ Commit `.env`

\- ไม่ Commit Password, API Key, Client Secret หรือ Token

\- ไม่ Commit ข้อมูลผู้ป่วยหรือข้อมูลส่วนบุคคลจริง

\- ไม่ Commit Database Dump หรือ Backup

\- ใช้ Parameterized Query สำหรับ SQL

\- ใช้บัญชี HOSxP แบบ Read Only

\- ใช้หลัก Least Privilege

\- ใช้ Role Based Access Control

\- หลีกเลี่ยงการ Hard-code Secret หรือ Environment-specific Configuration

\- ทดสอบ `python manage.py check` ก่อนส่ง Pull Request



\## การตั้งค่า Environment



ให้สร้างไฟล์ `.env` จาก:



```text

.env.example

```



ตัวอย่าง:



```powershell

Copy-Item .env.example .env

```



จากนั้นกำหนดค่าของ Environment ของคุณเอง



ห้ามนำ `.env` จริงขึ้น Git Repository



\## การทดสอบก่อนส่ง Pull Request



อย่างน้อยควรตรวจ:



```powershell

python manage.py check

```



และควรทดสอบ Feature ที่แก้ไขให้ทำงานได้ตามที่คาดหวัง



\## Security



หากพบช่องโหว่ด้านความมั่นคงปลอดภัย กรุณาอย่าเปิดเผยรายละเอียดช่องโหว่ที่สามารถนำไปโจมตีระบบจริงผ่าน Public Issue



โปรดดูแนวทางเพิ่มเติมใน:



```text

SECURITY.md

```



\## Pull Request



Pull Request ควรระบุ:



\- ปัญหาหรือ Feature ที่แก้ไข

\- แนวทางที่ใช้

\- ไฟล์หรือส่วนของระบบที่ได้รับผลกระทบ

\- วิธีทดสอบ

\- Screenshot หากเกี่ยวข้องกับ UI



\## License



การมีส่วนร่วมในโครงการนี้ถือว่ายอมรับว่า Contribution ของคุณสามารถเผยแพร่ภายใต้ MIT License ของโครงการได้



โปรดดูรายละเอียดใน:



```text

LICENSE

```

