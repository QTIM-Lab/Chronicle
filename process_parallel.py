import os, math, pdb, time
import subprocess
import multiprocessing



IMAGES_DB_and_DATAFOLDER_KEY={
    "axispacs": '/persist/PACS/DICOM',
    "forum": '/persist/PACS/forum',
    "forum_all": '/persist/PACS/forum_all',
    "imagepools": '/persist/PACS/imagepools',
}

IMAGES_DB = 'forum_all'
DATAFOLDER = IMAGES_DB_and_DATAFOLDER_KEY[IMAGES_DB]




# URL and dbname
COUCHDB_USER="admin"
COUCHDB_PASSWORD="password_qtim"
url=f"http://{COUCHDB_USER}:{COUCHDB_PASSWORD}@localhost:5984"

directories = os.listdir(DATAFOLDER)

def process_directory(dir=""):
    cmd = ['/persist/python_virtual_environments/bearceb/.pyenv/shims/python', './bin/record.py', os.path.join(DATAFOLDER, dir), '--url', url, '--dbName', IMAGES_DB, '--dontAttachOriginals']
    # print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


pool = multiprocessing.Pool(15)
start_time = time.perf_counter()
processes = [pool.apply_async(process_directory, args=(x,)) for x in directories]
result = [p.get() for p in processes]
finish_time = time.perf_counter()
print(f"Program finished in {finish_time-start_time} seconds")
print(result)


# def process_directory(dir=""):
#     cmd = ['/home/bearceb/.local/share/pdm/venvs/Chronicle-FgmQ98C8-Chronicle/bin/python', './bin/record.py', os.path.join(DATAFOLDER, dir), '--url', url, '--dbName', IMAGES_DB]
#     print(cmd)
#     os.system(" ".join(cmd))
#     # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     # stdout, stderr = process.communicate()

# section = math.floor(len(directories)/10)
# dir = directories[0]
# for dir in directories[0*section:1*section]:
#     cmd = ['/home/bearceb/.local/share/pdm/venvs/Chronicle-FgmQ98C8-Chronicle/bin/python', './bin/record.py', os.path.join(DATAFOLDER, dir), '--url', url, '--dbName', IMAGES_DB]
#     os.system(" ".join(cmd))
# directories[1*section:2*section]
# directories[2*section:3*section]
# directories[3*section:4*section]
# directories[4*section:5*section]
# directories[5*section:6*section]
# directories[6*section:7*section]
# directories[7*section:8*section]
# directories[8*section:9*section]
# directories[9*section:10*section]
# directories[10*section:11*section]

