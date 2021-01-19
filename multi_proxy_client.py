from multiprocessing import Pool
def main():
    with Pool() as p:
        p.map(connect, address * 10)

        p = Process(target=handle_echo, args=(addr,conn))
        p.daemon()
        p.start()