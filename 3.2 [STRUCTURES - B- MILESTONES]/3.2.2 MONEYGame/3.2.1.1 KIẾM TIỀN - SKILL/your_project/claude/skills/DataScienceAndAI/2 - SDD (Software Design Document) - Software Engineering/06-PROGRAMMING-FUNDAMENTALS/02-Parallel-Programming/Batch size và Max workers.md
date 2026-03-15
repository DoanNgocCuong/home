```python 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parallel Processing Module for Main Pipeline
===========================================

Features:
- Adaptive batch sizing based on data complexity
- Smart worker management with performance monitoring
- Thread-safe result collection
- Progress tracking and ETA calculation
- Error handling and retry mechanisms
- Memory usage optimization
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable, Optional
import psutil
import math

class ParallelProcessor:
    """
    Advanced parallel processor with adaptive optimization
    """
    
    def __init__(self, 
                 max_workers: Optional[int] = None,
                 batch_size: Optional[int] = None,
                 memory_limit_mb: int = 1024,
                 enable_adaptive: bool = True,
                 timeout_seconds: int = 300):
        """
        Initialize parallel processor
        
        Args:
            max_workers: Maximum number of worker threads (None = auto-detect)
            batch_size: Items per batch (None = auto-calculate)
            memory_limit_mb: Memory limit in MB
            enable_adaptive: Enable adaptive optimization
        """
        self.max_workers = max_workers or self._auto_detect_workers()
        self.batch_size = batch_size
        self.memory_limit_mb = memory_limit_mb
        self.enable_adaptive = enable_adaptive
        self.timeout_seconds = timeout_seconds
        
        # Performance tracking
        self.start_time = None
        self.completed_items = 0
        self.total_items = 0
        self.error_count = 0
        self.retry_count = 0
        
        # Thread safety
        self.lock = threading.Lock()
        self.results = []
        
        # Memory monitoring
        self.process = psutil.Process()
        
    def _auto_detect_workers(self) -> int:
        """Auto-detect optimal number of workers based on system"""
        cpu_count = psutil.cpu_count(logical=True)
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Conservative approach: don't overwhelm the system
        if memory_gb < 4:
            return min(2, cpu_count)
        elif memory_gb < 8:
            return min(4, cpu_count)
        else:
            return min(8, cpu_count)
    
    def _calculate_optimal_batch_size(self, total_items: int, avg_time_per_item: float = None) -> int:
        """Calculate optimal batch size based on data characteristics"""
        if self.batch_size:
            return self.batch_size
            
        # Adaptive batch sizing
        if self.enable_adaptive:
            # Estimate based on available memory
            available_memory_mb = psutil.virtual_memory().available / (1024**2)
            estimated_memory_per_item = 50  # MB per item (conservative estimate)
            
            memory_based_batch = max(1, int(available_memory_mb / estimated_memory_per_item))
            
            # Time-based optimization
            if avg_time_per_item:
                # Aim for batches that take 30-60 seconds to process
                target_batch_time = 45  # seconds
                time_based_batch = max(1, int(target_batch_time / avg_time_per_item))
            else:
                time_based_batch = 10
            
            # Worker-based optimization
            worker_based_batch = max(1, total_items // (self.max_workers * 2))
            
            # Take the minimum to be conservative
            optimal_batch = min(memory_based_batch, time_based_batch, worker_based_batch)
            
            return max(1, min(optimal_batch, 50))  # Between 1 and 50
        
        return 10  # Default fallback
    
    def _create_batches(self, items: List[Any], batch_size: int) -> List[List[Any]]:
        """Create batches from items list"""
        return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    
    def _monitor_memory(self) -> float:
        """Monitor current memory usage"""
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / (1024**2)
        return memory_mb
    
    def _should_pause_for_memory(self) -> bool:
        """Check if we should pause for memory management"""
        current_memory = self._monitor_memory()
        return current_memory > self.memory_limit_mb
    
    def process_parallel(self, 
                        items: List[Any], 
                        process_func: Callable,
                        progress_callback: Optional[Callable] = None,
                        **kwargs) -> List[Any]:
        """
        Process items in parallel with advanced optimization
        
        Args:
            items: List of items to process
            process_func: Function to process each batch
            progress_callback: Optional callback for progress updates
            **kwargs: Additional arguments for process_func
            
        Returns:
            List of results from all batches
        """
        self.total_items = len(items)
        self.completed_items = 0
        self.start_time = datetime.now()
        self.results = []
        
        if not items:
            return []
        
        # Calculate optimal batch size
        batch_size = self._calculate_optimal_batch_size(len(items))
        batches = self._create_batches(items, batch_size)
        
        print(f"🚀 Parallel Processing Setup:")
        print(f"   📊 Total items: {self.total_items}")
        print(f"   📦 Batch size: {batch_size}")
        print(f"   🧵 Max workers: {self.max_workers}")
        print(f"   📋 Total batches: {len(batches)}")
        print(f"   💾 Memory limit: {self.memory_limit_mb}MB")
        print(f"   🔧 Adaptive mode: {'✅' if self.enable_adaptive else '❌'}")
        
        # Process batches in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all batches - filter out timeout_seconds from kwargs
            process_kwargs = {k: v for k, v in kwargs.items() if k != 'timeout_seconds'}
            future_to_batch = {
                executor.submit(self._process_batch_with_retry, batch, process_func, **process_kwargs): batch
                for batch in batches
            }
            
            # Process completed batches with timeout
            for future in as_completed(future_to_batch):
                try:
                    # Add timeout to prevent hanging
                    batch_result = future.result(timeout=self.timeout_seconds)
                    with self.lock:
                        self.results.extend(batch_result)
                        self.completed_items += len(batch_result)
                    
                    # Progress update
                    if progress_callback:
                        progress_callback(self.completed_items, self.total_items)
                    
                    # Memory management
                    if self._should_pause_for_memory():
                        print(f"⚠️  High memory usage ({self._monitor_memory():.1f}MB), pausing...")
                        time.sleep(1)  # Brief pause
                    
                    # Performance monitoring
                    self._log_progress()
                    
                except TimeoutError:
                    self.error_count += 1
                    print(f"⏰ Batch processing timeout after {self.timeout_seconds}s, skipping...")
                    continue
                except Exception as e:
                    self.error_count += 1
                    print(f"❌ Batch processing error: {e}")
                    continue
        
        # Final summary
        self._log_final_summary()
        return self.results
    
    def _process_batch_with_retry(self, 
                                 batch: List[Any], 
                                 process_func: Callable,
                                 max_retries: int = 2,
                                 **kwargs) -> List[Any]:
        """Process a batch with retry mechanism"""
        for attempt in range(max_retries + 1):
            try:
                return process_func(batch, **kwargs)
            except Exception as e:
                if attempt < max_retries:
                    self.retry_count += 1
                    print(f"🔄 Retry {attempt + 1}/{max_retries} for batch due to: {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"💥 Batch failed after {max_retries} retries: {e}")
                    return []  # Return empty result for failed batch
    
    def _log_progress(self):
        """Log current progress with ETA"""
        if self.completed_items == 0:
            return
            
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        avg_time_per_item = elapsed_time / self.completed_items
        remaining_items = self.total_items - self.completed_items
        estimated_remaining_time = avg_time_per_item * remaining_items
        
        progress_percent = (self.completed_items / self.total_items) * 100
        eta = datetime.now() + timedelta(seconds=estimated_remaining_time)
        
        memory_usage = self._monitor_memory()
        
        print(f"📊 Progress: {self.completed_items}/{self.total_items} ({progress_percent:.1f}%)")
        print(f"   ⏱️  Elapsed: {elapsed_time/60:.1f}min | ETA: {eta.strftime('%H:%M:%S')}")
        print(f"   🚀 Speed: {avg_time_per_item:.1f}s/item | 💾 Memory: {memory_usage:.1f}MB")
        print(f"   ❌ Errors: {self.error_count} | 🔄 Retries: {self.retry_count}")
    
    def _log_final_summary(self):
        """Log final processing summary"""
        total_time = (datetime.now() - self.start_time).total_seconds()
        success_rate = ((self.total_items - self.error_count) / self.total_items) * 100
        
        print(f"\n🎉 Parallel Processing Complete!")
        print(f"   ⏱️  Total time: {total_time/60:.1f} minutes")
        print(f"   📊 Success rate: {success_rate:.1f}%")
        print(f"   ❌ Errors: {self.error_count}")
        print(f"   🔄 Retries: {self.retry_count}")
        print(f"   💾 Peak memory: {self._monitor_memory():.1f}MB")
        
        if self.total_items > 0:
            throughput = self.total_items / total_time
            print(f"   🚀 Throughput: {throughput:.2f} items/second")


# Convenience functions for easy integration
def process_situations_parallel(situations: List[Dict], 
                               process_func: Callable,
                               max_workers: int = None,
                               batch_size: int = None,
                               timeout_seconds: int = 300,
                               **kwargs) -> List[Dict]:
    """
    Convenience function to process situations in parallel
    
    Args:
        situations: List of situation dictionaries
        process_func: Function to process each situation
        max_workers: Maximum worker threads
        batch_size: Items per batch
        **kwargs: Additional arguments for process_func
        
    Returns:
        List of processed results
    """
    processor = ParallelProcessor(
        max_workers=max_workers,
        batch_size=batch_size,
        enable_adaptive=True
    )
    
    def progress_callback(completed, total):
        if completed % 10 == 0:  # Update every 10 items
            print(f"🔄 Processed {completed}/{total} situations...")
    
    return processor.process_parallel(
        items=situations,
        process_func=process_func,
        progress_callback=progress_callback,
        timeout_seconds=timeout_seconds,
        **kwargs
    )


if __name__ == "__main__":
    # Demo usage
    def demo_process_func(batch, **kwargs):
        """Demo processing function"""
        time.sleep(0.1)  # Simulate work
        return [f"Processed: {item}" for item in batch]
    
    # Test data
    test_items = list(range(100))
    
    print("🧪 Testing Parallel Processor...")
    processor = ParallelProcessor(max_workers=4, batch_size=10)
    results = processor.process_parallel(test_items, demo_process_func)
    
    print(f"✅ Demo completed with {len(results)} results")
```


