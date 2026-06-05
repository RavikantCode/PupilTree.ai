import threading, queue, time
from main import run

job_queue = queue.Queue()

def worker(worker_id: int):
    while True:
        try:
            job = job_queue.get(timeout=5)
        except queue.Empty:
            break
        try:
            run(job["pdf_path"], output_dir=f"output/{job['job_id']}")
        except Exception as e:
            print(f"[Worker {worker_id}] Failed {job['job_id']}: {e}")
        finally:
            job_queue.task_done()

def enqueue_batch(pdf_paths: list[str], num_workers: int = 5):
    for i, path in enumerate(pdf_paths):
        job_queue.put({"pdf_path": path, "job_id": f"job_{i:03d}"})

    threads = [
        threading.Thread(target=worker, args=(i,), daemon=True)
        for i in range(num_workers)
    ]
    for t in threads:
        t.start()

    job_queue.join()
