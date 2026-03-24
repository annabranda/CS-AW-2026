import time
import string
import random
import sys
import concurrent.futures
import numpy as np
from numba import njit

class ListNode:
    __slots__ = ['data', 'next']
    def __init__(self, data):
        self.data = data
        self.next = None

@njit
def selection_sort_numba(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]: 
                min_idx = j
        arr[min_idx], arr[i] = arr[i], arr[min_idx]

@njit
def bubble_sort_numba(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped: 
            break

@njit
def insertion_sort_numba(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

@njit
def _merge_numba(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1
    for idx in range(left, right + 1):
        arr[idx] = temp[idx]

@njit
def _merge_sort_recursive_numba(arr, temp, left, right):
    if left < right:
        mid = left + (right - left) // 2
        _merge_sort_recursive_numba(arr, temp, left, mid)
        _merge_sort_recursive_numba(arr, temp, mid + 1, right)
        _merge_numba(arr, temp, left, mid, right)

@njit
def merge_sort_numba(arr):
    temp = np.empty_like(arr)
    _merge_sort_recursive_numba(arr, temp, 0, len(arr) - 1)

@njit
def _quick_sort_recursive_numba(arr, low, high):
    if low < high:
        mid = low + (high - low) // 2
        pivot = arr[mid]
        lt = low
        gt = high
        i = low
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[gt], arr[i] = arr[i], arr[gt]
                gt -= 1
            else:
                i += 1
        
        _quick_sort_recursive_numba(arr, low, lt - 1)
        _quick_sort_recursive_numba(arr, gt + 1, high)

@njit
def quick_sort_numba(arr):
    _quick_sort_recursive_numba(arr, 0, len(arr) - 1)

@njit
def heapify_numba(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_numba(arr, n, largest)

@njit
def heap_sort_numba(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1): 
        heapify_numba(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify_numba(arr, i, 0)

@njit
def shell_sort_numba(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

def parallel_merge_sort_numba(arr):
    if len(arr) <= 10000:
        merge_sort_numba(arr)
        return
    mid = len(arr) // 2
    left = arr[:mid].copy()
    right = arr[mid:].copy()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(merge_sort_numba, left)
        f2 = executor.submit(merge_sort_numba, right)
        f1.result()
        f2.result()
    arr[:mid] = left
    arr[mid:] = right
    temp = np.empty_like(arr)
    _merge_numba(arr, temp, 0, mid - 1, len(arr) - 1)

def selection_sort_py(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]: 
                min_idx = j
        arr[min_idx], arr[i] = arr[i], arr[min_idx]

def bubble_sort_py(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped: 
            break

def insertion_sort_py(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def _merge_py(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1
    for idx in range(left, right + 1):
        arr[idx] = temp[idx]

def _merge_sort_recursive_py(arr, temp, left, right):
    if left < right:
        mid = left + (right - left) // 2
        _merge_sort_recursive_py(arr, temp, left, mid)
        _merge_sort_recursive_py(arr, temp, mid + 1, right)
        _merge_py(arr, temp, left, mid, right)

def merge_sort_py(arr):
    temp = [None] * len(arr)
    _merge_sort_recursive_py(arr, temp, 0, len(arr) - 1)

def _quick_sort_recursive_py(arr, low, high):
    if low < high:
        mid = low + (high - low) // 2
        pivot = arr[mid]
        lt = low
        gt = high
        i = low
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[gt], arr[i] = arr[i], arr[gt]
                gt -= 1
            else:
                i += 1
        
        _quick_sort_recursive_py(arr, low, lt - 1)
        _quick_sort_recursive_py(arr, gt + 1, high)

def quick_sort_py(arr):
    _quick_sort_recursive_py(arr, 0, len(arr) - 1)

def heapify_py(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_py(arr, n, largest)

def heap_sort_py(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1): 
        heapify_py(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify_py(arr, i, 0)

def shell_sort_py(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

def parallel_merge_sort_py(arr):
    if len(arr) <= 10000:
        merge_sort_py(arr)
        return
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(merge_sort_py, left)
        f2 = executor.submit(merge_sort_py, right)
        f1.result()
        f2.result()
    arr[:mid] = left
    arr[mid:] = right
    temp = [None] * len(arr)
    _merge_py(arr, temp, 0, mid - 1, len(arr) - 1)

def list_to_linked_list(arr):
    if len(arr) == 0: return None
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def get_middle(head):
    if not head: return head
    slow = head
    fast = head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def sorted_merge(a, b):
    dummy = ListNode(None)
    tail = dummy
    while a and b:
        if a.data <= b.data:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next

def ll_merge_sort(head):
    if not head or not head.next:
        return head
    mid = get_middle(head)
    next_to_mid = mid.next
    mid.next = None
    left = ll_merge_sort(head)
    right = ll_merge_sort(next_to_mid)
    return sorted_merge(left, right)

def linked_list_sort_wrapper(arr):
    if len(arr) == 0: return
    head = list_to_linked_list(arr)
    head = ll_merge_sort(head)

def generate_dataset(size, structure="random", dtype_str="int", use_numpy=True):
    rng = np.random.default_rng()
    if dtype_str == "int":
        if use_numpy:
            if structure == "random": return rng.integers(1, 1000000, size=size, dtype=np.int32)
            elif structure == "sorted": return np.arange(size, dtype=np.int32)
            elif structure == "reverse": return np.arange(size, 0, -1, dtype=np.int32)
            elif structure == "almost":
                arr = np.arange(size, dtype=np.int32)
                swaps = max(1, int(size * 0.02))
                for _ in range(swaps):
                    i, j = rng.integers(0, size, 2)
                    arr[i], arr[j] = arr[j], arr[i]
                return arr
            elif structure == "mixed":
                half = size // 2
                arr1 = np.arange(half, dtype=np.int32)
                arr2 = rng.integers(1, 1000000, size=size - half, dtype=np.int32)
                return np.concatenate((arr1, arr2))
            elif structure == "flat": return rng.choice(np.array([1, 2, 3, 4, 5], dtype=np.int32), size=size)
            
    elif dtype_str == "float":
        if use_numpy:
            arr = rng.random(size=size, dtype=np.float64) * 1000.0
            if structure == "random": return arr
            elif structure == "sorted":
                arr.sort()
                return arr
            elif structure == "reverse":
                arr.sort()
                return arr[::-1]
            elif structure == "almost":
                arr.sort()
                swaps = max(1, int(size * 0.02))
                for _ in range(swaps):
                    i, j = rng.integers(0, size, 2)
                    arr[i], arr[j] = arr[j], arr[i]
                return arr
            elif structure == "mixed":
                half = size // 2
                arr1 = rng.random(size=half, dtype=np.float64) * 1000.0
                arr1.sort()
                arr2 = rng.random(size=size - half, dtype=np.float64) * 1000.0
                return np.concatenate((arr1, arr2))
            elif structure == "flat":
                choices = rng.random(size=5, dtype=np.float64) * 1000.0
                return rng.choice(choices, size=size)
                
    elif dtype_str == "string":
        chars = string.ascii_lowercase
        if structure == "random": return [''.join(random.choices(chars, k=5)) for _ in range(size)]
        elif structure == "sorted":
            arr = [''.join(random.choices(chars, k=5)) for _ in range(size)]
            arr.sort()
            return arr
        elif structure == "reverse":
            arr = [''.join(random.choices(chars, k=5)) for _ in range(size)]
            arr.sort(reverse=True)
            return arr
        elif structure == "almost":
            arr = [''.join(random.choices(chars, k=5)) for _ in range(size)]
            arr.sort()
            swaps = max(1, int(size * 0.02))
            for _ in range(swaps):
                i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        elif structure == "mixed":
            half = size // 2
            arr1 = [''.join(random.choices(chars, k=5)) for _ in range(half)]
            arr1.sort()
            arr2 = [''.join(random.choices(chars, k=5)) for _ in range(size - half)]
            return arr1 + arr2
        elif structure == "flat":
            choices = [''.join(random.choices(chars, k=5)) for _ in range(5)]
            return [random.choice(choices) for _ in range(size)]

def run_performance_test():
    numba_algorithms = [
        ("Bubble Sort", bubble_sort_numba, True),     
        ("Selection Sort", selection_sort_numba, True),
        ("Insertion Sort", insertion_sort_numba, True),
        ("Shell Sort", shell_sort_numba, False),      
        ("Merge Sort", merge_sort_numba, False),
        ("Quick Sort", quick_sort_numba, False),
        ("Heap Sort", heap_sort_numba, False),
        ("Parallel Merge", parallel_merge_sort_numba, False),
        ("Linked List Merge", linked_list_sort_wrapper, False)
    ]

    py_algorithms = [
        ("Bubble Sort", bubble_sort_py, True),     
        ("Selection Sort", selection_sort_py, True),
        ("Insertion Sort", insertion_sort_py, True),
        ("Shell Sort", shell_sort_py, False),      
        ("Merge Sort", merge_sort_py, False),
        ("Quick Sort", quick_sort_py, False),
        ("Heap Sort", heap_sort_py, False),
        ("Parallel Merge", parallel_merge_sort_py, False),
        ("Linked List Merge", linked_list_sort_wrapper, False)
    ]

    structures = ["random", "sorted", "reverse", "almost", "mixed", "flat"]
    
    warmup_data_int = np.array([5, 2, 9, 1, 5, 6], dtype=np.int32)
    warmup_data_float = np.array([5.0, 2.0, 9.0, 1.0, 5.0, 6.0], dtype=np.float64)
    for _, func, _ in numba_algorithms:
        if func != linked_list_sort_wrapper:
            func(warmup_data_int.copy())
            func(warmup_data_float.copy())

    for dtype in ["int", "float", "string"]:
        use_numba = dtype in ["int", "float"]
        algorithms = numba_algorithms if use_numba else py_algorithms
        sizes = [30, 1000, 50000, 1000000] if use_numba else [30, 1000, 10000, 50000]
        max_quad = 20000 if use_numba else 5000
        
        for struct in structures:
            print(f"\nType: {dtype.upper()} | Structure: {struct.upper()} | Engine: {'Numba' if use_numba else 'Python Native'}")
            header_sizes = " | ".join([f"N={s:<17}" for s in sizes])
            print(f"{'Algorithm':<18} | {header_sizes}")
            print("-" * (21 + 20 * len(sizes)))

            datasets = {size: generate_dataset(size, struct, dtype, use_numpy=use_numba) for size in sizes}

            for name, func, is_quadratic in algorithms:
                results = []
                for size in sizes:
                    if is_quadratic and size > max_quad:
                        results.append("Skipped")
                        continue
                    
                    data_template = datasets[size]
                    
                    if size <= 50:
                        iterations = 10000 if use_numba else 2000
                        start_time = time.perf_counter()
                        for _ in range(iterations):
                            data = data_template.copy()
                            func(data)
                        end_time = time.perf_counter()
                        avg_time = (end_time - start_time) / iterations
                        results.append(f"{avg_time:.12f}s")
                    else:
                        data = data_template.copy()
                        start_time = time.perf_counter()
                        func(data)
                        end_time = time.perf_counter()
                        results.append(f"{end_time - start_time:.12f}s")
                
                row_results = " | ".join([f"{res:<17}" for res in results])
                print(f"{name:<18} | {row_results}")

if __name__ == "__main__":
    sys.setrecursionlimit(200000)
    run_performance_test()
