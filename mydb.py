# 导入pymysql模块
import pymysql
import xlwt
import os
# 创建数据库操作类


class Sql_operation(object):
    '''
    数据库操作
    '''

    def __init__(self, mydb):
        # 实例变量
        self.mydb = mydb
        # 打开数据库连接
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="rootroot",
            db=self.mydb,
            charset="utf8")
        # 创建游标对象
        self.cursor = self.db.cursor()

    def export(self, table_name, output_path):
        if os.path.exists(output_path):  # 如果文件存在
            os.remove(output_path)  # 则删除
        count = self.cursor.execute('select * from ' + table_name)
        # print(self._cursor.lastrowid)
        # print(count)
        # 重置游标的位置
        self.cursor.scroll(0, mode='absolute')
        # 搜取所有结果
        results = self.cursor.fetchall()

        # 获取MYSQL里面的数据字段名称
        fields = self.cursor.description
        workbook = xlwt.Workbook()

        # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
        # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
        sheet = workbook.add_sheet(
            'table_' + table_name,
            cell_overwrite_ok=True)
        # 写上字段信息
        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])
        # 获取并写入数据段信息
        row = 1
        col = 0
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                sheet.write(row, col, u'%s' % results[row - 1][col])
        workbook.save(output_path)

    # 定义查看数据表信息函数，并引入table_field、table_name参数，实现查看不同数据表的建表语句
    def FindAll(self, table_name, x, count):
        # 实例变量
        self.table_name = table_name
        # 定义SQL语句
        x = (x - 1) * 18
        # print(x)
        sql = "select * from " + self.table_name + " limit " + str(x) + ",18"
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 处理结果
            data = self.cursor.fetchall()
            # print(data)
            return data
        except Exception as err:
            print("SQL执行错误，原因：", err)

    def FindAll1(self, table_name):
        # 实例变量
        self.table_name = table_name
        # 定义SQL语句
        sql = "select * from %s" % (self.table_name)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 处理结果
            data = self.cursor.fetchall()
            # print(data)
            return data
        except Exception as err:
            print("SQL执行错误，原因：", err)

    def FindOne(self, id):
        # 实例变量
        self.id = id
        # 定义SQL语句
        sql = "select * from expert_info where id = %d" % (self.id)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 处理结果
            data = self.cursor.fetchall()
            # print(data)
            return data
        except Exception as err:
            print("SQL执行错误，原因：", err)

        # 定义查看数据表信息函数，并引入table_field、table_name参数，实现查看不同数据表的建表语句

    def Find(self, name, hospital, department, skill, content, phone, link):
        # 实例变量
        self.name = name
        self.hospital = hospital
        self.department = department
        self.skill = skill
        self.content = content
        self.phone = phone
        self.link = link
        # 定义SQL语句
        list = [name, hospital, department, skill, content, phone, link]
        list1 = [
            'name',
            'hospital',
            'department',
            'skill',
            'content',
            'phone',
            'link']
        a = []
        b = []
        for i in range(0, 7):
            if list[i] != '':
                a.append(list1[i])
                b.append(list[i])
        print(a)
        print(b)
        sql = "select * from expert_info where "
        for i in range(0, len(a)):
            if i != len(a) - 1:
                sql = sql + a[i] + " like " + "'%" + b[i] + "%'" + " and "
                # sql = sql + a[i] + " like " + "concat('%',"+b[i] + ",'%')" + " and "
                # sql=sql+a[i]+" like "+"concat('%',b["+str(i)+"],'%')"+" and "
            else:
                sql = sql + a[i] + " like " + "'%" + b[i] + "%'"
        sql = "insert into inquire " + sql
        print(sql)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
            # 处理结果
            # data = self.cursor.fetchall()
            # return data
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    def Find1(self, name, hospital, department, skill, content, phone, link):
        # 实例变量
        self.name = name
        self.hospital = hospital
        self.department = department
        self.skill = skill
        self.content = content
        self.phone = phone
        self.link = link
        # 定义SQL语句
        list = [name, hospital, department, skill, content, phone, link]
        list1 = [
            'name',
            'hospital',
            'department',
            'skill',
            'content',
            'phone',
            'link']
        a = []
        b = []
        for i in range(0, 7):
            if list[i] != '':
                a.append(list1[i])
                b.append(list[i])
        print(a)
        print(b)
        sql = "select * from expert_info where "
        for i in range(0, len(a)):
            if i != len(a) - 1:
                sql = sql + a[i] + " like " + "'%" + b[i] + "%'" + " and "
                # sql = sql + a[i] + " like " + "concat('%',"+b[i] + ",'%')" + " and "
                # sql=sql+a[i]+" like "+"concat('%',b["+str(i)+"],'%')"+" and "
            else:
                sql = sql + a[i] + " like " + "'%" + b[i] + "%'"
        print(sql)

        try:
            # 执行数据库操作
            self.cursor.execute(sql)

            # 处理结果
            data = self.cursor.fetchall()
            return data
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    # 定义添加表数据函数
    def Insert(self, name, hospital, department, skill, content, phone, link):
        # 实例变量
        self.name = name
        self.hospital = hospital
        self.department = department
        self.skill = skill
        self.content = content
        self.phone = phone
        self.link = link

        # 定义SQL语句
        sql = "alter table expert_info auto_increment=1"
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)
        sql = "insert into expert_info(name,hospital,department,skill,content,phone,link) values('%s','%s','%s','%s','%s','%s','%s')" % (
            self.name, self.hospital, self.department, self.skill, self.content, self.phone, self.link)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    def InsertUser(self, name, password):
        # 实例变量
        self.name = name
        self.password = password
        # 定义SQL语句
        sql = "alter table users auto_increment=1"
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)
        sql = "insert into users(user_name,user_password) values('%s','%s')" % (
            self.name, self.password)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    # 定义删除表数据函数
    def Del(self, id):
        # 实例变量
        self.id = id
        # 定义SQL语句
        sql = "delete from expert_info where id=%d" % (self.id)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)
        sql = "update expert_info set id = id - 1 where id > %d" % (self.id)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    def Del1(self, id):
        # 实例变量
        self.id = id
        # 定义SQL语句
        sql = "delete from inquire where id=%d" % (self.id)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)
        sql = "update expert_info set id = id - 1 where id > %d" % (self.id)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    def DelAll(self):
        # 定义SQL语句
        sql = "truncate table inquire"
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    def Modify(
            self,
            id,
            name,
            hospital,
            department,
            skill,
            content,
            phone,
            link):
        self.id = id
        self.name = name
        self.hospital = hospital
        self.department = department
        self.skill = skill
        self.content = content
        self.phone = phone
        self.link = link
        list = [name, hospital, department, skill, content, phone, link]
        list1 = [
            'name',
            'hospital',
            'department',
            'skill',
            'content',
            'phone',
            'link']
        a = []
        b = []
        for i in range(0, 7):
            if list[i] != '':
                a.append(list1[i])
                b.append(list[i])
        print(a)
        print(b)
        # 定义SQL语句
        sql = "update expert_info set "
        for i in range(0, len(a)):
            if i != len(a) - 1:
                sql = sql + a[i] + "='" + b[i] + "',"
            else:
                sql = sql + a[i] + "='" + b[i] + "' where id=" + str(self.id)
        print(sql)
        try:
            # 执行数据库操作
            self.cursor.execute(sql)
            # 事务提交
            self.db.commit()
        except Exception as err:
            # 事务回滚
            self.db.rollback()
            print("SQL执行错误，原因：", err)

    # 用析构函数实现数据库关闭
    def __del__(self):
        # 关闭数据库连接
        self.db.close()
