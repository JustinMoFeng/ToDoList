from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

app = Flask(__name__)

# 获取允许的 origins
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',')

# 配置 CORS
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS, "supports_credentials": True}})

app.config['SECRET_KEY'] = 'xiaoye666'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:6541230MSq@localhost:3306/todolist_db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Todo项目模型
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 注册路由
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': '注册成功'}), 201

# 登录路由
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': '登录成功'}), 200
    
    return jsonify({'message': '用户名或密码错误'}), 401

# 登出路由
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': '已登出'}), 200

# 添加Todo项目
@app.route('/todo', methods=['POST'])
@login_required
def add_todo():
    data = request.get_json()
    new_todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 1),
        user_id=current_user.id
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo项目已添加', 'id': new_todo.id}), 201

# 获取所有Todo项目
@app.route('/todos', methods=['GET'])
@login_required
def get_todos():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'status': todo.status,
        'priority': todo.priority
    } for todo in todos]), 200

# 更新Todo项目
@app.route('/todo/<int:todo_id>', methods=['PUT'])
@login_required
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        return jsonify({'message': '无权限修改此Todo项目'}), 403
    
    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.status = data.get('status', todo.status)
    todo.priority = data.get('priority', todo.priority)
    
    db.session.commit()
    return jsonify({'message': 'Todo项目已更新'}), 200

# 删除Todo项目
@app.route('/todo/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        return jsonify({'message': '无权限删除此Todo项目'}), 403
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo项目已删除'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
