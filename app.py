from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from models import Database, UserModel, NovelModel, OrderModel, ReadingRecordModel
from functools import wraps
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import DESCENDING
import os
import PyPDF2

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db = Database(app.config['MONGODB_URI'], app.config['MONGODB_DB'])
user_model = UserModel(db)
novel_model = NovelModel(db)
order_model = OrderModel(db)
reading_record_model = ReadingRecordModel(db)

# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# 装饰器：要求登录
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# 装饰器：要求特定角色
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('请先登录', 'warning')
                return redirect(url_for('login'))
            
            user = user_model.find_by_id(session['user_id'])
            if not user or user['role'] != role:
                flash('无权限访问此页面', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 首页
@app.route('/')
def index():
    """首页 - 悦读坊"""
    # 获取精选推荐（热门小说）
    featured_novels = list(
        novel_model.collection.find({"status": "online"})
        .sort("readCount", DESCENDING)
        .limit(6)
    )
    
    # 获取新书上架
    new_novels = list(
        novel_model.collection.find({"status": "online"})
        .sort("createTime", DESCENDING)
        .limit(6)
    )
    
    # 为所有小说添加作者信息
    for novel in featured_novels + new_novels:
        author = user_model.find_by_id(str(novel['authorId']))
        novel['author_name'] = author['username'] if author else '未知'
    
    # 如果已登录，添加用户信息
    logged_in = 'user_id' in session
    
    return render_template('index.html',
                         featured_novels=featured_novels,
                         new_novels=new_novels,
                         logged_in=logged_in)


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = user_model.verify_password(username, password)
        if user:
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user['role']
            session.permanent = True
            flash('登录成功！欢迎回到悦读坊', 'success')
            # 登录后返回首页，而不是重定向到控制台
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'reader')
        
        if password != confirm_password:
            flash('两次密码输入不一致', 'danger')
            return render_template('register.html')
        
        # 检查用户名是否已存在
        if user_model.find_by_username(username):
            flash('用户名已存在', 'danger')
            return render_template('register.html')
        
        try:
            user_id = user_model.create_user(username, password, role)
            # 自动登录
            user = user_model.find_by_id(str(user_id))
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['role'] = user['role']
            session.permanent = True
            flash('注册成功！欢迎来到悦读坊', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'注册失败：{str(e)}', 'danger')
    
    return render_template('register.html')


# 登出
@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('login'))


# ==================== 管理员功能 ====================

# 管理员控制台
@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    # 统计数据
    total_users = user_model.collection.count_documents({"status": 1})
    total_novels = novel_model.count_novels()
    online_novels = novel_model.count_novels({"status": "online"})
    pending_novels = novel_model.count_novels({"status": "pending"})
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_novels=total_novels,
                         online_novels=online_novels,
                         pending_novels=pending_novels)


# 用户管理
@app.route('/admin/users')
@role_required('admin')
def admin_users():
    users = user_model.get_all_users()
    return render_template('admin/users.html', users=users)


# 删除用户
@app.route('/admin/users/<user_id>/delete', methods=['POST'])
@role_required('admin')
def admin_delete_user(user_id):
    user_model.delete_user(user_id)
    flash('用户已删除', 'success')
    return redirect(url_for('admin_users'))


# 待审核小说列表
@app.route('/admin/review')
@role_required('admin')
def admin_review():
    pending_novels = novel_model.find_novels({"status": "pending"})
    
    # 获取作者信息
    for novel in pending_novels:
        author = user_model.find_by_id(str(novel['authorId']))
        novel['author_name'] = author['username'] if author else '未知'
    
    return render_template('admin/review.html', novels=pending_novels)


# 审核小说
@app.route('/admin/review/<novel_id>', methods=['POST'])
@role_required('admin')
def admin_review_novel(novel_id):
    action = request.form.get('action')
    opinion = request.form.get('opinion', '')
    
    approved = action == 'approve'
    novel_model.review_novel(novel_id, session['user_id'], opinion, approved)
    
    status_text = '通过' if approved else '驳回'
    flash(f'小说已{status_text}', 'success')
    return redirect(url_for('admin_review'))


