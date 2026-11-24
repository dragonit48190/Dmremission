# DM Remission Dashboard
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Project Status](https://img.shields.io/badge/status-development-orange)](#development-status)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](CONTRIBUTING.md)

ระบบ Dashboard สำหรับติดตามข้อมูล DM Remission  
โรงพยาบาลโพนสวรรค์

พัฒนาด้วย Django และเชื่อมต่อข้อมูลจาก HOSxP

## Technology

- Python 3.10+
- Django 5.2
- Bootstrap 5
- MariaDB / MySQL (HOSxP)
- SQLite สำหรับฐานข้อมูล Application ใน Development
- ThaID / OpenID Connect
- Authlib

## Features

- Dashboard สำหรับ DM Remission
- Authentication แบบ Local
- เตรียมรองรับการยืนยันตัวตนด้วย ThaID / OpenID Connect
- ตรวจสอบบุคลากรจาก HOSxP
- Role / Permission
- Profile และ Avatar จาก HOSxP
- Privacy Policy
- Terms of Use

## Project Path

Development:

```text
F:\ProjectWeb\Dmremission
```

Production URL ที่ออกแบบไว้:

```text
https://pswhospital.moph.go.th/Dmremission/
```

## Installation

Clone Repository:

```powershell
git clone https://github.com/dragonit48190/Dmremission.git
cd Dmremission
```

สร้าง Virtual Environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

ติดตั้ง Dependencies:

```powershell
pip install -r requirements.txt
```

สร้างไฟล์ `.env` จากตัวอย่าง:

```powershell
Copy-Item .env.example .env
```

จากนั้นแก้ไข `.env` และใส่ค่าของ Environment ที่ใช้งานจริง

> ห้ามนำ `.env`, Password, API Key หรือ Client Secret ขึ้น Git Repository

## Database Migration

```powershell
python manage.py migrate
```

## Django System Check

```powershell
python manage.py check
```

## Run Development Server

```powershell
python manage.py runserver
```

เปิด:

```text
http://127.0.0.1:8000/
```

## Environment Variables

รายการตัวแปรที่ต้องกำหนดดูได้จาก:

```text
.env.example
```

ตัวแปรสำคัญประกอบด้วย:

- `DJANGO_SECRET_KEY`
- `APP_PREFIX`
- `HOSXP_DB_HOST`
- `HOSXP_DB_PORT`
- `HOSXP_DB_NAME`
- `HOSXP_DB_USER`
- `HOSXP_DB_PASSWORD`
- `THAID_CLIENT_ID`
- `THAID_CLIENT_SECRET`
- `THAID_API_KEY`
- `THAID_SERVER_METADATA_URL`
- `THAID_REDIRECT_URI`
- `THAID_CID_CLAIM`

## HOSxP

ระบบเชื่อมต่อฐานข้อมูล HOSxP ผ่าน Django Database Alias:

```text
hosxp
```

บัญชีฐานข้อมูลสำหรับ Application ควรเป็น **Read Only** และกำหนดสิทธิ์ตามหลัก Least Privilege

ห้ามนำ Username หรือ Password ของฐานข้อมูลจริงใส่ลงใน Source Code

## ThaID

ระบบเตรียมรองรับการยืนยันตัวตนผ่าน ThaID ด้วย OpenID Connect

ค่าที่เกี่ยวข้อง ได้แก่:

- Client ID
- Client Secret
- API Key
- OIDC Discovery / Server Metadata URL
- Redirect URI
- PID/CID Claim

ค่าจริงทั้งหมดต้องจัดเก็บใน `.env` หรือ Secret Management ของ Environment เท่านั้น

Production Callback:

```text
https://pswhospital.moph.go.th/Dmremission/accounts/thaid/callback/
```

## Authentication and Authorization

ระบบมีผู้ใช้งาน 2 กลุ่มหลัก:

### Local Account

ใช้สำหรับผู้ดูแลระบบและกรณีฉุกเฉิน

### ThaID Account

ใช้ ThaID สำหรับยืนยันตัวตน และตรวจสอบข้อมูลบุคลากรกับ HOSxP

ระบบกำหนดสิทธิ์ตาม Role / Group และใช้หลัก Default Deny สำหรับผู้ที่ไม่มีสิทธิ์

## Security

แนวทางด้านความมั่นคงปลอดภัยของระบบ:

- ไม่เก็บ Password ของ HOSxP ใน Source Code
- ไม่ Commit `.env`
- ไม่ Commit API Key หรือ Client Secret
- ใช้ Parameterized Query
- ใช้บัญชี HOSxP แบบ Read Only
- ใช้ Role Based Access Control
- Default Deny สำหรับผู้ไม่มีสิทธิ์
- ใช้ HTTPS ใน Production
- Secret จัดเก็บผ่าน Environment Variables
- ควรดำเนินการ VA Scan / Penetration Test ก่อนเปิดใช้งานจริง

## Legal Pages

Privacy Policy:

```text
/Dmremission/privacy/
```

Terms of Use:

```text
/Dmremission/terms/
```

## Production Checklist

ก่อนนำระบบขึ้น Production ควรตรวจสอบอย่างน้อย:

- `DEBUG=False`
- `ALLOWED_HOSTS`
- HTTPS Certificate
- Reverse Proxy
- `APP_PREFIX=/Dmremission`
- Secure Session Cookie
- Secure CSRF Cookie
- HSTS
- CSRF Trusted Origins
- ThaID Configuration
- Database Permission
- Logging / Audit Log
- Backup
- VA Scan / Penetration Test

## Secret Files

ไฟล์ต่อไปนี้ห้าม Commit ขึ้น Repository:

```text
.env
key.txt
```

ไฟล์ตัวอย่างที่สามารถ Commit ได้:

```text
.env.example
```

## Development Status

สถานะปัจจุบัน:

```text
Development / Prototype
```

โปรเจกต์นี้สามารถใช้เป็นต้นแบบสำหรับระบบ Django ที่เชื่อมต่อ HOSxP และ ThaID ของโรงพยาบาลได้

## Repository

Public GitHub Repository:

```text
https://github.com/dragonit48190/Dmremission
```

## Organization

โรงพยาบาลโพนสวรรค์  
จังหวัดนครพนม

## License and Attribution

โปรเจกต์นี้เผยแพร่ภายใต้ MIT License

ส่วนของ Frontend UI มีพื้นฐานจาก InApp Dashboard Template  
Copyright (c) 2025 Codescandy  
เผยแพร่ภายใต้ MIT License

โปรดดูรายละเอียดเพิ่มเติมในไฟล์:

```text
LICENSE
```

ผู้สนใจสามารถนำโปรเจกต์ไปศึกษา ใช้งาน แก้ไข Fork และพัฒนาต่อยอดได้  
ภายใต้เงื่อนไขของ MIT License