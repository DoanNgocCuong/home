#!/usr/bin/env python3
"""
ADVANCED OOP PITFALLS - Các lỗi OOP Python nâng cao và ít được biết đến
Tập hợp các lỗi thực tế mà ngay cả lập trình viên có kinh nghiệm cũng mắc phải
"""

print("="*80)
print("ADVANCED OOP PITFALLS - CÁC LỖI OOP PYTHON NÂNG CAO")
print("="*80)

# ============================================================================
# 1. MUTABLE DEFAULT ARGUMENTS - Lỗi nguy hiểm nhất
# ============================================================================
print("\n1. MUTABLE DEFAULT ARGUMENTS - LỖI NGUY HIỂM NHẤT")
print("-" * 60)

class StudentWrong:
    """Lỗi: Mutable default argument"""
    def __init__(self, name, grades=[]):  # NGUY HIỂM!
        self.name = name
        self.grades = grades  # Shared reference!

class StudentCorrect:
    """Đúng: Immutable default, tạo mới trong runtime"""
    def __init__(self, name, grades=None):
        self.name = name
        self.grades = grades if grades is not None else []

# Demo lỗi
print("=== WRONG WAY ===")
student1_wrong = StudentWrong("John")
student2_wrong = StudentWrong("Jane")
student1_wrong.grades.append(90)
print(f"Student1 grades: {student1_wrong.grades}")  # [90]
print(f"Student2 grades: {student2_wrong.grades}")  # [90] - BUG!
print(f"Same object? {student1_wrong.grades is student2_wrong.grades}")  # True

print("\n=== CORRECT WAY ===")
student1_correct = StudentCorrect("John")
student2_correct = StudentCorrect("Jane")
student1_correct.grades.append(90)
print(f"Student1 grades: {student1_correct.grades}")  # [90]
print(f"Student2 grades: {student2_correct.grades}")  # []
print(f"Same object? {student1_correct.grades is student2_correct.grades}")  # False

# ============================================================================
# 2. CLASS VARIABLES VS INSTANCE VARIABLES - Lỗi logic khó debug
# ============================================================================
print("\n\n2. CLASS VS INSTANCE VARIABLES - LỖI LOGIC KHÓ DEBUG")
print("-" * 60)

class CounterWrong:
    """Lỗi: Nhầm lẫn class và instance variables"""
    count = 0  # Class variable
    
    def __init__(self):
        # Không tạo instance variable, dùng class variable
        pass
    
    def increment(self):
        self.count += 1  # Tạo instance variable, che class variable!

class CounterCorrect:
    """Đúng: Phân biệt rõ class và instance variables"""
    total_instances = 0  # Class variable
    
    def __init__(self):
        CounterCorrect.total_instances += 1
        self.instance_count = 0  # Instance variable
    
    def increment(self):
        self.instance_count += 1

print("=== WRONG WAY ===")
c1_wrong = CounterWrong()
c2_wrong = CounterWrong()
print(f"Initial class count: {CounterWrong.count}")  # 0

c1_wrong.increment()
print(f"After c1 increment - Class count: {CounterWrong.count}")  # 0 (unchanged!)
print(f"c1.count: {c1_wrong.count}")  # 1 (instance variable created)
print(f"c2.count: {c2_wrong.count}")  # 0 (still class variable)

print("\n=== CORRECT WAY ===")
c1_correct = CounterCorrect()
c2_correct = CounterCorrect()
print(f"Total instances: {CounterCorrect.total_instances}")  # 2

c1_correct.increment()
c1_correct.increment()
c2_correct.increment()
print(f"c1 instance count: {c1_correct.instance_count}")  # 2
print(f"c2 instance count: {c2_correct.instance_count}")  # 1
print(f"Total instances: {CounterCorrect.total_instances}")  # 2

# ============================================================================
# 3. CIRCULAR REFERENCES - Memory leak potential
# ============================================================================
print("\n\n3. CIRCULAR REFERENCES - MEMORY LEAK POTENTIAL")
print("-" * 60)

import weakref
import gc

class ParentWrong:
    """Lỗi: Circular reference có thể gây memory leak"""
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self  # Strong reference back!

class ChildWrong:
    def __init__(self, name):
        self.name = name
        self.parent = None

class ParentCorrect:
    """Đúng: Sử dụng weak reference để tránh circular reference"""
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = weakref.ref(self)  # Weak reference!

class ChildCorrect:
    def __init__(self, name):
        self.name = name
        self.parent = None
    
    def get_parent(self):
        return self.parent() if self.parent else None

print("=== DEMONSTRATING CIRCULAR REFERENCE ISSUE ===")
def create_wrong_family():
    parent = ParentWrong("Dad")
    child = ChildWrong("Kid")
    parent.add_child(child)
    return parent, child