# ==================== 创作者功能 ====================

# 创作者控制台
@app.route('/creator/dashboard')
@role_required('creator')
def creator_dashboard():
    # 获取作者的小说
    my_novels = novel_model.find_novels({"authorId": ObjectId(session['user_id'])})
    
    # 统计数据
    total_novels = len(my_novels)
    online_novels = len([n for n in my_novels if n['status'] == 'online'])
    total_reads = sum(n.get('readCount', 0) for n in my_novels)
    
    return render_template('creator/dashboard.html',
                         novels=my_novels,
                         total_novels=total_novels,
                         online_novels=online_novels,
                         total_reads=total_reads)


# 小说列表
@app.route('/creator/novels')
@role_required('creator')
def creator_novels():
    novels = novel_model.find_novels({"authorId": ObjectId(session['user_id'])})
    return render_template('creator/novels.html', novels=novels)


# 创建小说
@app.route('/creator/novels/create', methods=['GET', 'POST'])
@role_required('creator')
def creator_create_novel():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        tags = request.form.get('tags', '').split(',')
        tags = [t.strip() for t in tags if t.strip()]
        intro = request.form.get('intro')
        price = float(request.form.get('price', 0))
        
        novel_id = novel_model.create_novel(
            title=title,
            author_id=session['user_id'],
            category=category,
            tags=tags,
            intro=intro,
            price=price
        )
        
        flash('小说创建成功', 'success')
        return redirect(url_for('creator_edit_novel', novel_id=novel_id))
    
    # 分类列表
    categories = ['玄幻', '言情', '武侠', '科幻', '悬疑', '历史', '校园', '其他']
    return render_template('creator/create_novel.html', categories=categories)


