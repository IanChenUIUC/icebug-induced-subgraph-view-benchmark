def reset_peak():
    """Reset VmHWM down to current VmRSS, so peak_mb() reflects only what follows."""
    with open("/proc/self/clear_refs", "w") as f:
        f.write("5")


def peak_mb():
    with open("/proc/self/status") as f:
        for line in f:
            if line.startswith("VmHWM:"):
                return int(line.split()[1]) / 1024