def create_correct_family():
    parent = ParentCorrect("Dad")
    child = ChildCorrect("Kid")
    parent.add_child(child)
    return parent, child

# Test memory cleanup
import sys
print(f"Reference count before: {sys.getrefcount(ParentWrong)}")
wrong_parent, wrong_child = create_wrong_family()
print(f"Wrong parent has child: {wrong_parent.children[0].name}")
print(f"Wrong child has parent: {wrong_child.parent.name}")

correct_parent, correct_child = create_correct_family()
print(f"Correct parent has child: {correct_parent.children[0].name}")
print(f"Correct child has parent: {correct_child.get_parent().name}")

# ============================================================================
# 4. MULTIPLE INHERITANCE DIAMOND PROBLEM
# ============================================================================
print("\n\n4. MULTIPLE INHERITANCE DIAMOND PROBLEM")
print("-" * 60)

class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")
        super().method()

class C(A):
    def method(self):
        print("C.method")
        super().method()

class DWrong(B, C):
    """Lỗi: Không hiểu MRO (Method Resolution Order)"""
    def method(self):
        print("D.method")
        B.method(self)  # Gọi trực tiếp - có thể gọi A.method nhiều lần!
        C.method(self)

class DCorrect(B, C):
    """Đúng: Sử dụng super() để tuân thủ MRO"""
    def method(self):
        print("D.method")
        super().method()  # Tuân thủ MRO

print("=== WRONG WAY (Multiple calls to A) ===")
d_wrong = DWrong()
d_wrong.method()

print("\n=== CORRECT WAY (Single call to A) ===")
d_correct = DCorrect()
d_correct.method()

print(f"\nMRO for DCorrect: {[cls.__name__ for cls in DCorrect.__mro__]}")

# ============================================================================
# 5. PROPERTY DECORATORS PITFALLS
# ============================================================================
print("\n\n5. PROPERTY DECORATORS PITFALLS")
print("-" * 60)

class TemperatureWrong:
    """Lỗi: Không validate input, không handle edge cases"""
    def __init__(self):
        self._celsius = 0
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        self._celsius = value  # Không validate!
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

class TemperatureCorrect:
    """Đúng: Validate input, handle edge cases"""
    def __init__(self, celsius=0):
        self.celsius = celsius  # Sử dụng setter để validate
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Temperature must be a number")
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = float(value)
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

print("=== WRONG WAY ===")
temp_wrong = TemperatureWrong()
temp_wrong.celsius = "invalid"  # Không báo lỗi!
print(f"Wrong temp celsius: {temp_wrong.celsius}")
# print(f"Wrong temp fahrenheit: {temp_wrong.fahrenheit}")  # Sẽ lỗi runtime

print("\n=== CORRECT WAY ===")
temp_correct = TemperatureCorrect()
temp_correct.celsius = 25
print(f"Correct temp celsius: {temp_correct.celsius}")
print(f"Correct temp fahrenheit: {temp_correct.fahrenheit}")

try:
    temp_correct.celsius = "invalid"
except TypeError as e:
    print(f"Caught error: {e}")

try:
    temp_correct.celsius = -300
except ValueError as e:
    print(f"Caught error: {e}")

# ============================================================================
# 6. METACLASS CONFUSION
# ============================================================================
print("\n\n6. METACLASS CONFUSION")
print("-" * 60)

class SingletonWrong:
    """Lỗi: Singleton implementation không thread-safe"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class SingletonMeta(type):
    """Đúng: Thread-safe singleton using metaclass"""
    _instances = {}
    _lock = __import__('threading').Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class SingletonCorrect(metaclass=SingletonMeta):
    def __init__(self):
        self.value = 0

print("=== TESTING SINGLETON ===")
s1_wrong = SingletonWrong()
s2_wrong = SingletonWrong()
print(f"Wrong singleton same object? {s1_wrong is s2_wrong}")

s1_correct = SingletonCorrect()
s2_correct = SingletonCorrect()
print(f"Correct singleton same object? {s1_correct is s2_correct}")

# ============================================================================
# 7. DESCRIPTOR PROTOCOL MISUSE
# ============================================================================
print("\n\n7. DESCRIPTOR PROTOCOL MISUSE")
print("-" * 60)

class ValidatedAttributeWrong:
    """Lỗi: Descriptor không handle multiple instances properly"""
    def __init__(self, validator):
        self.validator = validator
        self.value = None  # Shared across all instances!
    
    def __get__(self, obj, objtype=None):
        return self.value
    
    def __set__(self, obj, value):
        if self.validator(value):
            self.value = value
        else:
            raise ValueError("Invalid value")

class ValidatedAttributeCorrect:
    """Đúng: Descriptor lưu data per instance"""
    def __init__(self, validator):
        self.validator = validator
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, None)
    
    def __set__(self, obj, value):
        if self.validator(value):
            setattr(obj, self.name, value)
        else:
            raise ValueError("Invalid value")

def positive_validator(value):
    return isinstance(value, (int, float)) and value > 0

class PersonWrong:
    age = ValidatedAttributeWrong(positive_validator)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

class PersonCorrect:
    age = ValidatedAttributeCorrect(positive_validator)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

print("=== WRONG DESCRIPTOR (Shared state) ===")
p1_wrong = PersonWrong("John", 25)
p2_wrong = PersonWrong("Jane", 30)
print(f"p1 age: {p1_wrong.age}")  # 30 (not 25!)
print(f"p2 age: {p2_wrong.age}")  # 30

print("\n=== CORRECT DESCRIPTOR (Per-instance state) ===")
p1_correct = PersonCorrect("John", 25)
p2_correct = PersonCorrect("Jane", 30)
print(f"p1 age: {p1_correct.age}")  # 25
print(f"p2 age: {p2_correct.age}")  # 30

# ============================================================================
# 8. CONTEXT MANAGER PROTOCOL ERRORS
# ============================================================================
print("\n\n8. CONTEXT MANAGER PROTOCOL ERRORS")
print("-" * 60)

class DatabaseConnectionWrong:
    """Lỗi: Không handle exceptions properly trong context manager"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.db_name}")
        self.connection = f"connection_to_{self.db_name}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.db_name}")
        self.connection = None
        # Không handle exceptions!