# 编辑小说
@app.route('/creator/novels/<novel_id>/edit', methods=['GET', 'POST'])
@role_required('creator')
def creator_edit_novel(novel_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or str(novel['authorId']) != session['user_id']:
        flash('无权限编辑此小说', 'danger')
        return redirect(url_for('creator_novels'))
    
    if request.method == 'POST':
        update_data = {
            'title': request.form.get('title'),
            'category': request.form.get('category'),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'intro': request.form.get('intro'),
            'price': float(request.form.get('price', 0))
        }
        
        novel_model.update_novel(novel_id, update_data)
        flash('小说信息已更新', 'success')
        return redirect(url_for('creator_edit_novel', novel_id=novel_id))
    
    categories = ['玄幻', '言情', '武侠', '科幻', '悬疑', '历史', '校园', '其他']
    novel['tags_str'] = ','.join(novel.get('tags', []))
    return render_template('creator/edit_novel.html', novel=novel, categories=categories)


# 导入小说章节
@app.route('/creator/novels/<novel_id>/import', methods=['GET', 'POST'])
@role_required('creator')
def creator_import_chapters(novel_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or str(novel['authorId']) != session['user_id']:
        flash('无权限操作此小说', 'danger')
        return redirect(url_for('creator_novels'))
    
    if request.method == 'POST':
        file = request.files.get('file')
        
        if file and file.filename:
            filename = file.filename
            if filename.endswith('.txt'):
                # 处理TXT文件
                content = file.read().decode('utf-8', errors='ignore')
                chapters = parse_txt_chapters(content)
                
                for idx, chapter in enumerate(chapters):
                    chapter_data = {
                        'chapterId': f"CH{idx+1:03d}",
                        'title': chapter['title'],
                        'content': chapter['content'],
                        'isFree': idx < 3,  # 前3章免费
                        'createTime': datetime.utcnow()
                    }
                    novel_model.add_chapter(novel_id, chapter_data)
                
                flash(f'成功导入 {len(chapters)} 个章节', 'success')
                return redirect(url_for('creator_chapters', novel_id=novel_id))
            elif filename.endswith('.pdf'):
                # 处理PDF文件
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    content = ''
                    for page in pdf_reader.pages:
                        content += page.extract_text()
                    
                    chapters = parse_txt_chapters(content)
                    
                    for idx, chapter in enumerate(chapters):
                        chapter_data = {
                            'chapterId': f"CH{idx+1:03d}",
                            'title': chapter['title'],
                            'content': chapter['content'],
                            'isFree': idx < 3,
                            'createTime': datetime.utcnow()
                        }
                        novel_model.add_chapter(novel_id, chapter_data)
                    
                    flash(f'成功导入 {len(chapters)} 个章节', 'success')
                    return redirect(url_for('creator_chapters', novel_id=novel_id))
                except Exception as e:
                    flash(f'PDF解析失败：{str(e)}', 'danger')
    
    return render_template('creator/import_chapters.html', novel=novel)


def parse_txt_chapters(content):
    """解析TXT文本为章节"""
    import re
    
    # 尝试匹配章节标题（第X章、第X回等）
    chapter_pattern = r'第[零一二三四五六七八九十百千0-9]+[章回节][\s：:]*(.+?)(?=\n)'
    
    chapters = []
    matches = list(re.finditer(chapter_pattern, content))
    
    if not matches:
        # 如果没有找到章节标记，将整个内容作为一章
        chapters.append({
            'title': '正文',
            'content': content
        })
    else:
        for i, match in enumerate(matches):
            title = match.group(0).strip()
            start = match.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(content)
            chapter_content = content[start:end].strip()
            
            chapters.append({
                'title': title,
                'content': chapter_content
            })
    
    return chapters


# 章节管理
@app.route('/creator/novels/<novel_id>/chapters')
@role_required('creator')
def creator_chapters(novel_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or str(novel['authorId']) != session['user_id']:
        flash('无权限访问此小说', 'danger')
        return redirect(url_for('creator_novels'))
    
    return render_template('creator/chapters.html', novel=novel)


# 添加章节
@app.route('/creator/novels/<novel_id>/chapters/add', methods=['GET', 'POST'])
@role_required('creator')
def creator_add_chapter(novel_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or str(novel['authorId']) != session['user_id']:
        flash('无权限操作此小说', 'danger')
        return redirect(url_for('creator_novels'))
    
    if request.method == 'POST':
        chapter_count = len(novel.get('chapters', []))
        chapter_data = {
            'chapterId': f"CH{chapter_count+1:03d}",
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'isFree': request.form.get('isFree') == 'on',
            'createTime': datetime.utcnow()
        }
        
        novel_model.add_chapter(novel_id, chapter_data)
        flash('章节添加成功', 'success')
        return redirect(url_for('creator_chapters', novel_id=novel_id))
    
    return render_template('creator/add_chapter.html', novel=novel)


# 编辑章节
@app.route('/creator/novels/<novel_id>/chapters/<chapter_id>/edit', methods=['GET', 'POST'])
@role_required('creator')
def creator_edit_chapter(novel_id, chapter_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or str(novel['authorId']) != session['user_id']:
        flash('无权限操作此小说', 'danger')
        return redirect(url_for('creator_novels'))
    
    chapter = next((c for c in novel.get('chapters', []) if c['chapterId'] == chapter_id), None)
    
    if not chapter:
        flash('章节不存在', 'danger')
        return redirect(url_for('creator_chapters', novel_id=novel_id))
    
    if request.method == 'POST':
        chapter['title'] = request.form.get('title')
        chapter['content'] = request.form.get('content')
        chapter['isFree'] = request.form.get('isFree') == 'on'
        
        novel_model.update_chapter(novel_id, chapter_id, chapter)
        flash('章节已更新', 'success')
        return redirect(url_for('creator_chapters', novel_id=novel_id))
    
    return render_template('creator/edit_chapter.html', novel=novel, chapter=chapter)


# 删除章节
@app.route('/creator/novels/<novel_id>/chapters/<chapter_id>/delete', methods=['POST'])
@role_required('creator')
def creator_delete_chapter(novel_id, chapter_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or str(novel['authorId']) != session['user_id']:
        flash('无权限操作此小说', 'danger')
        return redirect(url_for('creator_novels'))
    
    novel_model.delete_chapter(novel_id, chapter_id)
    flash('章节已删除', 'success')
    return redirect(url_for('creator_chapters', novel_id=novel_id))


# 提交审核
@app.route('/creator/novels/<novel_id>/submit', methods=['POST'])
@role_required('creator')
def creator_submit_novel(novel_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or str(novel['authorId']) != session['user_id']:
        flash('无权限操作此小说', 'danger')
        return redirect(url_for('creator_novels'))
    
    if len(novel.get('chapters', [])) == 0:
        flash('请至少添加一个章节后再提交审核', 'warning')
        return redirect(url_for('creator_chapters', novel_id=novel_id))
    
    novel_model.submit_for_review(novel_id)
    flash('小说已提交审核', 'success')
    return redirect(url_for('creator_novels'))


# ==================== 读者功能 ====================

# 读者控制台
@app.route('/reader/dashboard')
@role_required('reader')
def reader_dashboard():
    # 获取已购小说
    orders = order_model.find_user_orders(session['user_id'])
    purchased_novel_ids = [str(o['novelId']) for o in orders if o['status'] == 'paid']
    
    purchased_novels = []
    for novel_id in purchased_novel_ids:
        novel = novel_model.find_by_id(novel_id)
        if novel:
            purchased_novels.append(novel)
    
    return render_template('reader/dashboard.html', 
                         purchased_novels=purchased_novels,
                         total_purchased=len(purchased_novels))


# 小说广场（包含搜索功能）
@app.route('/reader/novels')
@role_required('reader')
def reader_novels():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    keyword = request.args.get('keyword', '').strip()
    
    query = {"status": "online"}
    
    # 分类筛选
    if category:
        query['category'] = category
    
    # 搜索功能 - 使用MongoDB正则匹配
    if keyword:
        # 使用$or操作符，支持按书名或标签搜索
        # 使用$regex进行不区分大小写的模糊匹配
        query['$or'] = [
            {"title": {"$regex": keyword, "$options": "i"}},  # 按书名搜索
            {"tags": {"$regex": keyword, "$options": "i"}},   # 按标签搜索
        ]
    
    skip = (page - 1) * app.config['NOVELS_PER_PAGE']
    novels = novel_model.find_novels(query, skip=skip, limit=app.config['NOVELS_PER_PAGE'])
    
    # 获取作者信息，并支持按作者名搜索
    matched_novels = []
    for novel in novels:
        author = user_model.find_by_id(str(novel['authorId']))
        novel['author_name'] = author['username'] if author else '未知'
        matched_novels.append(novel)
    
    # 如果有关键词，需要额外处理作者名搜索
    if keyword:
        # 先搜索匹配关键词的作者
        author_query = {"username": {"$regex": keyword, "$options": "i"}, "role": "creator"}
        matching_authors = list(user_model.collection.find(author_query))
        
        if matching_authors:
            author_ids = [author['_id'] for author in matching_authors]
            # 搜索这些作者的小说
            author_novel_query = {
                "status": "online",
                "authorId": {"$in": author_ids}
            }
            if category:
                author_novel_query['category'] = category
            
            author_novels = novel_model.find_novels(author_novel_query, skip=0, limit=100)
            
            # 合并结果并去重
            novel_ids = {str(n['_id']) for n in matched_novels}
            for novel in author_novels:
                if str(novel['_id']) not in novel_ids:
                    author = user_model.find_by_id(str(novel['authorId']))
                    novel['author_name'] = author['username'] if author else '未知'
                    matched_novels.append(novel)
        
        # 重新分页
        total = len(matched_novels)
        start = (page - 1) * app.config['NOVELS_PER_PAGE']
        end = start + app.config['NOVELS_PER_PAGE']
        novels = matched_novels[start:end]
    else:
        novels = matched_novels
        total = novel_model.count_novels(query)
    
    total_pages = (total + app.config['NOVELS_PER_PAGE'] - 1) // app.config['NOVELS_PER_PAGE']
    
    categories = ['玄幻', '言情', '武侠', '科幻', '悬疑', '历史', '校园', '其他']
    
    return render_template('reader/novels.html', 
                         novels=novels,
                         page=page,
                         total_pages=total_pages,
                         categories=categories,
                         current_category=category,
                         keyword=keyword)


# 小说详情
@app.route('/reader/novels/<novel_id>')
@role_required('reader')
def reader_novel_detail(novel_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or novel['status'] != 'online':
        flash('小说不存在或未上线', 'warning')
        return redirect(url_for('reader_novels'))
    
    # 获取作者信息
    author = user_model.find_by_id(str(novel['authorId']))
    novel['author_name'] = author['username'] if author else '未知'
    
    # 检查是否已购买
    purchased = order_model.check_purchased(session['user_id'], novel_id)
    
    # 获取阅读进度
    progress = reading_record_model.get_progress(session['user_id'], novel_id)
    
    return render_template('reader/novel_detail.html', 
                         novel=novel,
                         purchased=purchased,
                         progress=progress)


# 阅读章节
@app.route('/reader/novels/<novel_id>/read/<chapter_id>')
@role_required('reader')
def reader_read_chapter(novel_id, chapter_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or novel['status'] != 'online':
        flash('小说不存在或未上线', 'warning')
        return redirect(url_for('reader_novels'))
    
    chapter = next((c for c in novel.get('chapters', []) if c['chapterId'] == chapter_id), None)
    
    if not chapter:
        flash('章节不存在', 'warning')
        return redirect(url_for('reader_novel_detail', novel_id=novel_id))
    
    # 检查是否需要购买
    if not chapter.get('isFree', False):
        purchased = order_model.check_purchased(session['user_id'], novel_id)
        if not purchased:
            flash('请先购买小说', 'warning')
            return redirect(url_for('reader_novel_detail', novel_id=novel_id))
    
    # 保存阅读进度
    reading_record_model.save_progress(session['user_id'], novel_id, chapter_id)
    
    # 增加阅读量
    novel_model.increment_read_count(novel_id)
    
    # 获取作者信息
    author = user_model.find_by_id(str(novel['authorId']))
    novel['author_name'] = author['username'] if author else '未知'
    
    # 获取章节索引
    chapter_index = next(i for i, c in enumerate(novel['chapters']) if c['chapterId'] == chapter_id)
    prev_chapter = novel['chapters'][chapter_index - 1] if chapter_index > 0 else None
    next_chapter = novel['chapters'][chapter_index + 1] if chapter_index < len(novel['chapters']) - 1 else None
    
    return render_template('reader/read_chapter.html',
                         novel=novel,
                         chapter=chapter,
                         prev_chapter=prev_chapter,
                         next_chapter=next_chapter)


# 购买小说
@app.route('/reader/novels/<novel_id>/purchase', methods=['POST'])
@role_required('reader')
def reader_purchase_novel(novel_id):
    novel = novel_model.find_by_id(novel_id)
    
    if not novel or novel['status'] != 'online':
        return jsonify({"success": False, "message": "小说不存在或未上线"})
    
    # 检查是否已购买
    if order_model.check_purchased(session['user_id'], novel_id):
        return jsonify({"success": False, "message": "您已购买过此小说"})
    
    # 创建订单
    order_id = order_model.create_order(session['user_id'], novel_id, novel['price'])
    
    # 模拟支付
    order_model.pay_order(order_id)
    
    # 增加销量
    novel_model.collection.update_one(
        {"_id": ObjectId(novel_id)},
        {"$inc": {"saleCount": 1}}
    )
    
    return jsonify({"success": True, "message": "购买成功"})


# 我的订单
@app.route('/reader/orders')
@role_required('reader')
def reader_orders():
    orders = order_model.find_user_orders(session['user_id'])
    
    # 获取小说信息
    for order in orders:
        novel = novel_model.find_by_id(str(order['novelId']))
        order['novel'] = novel
    
    return render_template('reader/orders.html', orders=orders)


# 添加评论
@app.route('/reader/novels/<novel_id>/comment', methods=['POST'])
@login_required
def add_comment(novel_id):
    content = request.form.get('content')
    
    if not content or not content.strip():
        return jsonify({"success": False, "message": "评论内容不能为空"})
    
    # 添加评论
    novel_model.add_comment(novel_id, session['user_id'], content.strip())
    
    return jsonify({"success": True, "message": "评论成功"})


# 回复评论
@app.route('/reader/novels/<novel_id>/comment/<int:comment_index>/reply', methods=['POST'])
@login_required
def reply_comment(novel_id, comment_index):
    content = request.form.get('content')
    
    if not content or not content.strip():
        return jsonify({"success": False, "message": "回复内容不能为空"})
    
    novel = novel_model.find_by_id(novel_id)
    if not novel or comment_index >= len(novel.get('comments', [])):
        return jsonify({"success": False, "message": "评论不存在"})
    
    # 获取用户信息
    user = user_model.find_by_id(session['user_id'])
    
    # 构建回复数据
    reply_data = {
        "userId": ObjectId(session['user_id']),
        "username": user['username'],
        "content": content.strip(),
        "createTime": datetime.utcnow()
    }
    
    # 添加回复到指定评论
    novel_model.collection.update_one(
        {"_id": ObjectId(novel_id)},
        {"$push": {f"comments.{comment_index}.replies": reply_data}}
    )
    
    return jsonify({"success": True, "message": "回复成功"})


# 删除评论
@app.route('/reader/novels/<novel_id>/comment/<int:comment_index>/delete', methods=['POST'])
@login_required
def delete_comment(novel_id, comment_index):
    novel = novel_model.find_by_id(novel_id)
    if not novel:
        return jsonify({"success": False, "message": "小说不存在"})
    
    comments = novel.get('comments', [])
    if comment_index >= len(comments):
        return jsonify({"success": False, "message": "评论不存在"})
    
    comment = comments[comment_index]
    
    # 只能删除自己的评论
    if str(comment['userId']) != session['user_id']:
        return jsonify({"success": False, "message": "无权删除此评论"})
    
    # 删除评论
    comments.pop(comment_index)
    novel_model.collection.update_one(
        {"_id": ObjectId(novel_id)},
        {"$set": {"comments": comments}}
    )
    
    return jsonify({"success": True, "message": "评论已删除"})


# 数据统计与可视化
@app.route('/admin/statistics')
@role_required('admin')
def admin_statistics():
    """管理员数据统计页面"""
    # 1. 小说分类统计
    category_stats = list(novel_model.collection.aggregate([
        {"$match": {"status": "online"}},
        {"$group": {
            "_id": "$category",
            "count": {"$sum": 1},
            "totalRead": {"$sum": "$readCount"},
            "totalSales": {"$sum": "$saleCount"}
        }},
        {"$sort": {"count": -1}}
    ]))
    
    # 2. 热门小说Top10（按阅读量）
    top_novels_read = list(novel_model.collection.find(
        {"status": "online"}
    ).sort("readCount", -1).limit(10))
    
    # 获取作者信息
    for novel in top_novels_read:
        author = user_model.find_by_id(str(novel['authorId']))
        novel['author_name'] = author['username'] if author else '未知'
    
    # 3. 热门小说Top10（按销量）
    top_novels_sales = list(novel_model.collection.find(
        {"status": "online"}
    ).sort("saleCount", -1).limit(10))
    
    for novel in top_novels_sales:
        author = user_model.find_by_id(str(novel['authorId']))
        novel['author_name'] = author['username'] if author else '未知'
    
    # 4. 创作者统计（发布量Top10）
    creator_stats = list(novel_model.collection.aggregate([
        {"$match": {"status": "online"}},
        {"$group": {
            "_id": "$authorId",
            "novelCount": {"$sum": 1},
            "totalRead": {"$sum": "$readCount"},
            "totalSales": {"$sum": "$saleCount"},
            "totalRevenue": {"$sum": {"$multiply": ["$saleCount", "$price"]}}
        }},
        {"$sort": {"novelCount": -1}},
        {"$limit": 10}
    ]))
    
    # 获取创作者名称
    for stat in creator_stats:
        author = user_model.find_by_id(str(stat['_id']))
        stat['author_name'] = author['username'] if author else '未知'
    
    # 5. 用户角色统计
    user_role_stats = list(user_model.collection.aggregate([
        {"$match": {"status": 1}},
        {"$group": {
            "_id": "$role",
            "count": {"$sum": 1}
        }}
    ]))
    
    # 6. 总体统计
    total_stats = {
        "total_users": user_model.collection.count_documents({"status": 1}),
        "total_novels": novel_model.collection.count_documents({"status": "online"}),
        "total_chapters": sum([len(n.get('chapters', [])) for n in novel_model.collection.find({"status": "online"})]),
        "total_orders": order_model.collection.count_documents({}),
        "total_revenue": sum([o['amount'] for o in order_model.collection.find({"status": "paid"})])
    }
    
    return render_template('admin/statistics.html',
                         category_stats=category_stats,
                         top_novels_read=top_novels_read,
                         top_novels_sales=top_novels_sales,
                         creator_stats=creator_stats,
                         user_role_stats=user_role_stats,
                         total_stats=total_stats)


# 推荐系统
@app.route('/reader/recommendations')
@role_required('reader')
def reader_recommendations():
    """智能推荐页面"""
    reader_id = session['user_id']
    
    # 1. 获取用户购买历史
    purchased_novels = []
    orders = order_model.find_user_orders(reader_id)
    for order in orders:
        if order['status'] == 'paid':
            novel = novel_model.find_by_id(str(order['novelId']))
            if novel:
                purchased_novels.append(novel)
    
    # 2. 获取用户阅读历史
    reading_history = reading_record_model.get_user_reading_history(reader_id, limit=10)
    read_novels = []
    for record in reading_history:
        novel = novel_model.find_by_id(str(record['novelId']))
        if novel:
            read_novels.append(novel)
    
    # 3. 提取用户兴趣标签和分类
    interested_tags = set()
    interested_categories = set()
    
    for novel in purchased_novels + read_novels:
        if 'category' in novel:
            interested_categories.add(novel['category'])
        if 'tags' in novel:
            for tag in novel['tags']:
                interested_tags.add(tag)
    
    # 4. 基于内容的推荐（相似标签和分类）
    content_based_recommendations = []
    if interested_tags or interested_categories:
        query = {"status": "online"}
        or_conditions = []
        
        if interested_categories:
            or_conditions.append({"category": {"$in": list(interested_categories)}})
        if interested_tags:
            or_conditions.append({"tags": {"$in": list(interested_tags)}})
        
        if or_conditions:
            query["$or"] = or_conditions
        
        # 排除已购买和已阅读的小说
        excluded_ids = [novel['_id'] for novel in purchased_novels + read_novels]
        if excluded_ids:
            query["_id"] = {"$nin": excluded_ids}
        
        content_based_recommendations = list(
            novel_model.collection.find(query).sort("readCount", DESCENDING).limit(6)
        )
    
    # 5. 热门推荐（阅读量Top6）- 作为补充
    hot_recommendations = list(
        novel_model.collection.find({"status": "online"}).sort("readCount", DESCENDING).limit(6)
    )
    
    # 6. 新书推荐（最新上线的6本）
    new_recommendations = list(
        novel_model.collection.find({"status": "online"}).sort("createTime", DESCENDING).limit(6)
    )
    
    # 为所有推荐添加作者信息
    for novel in content_based_recommendations + hot_recommendations + new_recommendations:
        author = user_model.find_by_id(str(novel['authorId']))
        novel['author_name'] = author['username'] if author else '未知'
    
    return render_template('reader/recommendations.html',
                         content_based=content_based_recommendations,
                         hot_recommendations=hot_recommendations,
                         new_recommendations=new_recommendations,
                         interested_tags=list(interested_tags),
                         interested_categories=list(interested_categories))


if __name__ == '__main__':
    # 尝试使用 5000 端口，如果被占用则使用 5001
    import socket
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('localhost', 5000)) == 0:
        port = 5001
        print(f"端口 5000 被占用，改用端口 {port}")
    sock.close()
    
    app.run(host='0.0.0.0', port=port, debug=True)
