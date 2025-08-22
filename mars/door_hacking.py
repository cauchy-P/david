import binascii
import itertools
import multiprocessing
import os
import time
import zipfile

def init_keys(passwd):
    keys = [0x12345678, 0x23456789, 0x34567890]
    for p in passwd:
        update_keys(keys, ord(p))
    return keys

def update_keys(keys, ch):
    keys[0] = binascii.crc32(bytes([ch]), keys[0]) & 0xffffffff
    keys[1] = (keys[1] + (keys[0] & 0xff)) & 0xffffffff
    keys[1] = (keys[1] * 134775813 + 1) & 0xffffffff
    ch2 = (keys[1] >> 24) & 0xff
    keys[2] = binascii.crc32(bytes([ch2]), keys[2]) & 0xffffffff

def decrypt_byte(keys):
    temp = keys[2] | 2
    return ((temp * (temp ^ 1)) >> 8) & 0xff

def check_password(passwd, enc_header, expected):
    keys = init_keys(passwd)
    decrypted = []
    for byte in enc_header:
        db = decrypt_byte(keys)
        plain = byte ^ db
        decrypted.append(plain)
        update_keys(keys, plain)
    return decrypted[11] == expected

def get_zip_info(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        info = zf.infolist()[0]
        flag = info.flag_bits
        bit3 = flag & 0x8
        crc = info.CRC
        mod_time = info._raw_time
        if bit3:
            expected = (mod_time >> 8) & 0xff
        else:
            expected = (crc >> 24) & 0xff
        header_offset = info.header_offset
        with open(zip_path, 'rb') as fp:
            fp.seek(header_offset)
            local_header = fp.read(30)
            name_len = int.from_bytes(local_header[26:28], 'little')
            extra_len = int.from_bytes(local_header[28:30], 'little')
            file_offset = header_offset + 30 + name_len + extra_len
            fp.seek(file_offset)
            enc_header_bytes = fp.read(12)
            enc_header = [b for b in enc_header_bytes]
        return enc_header, expected, info

def worker(args):
    prefix, enc_header, expected, freq_chars, queue, start_time = args
    process_name = multiprocessing.current_process().name
    attempt = 0
    for comb in itertools.product(freq_chars, repeat=5):
        passwd = prefix + ''.join(comb)
        attempt += 1
        if check_password(passwd, enc_header, expected):
            queue.put(passwd)
            elapsed = time.time() - start_time
            print(f'Candidate found by {process_name}: {passwd}, Attempts: {attempt}, Elapsed: {elapsed:.2f} s')
        if attempt % 1000000 == 0:
            elapsed = time.time() - start_time
            print(f'{process_name} Attempts: {attempt}, Elapsed: {elapsed:.2f} s')

    return None

def unlock_zip():
    zip_path = 'emergency_storage_key.zip'
    try:
        enc_header, expected, info = get_zip_info(zip_path)
    except FileNotFoundError:
        print(f'Error: Zip file {zip_path} not found.')
        return
    except Exception as e:
        print(f'Unexpected error getting zip info: {e}')
        return
    freq_chars = 'etaoinshrdlcumwfgpybvkxqjz0123456789'
    start_time = time.time()
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    cpu_count = os.cpu_count()
    pool = multiprocessing.Pool(processes=cpu_count)
    args_list = [(prefix, enc_header, expected, freq_chars, queue, start_time) for prefix in freq_chars]
    results = pool.map_async(worker, args_list)
    found = None
    last_progress_time = 0
    while True:
        if not queue.empty():
            candidate = queue.get()
            with zipfile.ZipFile(zip_path) as zf:
                try:
                    content = zf.read(info.filename, pwd=candidate.encode())
                    computed_crc = binascii.crc32(content) & 0xffffffff
                    if computed_crc == info.CRC:
                        found = candidate
                        elapsed = time.time() - start_time
                        print(f'Success! Password: {found}, Total time: {elapsed:.2f} s')
                        with open('password.txt', 'w') as f:
                            f.write(found)
                        break
                    else:
                        print(f'False positive: {candidate}, bad CRC')
                except RuntimeError as e:
                    if 'Bad password' in str(e):
                        print(f'False positive: {candidate}, bad password')
                    else:
                        raise
                except Exception as e:
                    print(f'Error testing {candidate}: {e}')
        if results.ready():
            break
        time.sleep(0.1)
        elapsed = time.time() - start_time
        if elapsed - last_progress_time >= 60:
            print(f'Progress check, Elapsed: {elapsed:.2f} s')
            last_progress_time = elapsed

    pool.terminate()
    pool.join()
    if not found:
        print('Password not found.')

if __name__ == '__main__':
    unlock_zip()