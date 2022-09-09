from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request
from app import db, app, utils
from app.model import Lop, HocSinh, Diem, MonHoc, UserRole, User
from datetime import datetime

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):

        return self.render('admin/index.html',
                           hocsinh_stats=utils.hocsinh_stats(),
                           giaovien_stats=utils.giaovien_stats(),
                           lop_stats=utils.lop_stats(),
                           nhanvien_stats=utils.nhanvien_stats())

class StatsViewDiem(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        ten_lop = request.args.get('ten_lop')
        ki_hoc = request.args.get('ki_hoc')
        nam_hoc = request.args.get('nam_hoc')
        mon_hoc = request.args.get('mon_hoc')

        return self.render('admin/lop_stats.html',
                           stats=utils.Diem_all(),
                           diemtb=utils.DiemTB(ten_lop=ten_lop, ki_hoc=ki_hoc, nam_hoc=nam_hoc, mon_hoc=mon_hoc))

class XuatViewDiem(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        nam_hoc = request.args.get('nam_hoc')

        return self.render('admin/diem_stats.html',
                           stats=utils.Diem_all(nam_hoc=nam_hoc))


class DiemView(AuthenticatedModelView):
    column_display_pk = True
    column_filters = ['IDHocSinh']
    can_export = True
    column_export_exclude_list= ['Diem15p_1', 'Diem15p_2', 'Diem15p_3', 'Diem15p_4', 'Diem15p_5',
                                  'Diem1Tiet_1', 'Diem1Tiet_2', 'Diem1Tiet_3', 'DiemCK']

class HocSinhView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    column_filters = ['IDHocSinh','name']
    column_labels = {'IDHocSinh':'Mã HS',
                     'name' :'Tên',
                     'birthday':'Ngày Sinh',
                     'address':'Địa chỉ',
                     'email':'Email',
                     'numbers':'SĐT',
                     'gender' :'Nữ',
                     'note' :'Ghi chú'}


class LopView(AuthenticatedModelView):
    column_descriptions = {'SiSo': 'Tối đa 40 em học sinh',
                           'TenLop': 'Khối 10, 11, 12. Định dạng theo bảng chữ cái. Ví dụ 10A, 10B, 10C'}


admin = Admin(app=app, name="QuanLyHocSinh", template_mode="bootstrap4", index_view=MyAdminIndex())


admin.add_view(HocSinhView(HocSinh, db.session,name="Toàn học sinh"))
admin.add_view(LopView(Lop, db.session, name='Lớp'))
admin.add_view(AuthenticatedModelView(User, db.session, name='User'))
admin.add_view(DiemView(Diem, db.session, name='Điểm'))
admin.add_view(XuatViewDiem(name='Xuất Điểm'))
admin.add_view(StatsViewDiem(name='Thống kê điểm'))
admin.add_view(LogoutView(name='Logout'))