|Tiêu chí|max_workers|batch_size|
|---|---|---|
|Định nghĩa|Số lượng luồng (thread) hoặc tiến trình (process) chạy song song cùng lúc|Số lượng dữ liệu (item) xử lý trong mỗi lượt của một worker|
|Vai trò|Tăng độ song song (parallelism cấp hệ thống)|Tối ưu hiệu năng, memory trong từng lượt xử lý của worker|
|Tác động|Ảnh hưởng tốc độ toàn pipeline và mức tiêu thụ CPU/RAM|Ảnh hưởng hiệu quả từng worker, mức tiêu thụ RAM từng batch|
|Giới hạn cấu hình|Bị giới hạn bởi số nhân CPU và tổng RAM hệ thống|Bị giới hạn bởi dung lượng RAM từng worker và khả năng xử lý lỗi|
|Ví dụ giá trị|4, 8, 16, 32|10, 20, 50, 100|
|Ảnh hưởng khi tăng|Xử lý nhanh hơn, chiếm nhiều tài nguyên hệ thống hơn, dễ quá tải nếu quá cao|Mỗi worker xử lý nhanh hơn/lớn hơn mỗi lượt, nhưng dễ lỗi, timeout, ngốn nhiều RAM hơn|
|Ứng dụng thực tế|Thiết lập song song tối ưu cho server mạnh hoặc dữ liệu lớn lâu|Chia batch nhỏ dễ retry, ngốn ít RAM (phù hợp dữ liệu siêu lớn hoặc nhiều lỗi)|
|Tối ưu hóa cùng nhau|Chọn max_workers dựa trên CPU/RAM tổng, tùy chỉnh batch_size nhỏ/lớn tối ưu memory, tốc độ|Tăng cả hai giúp hệ thống xử lý cực nhanh nếu cân đối tài nguyên|
|Hệ quả khi sai cấu hình|max_workers quá lớn khiến RAM/cpu cạn kiệt, hệ thống treo|batch_size quá lớn khiến worker dễ bị lỗi out-of-memory, timeout|
|Thông số trong module|max_workers:ThreadPoolExecutor(max_workers=...)|batch_size: chia nhỏ dữ liệu truyền vào mỗi worker|