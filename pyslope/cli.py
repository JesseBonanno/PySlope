import subprocess


def run_django_server():
    try:
        subprocess.run(["python", "manage.py", "migrate"])
        subprocess.run(["python", "manage.py", "collectstatic"])
        subprocess.run(["python", "manage.py", "runserver"])
    except KeyboardInterrupt:
        print("Django server stopped.")


def cli():
    run_django_server()
    if __name__ == "__main__":
        cli()
