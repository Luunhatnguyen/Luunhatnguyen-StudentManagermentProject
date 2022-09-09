from app import db
from sqlalchemy import Column, Integer, Float, String, Boolean, Enum, ForeignKey, DateTime, Enum, CHAR
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2
    TEACHER = 3
    STUDENT = 4

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    birthday = Column(DateTime)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)

    giaovien = relationship('GiaoVien', backref='User', lazy=True)
    nhanvien = relationship('NhanVien', backref='User', lazy=True)

    def __str__(self):
        return self.name

class GiaoVien(db.Model):
    IDGiaoVien = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime)
    email = Column(String(50))
    numbers = Column(String(50))
    gender = Column(String(50), nullable=False)
    avatar = Column(String(100))
    note = Column(String(100))

    user_id = Column(Integer, ForeignKey(User.id))

    def __str__(self):
        return self.name

class NhanVien(db.Model):
    IDNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime)
    email = Column(String(50))
    numbers = Column(String(50))
    gender = Column(String(50), nullable=False)
    note = Column(String(100))
    avatar = Column(String(100))

    nhanvien = Column(Integer, ForeignKey(User.id))

    def __str__(self):
        return self.name

class KyHoc(db.Model):
    IDKyHoc = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), default='HK1', nullable=False)
    NamHoc = Column(String(25), nullable=False)

    IDLop = relationship('Diem', backref='kyhoc', lazy=True)

    def __str__(self):
        return self.name

class Lop(db.Model):
    __tablename__ = 'lop'

    IDLop = Column(Integer, primary_key=True, autoincrement=True)
    TenLop = Column(String(15), nullable=False, unique=True)
    SiSo = Column(Integer)

    IDHocSinh = relationship('HocSinh', backref='lop', lazy=True)

class MonHoc(db.Model):
    __tablename__ = 'monhoc'
    IDMonHoc = Column(Integer, primary_key=True, autoincrement=True)
    TenMH = Column(String(30), nullable=False)

    diem = relationship('Diem', backref='monhoc', lazy=False)

    def __str__(self):
        return self.TenMH

class HocSinh(db.Model):
    IDHocSinh = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime)
    email = Column(String(50), nullable=False, unique=True)
    numbers = Column(String(50))
    gender = Column(String(50), nullable=False)
    avatar = Column(String(100))
    address = Column(String(100))
    note = Column(String(100))

    IDLop = Column(Integer, ForeignKey(Lop.IDLop))

    Diem_HocSinh = relationship('Diem', backref='hocsinh', lazy=False)

    def __str__(self):
        return self.name

class Diem(db.Model):
    IDHocSinh = Column(Integer, ForeignKey(HocSinh.IDHocSinh), primary_key=True)
    IDMonhoc = Column(Integer, ForeignKey(MonHoc.IDMonHoc), primary_key=True)
    IDKyHoc = Column(Integer, ForeignKey(KyHoc.IDKyHoc), primary_key=True)
    Diem15p_1 = Column(Float, default=0)
    Diem15p_2 = Column(Float, default=0)
    Diem15p_3 = Column(Float, default=0)
    Diem15p_4 = Column(Float, default=0)
    Diem15p_5 = Column(Float, default=0)

    Diem1Tiet_1 = Column(Float, default=0)
    Diem1Tiet_2 = Column(Float, default=0)
    Diem1Tiet_3 = Column(Float, default=0)

    DiemCK = Column(Float, default=0)
    DiemTB = Column(Float, default=0)




