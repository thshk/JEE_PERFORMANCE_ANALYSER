# JEE Analyser

This is a Python project I made to track my JEE mock test marks and
check my performance.

## Features

-   Add marks for Physics, Chemistry and Maths.
-   Save test data so it is available next time.
-   View previous test records.
-   Check total marks, average marks and highest and lowest scores.
-   Check subject-wise average marks.
-   Compare recent scores to see if performance is improving or
    declining.
-   View graphs of test scores and subject-wise performance.
-   Get suggestions using Gemini AI.
-   Export test records to a CSV file.

## Libraries Used

-   NumPy
-   Pandas
-   Matplotlib
-   Google Gen AI

## How to Run

1.  Install Python 3.
2.  Install the required libraries (Written in Requirments Folder)
3.  Run the program:

``` bash
python main.py
```

## Gemini AI Feature

The Gemini AI option needs a Google Gemini API key. The program asks for
the key when you select this option.

You can get an API key from [Google AI
Studio]
(https://aistudio.google.com/apikey).


## Data Storage

The program saves test records in `jee_data.json`. The CSV export option
creates `jee_data.csv`.


## Note

This project is made for tracking JEE mock test performance. It does not
predict official JEE rank or percentile.

## Note

This project is made for tracking JEE mock test performance. It does not
predict official JEE rank or percentile.