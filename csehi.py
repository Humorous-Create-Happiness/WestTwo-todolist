from flask_sqlalchemy import SQLAlchemy
from flask import Flask,redirect,url_for,request,render_template,current_app
import flask

app = Flask(__name__)

#配置MySQL服务器
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:password@127.0.0.1:3306/todolist'

#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+"/"

app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
#app.config["SQLALCHEMY_KEY"]="password"

db=SQLAlchemy(app)


with app.app_context():
 # 创建模型类
    class Project(db.Model):
    #设置表名
        __tablename__ = 'user'
    # 创建数据库表字段
    # db.Column(类型，约束)
        id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        title=db.Column(db.String(15),nullable=False)
        neiRong=db.Column(db.String(15),nullable=False)
        finishOrNot=db.Column(db.String(15),nullable=False)
        startTime=db.Column(db.Integer,nullable=False)
        endTime=db.Column(db.Integer,nullable=False)



        def __init__(self, title, neiRong, finishOrNot, startTime, endTime):  # __init__方法负责对象的初始化

            self.title = title
            self.neiRong = neiRong
            self.finishOrNot = finishOrNot
            self.startTime = startTime
            self.endTime = endTime

    db.create_all()  # 将上述类映射到数据库中：


###新增项目
@app.route('/new-project/', methods = ['GET', 'POST'])
def newproject():
    if request.method == 'POST':
        if request.form['title'] and request.form['neiRong'] and request.form['finishOrNot'] and request.form['startTime'] and request.form['endTime']:
            curuser = Project(request.form['title'], request.form['neiRong'], request.form['finishOrNot'], request.form['startTime'], request.form['endTime'])
            db.session.add(curuser)
            db.session.commit()
            return redirect(url_for('AllProject'))
    return render_template('todolist-add.html')



###修改项目
#改一个:从已办到待办、从待办到已办id
@app.route('/modify-project/<pjid>/')
def modifyproject(pjid):
    curuser = db.session.query(Project).filter_by(id=pjid).one()

    if curuser.finishOrNot=='Yes':
        curuser.finishOrNot='No'
        db.session.commit()
        return redirect(url_for('AllProject'))
    if curuser.finishOrNot=='No':
        curuser.finishOrNot='Yes'
        db.session.commit()
        return redirect(url_for('AllProject'))
    return render_template('todolist-showInfo.html',projects = Project.query.all())
#改全部待办到已办
@app.route('/modify-project-allfinish/')
def modifyprojectF():
    pj = Project.query.all()  #选择所有要修改的数据
    for i in pj:      #循环遍历
        if i.finishOrNot == 'No':
            i.finishOrNot = 'Yes'    #要修改的参数值
            db.session.commit()    #提交事务
        return redirect(url_for('AllProject'))
    return render_template('todolist-showInfo.html', projects=Project.query.all())

#改全部已办到待办
@app.route('/modify-project-allunfinish/')
def modifyprojectUF():
    pj = Project.query.all()  #选择所有要修改的数据
    for i in pj:      #循环遍历
        if i.finishOrNot == 'Yes':
            i.finishOrNot = 'No'    #要修改的参数值
            db.session.commit()    #提交事务
        return redirect(url_for('AllProject'))
    return render_template('todolist-showInfo.html', projects=Project.query.all())




###查看项目
#所有
@app.route('/check-allproject/')
def AllProject():
    page1 = request.args.get('page', 1, type=int)  # 获取当前页数
    # current_app.config['PER_PAGE_COUNT']是在设置中定义的每页页数
    pagination1 = Project.query.all.paginate(page1,per_page=current_app.config['PER_PAGE_COUNT'], error_out=False)
    conditional_query = pagination1.items  # 每页的数据

    return render_template('todolist-showInfo.html', conditional_query=conditional_query, pagination1=pagination1)

#所有已完成
@app.route('/check-allproject-finished/')
def AllProjectfinished():
    page1 = request.args.get('page', 1, type=int)  # 获取当前页数
    # current_app.config['PER_PAGE_COUNT']是在设置中定义的每页页数
    pagination1 = Project.query.filter_by(finishOrNot='Yes').all.paginate(page1,
                                                                     per_page=current_app.config['PER_PAGE_COUNT'],
                                                                     error_out=False)
    conditional_query = pagination1.items  # 每页的数据

    return render_template('todolist-showInfo.html', conditional_query=conditional_query, pagination1=pagination1)


#所有未完成
@app.route('/check-allproject-unfinished/')
def AllProjectUnfinished():
   page1 = request.args.get('page', 1, type=int)  # 获取当前页数
# current_app.config['PER_PAGE_COUNT']是在设置中定义的每页页数
   pagination1 = Project.query.filter_by(finishOrNot='No').all.paginate(page1, per_page=current_app.config['PER_PAGE_COUNT'],
                                                    error_out=False)
   conditional_query = pagination1.items  # 每页的数据

   return render_template('todolist-showInfo.html', conditional_query=conditional_query, pagination1=pagination1)


#id查看
@app.route('/check-oneproject-id/<int:number>/')
def OneProjecti(number):
   return render_template('todolist-showInfo.html', projects = Project.query.filter_by(id=number)() )

#关键字查看
@app.route('/check-oneproject-title/<message>/')
def OneProjectt(message):
    page1 = request.args.get('page', 1, type=int)  # 获取当前页数
    # current_app.config['PER_PAGE_COUNT']是在设置中定义的每页页数
    pagination1 = Project.query.filter_by(title=message).all.paginate(page1,
                                                                     per_page=current_app.config['PER_PAGE_COUNT'],
                                                                     error_out=False)
    conditional_query = pagination1.items  # 每页的数据

    return render_template('todolist-showInfo.html', conditional_query=conditional_query, pagination1=pagination1)




###删除项目
#删一个id
@app.route('/delete-oneproject/<pjid>/')
def deleteproject(pjid):
     db.session.query(Project).filter_by(id=pjid).delete()
     db.session.commit()
     return redirect(url_for('AllProject'))
#删所有项目
@app.route('/delete-allproject/')
def deleteprojectAll():
     db.session.query(Project).all.delete()
     db.session.commit()
     return redirect(url_for('AllProject'))

#删所有已办项目
@app.route('/delete-allproject-finish/')
def deleteprojectAllF():
     db.session.query(Project).filter_by(finishOrNot='Yes').delete()
     db.session.commit()
     return redirect(url_for('AllProject'))
#删所有待办项目
@app.route('/delete-allproject-unfinish/')
def deleteprojectAllUf():
     db.session.query(Project).filter_by(finishOrNot='No').delete()
     db.session.commit()
     return redirect(url_for('AllProject'))

if __name__ == '__main__':
    # 创建数据表
    app.run()