def get_macbook_enviroment():
    import subprocess
    try:
        # Execute system_profiler command and capture the output
        output = subprocess.check_output(["system_profiler", "SPHardwareDataType"], universal_newlines=True)

        # Look for the line that contains "Model Name"
        for line in output.splitlines():
            if "Model Name" in line:
                # Check if it's a MacBook Air or MacBook Pro
                if "MacBook Air" in line:
                    return "MacBook Air"
                elif "MacBook Pro" in line:
                    return "MacBook Pro"
                else:
                    return "Unknown MacBook Model"
    except Exception as e:
        return str(e)
