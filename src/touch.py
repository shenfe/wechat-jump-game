from subprocess import call


def run(ms):
    call(["adb", "shell", "input", "swipe", "300", "1000", "300", "1000", str(int(ms))])
