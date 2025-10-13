def read_log(path='mission_computer_main.log'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise
    except UnicodeDecodeError:
        raise
    except Exception:
        raise
def log2tuple(log):
    lines = log.strip().split('\n')
    pairs = []
    if lines[0] != 'timestamp,event,message':
        raise ValueError
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split(',',2)
        if len(parts) != 3 or len(parts[0]) != 19:
            raise ValueError
        pairs.append((parts[0], parts[2]))
    return pairs
        
def main():
    try:
        log = read_log()
        print(log)
        pairs = log2tuple(log)
        print(pairs)
        spairs = sorted(pairs, key= lambda x: x[0], reverse=True)
        print(spairs)
        ldict = dict(spairs)
        print(ldict)
    except FileNotFoundError:
        print('file open error.')
    except UnicodeDecodeError:
        print('decoding error.')
    except ValueError:
        print('Invalid log format')
    except Exception:
        print('Processing error.')

if __name__=="__main__":
    main()
