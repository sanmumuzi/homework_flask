from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from . import user
from .. import db
from ..models import User, Post, Homework
from .forms import LoginForm, RegistrationForm, PostForm, HomeworkForm, ChangePasswordForm


@user.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_item = User.query.filter_by(account=form.account.data).first()
        print(user_item.username)
        print(user_item.account)
        if user_item is not None and user_item.verify_password(form.password.data):
            login_user(user_item, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        # flash('Invalid username or password.')
        flash('无效的用户名或密码')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash("你已经登出了")
    return redirect(url_for('main.index'))


@user.route('/publish_homework', methods=['GET', 'POST'])
@login_required
def publish_homework():
    if current_user.is_teacher:
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data,
                        body=form.body.data,
                        group=form.group.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            return redirect(url_for('main.index'))
        return render_template('user/publish_homework.html', form=form)
    else:
        flash('Sorry, 你暂时没有该权限')
        return redirect(url_for('main.index'))


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:  # 防止别人修改....
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash('作业内容已被更新.')
        return redirect(url_for('user.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('user/edit_post.html', form=form)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_info = User(username=form.username.data,
                         account=form.account.data,
                         password=form.password.data)
        db.session.add(user_info)
        flash('现在可以进行登录了.')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = HomeworkForm()
    if form.validate_on_submit():
        homework = Homework(body=form.body.data,
                            post=post,
                            author=current_user._get_current_object())
        db.session.add(homework)
        flash('你的作业已经提交')
        return redirect(url_for('user.post', id=post.id))
    return render_template('user/post.html', posts=[post], form=form)


@user.route('/stu_homework_list/<int:id>')
@login_required
def stu_homework_list(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:  # 防止别人修改....
        abort(403)
    homeworks = Homework.query.filter_by(post_id=id).all()
    return render_template('user/stu_homework_list.html', homeworks=homeworks)


@user.route('/stu_homework/<int:id>')
@login_required
def stu_homework(id):
    stu_homework = Homework.query.get_or_404(id)
    if current_user != stu_homework.author and current_user != stu_homework.post.author:
        abort(403)
    return render_template('user/stu_homework.html', stu_homework=stu_homework, post=stu_homework.post)


@user.route('/my_homework')
@login_required
def my_homework():
    homeworks = Homework.query.filter_by(author=current_user).all()
    return render_template('user/my_homework.html', homeworks=homeworks)


@user.route('/homework/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_homework(id):
    homework = Homework.query.get_or_404(id)
    if current_user != homework.author:
        abort(403)
    form = HomeworkForm()
    if form.validate_on_submit():
        homework.body = form.body.data
        db.session.add(homework)
        flash('作业回答已经更新.')
        return redirect(url_for('user.my_homework'))
    form.body.data = homework.body
    return render_template('user/edit_homework.html', form=form, homework=homework)


# @user.route('/user_info/<account>')  # 不存在的
# def user_info(account):
#     user = User.query.filter_by(account=account).first()
#     if user is None:
#         abort(404)
#     return render_template('user/user_info.html', user=user)


@user.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('你的密码已经更新完成.')
            return redirect(url_for('main.index'))
        else:
            flash('无效的密码.')
    return render_template("user/change_password.html", form=form)
