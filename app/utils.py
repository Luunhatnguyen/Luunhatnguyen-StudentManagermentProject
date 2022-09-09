from app import app, db
from app.model import User, UserRole, Lop, HocSinh, GiaoVien, NhanVien, Diem, MonHoc, KyHoc
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib
import json
from flask import jsonify
import sqlite3

conn = sqlite3.connect('studentsmanagement.db')

def general_stats():
    return db.session.query(Lop.IDLop, Lop.TenLop, func.count(HocSinh.IDHocSinh))\
                      .join(HocSinh, Lop.IDLop.__eq__(HocSinh.IDLop), isouter=True)\
                      .group_by(Lop.IDLop, Lop.TenLop).all()

def hocsinh_stats():
    return db.session.query(func.count(HocSinh.IDHocSinh))\
                        .select_from(HocSinh).all()

def giaovien_stats():
    return db.session.query(func.count(GiaoVien.IDGiaoVien))\
                        .select_from(GiaoVien).all()

def nhanvien_stats():
    return db.session.query(func.count(NhanVien.IDNhanVien))\
                        .select_from(NhanVien).all()

def lop_stats():
    return db.session.query(Lop.TenLop, func.count(Lop.IDLop))\
                        .select_from(Lop).all()

def ds_lop():
    return db.session.query(Lop.TenLop, Lop.IDLop) \
        .select_from(Lop).all()

#  Tinh Trung Binh Diem Cac Mon Hoc Cua Cac Hoc Sinh Lop Bat Ki
# Select SinhVien.MaSV,TenSV,Lop.TenLop,
#   From SinhVien,Diem,MonHoc,Lop
#    Where SinhVien.MaLop=Lop.MaLop And Diem.MaSV=SinhVien.MaSV And Diem.MaMH=MonHoc.MaMH
#    Group By SinhVien.MaSV,TenSV,Lop.TenLop
def DiemTB(ten_lop=None, ki_hoc=None, nam_hoc=None, mon_hoc=None):
    # q = db.session.query(Lop.TenLop, KyHoc.name, KyHoc.NamHoc, HocSinh.name, MonHoc.TenMH, Diem.DiemTB
    q = db.session.query(Lop.TenLop, KyHoc.name, KyHoc.NamHoc, Diem.DiemTB,
                         func.count(HocSinh.name), Lop.SiSo)\
                    .join(HocSinh, Lop.IDLop.__eq__(HocSinh.IDLop))\
                    .join(Diem, Diem.IDHocSinh.__eq__(HocSinh.IDHocSinh))\
                    .join(KyHoc, KyHoc.IDKyHoc.__eq__(Diem.IDKyHoc))\
                    .join(MonHoc, MonHoc.IDMonHoc.__eq__(Diem.IDMonhoc))
    if ten_lop:
        q = q.filter(Lop.TenLop.__eq__(ten_lop))
    if ki_hoc:
        q = q.filter(KyHoc.name.__eq__(ki_hoc))
    if nam_hoc:
        q = q.filter(KyHoc.NamHoc.__eq__(nam_hoc))
    if mon_hoc:
        q = q.filter(MonHoc.TenMH.__eq__(mon_hoc))
    q.filter(Diem.DiemTB >= 5 )
    # return q.group_by(Lop.TenLop, KyHoc.name, KyHoc.NamHoc, Diem.DiemTB).all()
    return q.group_by(Lop.TenLop).all()

def Diem_all(nam_hoc=None):
    q = db.session.query(Lop.TenLop, KyHoc.name, KyHoc.NamHoc, HocSinh.name, MonHoc.TenMH, Diem.DiemTB,
                         func.count(HocSinh.name), Lop.SiSo) \
        .join(HocSinh, Lop.IDLop.__eq__(HocSinh.IDLop)) \
        .join(Diem, Diem.IDHocSinh.__eq__(HocSinh.IDHocSinh)) \
        .join(KyHoc, KyHoc.IDKyHoc.__eq__(Diem.IDKyHoc)) \
        .join(MonHoc, MonHoc.IDMonHoc.__eq__(Diem.IDMonhoc))
    if nam_hoc:
        q = q.filter(KyHoc.NamHoc.__eq__(nam_hoc))

    return q.group_by(Lop.TenLop, KyHoc.name, KyHoc.NamHoc, Diem.DiemTB).all()

