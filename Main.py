import json
import csv
import math
import statistics
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google import genai


FILE = "jee_data.json"
CSV_FILE = "jee_data.csv"



# DATA MANAGEMENT


def load_data():

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        return []


def save_data(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)



# ADD TEST


def add_test():

    data = load_data()

    print("\n===== ADD NEW TEST =====")

    date = input(
        "Enter test date (YYYY-MM-DD), or press Enter for today: "
    )

    if date == "":
        date = datetime.date.today().isoformat()

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date!")
        return

    try:

        physics = float(input("Physics marks (0-100): "))
        chemistry = float(input("Chemistry marks (0-100): "))
        maths = float(input("Maths marks (0-100): "))

        marks = [physics, chemistry, maths]

        if any(math.isnan(x) or math.isinf(x) for x in marks):
            print("Invalid marks!")
            return

        if any(x < 0 or x > 100 for x in marks):
            print("Marks must be between 0 and 100!")
            return

    except ValueError:
        print("Enter valid numerical marks!")
        return

    total = sum(marks)

    record = {

        "date": date,

        "physics": physics,

        "chemistry": chemistry,

        "maths": maths,

        "total": total,

        "percentage": (total / 300) * 100

    }

    data.append(record)

    data.sort(key=lambda x: x["date"])

    save_data(data)

    print("\nTest successfully saved!")

    print("Total Marks:", total, "/ 300")


# CSV EXPORT


def export_csv():

    data = load_data()

    if not data:
        print("No records available!")
        return

    with open(CSV_FILE, "w", newline="") as f:

        writer = csv.DictWriter(f,fieldnames=data[0].keys())

        writer.writeheader()

        writer.writerows(data)

    print("CSV exported successfully!")



# HISTORY


def show_history():

    data = load_data()

    if not data:
        print("No test history found!")
        return

    df = pd.DataFrame(data)

    print("\n========== TEST HISTORY ==========")

    print(df.to_string(index=False))



# PERFORMANCE ANALYSIS


def analyse():

    data = load_data()

    if not data:
        print("No data available!")
        return

    df = pd.DataFrame(data)

    totals = df["total"].to_numpy()

    physics = df["physics"].to_numpy()

    chemistry = df["chemistry"].to_numpy()

    maths = df["maths"].to_numpy()

    latest = totals[-1]

    print("\n========== PERFORMANCE REPORT ==========")

    print("Total Tests:", len(data))

    print("Latest Score:", latest, "/ 300")

    print(
        "Overall Average:",
        round(statistics.mean(totals), 
2)
    )

    print(
        "Highest Score:",
        max(totals)
    )

    print(
        "Lowest Score:",
        min(totals)
    )

    print("\n========== SUBJECT ANALYSIS ==========")

    print(
        "Physics Average:",
        round(statistics.mean(physics), 
2)
    )

    print(
        "Chemistry Average:",
        round(statistics.mean(chemistry), 2)
    )

    print(
        "Maths Average:",
        round(statistics.mean(maths), 2)
    )

    # Previous average comparison

    if len(totals) > 1:

        previous_average = statistics.mean(totals[:-1])

        difference = latest - previous_average

        print("\n========== PROGRESS ==========")

        print(
            "Previous Average:",
            round(previous_average, 2)
        )

        print("Latest Score:", latest)

        print(
            "Difference:",
            round(difference, 2)
        )

        if difference > 0:

            progress = (difference / previous_average) * 100

            print(
                "Improvement:",
                round(progress, 2),
                "%"
            )

        elif difference < 0:

            decline = abs(difference) / previous_average * 100

            print(
                "Decline:",
                round(decline, 2),
                "%"
            )

        else:
            print("Performance unchanged.")

    else:

        print(
            "\nAdd another test to calculate progress "
            "against your previous average."
        )

    # Current status

    print("\n========== CURRENT STATUS ==========")

    if len(totals) >= 3:

        recent_average = statistics.mean(totals[-3:])

        print(
            "Recent 3-Test Average:",
            round(recent_average, 2)
        )

        if len(totals) > 3:

            old_average = statistics.mean(totals[:-3])

            if recent_average > old_average:
                print("Status: IMPROVING")

            elif recent_average < old_average:
                print("Status: DECLINING")

            else:
                print("Status: STABLE")

        else:
            print("Status: More tests needed.")

    else:

        print("Status: Insufficient data.")

    print("\nAnalysis completed!")


