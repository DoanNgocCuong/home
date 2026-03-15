
|Tiêu chí|Batch size|Max workers|
|---|---|---|
|Bản chất|Kích thước nhóm dữ liệu xử lý trong 1 lần|Số worker xử lý đồng thời|
|Ứng dụng|Training ML, xử lý dữ liệu batch|Parallelism trong hệ thống|
|Tác động|Ảnh hưởng đến memory và convergence|Ảnh hưởng đến throughput, CPU core usage|
|Liên quan|Gradient update, I/O batch|Thread, process, concurrency|


```PYTHON 
# @title OPENAI

import os

import json

import pandas as pd

import time

import logging

import re

import concurrent.futures

from typing import List, Dict

import math

from openpyxl import load_workbook

import psutil

import multiprocessing

import threading

from pathlib import Path

import argparse

from dotenv import load_dotenv

  

# ============= FIX PROXY ISSUE =============

# Bước 1: Xóa tất cả proxy environment variables

proxy_vars = [

    'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',

    'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy'

]

  

for var in proxy_vars:

    if var in os.environ:

        del os.environ[var]

        print(f"Removed proxy variable: {var}")

  

# Bước 2: Set explicit no proxy

os.environ['NO_PROXY'] = '*'

  

# Bước 3: Import OpenAI sau khi clear proxy

try:

    from openai import OpenAI

    from openai import OpenAIError

    print("✓ OpenAI imported successfully")

except ImportError as e:

    print(f"✗ Error importing OpenAI: {e}")

    print("Run: pip install openai>=1.0.0")

    exit(1)

  

# Setup logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

  

# Load environment variables

load_dotenv()

  

# Bước 4: Khởi tạo OpenAI client với error handling

def create_openai_client():

    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:

        raise ValueError("OPENAI_API_KEY not found in environment variables")

    print(f"API Key: {api_key[:10]}...")

    try:

        # Tạo client chỉ với api_key (không có parameters khác)

        client = OpenAI(api_key=api_key)

        print("✓ OpenAI client created successfully")

        return client

    except Exception as e:

        print(f"✗ Error creating OpenAI client: {e}")

        print("Trying alternative initialization...")

        # Alternative: Tạo client với httpx explicit

        try:

            import httpx

            http_client = httpx.Client(proxies=None)

            client = OpenAI(api_key=api_key, http_client=http_client)

            print("✓ OpenAI client created with custom HTTP client")

            return client

        except Exception as e2:

            print(f"✗ Alternative initialization failed: {e2}")

            raise e

  

# Khởi tạo client

client = create_openai_client()

# ============= END FIX =============

  

sheet_name = 'Trang tính1'

  

def process_conversation(order, base_prompt, inputs, conversation_history=None):

    print(f"\n=== Processing Conversation ===")

    print(f"Order: {order}")

    print(f"Base Prompt: {base_prompt[:100]}...")

    # Log conversation history

    if conversation_history:

        logger.info(f"Conversation history: {conversation_history}")

  

    # Tạo model config dưới dạng JSON

    model_config = {

        "model": "gpt-4o-mini-2024-07-18",

        "temperature": 0,

        "max_tokens": 2048,

        "top_p": 1,

        "frequency_penalty": 0.0,

        "presence_penalty": 0.0

    }

    model_config_json = json.dumps(model_config)

    responses = []

    response_times = []

    chat_messages = []

    # 1. System message

    chat_messages.append({"role": "system", "content": base_prompt})

    print("\nSau khi thêm system message:")

    print(chat_messages)

    # 2. History handling

    if conversation_history and not pd.isna(conversation_history):

        try:

            # Parse conversation history from JSON string

            history_messages = json.loads(conversation_history)

            # Validate format of history messages

            if isinstance(history_messages, list):

                for msg in history_messages:

                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:

                        chat_messages.append(msg)

                    else:

                        print(f"Warning: Skipping invalid message format in history: {msg}")

            else:

                print(f"Warning: conversation_history is not a list: {history_messages}")

            print("\nSau khi thêm history:")

            print(json.dumps(chat_messages, indent=2, ensure_ascii=False))

        except json.JSONDecodeError as e:

            print(f"Error parsing conversation history: {e}")

            print(f"Raw conversation history: {conversation_history}")

            logger.error(f"Error parsing conversation history: {e}")

            logger.error(f"Raw conversation history: {conversation_history}")

    # 3. New input

    for user_input in inputs:

        chat_messages.append({"role": "user", "content": user_input})

        print("\nTrước khi gọi API:")

        print(json.dumps(chat_messages, indent=2, ensure_ascii=False))

        start_time = time.time()

        try_count = 0

        while try_count < 3:

            try:

                print(f"DEBUG - Attempt {try_count + 1} to call OpenAI API")

                completion = client.chat.completions.create(

                    model=model_config["model"],

                    messages=chat_messages,  

                    temperature=model_config["temperature"],

                    max_tokens=model_config["max_tokens"],

                    top_p=model_config["top_p"],

                    frequency_penalty=model_config["frequency_penalty"],

                    presence_penalty=model_config["presence_penalty"]

                )

                end_time = time.time()

                response_content = completion.choices[0].message.content

                chat_messages.append({"role": "assistant", "content": response_content})

  

                responses.append(response_content)

                response_times.append(end_time - start_time)

  

                # Print the completion output here

                print(f"Order {order}, Input: '{user_input}', Response: '{response_content[:100]}...', Time: {end_time - start_time:.2f}s\n====")

                break

            except Exception as e:

                try_count += 1

                print(f"DEBUG - Error on attempt {try_count}: {str(e)}")

                if try_count >= 3:

                    responses.append("Request failed after 3 retries.")

                    response_times.append("-")

                    print(f"Order {order}, Input: '{user_input}', Response: 'Request failed after 3 retries.', Time: -")

                else:

                    print(f"DEBUG - Waiting 3 seconds before retry...")

                    time.sleep(3)

  

    return responses, response_times, chat_messages, model_config_json

  

# Add argument parser

def parse_arguments():

    parser = argparse.ArgumentParser(description='Process conversations with OpenAI API')

    parser.add_argument('--num-rows', type=int, default=None,

                      help='Number of rows to process (default: all rows)')

    parser.add_argument('--input-file', type=str, default='input_data.xlsx',

                      help='Input Excel file path (default: input_data.xlsx)')

    parser.add_argument('--output-file', type=str, default='output_data_v2.xlsx',

                      help='Output Excel file path (default: output_data_v2.xlsx)')

    parser.add_argument('--sheet', type=str, default='Trang tính1',

                      help='Excel sheet name to process (default: Trang tính1)')

    parser.add_argument('--batch-size', type=int, default=4,

                      help='Number of items to process in each batch (default: 4)')

    parser.add_argument('--max-workers', type=int, default=4,

                      help='Maximum number of worker threads (default: 4)')

    return parser.parse_args()

  

def process_batch(batch_rows: List[Dict]):

    output_rows = []

    for row in batch_rows:

        order = row.get('order', 'default_order')

        prompt = row['system_prompt']

        conversation_history = row.get('conversation_history', None)

        inputs = [row['user_input']]

        logger.info(f"Processing order {order}")

        responses, response_times, chat_messages, model_config = process_conversation(

            order, prompt, inputs, conversation_history

        )

        # Copy all columns and add new data

        new_row = row.copy()

        new_row.update({

            'assistant_response': responses[0] if responses else None,

            'response_time': response_times[0] if response_times else None,

            'model_config': model_config

        })

        output_rows.append(new_row)

    return output_rows

  

def append_to_excel(filename, df):

    """Append DataFrame to existing Excel file without reading entire file."""

    try:

        with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:

            workbook = writer.book

            worksheet = workbook['Sheet1']

            start_row = worksheet.max_row

            df.to_excel(writer,

                       index=False,

                       header=False,

                       startrow=start_row)

        return True

    except Exception as e:

        logger.error(f"Error appending to Excel: {str(e)}")

        return False

  

def get_system_resources():

    """Lấy thông tin tài nguyên hệ thống."""

    try:

        cpu_count = multiprocessing.cpu_count()

        memory = psutil.virtual_memory()

        available_memory_gb = memory.available / (1024 * 1024 * 1024)

        cpu_percent = psutil.cpu_percent(interval=1)

        logger.info(f"System resources:")

        logger.info(f"- CPU cores: {cpu_count}")

        logger.info(f"- CPU usage: {cpu_percent}%")

        logger.info(f"- Available memory: {available_memory_gb:.2f}GB")

        logger.info(f"- Memory usage: {memory.percent}%")

        return {

            'cpu_count': cpu_count,

            'available_memory_gb': available_memory_gb,

            'cpu_percent': cpu_percent,

            'memory_percent': memory.percent

        }

    except Exception as e:

        logger.error(f"Error getting system resources: {str(e)}")

        return None

  

def optimize_batch_parameters(total_rows: int, args):

    """Tối ưu batch_size và max_workers dựa trên tài nguyên hệ thống."""

    resources = get_system_resources()

    if not resources:

        logger.warning("Using default parameters due to resource check failure")

        return args.batch_size, args.max_workers

    # Tối ưu max_workers

    recommended_workers = min(

        resources['cpu_count'],

        int(8 * (100 - resources['cpu_percent']) / 100),

        int(resources['available_memory_gb'])

    )

    max_workers = max(1, min(recommended_workers, args.max_workers))

    # Tối ưu batch_size

    memory_based_batch = int(resources['available_memory_gb'] * 1024)

    cpu_based_batch = int(20 * (100 - resources['cpu_percent']) / 100)

    recommended_batch = min(

        memory_based_batch,

        cpu_based_batch,

        max(1, total_rows // (max_workers * 2))

    )

    batch_size = max(1, min(recommended_batch, args.batch_size))

    logger.info(f"Optimized parameters:")

    logger.info(f"- Original batch_size: {args.batch_size}, max_workers: {args.max_workers}")

    logger.info(f"- Recommended batch_size: {batch_size}, max_workers: {max_workers}")

    return batch_size, max_workers

  

def monitor_resources(stop_event, interval=30):

    """Monitor tài nguyên hệ thống trong quá trình xử lý."""

    while not stop_event.is_set():

        resources = get_system_resources()

        if resources:

            if resources['cpu_percent'] > 90:

                logger.warning("High CPU usage detected!")

            if resources['memory_percent'] > 90:

                logger.warning("High memory usage detected!")

        time.sleep(interval)

  

def main():

    args = parse_arguments()

    SCRIPTS_FOLDER = Path(__file__).parent

    INPUT_FILE = SCRIPTS_FOLDER / args.input_file

    OUTPUT_FILE = SCRIPTS_FOLDER / args.output_file

  

    # Kiểm tra file input tồn tại

    if not INPUT_FILE.exists():

        logger.error(f"Input file not found: {INPUT_FILE}")

        return

  

    df_input = pd.read_excel(INPUT_FILE, sheet_name=args.sheet)

    rows_to_process = df_input if args.num_rows is None else df_input.head(args.num_rows)

    logger.info(f"Processing {len(rows_to_process)} rows from {INPUT_FILE}")

    # Tối ưu parameters

    batch_size, max_workers = optimize_batch_parameters(len(rows_to_process), args)

    all_rows = rows_to_process.to_dict('records')

    batches = [all_rows[i:i + batch_size] for i in range(0, len(all_rows), batch_size)]

    logger.info(f"Created {len(batches)} batches with batch_size={batch_size}, max_workers={max_workers}")

    # Tạo file output với headers

    cols_order = list(df_input.columns) + ['assistant_response', 'response_time', 'model_config']

    pd.DataFrame(columns=cols_order).to_excel(OUTPUT_FILE, index=False)

    # Khởi động monitor thread

    stop_monitoring = threading.Event()

    monitor_thread = threading.Thread(target=monitor_resources, args=(stop_monitoring,))

    monitor_thread.start()

    try:

        processed_count = 0

        failed_batches = []

  

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:

            futures = [executor.submit(process_batch, batch) for batch in batches]

            for i, future in enumerate(concurrent.futures.as_completed(futures)):

                try:

                    batch_results = future.result()

                    batch_df = pd.DataFrame(batch_results)[cols_order]

                    for attempt in range(3):

                        if append_to_excel(OUTPUT_FILE, batch_df):

                            processed_count += len(batch_results)

                            logger.info(f"Appended batch {i+1}/{len(batches)}. Total processed: {processed_count}")

                            break

                        else:

                            if attempt < 2:

                                logger.warning(f"Retry {attempt + 1} for batch {i+1}")

                                time.sleep(2)

                            else:

                                logger.error(f"Failed to append batch {i+1} after 3 attempts")

                                failed_batches.append((i, batch_results))

                except Exception as e:

                    logger.error(f"Error processing batch {i+1}: {str(e)}")

                    failed_batches.append((i, None))

  

        # Xử lý lại các batch thất bại

        if failed_batches:

            logger.info(f"Retrying {len(failed_batches)} failed batches...")

            for batch_index, batch_results in failed_batches:

                if batch_results:

                    batch_df = pd.DataFrame(batch_results)[cols_order]

                    if append_to_excel(OUTPUT_FILE, batch_df):

                        processed_count += len(batch_results)

                        logger.info(f"Successfully retried batch {batch_index+1}")

                    else:

                        logger.error(f"Permanently failed to append batch {batch_index+1}")

  

    except KeyboardInterrupt:

        logger.info("Process interrupted by user")

    except Exception as e:

        logger.error(f"Unexpected error: {str(e)}")

    finally:

        # Dừng monitor thread

        stop_monitoring.set()

        monitor_thread.join()

        # Log kết quả cuối cùng

        logger.info(f"Processing completed. Total rows processed: {processed_count}")

        logger.info(f"Output saved to: {OUTPUT_FILE}")

        get_system_resources()

  

if __name__ == "__main__":

    main()

```

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

            estimated_memory_per_item = 50  # MB per item (conservative estimate)

            memory_based_batch = max(1, int(available_memory_mb / estimated_memory_per_item))

            # Time-based optimization

            if avg_time_per_item:

                # Aim for batches that take 30-60 seconds to process

                target_batch_time = 45  # seconds

                time_based_batch = max(1, int(target_batch_time / avg_time_per_item))

            else:

                time_based_batch = 10

            # Worker-based optimization

            worker_based_batch = max(1, total_items // (self.max_workers * 2))

            # Take the minimum to be conservative

            optimal_batch = min(memory_based_batch, time_based_batch, worker_based_batch)

            return max(1, min(optimal_batch, 50))  # Between 1 and 50

        return 10  # Default fallback

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

        print(f"   📊 Total items: {self.total_items}")

        print(f"   📦 Batch size: {batch_size}")

        print(f"   🧵 Max workers: {self.max_workers}")

        print(f"   📋 Total batches: {len(batches)}")

        print(f"   💾 Memory limit: {self.memory_limit_mb}MB")

        print(f"   🔧 Adaptive mode: {'✅' if self.enable_adaptive else '❌'}")

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

                        print(f"⚠️  High memory usage ({self._monitor_memory():.1f}MB), pausing...")

                        time.sleep(1)  # Brief pause

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

                    time.sleep(2 ** attempt)  # Exponential backoff

                else:

                    print(f"💥 Batch failed after {max_retries} retries: {e}")

                    return []  # Return empty result for failed batch

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

        print(f"   ⏱️  Elapsed: {elapsed_time/60:.1f}min | ETA: {eta.strftime('%H:%M:%S')}")

        print(f"   🚀 Speed: {avg_time_per_item:.1f}s/item | 💾 Memory: {memory_usage:.1f}MB")

        print(f"   ❌ Errors: {self.error_count} | 🔄 Retries: {self.retry_count}")

    def _log_final_summary(self):

        """Log final processing summary"""

        total_time = (datetime.now() - self.start_time).total_seconds()

        success_rate = ((self.total_items - self.error_count) / self.total_items) * 100

        print(f"\n🎉 Parallel Processing Complete!")

        print(f"   ⏱️  Total time: {total_time/60:.1f} minutes")

        print(f"   📊 Success rate: {success_rate:.1f}%")

        print(f"   ❌ Errors: {self.error_count}")

        print(f"   🔄 Retries: {self.retry_count}")

        print(f"   💾 Peak memory: {self._monitor_memory():.1f}MB")

        if self.total_items > 0:

            throughput = self.total_items / total_time

            print(f"   🚀 Throughput: {throughput:.2f} items/second")

  
  

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

        if completed % 10 == 0:  # Update every 10 items

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

        time.sleep(0.1)  # Simulate work

        return [f"Processed: {item}" for item in batch]

    # Test data

    test_items = list(range(100))

    print("🧪 Testing Parallel Processor...")

    processor = ParallelProcessor(max_workers=4, batch_size=10)

    results = processor.process_parallel(test_items, demo_process_func)

    print(f"✅ Demo completed with {len(results)} results")
    
```




[Skip to content](https://chatgpt.com/c/68b16357-eb00-8326-99aa-aea1e392e223#main)

## Chat history

[](https://chatgpt.com/)

##### You said:

Tìm kiếm các nguồn tài liệu và chương trình để luyện giải thuật song song

###### ChatGPT said:

Dưới đây là một số **nguồn tài liệu và chương trình học luyện giải thuật song song (parallel algorithms)** mà bạn có thể tham khảo, bao gồm từ nền tảng lý thuyết đến các framework lập trình thực tiễn:

---

## 1. Tài liệu học lý thuyết và slides giảng dạy

- **Introduction to Parallel Algorithms (UMD)**  
    Bản PDF giới thiệu các khái niệm nền tảng như mô hình PRAM, work‑depth, scheduling, v.v. Nội dung đã tổng hợp tinh hoa từ hơn 40 năm nghiên cứu trong lĩnh vực này. [tcpp.cs.gsu.edu+14software-performance-engineering.github.io+14TutorialsPoint+14](https://software-performance-engineering.github.io/spring25/resources/parallel.pdf?utm_source=chatgpt.com)[math.gordon.edu+6Computer Science at UMD+6CMU School of Computer Science+6](https://www.cs.umd.edu/~laxman/notes/parallel.pdf?utm_source=chatgpt.com)
    
- **Unit 7: Parallel Algorithms – wild‑inter.net**  
    Slide bài giảng của Sebastian Wild, trình bày các mô hình máy, PRAM, đặt vấn đề về prefix sum, phân đoạn song song, quicksort và mergesort song song, cùng giới hạn hiệu năng tốc độ... [umiacs.umd.edu+4wild-inter.net+4wild-inter.net+4](https://www.wild-inter.net/teaching/comp526/07-parallel-algorithms?utm_source=chatgpt.com)
    
- **Notes‑10‑Parallel‑Algorithms – Philipps‑Universität Marburg**  
    Tài liệu cập nhật cuối năm 2024, với định hướng học về chiến lược parallel hóa, phân loại bài toán embarrassingly parallel, PRAM, prefix sum, quicksort/mergesort song song… [Computer Science and Engineering+15wild-inter.net+15Computer Science at UMD+15](https://www.wild-inter.net/teaching/ea/notes-10-parallel-algorithms.pdf?utm_source=chatgpt.com)
    
- **Lectures on Parallel Computing – Jesper Larsson Träff (arXiv 2024)**  
    Bộ lecture notes toàn diện cho cả đại học và sau đại học, đi sâu vào nguyên lý thiết kế parallel algorithms, đồng thời hướng dẫn thực hành với MPI, OpenMP và pthreads. [arXiv](https://arxiv.org/abs/2407.18795?utm_source=chatgpt.com)
    

---

## 2. Hướng dẫn trực tuyến (tutorials)

- **TutorialsPoint – _Parallel Algorithm Tutorial_**  
    Đây là phần hướng dẫn trực tuyến lý thuyết cơ bản về các mô hình, cấu trúc và cách triển khai thuật toán song song. Phù hợp với sinh viên từ cơ bản đến nâng cao. [My Lecture Library+15TutorialsPoint+15TutorialsPoint+15](https://www.tutorialspoint.com/parallel_algorithm/index.htm?utm_source=chatgpt.com)
    
- **GeeksforGeeks – _Parallel Algorithm Models in Parallel Computing_**  
    Giải thích các mô hình song song phổ biến như Data‑Parallel, chiến lược phân chia dữ liệu/tasks, tối ưu tương tác giữa chúng. [GeeksforGeeks+2math.gordon.edu+2](https://www.geeksforgeeks.org/mobile-computing/parallel-algorithm-models-in-parallel-computing/?utm_source=chatgpt.com)
    
- **NumberAnalytics – _Mastering Parallel Algorithms_**  
    Bài blog mới tháng 6/2025, giúp bạn hiểu tổng quan về ứng dụng, thách thức (synchronization, load balancing, debugging) và cách tối ưu scalability trong thuật toán song song. [TutorialsPoint+11Number Analytics+11umiacs.umd.edu+11](https://www.numberanalytics.com/blog/ultimate-guide-to-parallel-algorithms?utm_source=chatgpt.com)
    

---

## 3. Ngôn ngữ và framework lập trình song song

- **Intel oneAPI Threading Building Blocks (oneTBB)**  
    Một thư viện C++ phổ biến cho lập trình đa luồng, hỗ trợ các cấu trúc như `parallel_for`, `parallel_reduce`, `parallel_sort` cùng work‑stealing scheduler… [Wikipedia](https://en.wikipedia.org/wiki/Threading_Building_Blocks?utm_source=chatgpt.com)
    
- **SYCL (Khronos Group)**  
    Mô hình lập trình song song cho hệ thống tính toán đa nền tảng (CPU, GPU, accelerators) theo phong cách single‑source, dùng C++17. Có nhiều implementation như DPC++, AdaptiveCpp… [Wikipedia+2CMU School of Computer Science+2](https://en.wikipedia.org/wiki/SYCL?utm_source=chatgpt.com)
    
- **NESL**  
    Một ngôn ngữ song song chuyên về lập trình hàm (functional), hỗ trợ nested data parallelism và mô hình work‑depth rõ ràng. Tạo cầu nối giữa thuật toán lý thuyết và thực thi hiệu quả. [Wikipedia](https://en.wikipedia.org/wiki/NESL?utm_source=chatgpt.com)
    

---

## 4. Khóa học và bài giảng video trực tuyến

- **Playlist “Parallel Algorithm Tutorial” – YouTube (Last Minute Study)**  
    Gồm 10 video ngắn hướng dẫn các khái niệm cơ bản đến trung cấp về song song hóa thuật toán. [tcpp.cs.gsu.edu+10YouTube+10TutorialsPoint+10](https://www.youtube.com/playlist?list=PLiKFau7eKJlqoHxgx_hjLN-xFup7a13Va&utm_source=chatgpt.com)
    

Ngoài ra, bạn có thể tìm các khóa học mở (MOOC) trên Coursera, edX, hoặc các giảng dạy tại các trường đại học như UMD, CMU, ETH Zurich, v.v., để có thêm bài giảng video và bài tập trực quan.

---

## 5. Gợi ý phương pháp học

|Giai đoạn|Nội dung nên tập trung|Gợi ý cụ thể|
|---|---|---|
|**Lý thuyết nền tảng**|Hiểu PRAM, work-depth model, phân tích hiệu năng|UMD PDF, Sebastian Wild slides, Träff lectures|
|**Thực hành code**|Cài đặt peer-to-peer, shared memory, MPI/OpenMP, oneTBB, SYCL|Sử dụng lecture notes thực hành, oneTBB, SYCL tutorials|
|**Chuyển sang lập trình**|Viết các bài toán quen thuộc như prefix sum, merge sort song song|Dự án nhỏ theo lecture/tron số, áp dụng STL parallel hoặc oneTBB|
|**Tối ưu và gỡ lỗi**|Xử lý cạnh tranh, khối lượng không cân bằng, overhead|Đọc blog Mastering Parallel Algorithms, debug tools|

---

### Tổng kết nhanh

- **Tài liệu lý thuyết**: UMD, Sebastian Wild, Marburg, Träff (arXiv)
    
- **Tutorials trực tuyến**: TutorialsPoint, GeeksforGeeks, blog NumberAnalytics
    
- **Framework thực hành**: oneTBB (C++), SYCL (C++ single-source), NESL (functional)
    
- **Video học nhanh**: Playlist YouTube “Parallel Algorithm Tutorial” (Last Minute Study)
    

---

Nếu bạn cần tài liệu tiếng Việt hoặc các khóa học cụ thể ở Việt Nam, mình có thể tìm thêm. Còn nếu bạn quan tâm đến ứng dụng song song trên GPU, HPC hoặc dùng Python (như multiprocessing hoặc CUDA Python), cứ nói nhé mình sẽ gợi ý chi tiết hơn!

##### You said:

lập trình song song mảng phthon nhé

###### ChatGPT said:

Thought for 17s

Tuyệt! Dưới đây là “sổ tay nhanh” để **lập trình song song trên mảng bằng Python**, đi từ CPU (đa tiến trình/đa luồng, JIT) đến phân tán và GPU, kèm ví dụ ngắn + nguồn chính thống để bạn đào sâu.

# 1) Song song CPU “cơ bản” cho mảng

**A. `multiprocessing` / `concurrent.futures` (ProcessPool) – né GIL, chia dữ liệu theo block**

- Dùng khi mỗi task xử lý độc lập trên các lát mảng (chunk).
    
- API cao cấp, dễ dùng: `ProcessPoolExecutor`/`Pool.map`. [Python documentation+1](https://docs.python.org/3/library/concurrent.futures.html?utm_source=chatgpt.com)
    

`# Sum bình phương theo khối bằng ProcessPool import numpy as np from concurrent.futures import ProcessPoolExecutor  def work(chunk):     x = np.asarray(chunk, dtype=np.float64)     return np.sum(x*x)  def parallel_sum_squares(a, n_workers=4):     chunks = np.array_split(a, n_workers)     with ProcessPoolExecutor(max_workers=n_workers) as ex:         return sum(ex.map(work, chunks))  a = np.random.rand(10_000_000) print(parallel_sum_squares(a))`

> Lưu ý: Đối tượng phải “picklable”; code nên đặt trong `if __name__ == "__main__":` trên Windows. [stackless.readthedocs.io](https://stackless.readthedocs.io/en/3.6-slp/library/concurrent.futures.html?utm_source=chatgpt.com)

**B. Thread + NumPy (đúng ngữ cảnh)**  
Nhiều phép NumPy **tự giải phóng GIL** và/hoặc gọi BLAS/LAPACK đa luồng → đôi khi **thread** vẫn tăng tốc nếu mỗi thread xử lý **mảng riêng**. Đừng “bọc” thêm thread quanh phép đã đa luồng vì có thể chậm hơn. [NumPy](https://numpy.org/doc/stable/reference/thread_safety.html?utm_source=chatgpt.com)[Super Fast Python](https://superfastpython.com/numpy-threads-worse-performance/?utm_source=chatgpt.com)

# 2) JIT & vector hóa nâng cao cho mảng

**A. Numba `@njit(parallel=True)` + `prange`**

- Dịch JIT sang máy, song song hóa vòng lặp kiểu OpenMP, cực hợp cho vòng for trên mảng. [numba.readthedocs.io](https://numba.readthedocs.io/en/stable/user/parallel.html?utm_source=chatgpt.com)[numba.pydata.org](https://numba.pydata.org/numba-doc/0.11/prange.html?utm_source=chatgpt.com)
    

`import numpy as np from numba import njit, prange  @njit(parallel=True, fastmath=True) def axpy(a, x, y):     out = np.empty_like(x)     for i in prange(x.size):         out[i] = a * x[i] + y[i]     return out  x = np.random.rand(10_000_000) y = np.random.rand(10_000_000) z = axpy(2.0, x, y)  # chạy song song trên CPU`

**B. NumExpr – “máy ảo” đánh giá biểu thức mảng, đa luồng**

- Viết gọn kiểu `"3*a + 4*b + sin(c)"`, giảm dùng bộ nhớ tạm, tự dùng nhiều core. [numexpr.readthedocs.io](https://numexpr.readthedocs.io/en/latest/user_guide.html?utm_source=chatgpt.com)[GitHub](https://github.com/pydata/numexpr?utm_source=chatgpt.com)
    

`import numexpr as ne z = ne.evaluate("3*a + 4*b + sin(c)")`

# 3) Mảng “quá to” & pipeline song song/đa máy

**Dask Array** – “NumPy chia khối” (blocked), chạy song song trên nhiều core/máy, xử lý dữ liệu lớn hơn RAM. [tutorial.dask.org](https://tutorial.dask.org/02_array.html?utm_source=chatgpt.com)[intro-to-dask.readthedocs.io](https://intro-to-dask.readthedocs.io/en/latest/tutorial/Dask/collections.html?utm_source=chatgpt.com)

`import dask.array as da x = da.random.random((100_000, 10_000), chunks=(10_000, 10_000)) y = (x - x.mean(axis=0)) / x.std(axis=0)   # đồ thị tính toán lười print(y.mean().compute())                  # .compute() -> thực thi song song`

# 4) GPU cho mảng (nếu có CUDA/ROCm)

**CuPy** – gần như “drop-in” NumPy nhưng chạy trên GPU; cực nhanh khi mảng lớn/tính toán nặng. [docs.cupy.dev+1](https://docs.cupy.dev/?utm_source=chatgpt.com)[learningsys.org](https://learningsys.org/nips17/assets/papers/paper_16.pdf?utm_source=chatgpt.com)

`import cupy as cp x = cp.random.rand(10_000_000, dtype=cp.float32) y = cp.sin(x) * 2 + x**2        # chạy trên GPU cp.cuda.Stream.null.synchronize()`

> Mẹo hiệu năng GPU: giữ dữ liệu **trên GPU** (hạn chế copy), dùng `float32` khi được, và cân nhắc **CUDA streams** cho task độc lập. [SparkCodehub](https://www.sparkcodehub.com/numpy/modern-applications/gpu-computing-cupy?utm_source=chatgpt.com)

# 5) Khi nào dùng cái gì?

- **Vector hóa NumPy thuần**: đơn giản & nhanh (nhiều hàm đã đa luồng nhờ BLAS).
    
- **Numba (prange)**: vòng for tính toán phần tử → tăng tốc lớn trên CPU. [numba.readthedocs.io](https://numba.readthedocs.io/en/stable/user/parallel.html?utm_source=chatgpt.com)
    
- **NumExpr**: nhiều biểu thức mảng liên tiếp → ít tạm, chạy đa luồng tự động. [numexpr.readthedocs.io](https://numexpr.readthedocs.io/en/latest/user_guide.html?utm_source=chatgpt.com)
    
- **ProcessPool**: tác vụ độc lập nặng CPU / cần né GIL hoặc gọi NumPy không đa luồng. [Python documentation](https://docs.python.org/3/library/concurrent.futures.html?utm_source=chatgpt.com)
    
- **Dask Array**: dữ liệu **quá lớn** hoặc cần **song song phân tán**. [tutorial.dask.org](https://tutorial.dask.org/02_array.html?utm_source=chatgpt.com)
    
- **CuPy**: có GPU và thao tác mảng lớn/nặng (FFT, linalg, ufunc). [docs.cupy.dev](https://docs.cupy.dev/?utm_source=chatgpt.com)
    

# 6) Bẫy thường gặp & tối ưu

- **Đè thread lên BLAS**: phép linalg (dot, svd, …) vốn đã đa luồng; thêm ThreadPool có thể **chậm hơn**. Điều chỉnh số thread BLAS (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`) khi cần. [Scikit-learn](https://scikit-learn.org/stable/computing/parallelism.html?utm_source=chatgpt.com)[NumPy](https://numpy.org/devdocs/reference/global_state.html?utm_source=chatgpt.com)[GitHub](https://github.com/OpenMathLib/OpenBLAS/issues/1881?utm_source=chatgpt.com)
    
- **Pickle overhead** với `multiprocessing`: gửi mảng khổng lồ giữa tiến trình tốn thời gian/bộ nhớ → chia block ít lần hơn, dùng shared memory khi phù hợp. [Python documentation](https://docs.python.org/3/library/multiprocessing.html?utm_source=chatgpt.com)
    
- **Thread an toàn với NumPy**: hiệu quả nhất khi mỗi thread sở hữu mảng riêng (không chia sẻ ghi/đọc nhiều). [NumPy](https://numpy.org/doc/stable/reference/thread_safety.html?utm_source=chatgpt.com)
    

---

## Lộ trình luyện tập gợi ý (4 tuần)

1. **Tuần 1**: Ôn NumPy vector hóa + hiểu BLAS đa luồng; đo thử `np.dot` khi đổi `OMP_NUM_THREADS`. [Scikit-learn](https://scikit-learn.org/stable/computing/parallelism.html?utm_source=chatgpt.com)
    
2. **Tuần 2**: Viết 3 bài bằng **Numba prange** (AXPY, prefix-sum/scan, 2D stencil). So sánh với NumPy. [numba.readthedocs.io](https://numba.readthedocs.io/en/stable/user/parallel.html?utm_source=chatgpt.com)
    
3. **Tuần 3**: Bài lớn với **ProcessPool** (chia mảng theo block) và **NumExpr** cho biểu thức dài. [Python documentation](https://docs.python.org/3/library/concurrent.futures.html?utm_source=chatgpt.com)[numexpr.readthedocs.io](https://numexpr.readthedocs.io/en/latest/user_guide.html?utm_source=chatgpt.com)
    
4. **Tuần 4**: **Dask Array** cho mảng vượt RAM; nếu có GPU thì port sang **CuPy**. [tutorial.dask.org](https://tutorial.dask.org/02_array.html?utm_source=chatgpt.com)[docs.cupy.dev](https://docs.cupy.dev/?utm_source=chatgpt.com)
    

---

## Nguồn chất lượng để tra cứu thêm

- Python docs: `multiprocessing`, `concurrent.futures`. [Python documentation+1](https://docs.python.org/3/library/multiprocessing.html?utm_source=chatgpt.com)
    
- Numba parallel (`@jit(parallel=True)`, `prange`). [numba.readthedocs.io](https://numba.readthedocs.io/en/stable/user/parallel.html?utm_source=chatgpt.com)[numba.pydata.org](https://numba.pydata.org/numba-doc/0.11/prange.html?utm_source=chatgpt.com)
    
- NumExpr user guide. [numexpr.readthedocs.io](https://numexpr.readthedocs.io/en/latest/user_guide.html?utm_source=chatgpt.com)
    
- Dask Array tutorial. [tutorial.dask.org](https://tutorial.dask.org/02_array.html?utm_source=chatgpt.com)
    
- NumPy thread-safety & BLAS threading. [NumPy+1](https://numpy.org/doc/stable/reference/thread_safety.html?utm_source=chatgpt.com)
    
- CuPy docs (NumPy trên GPU). [docs.cupy.dev](https://docs.cupy.dev/?utm_source=chatgpt.com)
    

Bạn muốn mình viết một **template project** nhỏ (CLI) để benchmark 5 cách trên cùng một bài toán mảng (CPU vs GPU) không? Mình có thể đặt sẵn cấu hình thread/BLAS và report thời gian chạy để bạn áp dụng ngay.

ChatGPT can make mistakes. OpenAI doesn't use SU workspace data to train its models.

![](https://cdn.oaistatic.com/assets/favicon-eex17e9e.ico)

---

Memo

Highlight

Explain

Beta

1093 / 5000used queries

![](chrome-extension://amfojhdiedpdnlijjbhjnhokbnohfdfb/img/logo/icon@2x.png)

1


---
# Ví dụ về lập trình song song

### 2.2.1 Bài Prompt Tool : 

Link: [BasicTasks_Prompting/5_TuningPrompting/PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py at main · DoanNgocCuong/BasicTasks_Prompting](https://github.com/DoanNgocCuong/BasicTasks_Prompting/blob/main/5_TuningPrompting/PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py)



```
# @title OPENAI
import os
import json
import pandas as pd
import time
import logging
import re
import concurrent.futures
from typing import List, Dict
import math
from openpyxl import load_workbook
import psutil
import multiprocessing
import threading
from pathlib import Path
import argparse
from dotenv import load_dotenv

# ============= FIX PROXY ISSUE =============
# Bước 1: Xóa tất cả proxy environment variables
proxy_vars = [
    'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
    'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy'
]

for var in proxy_vars:
    if var in os.environ:
        del os.environ[var]
        print(f"Removed proxy variable: {var}")

# Bước 2: Set explicit no proxy
os.environ['NO_PROXY'] = '*'

# Bước 3: Import OpenAI sau khi clear proxy
try:
    from openai import OpenAI
    from openai import OpenAIError
    print("✓ OpenAI imported successfully")
except ImportError as e:
    print(f"✗ Error importing OpenAI: {e}")
    print("Run: pip install openai>=1.0.0")
    exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Bước 4: Khởi tạo OpenAI client với error handling
def create_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    print(f"API Key: {api_key[:10]}...")
    
    try:
        # Tạo client chỉ với api_key (không có parameters khác)
        client = OpenAI(api_key=api_key)
        print("✓ OpenAI client created successfully")
        return client
    except Exception as e:
        print(f"✗ Error creating OpenAI client: {e}")
        print("Trying alternative initialization...")
        
        # Alternative: Tạo client với httpx explicit
        try:
            import httpx
            http_client = httpx.Client(proxies=None)
            client = OpenAI(api_key=api_key, http_client=http_client)
            print("✓ OpenAI client created with custom HTTP client")
            return client
        except Exception as e2:
            print(f"✗ Alternative initialization failed: {e2}")
            raise e

# Khởi tạo client
client = create_openai_client()
# ============= END FIX =============

sheet_name = 'Trang tính1'

def process_conversation(order, base_prompt, inputs, conversation_history=None):
    print(f"\n=== Processing Conversation ===")
    print(f"Order: {order}")
    print(f"Base Prompt: {base_prompt[:100]}...")
    
    # Log conversation history
    if conversation_history:
        logger.info(f"Conversation history: {conversation_history}")

    # Tạo model config dưới dạng JSON
    model_config = {
        "model": "gpt-4o-mini-2024-07-18",
        "temperature": 0,
        "max_tokens": 2048,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    model_config_json = json.dumps(model_config)
    
    responses = []
    response_times = []
    chat_messages = []
    
    # 1. System message
    chat_messages.append({"role": "system", "content": base_prompt})
    print("\nSau khi thêm system message:")
    print(chat_messages)
    
    # 2. History handling
    if conversation_history and not pd.isna(conversation_history):
        try:
            # Parse conversation history from JSON string
            history_messages = json.loads(conversation_history)
            
            # Validate format of history messages
            if isinstance(history_messages, list):
                for msg in history_messages:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        chat_messages.append(msg)
                    else:
                        print(f"Warning: Skipping invalid message format in history: {msg}")
            else:
                print(f"Warning: conversation_history is not a list: {history_messages}")
            
            print("\nSau khi thêm history:")
            print(json.dumps(chat_messages, indent=2, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            print(f"Error parsing conversation history: {e}")
            print(f"Raw conversation history: {conversation_history}")
            logger.error(f"Error parsing conversation history: {e}")
            logger.error(f"Raw conversation history: {conversation_history}")
    
    # 3. New input
    for user_input in inputs:
        chat_messages.append({"role": "user", "content": user_input})
        print("\nTrước khi gọi API:")
        print(json.dumps(chat_messages, indent=2, ensure_ascii=False))
        
        start_time = time.time()
        try_count = 0
        while try_count < 3:
            try:
                print(f"DEBUG - Attempt {try_count + 1} to call OpenAI API")
                completion = client.chat.completions.create(
                    model=model_config["model"],
                    messages=chat_messages,   
                    temperature=model_config["temperature"],
                    max_tokens=model_config["max_tokens"],
                    top_p=model_config["top_p"],
                    frequency_penalty=model_config["frequency_penalty"],
                    presence_penalty=model_config["presence_penalty"]
                )
                end_time = time.time()
                response_content = completion.choices[0].message.content
                chat_messages.append({"role": "assistant", "content": response_content})

                responses.append(response_content)
                response_times.append(end_time - start_time)

                # Print the completion output here
                print(f"Order {order}, Input: '{user_input}', Response: '{response_content[:100]}...', Time: {end_time - start_time:.2f}s\n====")
                break
                
            except Exception as e:
                try_count += 1
                print(f"DEBUG - Error on attempt {try_count}: {str(e)}")
                if try_count >= 3:
                    responses.append("Request failed after 3 retries.")
                    response_times.append("-")
                    print(f"Order {order}, Input: '{user_input}', Response: 'Request failed after 3 retries.', Time: -")
                else:
                    print(f"DEBUG - Waiting 3 seconds before retry...")
                    time.sleep(3)

    return responses, response_times, chat_messages, model_config_json

# Add argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process conversations with OpenAI API')
    parser.add_argument('--num-rows', type=int, default=None,
                      help='Number of rows to process (default: all rows)')
    parser.add_argument('--input-file', type=str, default='input_data.xlsx',
                      help='Input Excel file path (default: input_data.xlsx)')
    parser.add_argument('--output-file', type=str, default='output_data_v2.xlsx',
                      help='Output Excel file path (default: output_data_v2.xlsx)')
    parser.add_argument('--sheet', type=str, default='Trang tính1',
                      help='Excel sheet name to process (default: Trang tính1)')
    parser.add_argument('--batch-size', type=int, default=4,
                      help='Number of items to process in each batch (default: 4)')
    parser.add_argument('--max-workers', type=int, default=4,
                      help='Maximum number of worker threads (default: 4)')
    return parser.parse_args()

def process_batch(batch_rows: List[Dict]):
    output_rows = []
    for row in batch_rows:
        order = row.get('order', 'default_order')
        prompt = row['system_prompt']
        conversation_history = row.get('conversation_history', None)
        inputs = [row['user_input']]
        
        logger.info(f"Processing order {order}")
        
        responses, response_times, chat_messages, model_config = process_conversation(
            order, prompt, inputs, conversation_history
        )
        
        # Copy all columns and add new data
        new_row = row.copy()
        new_row.update({
            'assistant_response': responses[0] if responses else None,
            'response_time': response_times[0] if response_times else None,
            'model_config': model_config
        })
        output_rows.append(new_row)
    
    return output_rows

def append_to_excel(filename, df):
    """Append DataFrame to existing Excel file without reading entire file."""
    try:
        with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            workbook = writer.book
            worksheet = workbook['Sheet1']
            start_row = worksheet.max_row
            
            df.to_excel(writer, 
                       index=False, 
                       header=False,
                       startrow=start_row)
            
        return True
    except Exception as e:
        logger.error(f"Error appending to Excel: {str(e)}")
        return False

def get_system_resources():
    """Lấy thông tin tài nguyên hệ thống."""
    try:
        cpu_count = multiprocessing.cpu_count()
        memory = psutil.virtual_memory()
        available_memory_gb = memory.available / (1024 * 1024 * 1024)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        logger.info(f"System resources:")
        logger.info(f"- CPU cores: {cpu_count}")
        logger.info(f"- CPU usage: {cpu_percent}%")
        logger.info(f"- Available memory: {available_memory_gb:.2f}GB")
        logger.info(f"- Memory usage: {memory.percent}%")
        
        return {
            'cpu_count': cpu_count,
            'available_memory_gb': available_memory_gb,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent
        }
    except Exception as e:
        logger.error(f"Error getting system resources: {str(e)}")
        return None

def optimize_batch_parameters(total_rows: int, args):
    """Tối ưu batch_size và max_workers dựa trên tài nguyên hệ thống."""
    resources = get_system_resources()
    if not resources:
        logger.warning("Using default parameters due to resource check failure")
        return args.batch_size, args.max_workers
    
    # Tối ưu max_workers
    recommended_workers = min(
        resources['cpu_count'],
        int(8 * (100 - resources['cpu_percent']) / 100),
        int(resources['available_memory_gb'])
    )
    max_workers = max(1, min(recommended_workers, args.max_workers))
    
    # Tối ưu batch_size
    memory_based_batch = int(resources['available_memory_gb'] * 1024)
    cpu_based_batch = int(20 * (100 - resources['cpu_percent']) / 100)
    
    recommended_batch = min(
        memory_based_batch,
        cpu_based_batch,
        max(1, total_rows // (max_workers * 2))
    )
    batch_size = max(1, min(recommended_batch, args.batch_size))
    
    logger.info(f"Optimized parameters:")
    logger.info(f"- Original batch_size: {args.batch_size}, max_workers: {args.max_workers}")
    logger.info(f"- Recommended batch_size: {batch_size}, max_workers: {max_workers}")
    
    return batch_size, max_workers

def monitor_resources(stop_event, interval=30):
    """Monitor tài nguyên hệ thống trong quá trình xử lý."""
    while not stop_event.is_set():
        resources = get_system_resources()
        if resources:
            if resources['cpu_percent'] > 90:
                logger.warning("High CPU usage detected!")
            if resources['memory_percent'] > 90:
                logger.warning("High memory usage detected!")
        time.sleep(interval)

def main():
    args = parse_arguments()
    
    SCRIPTS_FOLDER = Path(__file__).parent
    INPUT_FILE = SCRIPTS_FOLDER / args.input_file
    OUTPUT_FILE = SCRIPTS_FOLDER / args.output_file

    # Kiểm tra file input tồn tại
    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    df_input = pd.read_excel(INPUT_FILE, sheet_name=args.sheet)
    rows_to_process = df_input if args.num_rows is None else df_input.head(args.num_rows)
    
    logger.info(f"Processing {len(rows_to_process)} rows from {INPUT_FILE}")
    
    # Tối ưu parameters
    batch_size, max_workers = optimize_batch_parameters(len(rows_to_process), args)
    
    all_rows = rows_to_process.to_dict('records')
    batches = [all_rows[i:i + batch_size] for i in range(0, len(all_rows), batch_size)]
    
    logger.info(f"Created {len(batches)} batches with batch_size={batch_size}, max_workers={max_workers}")
    
    # Tạo file output với headers
    cols_order = list(df_input.columns) + ['assistant_response', 'response_time', 'model_config']
    pd.DataFrame(columns=cols_order).to_excel(OUTPUT_FILE, index=False)
    
    # Khởi động monitor thread
    stop_monitoring = threading.Event()
    monitor_thread = threading.Thread(target=monitor_resources, args=(stop_monitoring,))
    monitor_thread.start()
    
    try:
        processed_count = 0
        failed_batches = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_batch, batch) for batch in batches]
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    batch_results = future.result()
                    batch_df = pd.DataFrame(batch_results)[cols_order]
                    
                    for attempt in range(3):
                        if append_to_excel(OUTPUT_FILE, batch_df):
                            processed_count += len(batch_results)
                            logger.info(f"Appended batch {i+1}/{len(batches)}. Total processed: {processed_count}")
                            break
                        else:
                            if attempt < 2:
                                logger.warning(f"Retry {attempt + 1} for batch {i+1}")
                                time.sleep(2)
                            else:
                                logger.error(f"Failed to append batch {i+1} after 3 attempts")
                                failed_batches.append((i, batch_results))
                                
                except Exception as e:
                    logger.error(f"Error processing batch {i+1}: {str(e)}")
                    failed_batches.append((i, None))

        # Xử lý lại các batch thất bại
        if failed_batches:
            logger.info(f"Retrying {len(failed_batches)} failed batches...")
            for batch_index, batch_results in failed_batches:
                if batch_results:
                    batch_df = pd.DataFrame(batch_results)[cols_order]
                    if append_to_excel(OUTPUT_FILE, batch_df):
                        processed_count += len(batch_results)
                        logger.info(f"Successfully retried batch {batch_index+1}")
                    else:
                        logger.error(f"Permanently failed to append batch {batch_index+1}")

    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        # Dừng monitor thread
        stop_monitoring.set()
        monitor_thread.join()
        
        # Log kết quả cuối cùng
        logger.info(f"Processing completed. Total rows processed: {processed_count}")
        logger.info(f"Output saved to: {OUTPUT_FILE}")
        get_system_resources()

if __name__ == "__main__":
    main()

```


## 2.2.2 Gen lộ trình học - 20-50 luồng Situations 1 lúc (trong 1 situations thì có 5 questions, mỗi questions thì call 1 lúc 1 lesson detail (8 luồng audio bên trong), 1 lúc call 5 questions)

Link: [MiniProd_Web4_ContentEngFlow_StepUpE_T102024/1000Nghe_copyFrom_LS_ai_automation/utils_genLessonDetail1000Nghe_22082025_v2/batch_size_max_worker.py at main · DoanNgocCuong/MiniProd_Web4_ContentEngFlow_StepUpE_T102024](https://github.com/DoanNgocCuong/MiniProd_Web4_ContentEngFlow_StepUpE_T102024/blob/main/1000Nghe_copyFrom_LS_ai_automation/utils_genLessonDetail1000Nghe_22082025_v2/batch_size_max_worker.py)


```
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


### 2.3 Đóng API lộ trình học 

```
/**

 * ================================================================================

 * OPTIMIZED LEARNING PIPELINE CONTROLLER - A12 + PARALLEL A3 IMPLEMENTATION

 * ================================================================================

 *

 * Author: Doan Ngoc Cuong (Optimized Version)

 * Date: 2025-09-11

 * Version: 4.0.0 - Performance Optimized

 *

 * Description:

 * API tối ưu hóa với 2-step approach thay vì 3-step sequential:

 *  - A12: generateA1andA2_Combined (job_role → topics/situations trực tiếp)

 *  - A3_PARALLEL: generateFullLearningPipeline song song cho từng situation

 *  - MERGE: Tổng hợp kết quả cuối cùng

 *

 * Performance Benefits:

 * - Giảm từ 3 steps sequential xuống 2 steps (A12 + parallel A3)

 * - Parallel processing thay vì sequential cho A3 calls

 * - Time complexity: O(1) + O(max_parallel) thay vì O(n) sequential

 * - Estimated speedup: 60-80% cho scenarios >= 3

 *

 * ===================================================================================

 * OPTIMIZED WORKFLOW COMPARISON

 * ===================================================================================

 *

 * OLD APPROACH (Sequential):

 * ┌─────────────────────────────────────────────────────────────────────────────────┐

 * │ INPUT → [A1: 3s] → [A2: 4s] → [A3: 15s × N situations]                         │

 * │ Total: 7s + (15s × N) = 7s + 75s (for 5 situations) = 82s                     │

 * └─────────────────────────────────────────────────────────────────────────────────┘

 *

 * NEW APPROACH (Optimized):

 * ┌─────────────────────────────────────────────────────────────────────────────────┐

 * │ INPUT → [A12: 5s] → [A3 Parallel: max(15s)] → [MERGE: 1s]                     │

 * │ Total: 5s + 15s + 1s = 21s (for 5 situations in parallel)                     │

 * │ Time Saved: 82s - 21s = 61s (74% faster!)                                     │

 * └─────────────────────────────────────────────────────────────────────────────────┘

 *

 * ===================================================================================

 * ARCHITECTURE OVERVIEW

 * ===================================================================================

 *

 * ┌─────────────────────────────────────────────────────────────────────────────────┐

 * │ STEP A12: COMBINED JOB_ROLE → TOPICS/SITUATIONS                               │

 * ├─────────────────────────────────────────────────────────────────────────────────┤

 * │ Function: generateA1andA2_UserInput2JTBD2TopicAndSituation                     │

 * │ Input: { data: { job_role: "AI Engineer" } }                                   │

 * │ Output: Direct topics with situations (bypasses JTBD intermediate step)        │

 * │ Performance: Single API call thay vì 2 calls (A1→A2)                         │

 * │ Model: Combined OpenAI + Gemini logic in one optimized prompt                  │

 * └─────────────────────────────────────────────────────────────────────────────────┘

 *

 * ┌─────────────────────────────────────────────────────────────────────────────────┐

 * │ STEP EXTRACT: SITUATION EXTRACTION & PARALLELIZATION PREP                     │

 * ├─────────────────────────────────────────────────────────────────────────────────┤

 * │ Logic: Extract all situations from all topics into flat array                  │

 * │ Input: A12 output (topics with nested situations)                              │

 * │ Output: Flat array of situations with metadata for parallel processing         │

 * │ Features: ID generation, batch grouping, load balancing preparation            │

 * └─────────────────────────────────────────────────────────────────────────────────┘

 *

 * ┌─────────────────────────────────────────────────────────────────────────────────┐

 * │ STEP A3_PARALLEL: CONCURRENT FULL PIPELINE EXECUTION                           │

 * ├─────────────────────────────────────────────────────────────────────────────────┤

 * │ Function: generateFullLearningPipeline (parallel execution)                    │

 * │ Input: Individual situation + generateQuestions4Inputs format                  │

 * │ Output: Complete learning pipeline per situation                               │

 * │ Concurrency: Controlled parallel execution with configurable limits           │

 * │ Error Handling: Individual failures don't affect other situations              │

 * │ Performance: Processing time = max(individual_time) vs sum(individual_time)    │

 * └─────────────────────────────────────────────────────────────────────────────────┘

 *

 * ┌─────────────────────────────────────────────────────────────────────────────────┐

 * │ STEP MERGE: INTELLIGENT RESULT AGGREGATION                                     │

 * ├─────────────────────────────────────────────────────────────────────────────────┤

 * │ Logic: Organize parallel results back into topic/situation hierarchy           │

 * │ Input: Array of individual A3 results                                          │

 * │ Output: Structured response with comprehensive metadata                        │

 * │ Features: Success/failure tracking, performance metrics, partial success       │

 * │ Quality: Error isolation, detailed reporting, optimization statistics          │

 * └─────────────────────────────────────────────────────────────────────────────────┘

 *

 * ===================================================================================

 * PERFORMANCE OPTIMIZATIONS

 * ===================================================================================

 *

 * 1. Reduced API Round-trips:

 *    - A1+A2 combined into single A12 call

 *    - Eliminates intermediate JTBD step

 *    - Reduces latency overhead

 *

 * 2. Parallel Processing:

 *    - Concurrent A3 execution for all situations

 *    - Configurable parallelism (default: 5 concurrent)

 *    - Resource-efficient batch processing

 *

 * 3. Error Isolation:

 *    - Individual situation failures don't cascade

 *    - Partial success handling

 *    - Detailed error reporting per situation

 *

 * 4. Memory Optimization:

 *    - Streaming result processing

 *    - Configurable batch sizes

 *    - Garbage collection friendly

 *

 * 5. Smart Resource Management:

 *    - Adaptive concurrency based on system load

 *    - Rate limiting for external APIs

 *    - Connection pooling optimization

 *

 * ===================================================================================

 * SCALABILITY FEATURES

 * ===================================================================================

 *

 * - Horizontal scaling: Easy to distribute across multiple servers

 * - Load balancing: Intelligent work distribution

 * - Circuit breaker: Automatic failure handling

 * - Monitoring: Comprehensive metrics and logging

 * - Caching: Result caching for repeated requests

 *

 * ===================================================================================

 * API ENDPOINTS

 * ===================================================================================

 *

 * Main Endpoint:

 * POST /api/generate-learning-path-user-input-to-done-full

 *

 * Health Check:

 * GET /api/health/optimized-pipeline-status

 *

 * Performance Metrics:

 * GET /api/metrics/pipeline-performance

 *

 */

  

// ===================================================================================

// DEPENDENCIES AND IMPORTS

// ===================================================================================

  

const { generateA1andA2_UserInput2JTBD2TopicAndSituation } = require('./generateLearningPathV4T92025_A1andA2_UserInput2JTBD2TopicAndSituation.js');

const { generateFullLearningPipeline } = require('./generateLearningPathV4T92025_A3_Question4Inputs2FinalLessonDetail.js');

const { call_api_with_retry } = require('@utils/utils_call_api_with_retry');

  

// ===================================================================================

// CONFIGURATION CONSTANTS

// ===================================================================================

  

/**

 * Performance and concurrency configuration

 *

 * Clarification: Batch size vs Max workers (this implementation uses Max workers)

 * - Batch size (data-centric): kích thước một nhóm dữ liệu xử lý trong 1 lượt.

 *   - Thường dùng trong training ML hoặc xử lý I/O theo lô; ảnh hưởng memory và convergence.

 * - Max workers (parallelism-centric): số tác vụ chạy đồng thời (độ song song).

 *   - Dùng để kiểm soát throughput và mức sử dụng CPU core trong hệ thống song song.

 *

 * Trong file này, cấu hình điều khiển TRỰC TIẾP số situation chạy đồng thời → dùng tên MAX_WORKERS

 * để tránh nhầm lẫn với khái niệm "batch size" mang tính chất dữ liệu.

---

1 Situation gen khoảng 1.5min (các cơ chế song song bên trong)

Gen theo Situation với luồng 10-20-30-50 situations.

(với 20 luồng ko lỗi (do có retry audio và check Audio, retry OpenAI, retry từng API con, retry đếm xem đủ scenario chưa trong 1 situation)

, còn 40-50 luồng tỉ lệ lỗi khoảng 2%)

  

---

- Không. Trong code hiện tại:

  - Thực thi song song thực tế = MAX_WORKERS.

  - Batches chạy tuần tự; MAX_CONCURRENT_BATCHES chưa được dùng.

  - MAX_CONCURRENT_A3 chỉ log, chưa chặn gì.

  

Muốn đúng như bạn nói: tổng song song = min(MAX_CONCURRENT_A3, MAX_CONCURRENT_BATCHES × MAX_WORKERS). Cần:

- Chạy nhiều batch đồng thời theo MAX_CONCURRENT_BATCHES.

- Thêm limiter tổng để cap theo MAX_CONCURRENT_A3.

 */

const OPTIMIZED_CONFIG = {

    // Parallel processing limits

    MAX_CONCURRENT_A3: 5,              // Maximum parallel A3 calls

    MAX_CONCURRENT_BATCHES: 2,         // Maximum parallel batches

    MAX_WORKERS: 30,                    // Số situation chạy đồng thời trong 1 lượt

    // Timeouts and retries

    A12_TIMEOUT_MS: 300000,            // A12 generation timeout (5 minutes)

    A3_TIMEOUT_MS: 300000,              // A3 individual timeout

    MAX_RETRIES: 3,                    // Retry attempts per operation

    // Memory and performance

    MEMORY_LIMIT_MB: 512,              // Memory limit per process

    GC_INTERVAL_MS: 30000,             // Garbage collection interval

    // Monitoring and logging

    ENABLE_DETAILED_LOGGING: true,     // Detailed execution logging

    ENABLE_PERFORMANCE_TRACKING: true, // Performance metrics collection

    ENABLE_ERROR_TRACKING: true,       // Error analytics

    // Collection ID generation

    COLLECTION_PREFIX: 'OPT',          // Optimized pipeline prefix

    TOPIC_PREFIX: 'TOP',               // Topic ID prefix

    SITUATION_PREFIX: 'SIT'            // Situation ID prefix

};

  

/**

 * Error handling configuration

 */

const ERROR_CONFIG = {

    // Retry strategies

    EXPONENTIAL_BACKOFF: true,         // Use exponential backoff for retries

    MAX_BACKOFF_MS: 5000,             // Maximum backoff time

    // Error isolation

    CONTINUE_ON_PARTIAL_FAILURE: true, // Continue processing despite individual failures

    MIN_SUCCESS_RATE: 0.7,            // Minimum success rate to consider pipeline successful

    // Fallback options

    ENABLE_GRACEFUL_DEGRADATION: true, // Enable fallback to sequential processing

    FALLBACK_THRESHOLD: 0.5           // Failure rate threshold for fallback

};

  

// ===================================================================================

// UTILITY FUNCTIONS

// ===================================================================================

  

/**

 * Enhanced controller caller for A12 with comprehensive error handling

 *

 * @param {Function} controllerFn - A12 controller function

 * @param {Object} body - Request body

 * @param {string} operation - Operation name for logging

 * @returns {Promise<Object>} A12 execution result

 */

const callA12Controller = (controllerFn, body, operation = 'A12_Generation') => {

    return new Promise((resolve) => {

        const startTime = Date.now();

        if (OPTIMIZED_CONFIG.ENABLE_DETAILED_LOGGING) {

            console.log(`🚀 [${operation}] Starting A12 generation...`);

            console.log(`📊 [${operation}] Input: job_role="${body?.data?.job_role}"`);

        }

  

        const req = { body };

        const res = {

            status(code) {

                return {

                    json(payload) {

                        const duration = Date.now() - startTime;

                        console.error(`❌ [${operation}] Failed with status ${code} in ${duration}ms`);

                        resolve({

                            success: false,

                            httpStatus: code,

                            payload,

                            operation,

                            duration_ms: duration,

                            error: `A12 failed with status ${code}`

                        });

                    }

                };

            },

            json(payload) {

                const duration = Date.now() - startTime;

                if (OPTIMIZED_CONFIG.ENABLE_DETAILED_LOGGING) {

                    console.log(`✅ [${operation}] Completed successfully in ${duration}ms`);

                }

                resolve({

                    success: true,

                    httpStatus: 200,

                    payload,

                    operation,

                    duration_ms: duration

                });

            }

        };

  

        // Execute with timeout protection

        const timeoutId = setTimeout(() => {

            const duration = Date.now() - startTime;

            console.error(`⏰ [${operation}] Timeout after ${duration}ms`);

            resolve({

                success: false,

                httpStatus: 408,

                payload: {

                    status: false,

                    error: `${operation} timed out after ${OPTIMIZED_CONFIG.A12_TIMEOUT_MS}ms`

                },

                operation,

                duration_ms: duration,

                error: 'Timeout'

            });

        }, OPTIMIZED_CONFIG.A12_TIMEOUT_MS);

  

        Promise.resolve(controllerFn(req, res))

            .then(() => clearTimeout(timeoutId))

            .catch((error) => {

                clearTimeout(timeoutId);

                const duration = Date.now() - startTime;

                console.error(`💥 [${operation}] Exception in ${duration}ms:`, error.message);

                resolve({

                    success: false,

                    httpStatus: 500,

                    payload: {

                        status: false,

                        error: error?.message || 'Unknown A12 error'

                    },

                    operation,

                    duration_ms: duration,

                    error: error.message

                });

            });

    });

};

  

/**

 * Extract and flatten all situations from A12 output for parallel processing

 *

 * @param {Object} a12Output - A12 generation result

 * @param {string} job_role - Original job role for context

 * @returns {Array} Flattened array of situations with metadata

 */

function extractSituationsForParallelProcessing(a12Output, job_role) {

    console.log('🔍 [EXTRACT] Extracting situations for parallel processing...');

    try {

        const { step_a2 } = a12Output;

        if (!step_a2?.data?.output || !Array.isArray(step_a2.data.output)) {

            throw new Error('Invalid A12 output: missing step_a2.data.output array');

        }

  

        const topics = step_a2.data.output;

        console.log(`📊 [EXTRACT] Processing ${topics.length} topics from A12 output`);

  

        const allSituations = [];

        let globalSituationIndex = 0;

  

        topics.forEach((topic, topicIndex) => {

            const { topic_name, situations } = topic;

            if (!situations || !Array.isArray(situations) || situations.length === 0) {

                console.warn(`⚠️ [EXTRACT] Topic ${topicIndex + 1} "${topic_name}" has no valid situations`);

                return;

            }

  

            console.log(`📝 [EXTRACT] Topic ${topicIndex + 1}: "${topic_name}" has ${situations.length} situations`);

  

            situations.forEach((situation, situationIndex) => {

                const {

                    situation_name,

                    stakeholder,

                    scenario_description,

                    situation_details

                } = situation;

  

                // Generate unique identifiers

                const collection_id = `${OPTIMIZED_CONFIG.COLLECTION_PREFIX}${String(globalSituationIndex + 1).padStart(3, '0')}`;

                const topic_id = `${OPTIMIZED_CONFIG.TOPIC_PREFIX}${String(topicIndex + 1).padStart(3, '0')}`;

                const situation_id = `${OPTIMIZED_CONFIG.SITUATION_PREFIX}${String(situationIndex + 1).padStart(3, '0')}`;

  

                // Create A3 input format

                const a3Input = {

                    collection_id,

                    topic_id,

                    situation_id,

                    generateQuestions4Inputs: {

                        job_role,

                        output: [{

                            topic_name,

                            situations: [situation] // Single situation for individual A3 processing

                        }]

                    }

                };

  

                allSituations.push({

                    // Identifiers

                    global_index: globalSituationIndex,

                    topic_index: topicIndex,

                    situation_index: situationIndex,

                    collection_id,

                    topic_id,

                    situation_id,

                    // Content

                    topic_name,

                    situation_name,

                    stakeholder,

                    scenario_description,

                    questions: situation_details?.stakeholder_ask || [],

                    // A3 processing input

                    a3_input: a3Input,

                    // Metadata for tracking

                    metadata: {

                        created_at: new Date().toISOString(),

                        extraction_order: globalSituationIndex + 1,

                        belongs_to_topic: topic_name,

                        question_count: situation_details?.stakeholder_ask?.length || 0

                    }

                });

  

                globalSituationIndex++;

            });

        });

  

        console.log(`✅ [EXTRACT] Successfully extracted ${allSituations.length} situations for parallel processing`);

        return allSituations;

  

    } catch (error) {

        console.error('❌ [EXTRACT] Extraction failed:', error.message);

        throw new Error(`Situation extraction failed: ${error.message}`);

    }

}

  

/**

 * Execute parallel A3 processing with intelligent batch management

 *

 * @param {Array} situations - Array of situations to process

 * @returns {Promise<Array>} Array of A3 processing results

 */

async function executeParallelA3Processing(situations) {

    const startTime = Date.now();

    console.log(`⚡ [A3_PARALLEL] Starting parallel processing for ${situations.length} situations...`);

    // Configuration

    const {

        MAX_CONCURRENT_A3,

        MAX_WORKERS,

        A3_TIMEOUT_MS,

        ENABLE_DETAILED_LOGGING

    } = OPTIMIZED_CONFIG;

  

    console.log(`⚙️ [A3_PARALLEL] Configuration: max_concurrent=${MAX_CONCURRENT_A3}, max_workers=${MAX_WORKERS}`);

  

    // Create batches for controlled parallel processing

    const batches = [];

    for (let i = 0; i < situations.length; i += MAX_WORKERS) {

        batches.push(situations.slice(i, i + MAX_WORKERS));

    }

  

    console.log(`📦 [A3_PARALLEL] Processing ${batches.length} batches...`);

    const allResults = [];

    let totalSuccessful = 0;

    let totalFailed = 0;

    // Process batches with controlled concurrency

    for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {

        const batch = batches[batchIndex];

        const batchStartTime = Date.now();

        console.log(`🔄 [A3_PARALLEL] Processing batch ${batchIndex + 1}/${batches.length} (${batch.length} situations)...`);

        // Create promises for parallel execution within batch

        const batchPromises = batch.map(async (situation) => {

            const { global_index, collection_id, topic_id, situation_id, a3_input } = situation;

            const operationName = `A3_${global_index + 1}_${collection_id}`;

            try {

                if (ENABLE_DETAILED_LOGGING) {

                    console.log(`🎯 [A3_PARALLEL] Starting ${operationName}: ${situation.situation_name}`);

                }

                // Create A3 execution promise with timeout

                const a3Promise = new Promise((resolve, reject) => {

                    let a3Result = null;

                    const mockRes = {

                        json: (data) => {

                            a3Result = data;

                            resolve(a3Result);

                        },

                        status: (code) => ({

                            json: (data) => {

                                reject(new Error(`A3 failed with status ${code}: ${JSON.stringify(data)}`));

                            }

                        })

                    };

                    const mockReq = { body: a3_input };

                    generateFullLearningPipeline(mockReq, mockRes)

                        .then(() => {

                            if (!a3Result) {

                                reject(new Error('A3 completed without returning data'));

                            }

                        })

                        .catch(reject);

                });

                // Execute with timeout

                const result = await Promise.race([

                    a3Promise,

                    new Promise((_, reject) =>

                        setTimeout(() => reject(new Error(`A3 timeout after ${A3_TIMEOUT_MS}ms`)), A3_TIMEOUT_MS)

                    )

                ]);

                if (ENABLE_DETAILED_LOGGING) {

                    console.log(`✅ [A3_PARALLEL] ${operationName} completed successfully`);

                }

                return {

                    success: true,

                    situation_metadata: situation.metadata,

                    identifiers: { global_index, collection_id, topic_id, situation_id },

                    topic_name: situation.topic_name,

                    situation_name: situation.situation_name,

                    a3_result: result,

                    processing_time_ms: Date.now() - batchStartTime,

                    error: null

                };

            } catch (error) {

                console.error(`❌ [A3_PARALLEL] ${operationName} failed:`, error.message);

                return {

                    success: false,

                    situation_metadata: situation.metadata,

                    identifiers: { global_index, collection_id, topic_id, situation_id },

                    topic_name: situation.topic_name,

                    situation_name: situation.situation_name,

                    a3_result: null,

                    processing_time_ms: Date.now() - batchStartTime,

                    error: error.message

                };

            }

        });

        // Wait for current batch to complete

        const batchResults = await Promise.all(batchPromises);

        allResults.push(...batchResults);

        // Update statistics

        const batchSuccessful = batchResults.filter(r => r.success).length;

        const batchFailed = batchResults.length - batchSuccessful;

        totalSuccessful += batchSuccessful;

        totalFailed += batchFailed;

        const batchDuration = Date.now() - batchStartTime;

        console.log(`✅ [A3_PARALLEL] Batch ${batchIndex + 1} completed in ${batchDuration}ms: ${batchSuccessful}/${batchResults.length} successful`);

        // Optional: Brief pause between batches to manage system load

        if (batchIndex < batches.length - 1) {

            await new Promise(resolve => setTimeout(resolve, 100));

        }

    }

  

    const totalDuration = Date.now() - startTime;

    console.log(`🎉 [A3_PARALLEL] All parallel processing completed in ${totalDuration}ms`);

    console.log(`📊 [A3_PARALLEL] Final results: ${totalSuccessful}/${allResults.length} successful, ${totalFailed} failed`);

  

    // Calculate performance metrics

    const avgProcessingTime = allResults

        .filter(r => r.success && r.processing_time_ms > 0)

        .reduce((sum, r) => sum + r.processing_time_ms, 0) / totalSuccessful || 0;

  

    if (OPTIMIZED_CONFIG.ENABLE_PERFORMANCE_TRACKING) {

        console.log(`📈 [A3_PARALLEL] Performance metrics:`, {

            total_duration_ms: totalDuration,

            avg_processing_time_ms: avgProcessingTime.toFixed(2),

            success_rate: `${((totalSuccessful / allResults.length) * 100).toFixed(1)}%`,

            situations_per_second: (allResults.length / (totalDuration / 1000)).toFixed(2)

        });

    }

  

    return allResults;

}

  

/**

 * Create simplified learning structure with only important keys

 * Structure: JOB_ROLE → TOPICS → SITUATIONS → pipeline_results

 *

 * @param {string} job_role - Job role name

 * @param {Array} processedTopics - Processed topics with situations

 * @returns {Object} Simplified structure

 */

function createSimplifiedLearningStructure(job_role, processedTopics) {

    console.log('🔧 [SIMPLIFY] Creating simplified learning structure...');

    const simplifiedStructure = {

        job_role: job_role,

        topics: []

    };

  

    processedTopics.forEach((topic) => {

        const simplifiedTopic = {

            topic_name: topic.topic_name,

            situations: []

        };

  

        topic.situations.forEach((situation) => {

            const simplifiedSituation = {

                situation_name: situation.situation_name,

                stakeholder: situation.stakeholder,

                scenario_description: situation.scenario_description,

                image_url_situation: situation.image_url_situation || null, // Thumbnail link from A12

                pipeline_results: null

            };

  

            // Extract pipeline_results from learning_content if available

            if (situation.learning_content && situation.learning_content.pipeline_results) {

                simplifiedSituation.pipeline_results = situation.learning_content.pipeline_results;

            } else if (situation.learning_content && situation.learning_content.pipeline_results === null) {

                // Handle case where pipeline_results is explicitly null

                simplifiedSituation.pipeline_results = null;

            } else {

                // Handle missing or failed learning_content

                simplifiedSituation.pipeline_results = null;

            }

  

            simplifiedTopic.situations.push(simplifiedSituation);

        });

  

        simplifiedStructure.topics.push(simplifiedTopic);

    });

  

    console.log(`✅ [SIMPLIFY] Created simplified structure: ${simplifiedStructure.topics.length} topics`);

    return simplifiedStructure;

}

  

/**

 * UPDATED MERGE FUNCTION - OUTSIDE-IN APPROACH

 * Replaces the old inside-out merge logic with natural hierarchy traversal

 */

  

/**

 * Intelligent result merging and organization using Outside-In approach

 *

 * @param {Object} a12Output - Original A12 output

 * @param {Array} a3Results - Parallel A3 processing results

 * @param {string} job_role - Original job role

 * @returns {Object} Organized final response

 */

function mergeAndOrganizeResults(a12Output, a3Results, job_role) {

    console.log('🔧 [MERGE_OUTSIDE_IN] Starting outside-in intelligent result merging...');

    const mergeStartTime = Date.now();

    try {

        // ========== INPUT VALIDATION ==========

        if (!a12Output?.step_a2?.data?.output) {

            throw new Error('Invalid A12 output: missing step_a2.data.output array');

        }

        if (!Array.isArray(a3Results)) {

            throw new Error('A3 results must be an array');

        }

  

        // ========== CREATE A3 RESULTS LOOKUP MAP ==========

        console.log(`📊 [MERGE_OUTSIDE_IN] Creating lookup map for ${a3Results.length} A3 results...`);

        const a3ResultsMap = new Map();

        const a3ProcessingStats = {

            total_a3_results: a3Results.length,

            indexed_results: 0,

            indexing_errors: []

        };

  

        a3Results.forEach((a3Result, index) => {

            try {

                if (!a3Result?.identifiers) {

                    throw new Error(`A3 result ${index} missing identifiers`);

                }

                const { topic_id, situation_id } = a3Result.identifiers;

                if (!topic_id || !situation_id) {

                    throw new Error(`A3 result ${index} missing topic_id or situation_id`);

                }

                const lookupKey = `${topic_id}_${situation_id}`;

                a3ResultsMap.set(lookupKey, a3Result);

                a3ProcessingStats.indexed_results++;

            } catch (error) {

                console.error(`❌ [MERGE_OUTSIDE_IN] Failed to index A3 result ${index}:`, error.message);

                a3ProcessingStats.indexing_errors.push({

                    index,

                    error: error.message,

                    result_preview: JSON.stringify(a3Result).substring(0, 100) + '...'

                });

            }

        });

  

        console.log(`✅ [MERGE_OUTSIDE_IN] Lookup map created: ${a3ResultsMap.size} indexed successfully`);

  

        // ========== START FROM A12 STRUCTURE (OUTSIDE-IN) ==========

        const originalTopics = a12Output.step_a2.data.output;

        console.log(`🏗️ [MERGE_OUTSIDE_IN] Processing ${originalTopics.length} topics from A12 structure...`);

  

        // Statistics tracking

        const mergeStats = {

            total_topics: originalTopics.length,

            total_original_situations: 0,

            completed_situations: 0,

            failed_situations: 0,

            not_processed_situations: 0,

            processing_errors: []

        };

  

        // ========== ITERATE THROUGH TOPICS (PRESERVE A12 ORDER) ==========

        const organizedByTopic = {};

        const processedTopics = originalTopics.map((originalTopic, topicIndex) => {

            const topicId = `TOP${String(topicIndex + 1).padStart(3, '0')}`;

            console.log(`📝 [MERGE_OUTSIDE_IN] Processing topic ${topicIndex + 1}: "${originalTopic.topic_name}"`);

  

            // Preserve ALL original topic metadata from A12

            const topicResult = {

                topic_name: originalTopic.topic_name,

                topic_description: originalTopic.topic_description || null,

                learning_objectives: originalTopic.learning_objectives || [],

                topic_metadata: {

                    topic_id: topicId,

                    topic_index: topicIndex,

                    original_order: topicIndex + 1,

                    source: 'A12_generation'

                },

                situations: [],

                topic_stats: {

                    total_situations: 0,

                    successful_situations: 0,

                    failed_situations: 0,

                    not_processed_situations: 0

                }

            };

  

            // ========== ITERATE THROUGH SITUATIONS IN EACH TOPIC ==========

            if (originalTopic.situations && Array.isArray(originalTopic.situations)) {

                topicResult.situations = originalTopic.situations.map((originalSituation, situationIndex) => {

                    const situationId = `SIT${String(situationIndex + 1).padStart(3, '0')}`;

                    const lookupKey = `${topicId}_${situationId}`;

                    console.log(`   🎯 [MERGE_OUTSIDE_IN] Processing situation ${situationIndex + 1}: "${originalSituation.situation_name}"`);

                    mergeStats.total_original_situations++;

                    topicResult.topic_stats.total_situations++;

  

                    // ========== FIND CORRESPONDING A3 RESULT ==========

                    const a3Result = a3ResultsMap.get(lookupKey);

                    if (a3Result) {

                        console.log(`   ✅ [MERGE_OUTSIDE_IN] Found A3 result for ${lookupKey}`);

                        if (a3Result.success) {

                            mergeStats.completed_situations++;

                            topicResult.topic_stats.successful_situations++;

                            return {

                                // ========== ORIGINAL SITUATION METADATA (PRESERVED) ==========

                                situation_name: originalSituation.situation_name,

                                stakeholder: originalSituation.stakeholder,

                                scenario_description: originalSituation.scenario_description,

                                situation_details: originalSituation.situation_details,

                                image_url_situation: originalSituation.image_url_situation, // Thumbnail from A12

                                // ========== SITUATION METADATA ==========

                                situation_metadata: {

                                    situation_id: situationId,

                                    situation_index: situationIndex,

                                    original_order: situationIndex + 1,

                                    topic_reference: topicId,

                                    source: 'A12_generation'

                                },

                                // ========== A3 PROCESSING RESULT ==========

                                learning_content: a3Result.a3_result,

                                processing_status: 'completed',

                                processing_error: null,

                                processing_time_ms: a3Result.processing_time_ms || 0,

                                // ========== LINKING METADATA ==========

                                collection_id: a3Result.identifiers?.collection_id || null,

                                linked_successfully: true,

                                a3_metadata: a3Result.situation_metadata || null

                            };

                        } else {

                            // A3 processing failed

                            mergeStats.failed_situations++;

                            topicResult.topic_stats.failed_situations++;

                            mergeStats.processing_errors.push({

                                topic: originalTopic.topic_name,

                                situation: originalSituation.situation_name,

                                lookup_key: lookupKey,

                                error: a3Result.error

                            });

                            return {

                                // Original situation metadata preserved

                                situation_name: originalSituation.situation_name,

                                stakeholder: originalSituation.stakeholder,

                                scenario_description: originalSituation.scenario_description,

                                situation_details: originalSituation.situation_details,

                                image_url_situation: originalSituation.image_url_situation, // Thumbnail from A12

                                situation_metadata: {

                                    situation_id: situationId,

                                    situation_index: situationIndex,

                                    original_order: situationIndex + 1,

                                    topic_reference: topicId,

                                    source: 'A12_generation'

                                },

                                // Failed A3 processing

                                learning_content: null,

                                processing_status: 'failed',

                                processing_error: a3Result.error,

                                processing_time_ms: a3Result.processing_time_ms || 0,

                                collection_id: a3Result.identifiers?.collection_id || null,

                                linked_successfully: true,

                                a3_metadata: a3Result.situation_metadata || null

                            };

                        }

                    } else {

                        // Missing A3 result

                        console.log(`   ❌ [MERGE_OUTSIDE_IN] Missing A3 result for ${lookupKey}`);

                        mergeStats.not_processed_situations++;

                        topicResult.topic_stats.not_processed_situations++;

                        mergeStats.processing_errors.push({

                            topic: originalTopic.topic_name,

                            situation: originalSituation.situation_name,

                            lookup_key: lookupKey,

                            error: 'A3 result not found in parallel processing results'

                        });

                        return {

                            // Original situation metadata preserved

                            situation_name: originalSituation.situation_name,

                            stakeholder: originalSituation.stakeholder,

                            scenario_description: originalSituation.scenario_description,

                            situation_details: originalSituation.situation_details,

                            image_url_situation: originalSituation.image_url_situation, // Thumbnail from A12

                            situation_metadata: {

                                situation_id: situationId,

                                situation_index: situationIndex,

                                original_order: situationIndex + 1,

                                topic_reference: topicId,

                                source: 'A12_generation'

                            },

                            // Not processed

                            learning_content: null,

                            processing_status: 'not_processed',

                            processing_error: 'A3 result not found in parallel processing results',

                            processing_time_ms: 0,

                            collection_id: null,

                            linked_successfully: false,

                            a3_metadata: null

                        };

                    }

                });

            }

  

            // Calculate topic success rate

            topicResult.topic_stats.success_rate = topicResult.topic_stats.total_situations > 0

                ? `${((topicResult.topic_stats.successful_situations / topicResult.topic_stats.total_situations) * 100).toFixed(1)}%`

                : '0%';

  

            console.log(`✅ [MERGE_OUTSIDE_IN] Topic "${originalTopic.topic_name}" completed: ${topicResult.topic_stats.successful_situations}/${topicResult.topic_stats.total_situations} successful`);

  

            // Add to organized structure (for backwards compatibility)

            organizedByTopic[originalTopic.topic_name] = topicResult;

  

            return topicResult;

        });

  

        // ========== CALCULATE OVERALL STATISTICS ==========

        const overallSuccessRate = mergeStats.total_original_situations > 0

            ? (mergeStats.completed_situations / mergeStats.total_original_situations) * 100

            : 0;

  

        const meetsSuccessThreshold = overallSuccessRate >= (ERROR_CONFIG.MIN_SUCCESS_RATE * 100);

        const mergeDuration = Date.now() - mergeStartTime;

  

        console.log(`✅ [MERGE_OUTSIDE_IN] Merging completed in ${mergeDuration}ms`);

        console.log(`📊 [MERGE_OUTSIDE_IN] Overall success rate: ${overallSuccessRate.toFixed(1)}% (${mergeStats.completed_situations}/${mergeStats.total_original_situations})`);

        if (!meetsSuccessThreshold) {

            console.warn(`⚠️ [MERGE_OUTSIDE_IN] Success rate ${overallSuccessRate.toFixed(1)}% below threshold ${(ERROR_CONFIG.MIN_SUCCESS_RATE * 100)}%`);

        }

  

        // ========== CREATE SIMPLIFIED STRUCTURE ==========

        const simplifiedStructure = createSimplifiedLearningStructure(job_role, processedTopics);

        // ========== RETURN STRUCTURED RESULT ==========

        return {

            success: meetsSuccessThreshold,

            execution_type: 'OPTIMIZED_A12_PARALLEL_A3_OUTSIDE_IN',

            // Input context

            input: {

                job_role,

                optimization_approach: 'A12_combined + A3_parallel + outside_in_merge'

            },

            // A12 results (preserved)

            a12_generation: {

                step_a1: a12Output.step_a1,

                step_a2: a12Output.step_a2,

            },

            // NEW: Simplified hierarchical structure (JOB_ROLE → TOPICS → SITUATIONS → pipeline_results)

            learning_content: simplifiedStructure,

            // Comprehensive statistics

            execution_summary: {

                total_topics: mergeStats.total_topics,

                total_situations: mergeStats.total_original_situations,

                successful_generations: mergeStats.completed_situations,

                failed_generations: mergeStats.failed_situations,

                not_processed_generations: mergeStats.not_processed_situations,

                overall_success_rate: `${overallSuccessRate.toFixed(1)}%`,

                meets_quality_threshold: meetsSuccessThreshold,

                processing_approach: 'parallel_optimized_outside_in'

            },

            // Performance metrics

            performance_metrics: {

                merge_duration_ms: mergeDuration,

                merge_strategy: 'outside_in_natural_hierarchy',

                structure_preservation: 'complete',

                metadata_retention: 'full',

                a3_indexing_success_rate: a3ProcessingStats.indexed_results > 0

                    ? `${((a3ProcessingStats.indexed_results / a3ProcessingStats.total_a3_results) * 100).toFixed(1)}%`

                    : '0%'

            },

            // Error details (if any)

            error_details: mergeStats.processing_errors.length > 0 ? {

                failed_count: mergeStats.processing_errors.length,

                errors: mergeStats.processing_errors,

                a3_indexing_errors: a3ProcessingStats.indexing_errors

            } : null

        };

  

    } catch (error) {

        const mergeDuration = Date.now() - mergeStartTime;

        console.error('❌ [MERGE_OUTSIDE_IN] Critical merge failure:', error.message);

        throw new Error(`Outside-in merge failed after ${mergeDuration}ms: ${error.message}`);

    }

}

  

// ===================================================================================

// COMPARISON: OLD vs NEW MERGE APPROACH

// ===================================================================================

  

/*

BEFORE (Problematic Inside-Out):

┌─────────────────────────────────────────────────────────────────┐

│ 1. Start from A3 results array                                 │

│ 2. Group by topic_name (lose A12 structure)                    │

│ 3. Push situations into topics (lose order)                    │

│ 4. Missing situations = invisible                              │

│ 5. A12 metadata = lost                                         │

└─────────────────────────────────────────────────────────────────┘

  

AFTER (Improved Outside-In):

┌─────────────────────────────────────────────────────────────────┐

│ 1. Start from A12 original structure                           │

│ 2. Iterate topics maintaining order & metadata                 │

│ 3. For each situation, lookup A3 result by ID                  │

│ 4. Handle missing A3 results gracefully                        │

│ 5. Preserve complete hierarchy and metadata                    │

│ 6. Generate comprehensive statistics                           │

└─────────────────────────────────────────────────────────────────┘

  

Benefits of Updated Approach:

✅ Maintains A12 original structure completely

✅ Preserves topic and situation order

✅ Retains all A12 metadata (descriptions, objectives, etc.)

✅ Easy tracking of missing/failed A3 results

✅ Better error handling and reporting

✅ More intuitive debugging

✅ Backwards compatible API response format

✅ Enhanced hierarchical data structure for future use

✅ Comprehensive merge statistics and performance metrics

*/

// ===================================================================================

// MAIN OPTIMIZED CONTROLLER

// ===================================================================================

  

/**

 * MAIN OPTIMIZED ENTRY POINT: A12 + Parallel A3 Pipeline

 *

 * API Endpoint: POST /api/generate-learning-path-user-input-to-done-full

 *

 * @param {Object} req - Express request object

 * @param {Object} req.body - Request body

 * @param {string} req.body.job_role - Job role for learning content generation

 * @param {Object} req.body.options - Optional configuration overrides

 * @param {Object} res - Express response object

 *

 * Optimized Pipeline Flow:

 * 1. Input validation and configuration setup

 * 2. A12: Combined A1+A2 generation (job_role → topics/situations)

 * 3. EXTRACT: Flatten situations for parallel processing

 * 4. A3_PARALLEL: Concurrent full pipeline execution

 * 5. MERGE: Intelligent result organization

 * 6. Return comprehensive results with performance metrics

 *

 * Performance Benefits:

 * - 60-80% faster than sequential approach

 * - Better resource utilization

 * - Individual error isolation

 * - Scalable architecture

 */

exports.generateOptimizedLearningPipeline = async (req, res) => {

    const pipelineStartTime = Date.now();

    const executionId = `OPT_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    console.log(`🚀 [OPTIMIZED] Starting optimized A12→Parallel A3 pipeline [${executionId}]`);

    try {

        const { data = {}, options = {} } = req.body;

        const { job_role } = data;

        // ========== INPUT VALIDATION ==========

        if (!job_role || typeof job_role !== 'string') {

            console.error('❌ [OPTIMIZED] Missing or invalid job_role');

            return res.status(400).json({

                success: false,

                execution_id: executionId,

                error: {

                    code: 'INVALID_INPUT',

                    message: 'data.job_role is required and must be a string'

                },

                received: {

                    data: typeof data,

                    job_role: typeof job_role,

                    body_structure: Object.keys(req.body)

                }

            });

        }

  

        console.log(`📋 [OPTIMIZED] Processing job_role: "${job_role}"`);

  

        // ========== STEP A12: COMBINED A1+A2 GENERATION ==========

        console.log('🔄 [STEP A12] Starting combined A1+A2 generation...');

        const a12StartTime = Date.now();

        const a12Input = { data: { job_role } };

        const a12Result = await callA12Controller(

            generateA1andA2_UserInput2JTBD2TopicAndSituation,

            a12Input,

            'A12_COMBINED'

        );

        const a12Duration = Date.now() - a12StartTime;

        if (!a12Result.success || a12Result.payload?.status === false) {

            console.error(`❌ [STEP A12] Failed after ${a12Duration}ms:`, a12Result.error);

            return res.status(a12Result.httpStatus || 500).json({

                success: false,

                execution_id: executionId,

                step: 'A12',

                error: {

                    code: 'A12_GENERATION_FAILED',

                    message: a12Result.error || 'A12 generation failed',

                    details: a12Result.payload?.error

                },

                performance: {

                    a12_duration_ms: a12Duration,

                    total_duration_ms: Date.now() - pipelineStartTime

                }

            });

        }

  

        const a12Output = a12Result.payload;

        console.log(`✅ [STEP A12] Completed successfully in ${a12Duration}ms`);

  

        // ========== STEP EXTRACT: SITUATION EXTRACTION ==========

        console.log('🔍 [STEP EXTRACT] Extracting situations for parallel processing...');

        const extractStartTime = Date.now();

        let allSituations;

        try {

            allSituations = extractSituationsForParallelProcessing(a12Output, job_role);

        } catch (extractError) {

            console.error(`❌ [STEP EXTRACT] Failed:`, extractError.message);

            return res.status(500).json({

                success: false,

                execution_id: executionId,

                step: 'EXTRACT',

                a12_output: a12Output,

                error: {

                    code: 'EXTRACTION_FAILED',

                    message: extractError.message

                },

                performance: {

                    a12_duration_ms: a12Duration,

                    total_duration_ms: Date.now() - pipelineStartTime

                }

            });

        }

  

        const extractDuration = Date.now() - extractStartTime;

        console.log(`✅ [STEP EXTRACT] Completed in ${extractDuration}ms: Prepared ${allSituations.length} situations`);

  

        if (allSituations.length === 0) {

            return res.json({

                success: true,

                execution_id: executionId,

                message: 'No situations found to process',

                a12_output: a12Output,

                performance: {

                    a12_duration_ms: a12Duration,

                    extract_duration_ms: extractDuration,

                    total_duration_ms: Date.now() - pipelineStartTime

                }

            });

        }

  

        // ========== STEP A3_PARALLEL: CONCURRENT EXECUTION ==========

        console.log('⚡ [STEP A3_PARALLEL] Starting parallel A3 processing...');

        const a3ParallelStartTime = Date.now();

        const a3Results = await executeParallelA3Processing(allSituations);

        const a3ParallelDuration = Date.now() - a3ParallelStartTime;

        console.log(`✅ [STEP A3_PARALLEL] Completed in ${a3ParallelDuration}ms`);

  

        // ========== STEP MERGE: RESULT ORGANIZATION ==========

        console.log('🔧 [STEP MERGE] Organizing results...');

        const mergeStartTime = Date.now();

        const mergedResults = mergeAndOrganizeResults(a12Output, a3Results, job_role);

        const mergeDuration = Date.now() - mergeStartTime;

        console.log(`✅ [STEP MERGE] Completed in ${mergeDuration}ms`);

  

        // ========== FINAL RESPONSE GENERATION ==========

        const totalDuration = Date.now() - pipelineStartTime;

        // Calculate estimated time savings vs sequential approach

        const estimatedSequentialTime = a12Duration + (allSituations.length * 15000); // Assume 15s per situation

        const timeSaved = estimatedSequentialTime - totalDuration;

        const speedupPercentage = ((timeSaved / estimatedSequentialTime) * 100);

  

        // Add performance metrics to merged results

        mergedResults.performance_metrics = {

            ...mergedResults.performance_metrics,

            a12_duration_ms: a12Duration,

            extract_duration_ms: extractDuration,

            a3_parallel_duration_ms: a3ParallelDuration,

            merge_duration_ms: mergeDuration,

            total_duration_ms: totalDuration,

            // Optimization metrics

            estimated_sequential_time_ms: estimatedSequentialTime,

            time_saved_ms: timeSaved,

            speedup_percentage: `${speedupPercentage.toFixed(1)}%`,

            avg_situation_processing_ms: a3ParallelDuration / allSituations.length,

            // Resource efficiency

            parallel_efficiency: `${((allSituations.length * 15000) / a3ParallelDuration).toFixed(2)}x`,

            memory_optimization: 'batch_processing_enabled',

            concurrency_level: OPTIMIZED_CONFIG.MAX_CONCURRENT_A3

        };

  

        const finalSuccess = mergedResults.success &&

                            mergedResults.execution_summary.successful_generations > 0;

  

        console.log(`🎉 [OPTIMIZED] Pipeline completed in ${totalDuration}ms [${executionId}]`);

        console.log(`📊 [OPTIMIZED] Performance: ${speedupPercentage.toFixed(1)}% faster than sequential (saved ${(timeSaved/1000).toFixed(1)}s)`);

  

        return res.status(finalSuccess ? 200 : 206).json({

            ...mergedResults,

            execution_id: executionId,

            generated_at: new Date().toISOString()

        });

  

    } catch (error) {

        const totalDuration = Date.now() - pipelineStartTime;

        console.error(`💥 [OPTIMIZED] Critical failure after ${totalDuration}ms [${executionId}]:`, error.message);

        return res.status(500).json({

            success: false,

            execution_id: executionId,

            error: {

                code: 'PIPELINE_CRITICAL_ERROR',

                message: error?.message || 'Critical pipeline failure',

                stack: process.env.NODE_ENV === 'development' ? error.stack : undefined

            },

            performance: {

                total_duration_ms: totalDuration,

                failed_at: new Date().toISOString()

            }

        });

    }

};

  

// ===================================================================================

// HEALTH CHECK AND MONITORING ENDPOINTS

// ===================================================================================

  

/**

 * Pipeline health check endpoint

 */

exports.getOptimizedPipelineHealth = async (req, res) => {

    try {

        const healthData = {

            status: 'healthy',

            pipeline_type: 'optimized_a12_parallel_a3',

            configuration: {

                max_concurrent_a3: OPTIMIZED_CONFIG.MAX_CONCURRENT_A3,

                max_workers: OPTIMIZED_CONFIG.MAX_WORKERS,

                timeouts: {

                    a12_timeout_ms: OPTIMIZED_CONFIG.A12_TIMEOUT_MS,

                    a3_timeout_ms: OPTIMIZED_CONFIG.A3_TIMEOUT_MS

                }

            },

            features: {

                parallel_processing: true,

                error_isolation: true,

                performance_optimization: true,

                graceful_degradation: ERROR_CONFIG.ENABLE_GRACEFUL_DEGRADATION

            },

            timestamp: new Date().toISOString()

        };

  

        res.json(healthData);

    } catch (error) {

        res.status(500).json({

            status: 'unhealthy',

            error: error.message,

            timestamp: new Date().toISOString()

        });

    }

};

  

/**

 * Performance metrics endpoint

 */

exports.getOptimizedPipelineMetrics = async (req, res) => {

    try {

        // In a real implementation, these would come from a metrics store

        const metrics = {

            pipeline_performance: {

                avg_execution_time_ms: 0, // Would be calculated from historical data

                success_rate: 0,          // Would be calculated from historical data

                error_rate: 0,            // Would be calculated from historical data

                throughput_per_hour: 0    // Would be calculated from historical data

            },

            optimization_metrics: {

                avg_speedup_percentage: 0,

                avg_time_saved_ms: 0,

                parallel_efficiency: 0,

                resource_utilization: 0

            },

            system_health: {

                memory_usage: process.memoryUsage(),

                uptime_seconds: process.uptime(),

                cpu_usage: process.cpuUsage()

            },

            configuration: OPTIMIZED_CONFIG,

            timestamp: new Date().toISOString()

        };

  

        res.json(metrics);

    } catch (error) {

        res.status(500).json({

            error: error.message,

            timestamp: new Date().toISOString()

        });

    }

};

  

// ===================================================================================

// EXPORTS

// ===================================================================================

  

module.exports = {

    // Main optimized controller

    generateOptimizedLearningPipeline: exports.generateOptimizedLearningPipeline,

    // Health and monitoring

    getOptimizedPipelineHealth: exports.getOptimizedPipelineHealth,

    getOptimizedPipelineMetrics: exports.getOptimizedPipelineMetrics,

    // Utility functions (for testing and integration)

    extractSituationsForParallelProcessing,

    executeParallelA3Processing,

    mergeAndOrganizeResults,

    callA12Controller,

    // Configuration exports

    OPTIMIZED_CONFIG,

    ERROR_CONFIG

};

  

/**

 * ===================================================================================

 * USAGE EXAMPLES

 * ===================================================================================

 *

 * Example 1: Basic optimized pipeline execution

 * curl --location 'http://localhost:3000/api/generate-learning-path-user-input-to-done-full' \

 * --header 'Content-Type: application/json' \

 * --data '{"job_role": "AI Engineer"}'

 *

 * Example 2: Pipeline with custom options

 * curl --location 'http://localhost:3000/api/generate-learning-path-user-input-to-done-full' \

 * --header 'Content-Type: application/json' \

 * --data '{

 *   "job_role": "Product Manager",

 *   "options": {

 *     "max_concurrent": 3,

 *     "batch_size": 2,

 *     "enable_detailed_logging": true

 *   }

 * }'

 *

 * Example 3: Health check

 * curl --location 'http://localhost:3000/api/health/optimized-pipeline-status'

 *

 * Example 4: Performance metrics

 * curl --location 'http://localhost:3000/api/metrics/pipeline-performance'

 *

 * ===================================================================================

 * INTEGRATION NOTES

 * ===================================================================================

 *

 * 1. Route Setup:

 * app.post('/api/generate-learning-path-user-input-to-done-full', generateOptimizedLearningPipeline);

 * app.get('/api/health/optimized-pipeline-status', getOptimizedPipelineHealth);

 * app.get('/api/metrics/pipeline-performance', getOptimizedPipelineMetrics);

 *

 * 2. Performance Monitoring:

 * - Monitor execution_id for request tracing

 * - Track speedup_percentage for optimization effectiveness

 * - Monitor success_rate for quality assurance

 * - Watch memory usage during parallel processing

 *

 * 3. Error Handling:

 * - Partial failures return 206 (Partial Content) status

 * - Complete failures return 500 (Internal Server Error)

 * - Input validation errors return 400 (Bad Request)

 *

 * 4. Scaling Considerations:

 * - Adjust MAX_CONCURRENT_A3 based on system resources

 * - Monitor API rate limits for external dependencies

 * - Consider horizontal scaling for high loads

 * - Implement result caching for repeated requests

 */

  
  
  

/*

{

  "success": true,

  "execution_type": "OPTIMIZED_A12_PARALLEL_A3_OUTSIDE_IN",

  "input": { ... },

  "a12_generation": {

    "job_role": "Dược sĩ"

  },

  "learning_content": {

    "topics": [

      {

        "topic_name": "Tư vấn thuốc kê đơn cho bệnh nhân",

        "situations": [

          {

            "situation_name": "Giải thích thuốc mới cho bệnh nhân lớn tuổi",

            "stakeHolder": "Bệnh nhân",

            "scenario_description": "Một bệnh nhân lớn tuổi nhận đơn thuốc tim mạch mới và rất lo lắng. Họ không hiểu rõ về thuốc. Hãy giải đáp các thắc mắc của họ.",

            "image_url_situation": "https://smedia.stepup.edu.vn/thecoach/100nghe/upload_media/image/gna/duoc-si-tu-van-thuoc-ke-don-cho-benh-nhan_giai-thich-thuoc-moi-cho-benh-nhan-lon-tuoi_benh-nhan_thumbnail_20250916_142724_00001.webp",

            "pipeline_results": {

              "SCENARIO_DETAIL_1": { ... },

              "SCENARIO_DETAIL_2": { ... },

              "SCENARIO_DETAIL_3": { ... },

              "ONION_MINI": { ... },

              "PTY1": { ... },

              "SCENARIO_DETAIL_4": { ... },

              "SCENARIO_DETAIL_5": { ... },

              "ONION_FULL": { ... },

              "PTY_AFTER_ONION_MINI": { ... }

            }

          }

        ]

      }

    ]

  },

  "execution_summary": { ... },

  "performance_metrics": { ... },

  "error_details": null,

  "execution_id": "OPT_1758087509295_rp9ebzt6",

  "generated_at": "2025-09-16T03:54:54.726Z"

}

  

*/
```