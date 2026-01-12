from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
from bson.objectid import ObjectId
import bcrypt

class Database:
    """数据库连接管理类"""
    
    def __init__(self, uri, db_name):
        # 如果 uri 中没有用户名密码（本地开发模式），使用简单连接
        if not uri or uri == "mongodb://localhost:27017/novel_platform":
            self.client = MongoClient('mongodb://localhost:27017/')
        else:
            self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self._create_indexes()
    
    def _create_indexes(self):
        """创建索引以提升查询效率"""
        # users集合索引
        self.db.users.create_index([("username", ASCENDING)], unique=True)
        self.db.users.create_index([("role", ASCENDING)])
        
        # novels集合索引
        self.db.novels.create_index([("novelId", ASCENDING)], unique=True)
        self.db.novels.create_index([("category", ASCENDING)])
        self.db.novels.create_index([("status", ASCENDING)])
        self.db.novels.create_index([("authorId", ASCENDING)])
        self.db.novels.create_index([("createTime", DESCENDING)])
        # 复合索引用于多条件查询
        self.db.novels.create_index([("category", ASCENDING), ("status", ASCENDING)])
        
        # orders集合索引
        self.db.orders.create_index([("orderId", ASCENDING)], unique=True)
        self.db.orders.create_index([("readerId", ASCENDING)])
        self.db.orders.create_index([("novelId", ASCENDING)])
        
        # reading_records集合索引
        self.db.reading_records.create_index([("readerId", ASCENDING), ("novelId", ASCENDING)], unique=True)
    
    def get_collection(self, name):
        """获取集合"""
        return self.db[name]


class UserModel:
    """用户数据模型"""
    
    def __init__(self, db):
        self.collection = db.get_collection('users')
    
    def create_user(self, username, password, role='reader', avatar=None, tags=None):
        """创建用户"""
        # 密码加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_doc = {
            "username": username,
            "role": role,  # reader/creator/admin
            "password": hashed_password,
            "avatar": avatar,
            "tags": tags or [],
            "status": 1,  # 1-正常，0-注销
            "createTime": datetime.utcnow()
        }
        
        result = self.collection.insert_one(user_doc)
        return result.inserted_id
    
    def find_by_username(self, username):
        """根据用户名查找用户"""
        return self.collection.find_one({"username": username, "status": 1})
    
    def find_by_id(self, user_id):
        """根据ID查找用户"""
        return self.collection.find_one({"_id": ObjectId(user_id), "status": 1})
    
    def update_user(self, user_id, update_data):
        """更新用户信息"""
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    
    def delete_user(self, user_id):
        """逻辑删除用户"""
        return self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"status": 0}}
        )
    
    def verify_password(self, username, password):
        """验证用户密码"""
        user = self.find_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user
        return None
    
    def get_all_users(self, role=None):
        """获取所有用户"""
        query = {"status": 1}
        if role:
            query["role"] = role
        return list(self.collection.find(query))


