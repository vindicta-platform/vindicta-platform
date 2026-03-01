import asyncio
import sys

# Adjust path to find src
import os

sys.path.append(os.path.join(os.getcwd(), "src"))

from vindicta_agents.telemetry.monitor import HardwareMonitor


async def main():
    print("Starting Hardware Monitor Verification...")
    monitor = HardwareMonitor(polling_interval=1.0)

    def on_update(state):
        print("\n--- Hardware State Update ---")
        print(f"Timestamp: {state.timestamp}")
        print(f"CPU Total: {state.cpu.total_percent}%")
        print(f"Memory Used: {state.memory.percent}%")
        for gpu in state.gpus:
            print(
                f"GPU {gpu.id} ({gpu.name}): {gpu.load * 100:.1f}% Load, {gpu.temperature}C"
            )

    monitor.register_callback(on_update)
    monitor.start()

    print("Monitor started. Waiting for 3 seconds...")
    await asyncio.sleep(3.5)

    monitor.stop()
    print("Monitor stopped.")


if __name__ == "__main__":
    asyncio.run(main())
