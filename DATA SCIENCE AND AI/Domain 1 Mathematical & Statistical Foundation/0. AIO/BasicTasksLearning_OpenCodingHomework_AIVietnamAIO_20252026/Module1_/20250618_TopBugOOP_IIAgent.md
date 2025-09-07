# 🚨 CHECKLIST TOÀN DIỆN CÁC LỖI OOP PYTHON THƯỜNG GẶP

## 📊 PHÂN LOẠI LỖI THEO MỨC ĐỘ NGHIÊM TRỌNG

### 🔴 **CRITICAL ERRORS** (Làm crash chương trình)
### 🟡 **WARNING ERRORS** (Chạy được nhưng logic sai)  
### 🔵 **STYLE ERRORS** (Vi phạm best practices)

---

## 🔴 **CRITICAL ERRORS - LỖI NGHIÊM TRỌNG**

### **1. Constructor & Initialization Errors**

#### ❌ **1.1. Missing Required Parameters**
```python
# SAI
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student()  # TypeError: missing 2 required positional arguments
```

#### ❌ **1.2. Forgot super().__init__() in Inheritance**
```python
# SAI
class Person:
    def __init__(self, name):
        self.name = name
        self.id = self.generate_id()

class Student(Person):
    def __init__(self, name, grade):
        self.grade = grade  # Quên super().__init__(name)

student = Student("John", "A")
print(student.name)  # AttributeError: 'Student' object has no attribute 'name'
```

#### ❌ **1.3. Wrong Order of super() Call**
```python
# SAI - Có thể gây logic error
class Animal:
    def __init__(self):
        self.energy = 100

class Dog(Animal):
    def __init__(self):
        self.energy = 50  # Set trước
        super().__init__()  # Ghi đè thành 100

dog = Dog()
print(dog.energy)  # 100 (không phải 50 như mong đợi)
```

### **2. Attribute Access Errors**

#### ❌ **2.1. Accessing Private Variables Incorrectly**
```python
# SAI
class BankAccount:
    def __init__(self):
        self.__balance = 1000

    def show_balance(self):
        print(__balance)  # NameError: name '__balance' is not defined

account = BankAccount()
print(account.__balance)  # AttributeError
```

#### ❌ **2.2. Forgot self. for Instance Variables**
```python
# SAI
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        result = result + value  # NameError: name 'result' is not defined
        return result
```

#### ❌ **2.3. Mixing Class and Instance Variables**
```python
# SAI - Logic error
class Counter:
    count = 0  # Class variable
    
    def __init__(self):
        count = 0  # Tạo biến cục bộ, không phải instance variable
    
    def increment(self):
        self.count += 1  # Tạo instance variable, không update class variable

c1 = Counter()
c2 = Counter()
c1.increment()
print(Counter.count)  # 0 (không phải 1)
```

### **3. Method Definition Errors**

#### ❌ **3.1. Forgot self Parameter**
```python
# SAI
class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area():  # Quên self
        return 3.14 * self.radius ** 2  # NameError

circle = Circle(5)
circle.area()  # TypeError: area() takes 0 positional arguments but 1 was given
```

#### ❌ **3.2. Wrong self Parameter Name**
```python
# SAI - Gây nhầm lẫn
class Student:
    def __init__(obj, name):  # Nên dùng self
        obj.name = name
    
    def study(this):  # Nên dùng self
        print(f"{this.name} is studying")
```

### **4. Inheritance Errors**

#### ❌ **4.1. Circular Inheritance**
```python
# SAI
class A(B):
    pass

class B(A):  # TypeError: Cannot create a consistent method resolution order
    pass
```

#### ❌ **4.2. Multiple Inheritance Diamond Problem**
```python
# SAI - Không handle MRO properly
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()  # Có thể gây confusion về thứ tự gọi
```

---

## 🟡 **WARNING ERRORS - LỖI LOGIC**

### **5. Mutable Default Arguments**

#### ❌ **5.1. Mutable Default in Constructor**
```python
# SAI - Shared mutable default
class Student:
    def __init__(self, name, grades=[]):  # Nguy hiểm!
        self.name = name
        self.grades = grades

student1 = Student("John")
student2 = Student("Jane")
student1.grades.append(90)
print(student2.grades)  # [90] - Bị ảnh hưởng!

# ĐÚNG
class Student:
    def __init__(self, name, grades=None):
        self.name = name
        self.grades = grades if grades is not None else []
```