# -------------------------------
# GRAPHS
# -------------------------------

def show_graphs():

    data = load_data()

    if not data:
        print("No data available!")
        return

    df = pd.DataFrame(data)

    dates = df["date"]

    # GRAPH 1: TOTAL MARKS

    plt.figure(figsize=(10, 5))

    plt.plot(
        dates,
        df["total"],
        marker="o",
        label="Total Marks"
    )

    plt.axhline(
        df["total"].mean(),
        linestyle="--",
        label="Overall Average"
    )

    plt.title("JEE Total Marks Progress")

    plt.xlabel("Test Date")

    plt.ylabel("Marks / 300")

    plt.legend()

    plt.grid(True)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # GRAPH 2: SUBJECT COMPARISON

    plt.figure(figsize=(10, 5))

    plt.plot(
        dates,
        df["physics"],
        marker="o",
        label="Physics"
    )

    plt.plot(
        dates,
        df["chemistry"],
        marker="o",
        label="Chemistry"
    )

    plt.plot(
        dates,
        df["maths"],
        marker="o",
        label="Maths"
    )

    plt.title("Subject-wise Progress")

    plt.xlabel("Test Date")

    plt.ylabel("Marks / 100")

    plt.legend()

    plt.grid(True)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # GRAPH 3: SUBJECT AVERAGES

    subjects = [
        "Physics",
        "Chemistry",
        "Maths"
    ]

    averages = [
        df["physics"].mean(),
        df["chemistry"].mean(),
        df["maths"].mean()
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(subjects, averages)

    plt.title("Average Subject Performance")

    plt.ylabel("Average Marks")

    plt.ylim(0, 100)

    plt.grid(axis="y")

    plt.show()



# GEMINI AI ANALYSER


def gemini_analysis():

    data = load_data()

    if len(data) < 2:

        print("Add at least two tests first!")

        return

    df = pd.DataFrame(data)

    api_key = input(
        "\nEnter your Gemini API key: "
    ).strip()

    if not api_key:
        print("API key required!")
        return

    client = genai.Client(api_key=api_key)

    latest = df.iloc[-1]

    previous_avg = df.iloc[:-1]["total"].mean()

    recent_avg = df.tail(3)["total"].mean()

    prompt = f"""

You are an expert JEE preparation analyst.

Analyse the following student's performance.

TEST HISTORY:

{df.to_string(index=False)}

LATEST TEST:

Physics: {latest['physics']}
Chemistry: {latest['chemistry']}
Maths: {latest['maths']}

Latest Total: {latest['total']}/300

Previous Test Average: {previous_avg:.2f}

Recent Average: {recent_avg:.2f}

Your tasks:

1. Analyse the student's current preparation status.

2. Identify strong and weak subjects.

3. Identify subjects where marks are declining.

4. Compare latest marks with previous average.

5. Explain the student's progress.

6. Give 5 practical study tips.

7. Suggest subject-wise improvement strategies.

8. Suggest what the student should focus on
   during the next 7 days.

9. Identify possible preparation problems.

10. Give an honest and realistic assessment.

IMPORTANT:

Do not make unsupported predictions about JEE rank
or percentile from mock test marks.

Use clear headings and actionable advice.

"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        print("\n========== GEMINI AI REPORT ==========\n")

        print(response.text)

    except Exception as e:

        print("Gemini API error:", e)




# MAIN MENU


def main():

    while True:

        print("\n")
        print("=" * 45)

        print("       JEE PERFORMANCE ANALYSER")

        print("=" * 45)

        print("1. Add New Test")

        print("2. View Test History")

        print("3. Analyse Performance")

        print("4. View Graphs")

        print("5. Gemini AI Analysis")

        print("6. Export CSV")

        print("7. Exit")

        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":

            add_test()

        elif choice == "2":

            show_history()

        elif choice == "3":

            analyse()

        elif choice == "4":

            show_graphs()

        elif choice == "5":

            gemini_analysis()

        elif choice == "6":

            export_csv()

        elif choice == "7":

            print("Good luck with your JEE preparation!")

            break

        else:

            print("Invalid choice!")


main()