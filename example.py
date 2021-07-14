"""
用户你好！
lightmysql是一个可以简单地使用Python操作MySQL数据库的扩展。
我们的主要功能是根据Python传入的列表和字典生成MySQL语言，并通过pymysql提交。
由于以轻量为目标，我们暂时保留了INSERT SELECT UPDATE DELETE四条语句，创建库、表等操作没有写入。
针对未适配的操作，你可以通过run_code()函数手动编写SQL语句、MySQL客户端或使用图形化软件操作。

下面将介绍各个函数的详细功能和传参方式。
我们假设我们的MySQL中存在一个名为yxzl的数据库，其中有一个名为users的数据表，
表中有两个字段：name(TEXT) 和 age(int)

依赖安装：
pip3 install lightmysql
"""



# 让我们首先导入包
import lightmysql


# 下面让我们连接到数据库，并选定要操作的库名称为yxzl
conn = lightmysql.Connect(host="127.0.0.1", user="root", password="", database="yxzl", port=3306, charset="utf8")


# 插入一些数据用于测试
conn.insert("users", {"name": "user1", "age": 15})
conn.insert("users", {"name": "user2", "age": 20})
conn.insert("users", {"name": "user3", "age": 100})
# 等价SQL（第一个insert的）：
# INSERT INTO users name, age VALUES 'user1', 15;


# 下面的代码用于查询数据

# 这个写法可以获取数据表（test）中的所有记录
print(conn.get("test"))
# 等价SQL：SELECT * FROM test;
# 输出：[('user1', 15), ('user2', 20), ('user3', 100)]

# 查询记录的一个（或多个）字段
# target指定返回被选中记录需要返回的字段
print(conn.get("test", target=["age"]))
# 等价SQL：SELECT age FROM test;
# 输出：[(15), (20), (100)]

# 包含查询条件（WHERE子句）的查询
print(conn.get("test", target=["age"], condition={"name": "user1"}))
# 等价SQL：SELECT age FROM test WHERE name='user1';
# 输出：[(15)]

print(conn.get("test", condition={"age": 20}))
# 等价SQL：SELECT * FROM test WHERE age=20;
# 输出：[('user2', 20)]
# 提示：虽然对于int类型的数据在定义或书写查询条件时SQL语言支持两旁带引号的数值，
# 但是lightmysql由于Python字符串转义需要不支持。

print(conn.get("test", condition={"age": [20, 100]}))
# 等价SQL：SELECT * FROM test WHERE (age=20 or age=100);
# 输出：[('user2', 20), ('user3', 100)]

print(conn.get("test", condition={"name": "user2", "age": 20}))
# 等价SQL：SELECT * FROM test WHERE name='user2' and age=20;
# 输出：[('user2', 20)]

print(conn.get("test", condition={"name": "user2", "age": 100}, condition_sp="or"))
# 等价SQL：SELECT * FROM test WHERE name='user2' or age=100;
# 输出：[('user2', 20), ('user3', 100)]

# 暂不支持更复杂的条件关系。
# upsate和delete的WHERE子句于此处完全相同。


# 下面介绍update
conn.update("test", changes={"age": 50}, condition={"name": "user3"})
# 等价SQL：UPDATE test SET age=50 WHERE name='user3';

# 即changes里面存储的是需要更新的字段和新的值，
# condition对应WHERE子句的生成，规则与get一样。


# DELETE
conn.delete("test", condition={"name": "user1"})
# 等价SQL：DELETE FROM test WHERE name='user1';

# 非常简单，只需要传入condition生成WHERE子句，规则与前文相同。


# 重启
conn.restart()
# 由于MySQL服务器恶心的8小时一清session规则，导致每八小时需要重连一次。
# 在请求过多时也有可能造成堵塞，需要重启解决。
# 目前我们采取最简单的异常捕获，未来将使用连接池等方式避免问题出现。


# 关闭连接
conn.close()
