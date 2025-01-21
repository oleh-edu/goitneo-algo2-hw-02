#!/usr/bin/env python

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes the 3D print queue according to printer priorities and limitations

    Args:
        print_jobs: List of print jobs
        constraints: Printer constraints

    Returns:
        Dict with the print order and total time
    """
    # Converting input data to dataclass structures
    jobs = [PrintJob(**job) for job in print_jobs]
    constraints = PrinterConstraints(**constraints)

    # Sort jobs by priority and print time
    jobs.sort(key=lambda job: (job.priority, job.print_time))

    print_order = []
    total_time = 0
    current_volume = 0
    current_batch = []

    for job in jobs:
        # Checking volume and quantity limits
        if current_volume + job.volume <= constraints.max_volume and len(current_batch) < constraints.max_items:
            current_batch.append(job)
            current_volume += job.volume
        else:
            # Completion of the current group
            if current_batch:
                total_time += max(item.print_time for item in current_batch)
                print_order.extend([item.id for item in current_batch])
            # Starting a new group
            current_batch = [job]
            current_volume = job.volume

    # Adding the last group
    if current_batch:
        total_time += max(item.print_time for item in current_batch)
        print_order.extend([item.id for item in current_batch])

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Testing
def test_printing_optimization():
    # Test 1: Models of equal priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 125, "priority": 1, "print_time": 150},
        {"id": "M4", "volume": 180, "priority": 1, "print_time": 180}
    ]

    # Test 2: Models of different priorities
    test2_jobs = [
        {"id": "M1", "volume": 135, "priority": 1, "print_time": 105},
        {"id": "M2", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M3", "volume": 152, "priority": 1, "print_time": 90},
        {"id": "M4", "volume": 120, "priority": 3, "print_time": 150}
    ]

    # Test 3: Exceeding the volume limits
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 209, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 245, "priority": 3, "print_time": 165},
        {"id": "M4", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("[*] Test 1 (equal priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("\n[*] Test 2 (different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("\n[*] Test 3 (exceeding limits):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")

if __name__ == "__main__":
    test_printing_optimization()
