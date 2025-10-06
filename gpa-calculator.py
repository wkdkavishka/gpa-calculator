import sys

# Grade points mapping
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


def parse_courses(file_path):
    """Parse the courses file into a list of dictionaries."""
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
                        print(f"Warning: Invalid format on line {line_number}, skipping: {line}")
                        continue
                    code = parts[0]
                    credits = parts[1]
                    result = parts[2]
                    courses.append({
                        "code": code,
                        "credits": int(credits) if credits.isdigit() else 0,
                        "result": result.upper()  # Convert grade to uppercase
                    })
                except (ValueError, IndexError) as e:
                    print(f"Warning: Could not parse line {line_number}, skipping: {line}")
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
    """Calculate GPA from a list of courses, optionally excluding some course codes."""
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
    """Analyze grades and suggest improvements."""
    # Find failing grades that need to be redone
    must_retake = [c for c in courses if c["result"] in ["F", "E", "WH", "NC"]]

    # Find low grades that should be considered for retaking (only D, D+, E, F, WH, NC)
    should_retake = [c for c in courses if c["result"] in ["D", "D+", "E", "F", "WH", "NC"]]

    # Sort by credits (highest first) then by grade (worst first)
    must_retake.sort(key=lambda x: (-x["credits"], grade_points.get(x["result"], 0)))
    should_retake.sort(key=lambda x: (-x["credits"], grade_points.get(x["result"], 0)))

    # Calculate potential GPAs
    current_gpa = calculate_gpa(courses)

    # Calculate GPA after retaking only failed courses (assuming D grades)
    failed_codes = [c["code"] for c in must_retake]
    gpa_after_failed = calculate_gpa(
        [c for c in courses if c["code"] not in failed_codes]
        + [
            {"code": c["code"], "credits": c["credits"], "result": "D"}
            for c in must_retake
        ]
    )

    # Calculate GPA after retaking both failed and recommended (assuming D grades)
    recommended_codes = [c["code"] for c in should_retake]
    all_retake_codes = list(set(failed_codes + recommended_codes))
    gpa_after_all = calculate_gpa(
        [c for c in courses if c["code"] not in all_retake_codes]
        + [
            {"code": c["code"], "credits": c["credits"], "result": "D"}
            for c in must_retake + should_retake
            if c["code"] in all_retake_codes
        ]
    )

    # Print GPA projections
    print(f"\nCURRENT GPA: {current_gpa:.3f}")
    print(
        f"POTENTIAL GPA (after retaking failed): {gpa_after_failed:.3f} (+{gpa_after_failed - current_gpa:.3f})"
    )
    print(
        f"POTENTIAL GPA (after all retakes): {gpa_after_all:.3f} (+{gpa_after_all - current_gpa:.3f})"
    )

    # Print must-retake courses
    if must_retake:
        print("\nMUST RETAKE (Failing/Incomplete):")
        print("-" * 40)
        for course in must_retake:
            print(
                f"- {course['code']} (Current: {course['result']}, Credits: {course['credits']})"
            )

    # Print recommended retakes
    if should_retake:
        print("\nRECOMMENDED TO RETAKE (Grades below C-):")
        print("-" * 40)
        for course in should_retake[:10]:  # Top 10 recommendations
            new_gpa = calculate_gpa(courses, exclude_codes=[course["code"]])
            potential_gpa = (
                new_gpa * (sum(c["credits"] for c in courses) - course["credits"])
                + grade_points["D"] * course["credits"]
            ) / sum(c["credits"] for c in courses)
            improvement = potential_gpa - current_gpa

            print(
                f"- {course['code']} (Current: {course['result']}, Credits: {course['credits']})"
            )
            print(f"  Potential GPA: {potential_gpa:.3f} (+{improvement:.3f})")


if __name__ == "__main__":
    # Check if a file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python gpa_calculator.py <courses_file>")
        sys.exit(1)

    # Parse the courses from the file
    courses = parse_courses(sys.argv[1])

    # Calculate and print the GPA
    gpa = calculate_gpa(courses)
    print(f"\nYour Current GPA is: {gpa:.2f}")

    # Analyze grades and suggest improvements
    analyze_grades(courses)