### **6. Memory & Reference Issues**

#### ❌ **6.1. Circular References**
```python
# SAI - Memory leak potential
class Parent:
    def __init__(self):
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self  # Circular reference

class Child:
    def __init__(self):
        self.parent = None

# Có thể gây memory leak nếu không handle properly
```

#### ❌ **6.2. Modifying Class Variables Unintentionally**
```python
# SAI - Logic error
class Student:
    all_grades = []  # Class variable
    
    def __init__(self, name):
        self.name = name
    
    def add_grade(self, grade):
        self.all_grades.append(grade)  # Modify class variable!

student1 = Student("John")
student2 = Student("Jane")
student1.add_grade(90)
student2.add_grade(85)
print(Student.all_grades)  # [90, 85] - Shared between all instances!
```

### **7. Method Overriding Issues**

#### ❌ **7.1. Forgot to Call Parent Method**
```python
# SAI - Mất functionality của parent
class Animal:
    def __init__(self, name):
        self.name = name
        self.register_animal()  # Important functionality
    
    def register_animal(self):
        print(f"Registering {self.name}")

class Dog(Animal):
    def __init__(self, name, breed):
        # Quên super().__init__(name)
        self.breed = breed  # Mất register_animal()
```

#### ❌ **7.2. Incorrect Method Signature in Override**
```python
# SAI - Signature không match
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def area(self, length, width):  # Signature khác!
        return length * width

# Không thể dùng polymorphism
shapes = [Rectangle()]
for shape in shapes:
    print(shape.area())  # TypeError: missing 2 required positional arguments
```

---

## 🔵 **STYLE ERRORS - VI PHẠM BEST PRACTICES**

### **8. Naming Convention Violations**

#### ❌ **8.1. Wrong Naming Conventions**
```python
# SAI
class student_class:  # Nên là StudentClass (PascalCase)
    def __init__(self):
        self.StudentName = ""  # Nên là student_name (snake_case)
        self.STUDENT_AGE = 0   # Nên là student_age
    
    def GetStudentInfo(self):  # Nên là get_student_info
        pass
```

#### ❌ **8.2. Misleading Private/Protected Usage**
```python
# SAI - Inconsistent usage
class BankAccount:
    def __init__(self):
        self.balance = 1000      # Public nhưng nên protected
        self._account_number = "123"  # Protected nhưng có thể nên private
        self.__secret_key = "abc"     # Private nhưng không cần thiết
```

### **9. Design Pattern Violations**

#### ❌ **9.1. God Class (Too Many Responsibilities)**
```python
# SAI - Violates Single Responsibility Principle
class Student:
    def __init__(self, name):
        self.name = name
    
    def study(self): pass
    def eat(self): pass
    def sleep(self): pass
    def calculate_gpa(self): pass
    def send_email(self): pass  # Không thuộc về Student
    def manage_database(self): pass  # Không thuộc về Student
    def generate_report(self): pass  # Không thuộc về Student
```

#### ❌ **9.2. Tight Coupling**
```python
# SAI - Hard to test and maintain
class EmailService:
    def send_email(self, message):
        # Direct dependency on external service
        smtp_server = SMTPServer("gmail.com")
        smtp_server.send(message)

class User:
    def __init__(self):
        self.email_service = EmailService()  # Tight coupling
```

### **10. Performance & Memory Issues**

#### ❌ **10.1. Unnecessary Object Creation**
```python
# SAI - Inefficient
class Calculator:
    def add(self, a, b):
        result = Result(a + b)  # Tạo object mới mỗi lần
        return result.value

class Result:
    def __init__(self, value):
        self.value = value
```