def check_user(username, password, role=UserRole.EMPLOYEE):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()
def register(name, gender, email, birthday, numbers, username, password, role, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(), username=username.strip(), password=password, user_role=role, birthday=birthday,
                avatar=kwargs.get('avatar'))

    if role.__eq__('EMPLOYEE'):
        nhanvien = NhanVien(name=name.strip(), gender=gender, numbers=numbers, birthday=birthday,
                email=email.strip() if email else email, avatar=kwargs.get('avatar'))
        db.session.add(nhanvien)
        db.session.add(user)
    if role.__eq__('TEACHER'):
        giaovien = GiaoVien(name=name.strip(), gender=gender, numbers=numbers, birthday=birthday,
                email=email.strip() if email else email, avatar=kwargs.get('avatar'))
        db.session.add(giaovien)
        db.session.add(user)


    try:
        db.session.commit()
    except:
        return False
    else:
        return True

def register_hocsinh(IDHocSinh, name, gender, email, birthday, numbers, username, password, avatar, note, address, lop, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(), username=username.strip(), password=password, user_role='STUDENT', birthday=birthday,
                avatar=kwargs.get('avatar'))

    hocsinh = HocSinh(IDHocSinh=IDHocSinh, name=name.strip(), gender=gender, numbers=numbers, birthday=birthday, IDLop=lop,
                            email=email.strip() if email else email, avatar=kwargs.get('avatar'), note=note, address=address)
    db.session.add(hocsinh)
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True


#tim kiem mon hoc
def Quan_ly_mon_hoc(kw=None):
    subj = db.session.query(MonHoc.IDMonHoc, MonHoc.TenMH) \
        .select_from(MonHoc).all()

    if kw:
        subj = [s for s in subj if s['TenMH'].lower().find(kw.lower()) >= 0]

    return subj

#xoa mon hoc
def xoa_mon(ID_mon_hoc=None):
    c =conn.cursor()
    sql = "delete from monhoc where id=ID_mon_hoc"
    c.execute(sql)
    conn.commit()
    conn.close()
    # subj = db.session.query(MonHoc.IDMonHoc, MonHoc.TenMH).delete_from(MonHoc).all()

#them mon hoc
def them_mon(TenMH):
    monhoc = MonHoc(TenMH=TenMH.strip())

    db.session.add(monhoc)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True

def get_user_by_id(user_id):
    return User.query.get(user_id)

def write_json(from_age_valid, end_age_valid):
    age_json = {
        "fromAgeValid": from_age_valid,
        "endAgeValid": end_age_valid
    }
    with open("./data/age.json", "w") as file_write:
        json.dump(age_json, file_write, indent=4)
    file_write.close()

#đếm học sinh của lớp có id
def count_student_lop(id=1):
    idlop = db.session.query(Lop.TenLop, func.count(Lop.IDLop)) \
        .join(HocSinh, Lop.IDLop.__eq__(HocSinh.IDLop), isouter=True)

    if id:
        idlop = idlop.filter(HocSinh.IDLop.__eq__(id))

    return idlop.group_by(HocSinh.IDLop).all()

# def write_json_siso(id, maxNumber):
def read_json_siso(file_path):
    try:
        with open(file_path, 'rb') as myfile:
            data = myfile.read()
        contracts = json.loads(data)
    except:
        print("Some thing went wrong!")

    return contracts

def processing(id, list_of_dict, max_number_t):
    ids = [dict['id'] for dict in list_of_dict]
    max_nums = [dict['maxNumber'] for dict in list_of_dict]
    if id not in ids:
        new_dict = {
            'id': id,
            'maxNumber': max_number_t
        }
        list_of_dict.append(new_dict)

    return list_of_dict



def read_json(path):
    with open(path) as f:
        return json.loads(f.read())
# path : "./data/age.json"