class NovelModel:
    """小说数据模型"""
    
    def __init__(self, db):
        self.collection = db.get_collection('novels')
    
    def generate_novel_id(self):
        """生成小说ID"""
        count = self.collection.count_documents({})
        return f"NOVEL{datetime.now().strftime('%Y%m%d')}{count+1:04d}"
    
    def create_novel(self, title, author_id, category, tags, intro, cover=None, 
                    price=0.0, chapters=None):
        """创建小说"""
        novel_doc = {
            "novelId": self.generate_novel_id(),
            "title": title,
            "authorId": ObjectId(author_id),
            "category": category,
            "tags": tags or [],
            "intro": intro,
            "cover": cover,
            "price": float(price),
            "status": "draft",  # draft/pending/online/rejected
            "chapters": chapters or [],
            "comments": [],
            "review": None,
            "readCount": 0,
            "saleCount": 0,
            "createTime": datetime.utcnow()
        }
        
        result = self.collection.insert_one(novel_doc)
        return result.inserted_id
    
    def find_by_id(self, novel_id):
        """根据ID查找小说"""
        return self.collection.find_one({"_id": ObjectId(novel_id)})
    
    def find_by_novel_id(self, novel_id):
        """根据小说ID查找"""
        return self.collection.find_one({"novelId": novel_id})
    
    def update_novel(self, novel_id, update_data):
        """更新小说信息"""
        return self.collection.update_one(
            {"_id": ObjectId(novel_id)},
            {"$set": update_data}
        )
    
    def add_chapter(self, novel_id, chapter_data):
        """添加章节"""
        return self.collection.update_one(
            {"_id": ObjectId(novel_id)},
            {"$push": {"chapters": chapter_data}}
        )
    
    def update_chapter(self, novel_id, chapter_id, chapter_data):
        """更新章节"""
        return self.collection.update_one(
            {"_id": ObjectId(novel_id), "chapters.chapterId": chapter_id},
            {"$set": {"chapters.$": chapter_data}}
        )
    
    def delete_chapter(self, novel_id, chapter_id):
        """删除章节"""
        return self.collection.update_one(
            {"_id": ObjectId(novel_id)},
            {"$pull": {"chapters": {"chapterId": chapter_id}}}
        )
    
    def submit_for_review(self, novel_id):
        """提交审核"""
        return self.collection.update_one(
            {"_id": ObjectId(novel_id)},
            {"$set": {"status": "pending"}}
        )
    
    def review_novel(self, novel_id, admin_id, opinion, approved):
        """审核小说"""
        status = "online" if approved else "rejected"
        review_doc = {
            "adminId": ObjectId(admin_id),
            "opinion": opinion,
            "time": datetime.utcnow()
        }
        return self.collection.update_one(
            {"_id": ObjectId(novel_id)},
            {"$set": {"status": status, "review": review_doc}}
        )
    
    def find_novels(self, query=None, skip=0, limit=12, sort_by="createTime", 
                   sort_order=DESCENDING):
        """查询小说列表"""
        query = query or {}
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        return list(cursor)
    
    def count_novels(self, query=None):
        """统计小说数量"""
        query = query or {}
        return self.collection.count_documents(query)
    
    def increment_read_count(self, novel_id):
        """增加阅读量"""
        return self.collection.update_one(
            {"_id": ObjectId(novel_id)},
            {"$inc": {"readCount": 1}}
        )
    
    def add_comment(self, novel_id, user_id, content):
        """添加评论"""
        # 获取用户信息
        from pymongo import MongoClient
        user = self.collection.database.users.find_one({"_id": ObjectId(user_id)})
        
        comment_doc = {
            "userId": ObjectId(user_id),
            "username": user['username'] if user else '匿名用户',
            "content": content,
            "createTime": datetime.utcnow(),
            "replies": []
        }
        return self.collection.update_one(
            {"_id": ObjectId(novel_id)},
            {"$push": {"comments": comment_doc}}
        )


class OrderModel:
    """订单数据模型"""
    
    def __init__(self, db):
        self.collection = db.get_collection('orders')
    
    def generate_order_id(self):
        """生成订单ID"""
        count = self.collection.count_documents({})
        return f"ORDER{datetime.now().strftime('%Y%m%d')}{count+1:04d}"
    
    def create_order(self, reader_id, novel_id, amount):
        """创建订单"""
        order_doc = {
            "orderId": self.generate_order_id(),
            "readerId": ObjectId(reader_id),
            "novelId": ObjectId(novel_id),
            "amount": float(amount),
            "status": "pending",  # pending/paid/refunded
            "createTime": datetime.utcnow(),
            "payTime": None
        }
        
        result = self.collection.insert_one(order_doc)
        return result.inserted_id
    
    def find_by_id(self, order_id):
        """根据ID查找订单"""
        return self.collection.find_one({"_id": ObjectId(order_id)})
    
    def pay_order(self, order_id):
        """支付订单"""
        return self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": "paid", "payTime": datetime.utcnow()}}
        )
    
    def find_user_orders(self, reader_id):
        """查找用户订单"""
        return list(self.collection.find({"readerId": ObjectId(reader_id)}).sort("createTime", DESCENDING))
    
    def check_purchased(self, reader_id, novel_id):
        """检查是否已购买"""
        return self.collection.find_one({
            "readerId": ObjectId(reader_id),
            "novelId": ObjectId(novel_id),
            "status": "paid"
        }) is not None


class ReadingRecordModel:
    """阅读记录数据模型"""
    
    def __init__(self, db):
        self.collection = db.get_collection('reading_records')
    
    def save_progress(self, reader_id, novel_id, chapter_id, page=0):
        """保存阅读进度"""
        return self.collection.update_one(
            {"readerId": ObjectId(reader_id), "novelId": ObjectId(novel_id)},
            {
                "$set": {
                    "currentChapterId": chapter_id,
                    "page": page,
                    "updateTime": datetime.utcnow()
                }
            },
            upsert=True
        )
    
    def get_progress(self, reader_id, novel_id):
        """获取阅读进度"""
        return self.collection.find_one({
            "readerId": ObjectId(reader_id),
            "novelId": ObjectId(novel_id)
        })
    
    def get_user_reading_history(self, reader_id, limit=10):
        """获取用户阅读历史"""
        return list(self.collection.find(
            {"readerId": ObjectId(reader_id)}
        ).sort("updateTime", DESCENDING).limit(limit))