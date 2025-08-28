class Product:
    """商品类，存储商品信息"""

    def __init__(self, product_id, name, price, description, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock

    def __str__(self):
        return f"{self.name} (¥{self.price}) - {self.stock}件库存"

    def show_details(self):
        """显示商品详细信息"""
        print(f"\n===== 商品详情 =====")
        print(f"商品ID: {self.product_id}")
        print(f"商品名称: {self.name}")
        print(f"价格: ¥{self.price}")
        print(f"描述: {self.description}")
        print(f"库存: {self.stock}件")
        print("===================\n")


class User:
    """用户类，存储用户信息和购物相关操作"""

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.shopping_cart = []
        self.orders = []

    def add_to_cart(self, product, quantity=1):
        """添加商品到购物车"""
        if quantity <= 0:
            print("数量必须大于0")
            return False

        if product.stock >= quantity:
            # 检查购物车中是否已有该商品
            for item in self.shopping_cart:
                if item["product"].product_id == product.product_id:
                    item["quantity"] += quantity
                    print(f"已将{product.name}数量更新为{item['quantity']}")
                    return True

            # 如果购物车中没有该商品，则添加新条目
            self.shopping_cart.append({
                "product": product,
                "quantity": quantity
            })
            print(f"已将{product.name} x {quantity}添加到购物车")
            return True
        else:
            print(f"抱歉，{product.name}库存不足，当前库存: {product.stock}")
            return False

    def view_cart(self):
        """查看购物车"""
        if not self.shopping_cart:
            print("您的购物车是空的")
            return False

        print("\n===== 购物车 =====")
        total = 0
        for i, item in enumerate(self.shopping_cart, 1):
            product = item["product"]
            quantity = item["quantity"]
            subtotal = product.price * quantity
            total += subtotal
            print(f"{i}. {product.name} - ¥{product.price} x {quantity} = ¥{subtotal}")
        print(f"------------------")
        print(f"总计: ¥{total}")
        print("==================\n")
        return True

    def create_order(self):
        """创建订单"""
        if not self.shopping_cart:
            print("购物车为空，无法创建订单")
            return None

        # 检查库存
        for item in self.shopping_cart:
            if item["product"].stock < item["quantity"]:
                print(f"{item['product'].name}库存不足，无法创建订单")
                return None

        # 创建订单
        order_id = len(self.orders) + 1
        order_items = self.shopping_cart.copy()
        total = sum(item["product"].price * item["quantity"] for item in order_items)

        order = {
            "order_id": order_id,
            "items": order_items,
            "total": total,
            "status": "待支付"
        }

        self.orders.append(order)
        print(f"订单创建成功，订单ID: {order_id}，总金额: ¥{total}")
        return order

    def pay_order(self, order_id):
        """支付订单"""
        for order in self.orders:
            if order["order_id"] == order_id:
                if order["status"] == "待支付":
                    order["status"] = "已支付"
                    # 扣减库存
                    for item in order["items"]:
                        item["product"].stock -= item["quantity"]
                    # 清空购物车
                    self.shopping_cart = []
                    print(f"订单{order_id}支付成功！")
                    return True
                elif order["status"] == "已支付":
                    print(f"订单{order_id}已经支付过了")
                    return False
                else:
                    print(f"订单{order_id}状态异常，无法支付")
                    return False

        print(f"找不到订单ID: {order_id}")
        return False


class ECommerceSystem:
    """电商系统类，管理商品和用户，处理用户交互"""

    def __init__(self):
        self.products = self._initialize_products()
        self.users = self._initialize_users()
        self.current_user = None

    def _initialize_products(self):
        """初始化商品列表"""
        return [
            Product(
                1,
                "智能手机",
                5999,
                "最新款智能手机，6.7英寸屏幕，128GB存储，5000mAh电池",
                50
            ),
            Product(
                2,
                "笔记本电脑",
                8999,
                "高性能笔记本电脑，16GB内存，512GB SSD，英特尔i7处理器",
                30
            ),
            Product(
                3,
                "无线耳机",
                999,
                "主动降噪无线耳机，续航24小时，防水设计",
                100
            ),
            Product(
                4,
                "智能手表",
                1599,
                "多功能智能手表，心率监测，GPS定位，防水50米",
                75
            ),
            Product(
                5,
                "平板电脑",
                3299,
                "10.9英寸平板电脑，64GB存储，支持触控笔",
                40
            )
        ]

    def _initialize_users(self):
        """初始化用户列表"""
        return [
            User(1, "user1", "password1"),
            User(2, "user2", "password2"),
            User(3, "user3", "password3")
        ]

    def browse_products(self):
        """浏览商品列表"""
        print("\n===== 商品列表 =====")
        for product in self.products:
            print(f"{product.product_id}. {product}")
        print("====================\n")

    def view_product_details(self, product_id):
        """查看商品详情"""
        for product in self.products:
            if product.product_id == product_id:
                product.show_details()
                return True
        print(f"找不到商品ID: {product_id}")
        return False

    def login(self, username, password):
        """用户登录"""
        if self.current_user:
            print(f"您已经登录，用户: {self.current_user.username}")
            return True

        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"登录成功，欢迎回来，{username}！")
                return True

        print("用户名或密码错误，登录失败")
        return False

    def logout(self):
        """用户登出"""
        if self.current_user:
            username = self.current_user.username
            self.current_user = None
            print(f"{username}已登出")
            return True
        print("您尚未登录")
        return False

    def add_to_cart(self, product_id, quantity=1):
        """添加商品到购物车"""
        if not self.current_user:
            print("请先登录")
            return False

        for product in self.products:
            if product.product_id == product_id:
                return self.current_user.add_to_cart(product, quantity)

        print(f"找不到商品ID: {product_id}")
        return False

    def view_cart(self):
        """查看购物车"""
        if not self.current_user:
            print("请先登录")
            return False
        return self.current_user.view_cart()

    def create_order(self):
        """创建订单"""
        if not self.current_user:
            print("请先登录")
            return None
        return self.current_user.create_order()

    def pay_order(self, order_id):
        """支付订单"""
        if not self.current_user:
            print("请先登录")
            return False
        return self.current_user.pay_order(order_id)

    def run_simulation(self):
        """运行购物流程模拟"""
        print("欢迎来到电商购物系统模拟！")

        # 模拟用户浏览商品
        print("\n--- 1. 用户浏览商品列表 ---")
        self.browse_products()

        # 模拟用户查看商品详情
        print("--- 2. 用户查看商品详情 ---")
        self.view_product_details(1)  # 查看智能手机详情

        # 模拟用户登录
        print("--- 3. 用户登录 ---")
        self.login("user1", "password1")

        # 模拟用户添加商品到购物车
        print("--- 4. 用户添加商品到购物车 ---")
        self.add_to_cart(1, 1)  # 添加1台智能手机
        self.add_to_cart(3, 2)  # 添加2副无线耳机
        self.view_cart()  # 查看购物车

        # 模拟用户下单
        print("--- 5. 用户下单 ---")
        order = self.create_order()

        # 模拟用户支付
        if order:
            print("--- 6. 用户支付 ---")
            self.pay_order(order["order_id"])

        print("\n购物流程模拟结束，谢谢使用！")


if __name__ == "__main__":
    # 创建电商系统并运行模拟
    ecommerce = ECommerceSystem()
    ecommerce.run_simulation()
