#!/usr/bin/env python3
"""
GPA Calculator

This script calculates and analyzes Grade Point Averages (GPA) from course data.
It can process course results, calculate current GPA, and provide recommendations
for grade improvement through retaking courses.

Usage:
    python gpa-calculator.py <input_file>

Input file format (CSV):
    course_code,credits,grade
    Example: CSE101,3,A

Grades should be one of: A, A-, B+, B, B-, C+, C, C-, D+, D, E, F, WH (Withheld), NC (Not Completed), CM (Completed Module)
"""

import sys

# Mapping of letter grades to their corresponding grade points
grade_points = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "E": 0.0,
    "F": 0.0,
    "WH": 0.0,  # Withheld
    "NC": 0.0,  # Not Completed
    "CM": 0.0,  # Completed Module
}

# Set of grades that should be considered for retaking (D and below)
grade_points_should_retake = {"D", "D+", "E", "F", "WH", "NC"}

# Set of failing grades that must be retaken (F, E, WH, NC)
grade_points_must_retake = {"F", "E", "WH", "NC"}


def parse_courses(file_path):
    """
    Parse a CSV file containing course information into a list of course dictionaries.

    Args:
        file_path (str): Path to the input CSV file

    Returns:
        list: List of dictionaries, each containing course code, credits, and result

    Exits with error code 1 if:
        - File is not found
        - No valid course entries are found
        - Any other file reading error occurs
    """
    courses = []
    line_number = 0
    try:
        with open(file_path, "r") as file:
            for line in file:
                line_number += 1
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    # Try to split by comma and strip whitespace
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) < 3:  # Check if we have all required parts
                        print(
                            f"Warning: Invalid format on line {line_number}, skipping: {line}"
                        )
                        continue
                    code = parts[0]
                    credits = parts[1]
                    result = parts[2]
                    courses.append(
                        {
                            "code": code,
                            "credits": int(credits) if credits.isdigit() else 0,
                            "result": result.upper(),  # Convert grade to uppercase
                        }
                    )
                except (ValueError, IndexError) as e:
                    print(
                        f"Warning: Could not parse line {line_number}, skipping: {line}"
                    )
                    continue

        if not courses:
            print("Error: No valid course entries found in the file.")
            sys.exit(1)

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return courses


def calculate_gpa(courses, exclude_codes=None):
    """
    Calculate the Grade Point Average (GPA) from a list of courses.

    Args:
        courses (list): List of course dictionaries with 'code', 'credits', and 'result' keys
        exclude_codes (list, optional): List of course codes to exclude from calculation

    Returns:
        float: The calculated GPA, or 0 if no valid courses are provided
    """
    total_grade_points = 0
    total_credits = 0

    for course in courses:
        if exclude_codes and course["code"] in exclude_codes:
            continue
        grade = course["result"]
        credits = course["credits"]
        total_grade_points += grade_points.get(grade, 0) * credits
        total_credits += credits

    # Avoid division by zero
    return total_grade_points / total_credits if total_credits > 0 else 0


def analyze_grades(courses):
    """
    Analyze course grades and provide recommendations for improvement.

    Args:
        courses (list): List of course dictionaries with 'code', 'credits', and 'result' keys

    Returns:
        dict: Dictionary containing:
            - current_gpa: Current GPA based on all courses
            - gpa_after_retaking_failed: Projected GPA if failing courses are retaken
            - must_retake: List of courses that must be retaken (F, E, WH, NC)
            - should_retake: List of courses that should be considered for retaking (D and below)
    """
    # Find failing grades that need to be redone
    must_retake = [c for c in courses if c["result"] in grade_points_must_retake]

    # Find low grades that should be considered for retaking (only D, D+, E, F, WH, NC)
    should_retake = [c for c in courses if c["result"] in grade_points_should_retake]

    # Sort by credits (highest first) then by grade (worst first)
    must_retake.sort(key=lambda x: (-x["credits"], grade_points.get(x["result"], 0)))
    should_retake.sort(key=lambda x: (-x["credits"], grade_points.get(x["result"], 0)))

    # Calculate potential GPAs
    current_gpa = calculate_gpa(courses)

    # Calculate GPA after retaking only failed courses (assuming D grades)
    failed_codes = [c["code"] for c in must_retake]
    gpa_after_retaking_failed = calculate_gpa(
        [c for c in courses if c["code"] not in failed_codes]
        + [
            {"code": c["code"], "credits": c["credits"], "result": "D"}
            for c in must_retake
        ]
    )

    return {
        "current_gpa": current_gpa,
        "gpa_after_retaking_failed": gpa_after_retaking_failed,
        "must_retake": must_retake,
        "should_retake": should_retake,
    }


def print_current_gpa(current_gpa):
    """Print the current GPA."""
    if current_gpa is not None:
        print(f"Your CURRENT GPA is: {current_gpa:.3f}")


def print_potential_gpa_after_retaking_failed(current_gpa, potential_gpa):
    """Print the potential GPA after retaking failed courses."""
    if potential_gpa is not None and current_gpa is not None:
        print(
            f"POTENTIAL GPA (after retaking failed): {potential_gpa:.3f} "
            f"(+{potential_gpa - current_gpa:.3f})"
        )


def print_must_retake_courses(must_retake):
    """Print the list of courses that must be retaken."""
    if must_retake:
        print("\nMUST RETAKE (Failing/Incomplete):")
        print("-" * 40)
        for course in must_retake:
            print(
                f"- {course['code']} (Current: {course['result']}, "
                f"Credits: {course['credits']})"
            )


def print_recommended_retake_courses(should_retake, courses, current_gpa):
    """Print the list of courses recommended for retaking."""
    if should_retake:
        print("\nRECOMMENDED TO RETAKE (Grades below C-):")
        print("-" * 40)
        for course in should_retake:
            new_gpa = calculate_gpa(courses, exclude_codes=[course["code"]])
            total_credits = sum(c["credits"] for c in courses)
            potential_gpa = (
                new_gpa * (total_credits - course["credits"])
                + grade_points["D"] * course["credits"]
            ) / total_credits
            improvement = potential_gpa - current_gpa

            print(
                f"- {course['code']} (Current: {course['result']}, "
                f"Credits: {course['credits']})"
            )
            print(f"  Potential GPA: {potential_gpa:.3f} (+{improvement:.3f})")


def print_gpa_analysis(result, courses):
    """Print the complete GPA analysis."""
    print_current_gpa(result["current_gpa"])
    print_potential_gpa_after_retaking_failed(
        result["current_gpa"], result["gpa_after_retaking_failed"]
    )
    print_must_retake_courses(result["must_retake"])
    print_recommended_retake_courses(
        result["should_retake"], courses, result["current_gpa"]
    )


if __name__ == "__main__":
    # Check if a file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python gpa_calculator.py <courses_file>")
        sys.exit(1)

    # Parse the courses from the file and analyze grades
    courses = parse_courses(sys.argv[1])
    result = analyze_grades(courses)

    # Print the complete GPA analysis
    print_gpa_analysis(result, courses)
