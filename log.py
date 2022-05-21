def log(var):
	print(f"\033[0;32m[LOG]:\033[0m {var}")

def info(var):
	print(f"\033[0;36m[INFO]:\033[0m {var}")

def error(var):
	print(f"\033[0;33m[ERROR]:\033[0m {var}")

def warn(var):
	print(f"\033[0;31m[WARNING]:\033[0m {var}")

def crit(var):
	print(f"\033[5;35;40m[CRITICAL]:\033[0m {var}")
