import subprocess
import time
from multiprocessing import Process, Value

def call(type, command, f, c):
    now = time.time()
    status = subprocess.check_output(command, shell=True)
    elapsed = time.time() - now
    print("%s took %s ms." % (type, round(elapsed * 1000, 2)))
    c.value = c.value + 1
    if status != '200':
        print("Status: %s" % status)
        f.value = f.value + 1

def run(f1, c1, f2, c2, f3, c3):
    p1 = Process(target=call, args=("profile", "curl --write-out %{http_code} --silent --output /dev/null steam.murgo.iki.fi/backend/profiles/murgonen", f1, c1))
    p2 = Process(target=call, args=("profilegame", "curl --write-out %{http_code} --silent --output /dev/null steam.murgo.iki.fi/backend/profiles/murgonen/games", f2, c2))
    p3 = Process(target=call, args=("game", "curl --write-out %{http_code} --silent --output /dev/null steam.murgo.iki.fi/backend/games/105600", f3, c3))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

if __name__ == '__main__':
    import multiprocessing
    profilefails = Value('i', 0)
    profilecalls = Value('i', 0)
    profilegamesfails = Value('i', 0)
    profilegamescalls = Value('i', 0)
    gamesfails = Value('i', 0)
    gamescalls = Value('i', 0)

    processes = []
    now = time.time()
    for i in xrange(40):
        p = Process(target=run, args=(profilefails, profilecalls, profilegamesfails, profilegamescalls, gamesfails, gamescalls))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    elapsed = time.time() - now
    print "%s out of %s profile calls failed" % (profilefails.value, profilecalls.value)
    print "%s out of %s profile games calls failed" % (profilegamesfails.value, profilegamescalls.value)
    print "%s out of %s games calls failed" % (gamesfails.value, gamescalls.value)

    totalcalls = profilecalls.value + profilegamescalls.value + gamescalls.value
    print "%s calls took %s ms (avg. %s ms per call)." % (totalcalls, round(elapsed * 1000, 2), round(elapsed * 1000 / totalcalls, 2))

