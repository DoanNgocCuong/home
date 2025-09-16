
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