class DatabaseConnectionCorrect:
    """Đúng: Handle exceptions properly"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.db_name}")
        self.connection = f"connection_to_{self.db_name}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.db_name}")
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
            # Log error, rollback transaction, etc.
        self.connection = None
        return False  # Don't suppress exceptions

print("=== TESTING CONTEXT MANAGERS ===")
try:
    with DatabaseConnectionCorrect("test_db") as conn:
        print(f"Using connection: {conn}")
        raise ValueError("Something went wrong!")
except ValueError as e:
    print(f"Caught exception: {e}")

# ============================================================================
# 9. OPERATOR OVERLOADING PITFALLS
# ============================================================================
print("\n\n9. OPERATOR OVERLOADING PITFALLS")
print("-" * 60)

class VectorWrong:
    """Lỗi: Không implement đầy đủ các operators"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return VectorWrong(self.x + other.x, self.y + other.y)
    
    # Thiếu __radd__, __iadd__, __eq__, __hash__, etc.

class VectorCorrect:
    """Đúng: Implement đầy đủ các operators cần thiết"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, VectorCorrect):
            return VectorCorrect(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __iadd__(self, other):
        if isinstance(other, VectorCorrect):
            self.x += other.x
            self.y += other.y
            return self
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, VectorCorrect):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"VectorCorrect({self.x}, {self.y})"

print("=== TESTING OPERATOR OVERLOADING ===")
v1 = VectorCorrect(1, 2)
v2 = VectorCorrect(3, 4)
v3 = v1 + v2
print(f"v1 + v2 = {v3}")

v1 += v2
print(f"v1 after += v2: {v1}")

print(f"v1 == VectorCorrect(4, 6): {v1 == VectorCorrect(4, 6)}")

# ============================================================================
# 10. ABSTRACT BASE CLASS MISUSE
# ============================================================================
print("\n\n10. ABSTRACT BASE CLASS MISUSE")
print("-" * 60)

from abc import ABC, abstractmethod

class ShapeWrong:
    """Lỗi: Không enforce abstract methods"""
    def area(self):
        pass  # Không báo lỗi nếu subclass không implement

class ShapeCorrect(ABC):
    """Đúng: Sử dụng ABC để enforce abstract methods"""
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    def description(self):
        return f"Shape with area {self.area()} and perimeter {self.perimeter()}"

class CircleWrong(ShapeWrong):
    def __init__(self, radius):
        self.radius = radius
    # Không implement area() - không báo lỗi!

class CircleCorrect(ShapeCorrect):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

print("=== TESTING ABSTRACT BASE CLASSES ===")
circle_wrong = CircleWrong(5)  # Tạo được dù không implement area()
print(f"Wrong circle created: {circle_wrong}")

circle_correct = CircleCorrect(5)
print(f"Correct circle area: {circle_correct.area()}")
print(f"Correct circle description: {circle_correct.description()}")

# Thử tạo abstract class trực tiếp
try:
    shape = ShapeCorrect()  # Sẽ lỗi
except TypeError as e:
    print(f"Cannot instantiate abstract class: {e}")

print("\n" + "="*80)
print("SUMMARY: ĐÂY LÀ CÁC LỖI OOP PYTHON NÂNG CAO THƯỜNG BỊ BỎ QUA!")
print("Những lỗi này có thể gây ra bugs khó debug và performance issues.")
print("="*80)