if __name__=='__main__':

    db.create_all()

    k1 = KyHoc(name='HK1', NamHoc='2020')
    k2 = KyHoc(name='HK2', NamHoc='2020')
    k3 = KyHoc(name='HK3', NamHoc='2020')

    db.session.add(k1)
    db.session.add(k2)
    db.session.add(k3)
    db.session.commit()

    l1 = Lop(TenLop='10A1', SiSo=5)
    l2 = Lop(TenLop='10A2', SiSo=5)
    l3 = Lop(TenLop='10A3', SiSo=5)

    db.session.add(l1)
    db.session.add(l2)
    db.session.add(l3)
    db.session.commit()

    s1 = HocSinh(IDHocSinh='1951052134', name='Diệp Quỳnh Như', birthday='2001-11-20 00:00:00', address='Bình Định', email='nhu@gmail.com',
                 numbers='0123456789', gender=1, IDLop=1)
    s2 = HocSinh(IDHocSinh='1951052135', name='Trần Ái vi', birthday='2001-11-20 00:00:00', address='Bình Định', email='vi@gmail.com',
                 numbers='01234567891', gender=1, IDLop=1)
    s3 = HocSinh(IDHocSinh='1951052136', name='Huỳnh Thanh Thoa', birthday='2001-11-20 00:00:00', address='Bình Định', email='thoa@gmail.com',
                 numbers='01234567892', gender=1, IDLop=1)
    s4 = HocSinh(IDHocSinh='1951052137', name='Nguyễn Quốc', birthday='2001-11-20 00:00:00', address='Bình Định', email='quoc@gmail.com',
                 numbers='01234567893', gender=0, IDLop=1)
    s5 = HocSinh(IDHocSinh='1951052138', name='Đặng Văn Mạnh', birthday='2001-11-20 00:00:00', address='Bình Định', email='mạnh@gmail.com',
                 numbers='01234567894', gender=0, IDLop=1)
    s6 = HocSinh(IDHocSinh='1951052139', name='Nguyễn Văn Thân', birthday='2001-11-20 00:00:00', address='Bình Định', email='than@gmail.com',
                 numbers='01234567895', gender=1, IDLop=2)
    s7 = HocSinh(IDHocSinh='1951052110', name='Ngân Nguyễn', birthday='2001-11-20 00:00:00', address='Bình Định', email='ngan@gmail.com',
                 numbers='01234567896', gender=1, IDLop=2)
    s8 = HocSinh(IDHocSinh='1951052111', name='Lê Phương', birthday='2001-11-20 00:00:00', address='Bình Định', email='phuong@gmail.com',
                 numbers='01234567897', gender=1, IDLop=2)
    s9 = HocSinh(IDHocSinh='1951052112', name='Võ Văn Hiếu', birthday='2001-11-20 00:00:00', address='Bình Định', email='hieu@gmail.com',
                 numbers='01234567898', gender=1, IDLop=2)
    s10 = HocSinh(IDHocSinh='1951052113', name='Đặng Thúy Nga', birthday='2001-11-20 00:00:00', address='Bình Định', email='nga@gmail.com',
                  numbers='01234567899', gender=1, IDLop=2)
    s11 = HocSinh(IDHocSinh='1951052114', name='Nguyễn Quốc Toàn', birthday='2001-11-20 00:00:00', address='Bình Định', email='toan@gmail.com',
                  numbers='01234567810', gender=1, IDLop=3)
    s12 = HocSinh(IDHocSinh='1951052115', name='Nguyễn Văn Tiến', birthday='2001-11-20 00:00:00', address='Bình Định', email='tien@gmail.com',
                  numbers='0123456711', gender=1, IDLop=3)
    s13 = HocSinh(IDHocSinh='1951052116', name='Nguyễn Thu', birthday='2001-11-20 00:00:00', address='Bình Định', email='thu@gmail.com',
                  numbers='0123456712', gender=1, IDLop=3)
    s14 = HocSinh(IDHocSinh='1951052117', name='Võ Phương Chi', birthday='2001-11-20 00:00:00', address='Bình Định', email='chi@gmail.com',
                  numbers='0123456713', gender=1, IDLop=3)
    s15 = HocSinh(IDHocSinh='1951052118', name='Nguyễn Hữu Thắng', birthday='2001-11-20 00:00:00', address='Bình Định', email='thang@gmail.com',
                  numbers='0123456714', gender=1, IDLop=3)

    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    db.session.add(s6)
    db.session.add(s7)
    db.session.add(s8)
    db.session.add(s9)
    db.session.add(s10)
    db.session.add(s11)
    db.session.add(s12)
    db.session.add(s13)
    db.session.add(s14)
    db.session.add(s15)
    db.session.commit()

    m1 = MonHoc(TenMH='Toán')
    m2 = MonHoc(TenMH='Lý')
    m3 = MonHoc(TenMH='Hóa')

    db.session.add(m1)
    db.session.add(m2)
    db.session.add(m3)
    db.session.commit()

    # d1 = Diem(IDHocSinh=1, IDMonHoc=1, IDKyHoc=1,
    #           Diem15p_1=8, Diem15p_2=8, Diem15p_3=8, Diem15p_4=8, Diem15p_5=8,
    #           Diem1Tiet_1=8, Diem1Tiet_2=8, Diem1Tiet_3=8,
    #           DiemCK=8, DiemTB=9)
    # db.session.add(d1)
    # db.session.commit()

    admin = User(name='admin', username='admin', password='21232f297a57a5a743894a0e4a801fc3', birthday='2001-11-20 00:00:00' ,user_role='ADMIN')
    user = User(name='user', username='user', password='ee11cbb19052e40b07aac0ca060c23ee', birthday='2001-11-20 00:00:00' ,user_role='EMPLOYEE')
    db.session.add(admin)
    db.session.add(user)
    # mk admin:admin
    # user: user
    db.session.commit()
