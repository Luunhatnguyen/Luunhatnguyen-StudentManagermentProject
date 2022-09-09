import cloudinary.uploader
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_user, logout_user, login_required
import datetime
import json
import utils
from app.admin import *
from app.model import UserRole
from app import login, app


@app.route("/")
def home():
    return render_template('index.html')


# login method for employee
@app.route('/nhanvien_login', methods=['get', 'post'])
def nhanvien_login():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_user(username=username, password=password, role=UserRole.EMPLOYEE)
            if user:
                login_user(user=user)

                return render_template('index.html')
                # next = request.args.get('next', 'home')
                # return redirect(url_for(next))
            else:
                error_msg = "Sai tên đăng nhập hoặc mật khẩu!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)


# Login method for admin, page admin
@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_user(username=username,
                            password=password,
                            role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    else:
        flash("Sai tên đăng nhập hoặc mật khẩu!")

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/logout')
def nhanvien_logout():
    logout_user()

    return redirect(url_for('home'))


@app.route('/register', methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']
            gender = request.form['gender']
            birthday = request.form['birthday']
            numbers = request.form['numbers']
            role = request.form['role']
            email = request.form['email']
            avatar_path = None

            if password.__eq__(confirm):
                avatar = request.files['avatar']
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                if role.__eq__('EMPLOYEE'):
                    if (utils.register(name=name, gender=gender, email=email, birthday=birthday, numbers=numbers,
                                       username=username, password=password, role=role, avatar=avatar_path)):
                        error_msg = "Successful"
                        return redirect(url_for('register', error_msg=error_msg))
                    else:
                        error_msg = "Failed"
                        return redirect(url_for('register', error_msg=error_msg))
                if role.__eq__('TEACHER'):
                    if (utils.register(name=name, gender=gender, email=email, birthday=birthday, numbers=numbers,
                                       username=username, password=password, role=role, avatar=avatar_path)):
                        error_msg = "Successful"
                        return redirect(url_for('register', error_msg=error_msg))
                    else:
                        error_msg = "Failed"
                        return redirect(url_for('register', error_msg=error_msg))
            else:
                error_msg = "Password incorrect!!!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('nhanvien_register.html', error_msg=error_msg)



@app.route('/rule_age', methods=['get', 'post'])
def rule_age():
    error_msg = ""
    from_age_valid = 0
    end_age_valid = 0
    path = "./data/age.json"
    res = utils.read_json(path)
    from_age_valid = res["fromAgeValid"]
    end_age_valid = res["endAgeValid"]
    if request.method.__eq__('POST'):
        try:
            from_age = request.form['from_age']
            end_age = request.form['end_age']
            from_age_valid = int(from_age)
            end_age_valid = int(end_age)
            utils.write_json(from_age_valid=from_age_valid, end_age_valid=end_age_valid)
            error_msg = "Thay đổi hợp lệ"
            return redirect(url_for('rule_age', error_msg=error_msg))
        except Exception as ex:
            error_msg = str(ex)

    return render_template('rule-age.html', error_msg=error_msg, from_age_valid=from_age_valid, end_age_valid=end_age_valid)


@app.route('/regiter_hocsinh', methods=['get', 'post'])
def regiter_hocsinh():
    error_msg = ""
    datetime_object = int((datetime.now()).year)
    from_age_valid = 0
    end_age_valid = 0
    path = "./data/age.json"
    res = utils.read_json(path)
    from_age_valid = res["fromAgeValid"]
    end_age_valid = res["endAgeValid"]
    if request.method.__eq__('POST'):
        try:
            IDHocSinh = request.form['IDHocSinh']
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']
            gender = request.form['gender']
            birthday = request.form['birthday']
            numbers = request.form['numbers']
            lop = request.form['lop']
            email = request.form['email']
            note = request.form['note']
            address = request.form['address']
            avatar_path = None
            do_tuoi = int(birthday[0:4])
            if from_age_valid <= (datetime_object - do_tuoi) <= end_age_valid:
                if password.__eq__(confirm):
                    avatar = request.files['avatar']
                    if avatar:
                        res = cloudinary.uploader.upload(avatar)
                        avatar_path = res['secure_url']
                    if (utils.register_hocsinh(IDHocSinh=IDHocSinh, name=name, gender=gender, email=email,
                                               birthday=birthday,
                                               numbers=numbers, username=username, password=password, avatar=avatar,
                                               lop=lop,
                                               note=note, address=address)):
                        error_msg = "Successful"
                        return redirect(url_for('regiter_hocsinh'))
                    else:
                        error_msg = "Failed"
                else:
                    error_msg = 'Incorrect Password!!!'
            else:
                error_msg = 'Học sinh chưa đủ tuổi'
        except Exception as ex:
            error_msg = str(ex)

    return render_template('hocsinh_register.html', error_msg=error_msg, lop=utils.ds_lop())

#si so
@app.route('/number_rule', methods=['get', 'post'])
def number_rule():
    error_msg = ""
    path = "./data/siso.json"
    res = utils.read_json_siso(path)
    id = 1
    IDlop = 1
    if request.method.__eq__("POST"):
        try:
            maxNumber_f = request.form['maxNumber']
            IDlop = request.form['IDlop']
            id = int(IDlop)
            maxNumber_int = int(maxNumber_f)
            list_of_dict = utils.processing(id, res, maxNumber_int)
            with open(path, 'w') as fp:
                json.dumps(list_of_dict, fp, indent=4)
            error_msg = "Thay đổi thành công"
            return redirect(url_for('number_rule', error_msg=error_msg, maxNumber=maxNumber))
            # else:
            #     error_msg = "Thay đổi không thành công"
            #     return redirect(url_for('number_rule', error_msg=error_msg))
        except Exception as ex:
            error_msg = ""

    return render_template('siso.html', error_msg=error_msg, lop=utils.ds_lop(), idlop=utils.count_student_lop(IDlop),
                           maxNumber=res[id-1]["maxNumber"])


# tìm kiếm môn học
@app.route('/subjects', methods=['get', 'post'])
def subjects():
    kw = request.args.get("keyword")

    subjects = utils.Quan_ly_mon_hoc(kw=kw)

    return render_template('mon_hoc.html', subjects=subjects)


#xóa môn học
@app.route('/subjects_remove', methods=['post'])
def subjects_remove():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            ID_mon_hoc = request.form['IDMonHoc']
            if utils.xoa_mon(ID_mon_hoc=ID_mon_hoc):
                error_msg="Xóa môn học thành công"
                return render_template('mon_hoc.html', error_msg = error_msg)
            else:
                error_msg = "Xóa môn học không thành công"
                return render_template('mon_hoc.html', error_msg=error_msg)
        except Exception as ex:
            error_msg = str(ex)

    return render_template('mon_hoc.html', error_msg=error_msg)

#thêm môn học
@app.route('/subject_add', methods=['get','post'])
def subject_add():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            TenMH = request.form['TenMH']
            if utils.them_mon(TenMH=TenMH):
                error_msg = "Thêm môn học thành công"
                return render_template('mon_hoc.html', error_msg=error_msg)
            else:
                error_msg = "Thêm không thành công"
                return render_template('mon_hoc.html', error_msg=error_msg)
        except Exception as ex:
            error_msg = str(ex)

    return render_template('mon_hoc.html', error_msg=error_msg)

#xuất điểm
@app.route('/diem_all', methods=['get', 'post'])
def diem_all():
    nam_hoc = '2020'
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            nam_hoc = request.form['nam_hoc']
            if utils.Diem_all(nam_hoc=nam_hoc):
                stats = utils.Diem_all(nam_hoc=nam_hoc)
                error_msg = "thành công"
                return render_template('xuatdiem_register.html', stats, error_msg)
            else:
                error_msg = "Some thing went wrong!!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('xuatdiem_register.html',
                       stats=utils.Diem_all(nam_hoc=nam_hoc), error_msg=error_msg)


if __name__ == '__main__':
    app.run(debug=True)
