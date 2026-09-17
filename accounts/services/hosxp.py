from django.db import connections


def get_staff_by_cid(cid):
    """
    ค้นหาบุคลากรจาก HOSxP ด้วย CID
    HOSxP เป็น Source of Truth
    """

    if not cid:
        return None

    cid = str(cid).strip()

    if not cid.isdigit() or len(cid) != 13:
        return None

    sql = """
        SELECT
            d.cid,
            u.loginname,
            u.entryposition,
            u.groupname
        FROM opduser u
        INNER JOIN doctor d
            ON u.doctorcode = d.code
        WHERE d.cid = %s
        LIMIT 1
    """

    with connections["hosxp"].cursor() as cursor:
        cursor.execute(sql, [cid])
        row = cursor.fetchone()

    if not row:
        return None

    return {
        "cid": row[0],
        "loginname": row[1],
        "entryposition": row[2],
        "groupname": row[3],
    }
    
def get_staff_picture_by_cid(cid):
    """
    อ่านรูปบุคลากรจาก HOSxP เฉพาะเมื่อมีการร้องขอ Avatar
    """

    if not cid:
        return None

    cid = str(cid).strip()

    if not cid.isdigit() or len(cid) != 13:
        return None

    sql = """
        SELECT
            u.picture
        FROM opduser u
        INNER JOIN doctor d
            ON u.doctorcode = d.code
        WHERE d.cid = %s
        LIMIT 1
    """

    with connections["hosxp"].cursor() as cursor:
        cursor.execute(sql, [cid])
        row = cursor.fetchone()

    if not row or not row[0]:
        return None

    return bytes(row[0])