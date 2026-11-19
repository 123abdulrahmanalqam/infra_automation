import json
import subprocess
from src.machine import Machine, logger

def get_machines():
    valid_os = ["linux", "ubuntu", "centos", "windows", "macos"]
    machines = []
    
    while True:
        name = input("Enter machine name (or 'f' to finish): ").strip()
        if name.lower() == "f":
            break
        if not name:
            print("[ERROR] Machine name cannot be empty.")
            continue

        os = input("Enter OS (Linux/Ubuntu/CentOS/Windows/macOS): ").strip()
        if os.lower() not in valid_os:
            print(f"[ERROR] Invalid OS. Choose from: {', '.join(valid_os)}")
            continue

        try:
            cpu = int(input("Enter CPU cores (positive integer): "))
            ram = int(input("Enter RAM in GB (positive integer): "))
            if cpu <= 0 or ram <= 0:
                print("[ERROR] CPU and RAM must be greater than 0.")
                continue
        except ValueError:
            print("[ERROR] CPU and RAM must be valid numbers.")
            continue

        machine = Machine(name, os, cpu, ram)
        machines.append(machine.to_dict())
        
    return machines

def run_setup_script():
    try:
        logger.info("Executing service installation Bash script...")
        subprocess.run(["bash", "scripts/setup_nginx.sh"], check=True)
        logger.info("Service installation completed successfully.")
        print("The installation of nginx is completed successfully!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Bash script failed with exit code {e.returncode}: {e}")
        print(f"[ERROR] failed to install Nginx: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during script execution: {e}")
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    logger.info("=== Provisioning started ===")
    try:
        machines = get_machines()
        if machines:
            with open("configs/instances.json", "w") as f:
                json.dump(machines, f, indent=4)
            logger.info(f"Successfully saved {len(machines)} machine(s) to configs/instances.json.")
            run_setup_script()
        else:
            logger.info("No machines were entered. Skipping configuration and installation.")
    except Exception as e:
        logger.error(f"Provisioning process failed: {e}")
        print(f"[ERROR] Provisioning failed: {e}")
    finally:
        logger.info("=== Provisioning finished ===")
