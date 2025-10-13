def read_log(path = 'mission_computer_main.log'):
    try:
        with open(path, 'r', encoding = 'utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise
    except UnicodeDecodeError:
        raise
    except Exception:
        raise
def log2tuple(log):
    logs = log.strip().split('\n')
    if logs[0] != 'timestamp,event,message':
        raise ValueError
    pairs = []
    for line in logs[1:]:
        if line.strip():
            parts = line.split(',', 2)
            if len(parts) != 3:
                raise ValueError
            if len(parts[0]) != 19:
                raise ValueError
            pairs.append((parts[0], parts[2]))
    return pairs
def sort_log(tuples):
    return sorted(tuples, key=lambda x:x[0], reverse= True)
def main():
    try:
    
        log = read_log()
        print(log)
        tuples = log2tuple(log)
        print(tuples)
        sorted_tuples = sort_log(tuples)
        print(sorted_tuples)
        dict_log = dict(sorted_tuples)
        print(dict_log)
    except FileNotFoundError:
        print("File open error.")
    except UnicodeDecodeError:
        print("Decoding error.")
    except ValueError:
        print("Invalid log format.")
    except Exception:
        print("Processing Error.")
    finally:
        return

if __name__ == "__main__":
    main()