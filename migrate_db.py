#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库迁移脚本，用于添加新字段
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import User, Item

with app.app_context():
    try:
        # 为User表添加views字段
        db.session.execute("ALTER TABLE user ADD COLUMN views INTEGER DEFAULT 0")
        
        # 为Item表添加sales_count字段
        db.session.execute("ALTER TABLE item ADD COLUMN sales_count INTEGER DEFAULT 0")
        
        # 提交事务
        db.session.commit()
        print("数据库迁移成功！已添加views和sales_count字段")
    except Exception as e:
        print(f"数据库迁移失败: {e}")
        db.session.rollback()
        # 如果字段已经存在，跳过错误
        if "duplicate column name" in str(e):
            print("字段已存在，跳过迁移")
        else:
            raise