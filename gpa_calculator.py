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
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Split by comma and trim whitespace
                code, credits, result = line.strip().split(",")
                courses.append(
                    {"code": code, "credits": int(credits), "result": result}
                )
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
    must_retake = [c for c in courses if c["result"] in ["F", "E", "WH"]]

    # Find low grades that should be considered for retaking (only D, D+, E, F, WH)
    should_retake = [c for c in courses 
                    if c["result"] in ["D", "D+", "E", "F", "WH"]]

    # Sort by credits (highest first) then by grade (worst first)
    must_retake.sort(key=lambda x: (-x["credits"], grade_points.get(x["result"], 0)))
    should_retake.sort(key=lambda x: (-x["credits"], grade_points.get(x["result"], 0)))

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
        print("\nRECOMMENDED TO RETAKE (For GPA Improvement):")
        print("-" * 40)
        for course in should_retake[:10]:  # Top 10 recommendations
            current_gpa = calculate_gpa(courses)
            new_gpa = calculate_gpa(courses, exclude_codes=[course["code"]])
            potential_gpa = (
                new_gpa * (sum(c["credits"] for c in courses) - course["credits"])
                + grade_points["A"] * course["credits"]
            ) / sum(c["credits"] for c in courses)
            improvement = potential_gpa - current_gpa

            print(
                f"- {course['code']} (Current: {course['result']}, Credits: {course['credits']})"
            )
            print(f"  Potential GPA Improvement: +{improvement:.3f}")


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