#### ❌ **10.2. Not Using __slots__ When Appropriate**
```python
# SAI - Memory inefficient for large number of instances
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ĐÚNG - For memory efficiency
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

---

## 📋 **COMPREHENSIVE ERROR CHECKLIST**

### **🔍 Pre-Code Review Checklist**

#### **Constructor & Initialization**
- [ ] Tất cả required parameters được truyền vào `__init__`?
- [ ] `super().__init__()` được gọi trong inheritance?
- [ ] Thứ tự gọi `super()` đúng chưa?
- [ ] Không dùng mutable default arguments?

#### **Attribute Access**
- [ ] Tất cả instance variables đều dùng `self.`?
- [ ] Private variables được truy cập đúng cách?
- [ ] Phân biệt rõ class vs instance variables?
- [ ] Không modify class variables unintentionally?

#### **Method Definition**
- [ ] Tất cả instance methods đều có `self` parameter?
- [ ] Tên parameter đầu tiên là `self` (không phải `obj`, `this`)?
- [ ] Method signatures consistent khi override?
- [ ] Parent methods được gọi khi cần thiết?

#### **Inheritance**
- [ ] Không có circular inheritance?
- [ ] MRO (Method Resolution Order) được handle đúng?
- [ ] Diamond problem được giải quyết?
- [ ] Polymorphism hoạt động đúng?

#### **Design & Style**
- [ ] Naming conventions đúng (PascalCase cho class, snake_case cho methods)?
- [ ] Single Responsibility Principle được tuân thủ?
- [ ] Loose coupling giữa các classes?
- [ ] Appropriate use của private/protected/public?

#### **Performance & Memory**
- [ ] Không có memory leaks từ circular references?
- [ ] Efficient object creation?
- [ ] `__slots__` được dùng khi cần thiết?
- [ ] Không có unnecessary object creation trong loops?

---

## 🛠️ **DEBUGGING WORKFLOW**

### **Khi gặp lỗi OOP, check theo thứ tự:**

1. **AttributeError** → Check `self.` và `super().__init__()`
2. **NameError** → Check private variable access và variable scope
3. **TypeError** → Check method parameters và inheritance
4. **Logic errors** → Check class vs instance variables
5. **Performance issues** → Check object creation và memory usage

### **Common Error Patterns:**

| **Error Type** | **Typical Cause** | **Quick Fix** |
|----------------|-------------------|---------------|
| `AttributeError: 'X' object has no attribute 'Y'` | Forgot `self.` or `super().__init__()` | Add `self.` or call parent constructor |
| `NameError: name 'X' is not defined` | Wrong private variable access | Use `self.__variable` |
| `TypeError: X() missing N required positional arguments` | Missing constructor parameters | Provide all required arguments |
| `TypeError: X() takes N positional arguments but M were given` | Forgot `self` parameter | Add `self` as first parameter |

---

## 💡 **PREVENTION STRATEGIES**

### **1. Code Templates**
```python
# Standard class template
class ClassName:
    """Class docstring"""
    
    class_variable = "default"  # Class variable
    
    def __init__(self, required_param, optional_param=None):
        """Constructor docstring"""
        super().__init__()  # If inheriting
        self.required_param = required_param
        self.optional_param = optional_param or []
        self._protected_var = "internal"
        self.__private_var = "secret"
    
    def public_method(self):
        """Public method docstring"""
        return self._protected_method()
    
    def _protected_method(self):
        """Protected method docstring"""
        return self.__private_var
    
    def __str__(self):
        """String representation"""
        return f"ClassName({self.required_param})"
    
    def __repr__(self):
        """Developer representation"""
        return f"ClassName(required_param={self.required_param!r})"
```

### **2. Testing Strategy**
```python
# Always test your classes
def test_class():
    # Test constructor
    obj = ClassName("test")
    assert obj.required_param == "test"
    
    # Test methods
    result = obj.public_method()
    assert result is not None
    
    # Test inheritance
    if hasattr(obj, 'parent_method'):
        obj.parent_method()
    
    # Test edge cases
    try:
        ClassName()  # Should raise TypeError
        assert False, "Should have raised TypeError"
    except TypeError:
        pass
```

### **3. Code Review Questions**
- Có thể tạo object mà không crash không?
- Inheritance hierarchy có logic không?
- Memory usage có efficient không?
- Code có dễ test và maintain không?
- Naming conventions có consistent không?

---

## 🎯 **SUMMARY - TOP 10 LỖI THƯỜNG GẶP NHẤT**

1. **Quên `super().__init__()`** trong inheritance
2. **Quên `self.`** khi gán instance variables  
3. **Truy cập private variables sai cách** (`__var` vs `self.__var`)
4. **Mutable default arguments** trong constructor
5. **Quên `self` parameter** trong method definition
6. **Nhầm lẫn class vs instance variables**
7. **Thứ tự sai** khi gọi `super()`
8. **Circular references** gây memory leak
9. **Wrong method signatures** khi override
10. **Violating naming conventions** và design principles

**Remember: 80% lỗi OOP Python đến từ việc quên `self.` và `super().__init__()`!**