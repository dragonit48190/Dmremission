\# Security Policy



โครงการ DM Remission Dashboard ให้ความสำคัญกับความมั่นคงปลอดภัยของระบบ ข้อมูลผู้ใช้งาน และข้อมูลที่เกี่ยวข้องกับระบบสารสนเทศของโรงพยาบาล



\## การรายงานช่องโหว่



หากพบช่องโหว่ด้านความมั่นคงปลอดภัย กรุณาอย่าเปิดเผยรายละเอียดช่องโหว่ที่สามารถนำไปใช้โจมตีระบบจริงผ่าน Public Issue



โดยเฉพาะข้อมูลต่อไปนี้ไม่ควรถูกเผยแพร่ใน Issue, Pull Request, Screenshot หรือ Source Code:



\- Password

\- API Key

\- Client Secret

\- Access Token

\- Refresh Token

\- Session Cookie

\- Database Credential

\- Private Key

\- ข้อมูลผู้ป่วย

\- CID / PID จริง

\- ข้อมูลส่วนบุคคล

\- IP Address หรือรายละเอียดโครงสร้างระบบภายในที่มีความอ่อนไหว

\- ตัวอย่าง Payload ที่สามารถนำไปโจมตีระบบจริงได้โดยตรง



\## วิธีรายงาน



กรุณาติดต่อผู้ดูแล Repository ผ่านช่องทางส่วนตัวของ GitHub หรือช่องทางที่เจ้าของโครงการประกาศไว้



รายงานควรประกอบด้วย:



\- คำอธิบายช่องโหว่

\- ส่วนของระบบที่ได้รับผลกระทบ

\- ขั้นตอนในการตรวจสอบปัญหา

\- ผลกระทบที่อาจเกิดขึ้น

\- แนวทางแก้ไข หากมี



กรุณาหลีกเลี่ยงการแนบข้อมูลจริงจากระบบ Production



\## ขอบเขต



โครงการนี้อยู่ในสถานะ Development / Prototype



ผู้ที่นำโครงการไปติดตั้งใช้งานจริงมีหน้าที่ตรวจสอบและกำหนดมาตรการด้านความมั่นคงปลอดภัยของ Environment ของตนเอง เช่น:



\- Production Configuration

\- HTTPS

\- Reverse Proxy

\- Firewall

\- Access Control

\- Database Permission

\- Secret Management

\- Logging / Audit Log

\- Backup

\- Patch Management

\- Vulnerability Assessment

\- Penetration Test



\## Secret Management



ห้าม Commit Secret ลง Git Repository



ไฟล์หรือข้อมูลลับควรจัดเก็บผ่าน Environment Variables หรือ Secret Management ที่เหมาะสม



ตัวอย่างไฟล์ที่ห้าม Commit:



```text

.env

key.txt

```



ไฟล์ตัวอย่างที่สามารถ Commit ได้:



```text

.env.example

```



\## HOSxP



การเชื่อมต่อ HOSxP ควรใช้บัญชีฐานข้อมูลแบบ Read Only และกำหนดสิทธิ์ตามหลัก Least Privilege



ไม่ควรใช้บัญชีที่มีสิทธิ์แก้ไขข้อมูล HOSxP เว้นแต่ระบบมีความจำเป็นและผ่านการประเมินความเสี่ยงแล้ว



\## ThaID / OpenID Connect



ห้ามเผยแพร่ค่าจริงของ:



\- Client Secret

\- API Key

\- Token

\- Private Key

\- Credential อื่นที่เกี่ยวข้องกับระบบยืนยันตัวตน



ค่าดังกล่าวต้องจัดเก็บนอก Source Code



\## ข้อมูลจริง



ห้ามใช้หรือ Commit ข้อมูลผู้ป่วยหรือข้อมูลส่วนบุคคลจริงลง Repository สาธารณะ



สำหรับการพัฒนาและทดสอบ ควรใช้ข้อมูลจำลองหรือข้อมูลที่ไม่สามารถระบุตัวบุคคลได้



\## Responsible Disclosure



ผู้พัฒนาสนับสนุนการรายงานช่องโหว่อย่างรับผิดชอบ เพื่อให้มีโอกาสตรวจสอบและแก้ไขปัญหาก่อนมีการเปิดเผยรายละเอียดต่อสาธารณะ



###### ขอบคุณทุกท่านที่ช่วยทำให้โครงการนี้มีความปลอดภัยมากขึ้น

