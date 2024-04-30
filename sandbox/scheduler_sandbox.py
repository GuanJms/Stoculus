import os
from sandbox.scheduler_run_test.printer import Printer
def main():
    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        print(f"Secret Key: {secret_key}")
    else:
        print("SECRET_KEY not set.")

    p = Printer(input_data=secret_key)
    p.print_data()
    print("Done.")

if __name__ == "__main__":
    main()
