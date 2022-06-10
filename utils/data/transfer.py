import threadpool
import shutil
from pathlib import Path


def copy_data(plist, mode='copy'):
    ps = plist[0]
    pt = plist[1]
    shutil.copyfile(ps, pt)

def copy_data_mkdir(plist, mode='copy'):
    ps = Path(plist[0])
    pt = Path(plist[1])
    if not pt.parent.is_dir():
        pt.parent.mkdir(parents=True, exist_ok=True)
    if not pt.is_file():
        if mode=='move':
            Path.rename(ps, pt)
        else:
            shutil.copyfile(ps, pt)

def write_txt(label_path, text):
    with open(label_path, 'a+') as f:
        f.write(text)
        
    
# def write_file(plist, mode='copy'):
#     ps = plist[0]
#     shutil.copyfile(ps, pt)
    
def run_multithread(input_list, func, thread_num = 10):
    task_pool = threadpool.ThreadPool(thread_num)
    requests = threadpool.makeRequests(func, input_list)
    for req in requests:
        res = task_pool.putRequest(req)
    task_pool.wait()

    
def copy_data_multithread(source_list, target_list, func=copy_data, thread_num = 10):
    input_list = [[source_list[i], target_list[i]] for i in range(len(source_list))]
    run_multithread(input_list, func, thread_num = 10)
    # task_pool=threadpool.ThreadPool(thread_num)
    # requests=threadpool.makeRequests(copy_data, input_list)
    # for req in requests:
    #     res = task_pool.putRequest(req)
    # task_pool.wait()

    
def run_task_multithread(input_list, func=copy_data, thread_num = 10):
    run_multithread(input_list, func, thread_num = 10)

    
    
    