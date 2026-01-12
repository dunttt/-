"""
初始化数据脚本
创建管理员账号和示例数据
"""

from pymongo import MongoClient
import bcrypt
from datetime import datetime
import os

# 数据库配置
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))
MONGODB_USER = os.environ.get('MONGODB_USER', '')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '')
MONGODB_DB = os.environ.get('MONGODB_DB', 'novel_platform')

# 构建连接 URI
if MONGODB_USER and MONGODB_PASSWORD:
    MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}?authSource=admin"
else:
    MONGODB_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}"

def init_database():
    """初始化数据库"""
    print("正在连接 MongoDB...")
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    
    # 清空现有数据（可选）
    print("清理现有数据...")
    db.users.delete_many({})
    db.novels.delete_many({})
    db.orders.delete_many({})
    db.reading_records.delete_many({})
    
    # 创建管理员账号
    print("创建管理员账号...")
    admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
    admin_user = {
        "username": "admin",
        "role": "admin",
        "password": admin_password,
        "avatar": None,
        "tags": [],
        "status": 1,
        "createTime": datetime.utcnow()
    }
    admin_id = db.users.insert_one(admin_user).inserted_id
    print(f"✓ 管理员账号创建成功")
    print(f"  用户名: admin")
    print(f"  密码: admin123")
    
    # 创建示例创作者
    print("\n创建示例创作者...")
    creator_password = bcrypt.hashpw('creator123'.encode('utf-8'), bcrypt.gensalt())
    creator_user = {
        "username": "作家小明",
        "role": "creator",
        "password": creator_password,
        "avatar": None,
        "tags": ["玄幻", "科幻"],
        "status": 1,
        "createTime": datetime.utcnow()
    }
    creator_id = db.users.insert_one(creator_user).inserted_id
    print(f"✓ 创作者账号创建成功")
    print(f"  用户名: 作家小明")
    print(f"  密码: creator123")
    
    # 创建示例读者
    print("\n创建示例读者...")
    reader_password = bcrypt.hashpw('reader123'.encode('utf-8'), bcrypt.gensalt())
    reader_user = {
        "username": "读者小红",
        "role": "reader",
        "password": reader_password,
        "avatar": None,
        "tags": ["玄幻", "言情"],
        "status": 1,
        "createTime": datetime.utcnow()
    }
    reader_id = db.users.insert_one(reader_user).inserted_id
    print(f"✓ 读者账号创建成功")
    print(f"  用户名: 读者小红")
    print(f"  密码: reader123")
    
    # 创建示例小说
    print("\n创建示例小说...")
    sample_novel = {
        "novelId": "NOVEL20260111001",
        "title": "穿越之科技强国",
        "authorId": creator_id,
        "category": "科幻",
        "tags": ["穿越", "科技", "热血"],
        "intro": "一名现代程序员意外穿越到平行世界的古代，利用现代科技知识，开启科技强国之路。从蒸汽机到电力革命，从无线电报到计算机，看主角如何在古代掀起科技风暴！",
        "cover": None,
        "price": 9.9,
        "status": "online",
        "chapters": [
            {
                "chapterId": "CH001",
                "title": "第一章 意外穿越",
                "content": """深夜，程序员李明加班到凌晨三点，终于完成了最后一行代码。
                
他伸了个懒腰，准备关机回家。突然，电脑屏幕闪过一道刺眼的白光！

"啊！"李明惊叫一声，眼前一黑，失去了意识。

不知过了多久，李明缓缓睁开眼睛，映入眼帘的是古色古香的木制房梁。

"这是哪里？"他猛地坐起来，发现自己躺在一张硬邦邦的木板床上，身上盖着粗布被子。

环顾四周，这是一间简陋的房间，墙壁是泥土糊成的，家具少得可怜，只有一张桌子、一把椅子和这张床。

"难道...我穿越了？"李明的心跳加速，作为一个资深网文读者，他立刻想到了这个可能。

就在这时，一段陌生的记忆涌入他的脑海...

原来，这具身体的原主人也叫李明，是一个穷书生，父母早亡，靠着给村里的私塾做杂工勉强度日。

"既来之则安之。"李明深吸一口气，"既然老天给了我第二次生命，那我就要活出精彩！"

他走到窗前，推开窗户，阳光洒进来。这是一个古代的小村庄，远处是连绵的群山。

李明的嘴角露出一丝笑容："这个世界，准备好迎接科技革命了吗？"
""",
                "isFree": True,
                "createTime": datetime.utcnow()
            },
            {
                "chapterId": "CH002",
                "title": "第二章 初露锋芒",
                "content": """第二天一早，李明就起床了。

昨晚他整理了原主的记忆，发现这个世界的科技水平大约相当于地球的明朝时期，但没有火药，也没有印刷术。

"这可是个好机会！"李明兴奋不已。

他决定先从简单的开始——制作肥皂。

在现代，肥皂制作原理很简单：油脂加碱，经过皂化反应就能得到肥皂。

李明走出房间，来到村长家，说明来意后借了一些草木灰和猪油。

村长疑惑地看着他："李明，你要这些做什么？"

"村长，您等着看好戏吧！"李明神秘地笑了笑。

回到家中，李明开始动手制作。他先用草木灰加水熬煮，得到碱液，然后加热猪油，慢慢加入碱液，不断搅拌...

三个时辰后，一块块白色的固体出现了——这就是肥皂！

李明拿起一块肥皂，沾水搓了搓，立刻产生了丰富的泡沫。

"成功了！"他激动地握紧拳头。

这一小步，是他在这个世界迈出的第一步，也是这个世界科技革命的第一步！
""",
                "isFree": True,
                "createTime": datetime.utcnow()
            },
            {
                "chapterId": "CH003",
                "title": "第三章 声名鹊起",
                "content": """李明制作的肥皂很快在村里传开了。

村民们从来没见过这种神奇的东西，只需要一点点，就能洗得干干净净，而且还有淡淡的香味。

"李明，你这东西卖不卖？"村长第一个找上门来。

"卖！当然卖！"李明笑道，"一块十文钱，童叟无欺。"

十文钱在这个时代不算贵，村民们纷纷购买。短短几天，李明就卖出了上百块肥皂，赚了一千多文钱。

但李明并不满足于此。他知道，肥皂只是开始，真正的大事业还在后面。

这天，镇上的富商王掌柜来到村里，听说了肥皂的神奇功效，特地赶来一探究竟。

"李公子，老夫王富贵，镇上王记商行的掌柜。"王掌柜拱手道，"听闻公子发明了神奇的洗涤之物，不知可否让老夫见识一下？"

李明早就等着这一天，他带着王掌柜进屋，详细演示了肥皂的用法。

王掌柜看完，眼睛都亮了："妙啊！妙啊！李公子，老夫想和你合作，将这肥皂推广到整个州府，甚至京城！"

李明微微一笑："王掌柜，我等的就是你这句话！"
""",
                "isFree": True,
                "createTime": datetime.utcnow()
            },
            {
                "chapterId": "CH004",
                "title": "第四章 商业帝国",
                "content": """与王掌柜的合作很顺利。

李明负责提供肥皂配方和技术指导，王掌柜负责生产和销售，利润五五分成。

很快，"李记肥皂"就在整个州府火了起来，从富商贵族到平民百姓，人人都在使用。

三个月后，李明已经赚到了一万两银子，成了远近闻名的富翁。

但他并没有停下脚步。

"王掌柜，我又有了新的想法。"李明说。

"哦？李公子请讲。"王掌柜洗耳恭听。

"我想做纸——更便宜、更好的纸！"

现在这个世界的纸张非常昂贵，普通人根本用不起。李明决定改进造纸术，让纸张变得便宜，让知识得以传播。

这不仅是生意，更是改变这个世界的机会！

（此章节需要购买小说才能继续阅读）
""",
                "isFree": False,
                "createTime": datetime.utcnow()
            },
            {
                "chapterId": "CH005",
                "title": "第五章 造纸革命",
                "content": """李明开始着手改进造纸术。

他购买了大量的竹子、树皮和废旧渔网，作为造纸的原料。

在现代学过化学的李明，深知纤维素是造纸的关键。他将原料切碎，用石灰水浸泡，去除杂质，然后捣成纸浆...

经过无数次实验和改进，终于，第一批"李记纸"诞生了！

这种纸张洁白平整，书写流畅，价格却只有传统纸张的十分之一！

"太好了！有了这种纸，天下的读书人都能买得起书了！"李明激动不已。

王掌柜看到样品后，也是惊叹不已："李公子真乃神人也！这纸若是推向市场，必将引起轰动！"

果然，"李记纸"一上市，就引起了巨大的反响...

（需购买完整版）
""",
                "isFree": False,
                "createTime": datetime.utcnow()
            }
        ],
        "comments": [],
        "review": {
            "adminId": admin_id,
            "opinion": "内容健康，情节精彩，通过审核。",
            "time": datetime.utcnow()
        },
        "readCount": 1580,
        "saleCount": 237,
        "createTime": datetime.utcnow()
    }
    novel_id = db.novels.insert_one(sample_novel).inserted_id
    print(f"✓ 示例小说创建成功: {sample_novel['title']}")
    
    # 创建示例订单
    print("\n创建示例订单...")
    sample_order = {
        "orderId": "ORDER20260111001",
        "readerId": reader_id,
        "novelId": novel_id,
        "amount": 9.9,
        "status": "paid",
        "createTime": datetime.utcnow(),
        "payTime": datetime.utcnow()
    }
    db.orders.insert_one(sample_order)
    print(f"✓ 示例订单创建成功")
    
    print("\n" + "="*50)
    print("数据库初始化完成！")
    print("="*50)
    print("\n测试账号信息：")
    print("\n1. 管理员账号")
    print("   用户名: admin")
    print("   密码: admin123")
    print("\n2. 创作者账号")
    print("   用户名: 作家小明")
    print("   密码: creator123")
    print("\n3. 读者账号")
    print("   用户名: 读者小红")
    print("   密码: reader123")
    print("\n请访问 http://localhost:5000 开始使用！")
    print("="*50)

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n错误: {str(e)}")
        print("请确保 MongoDB 服务已启动，并检查连接配置。")
