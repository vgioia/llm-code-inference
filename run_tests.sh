#!/bin/bash

CODE_PATH="./runs"
PYTHON_PATH="./temp"
TEST_TASK_DIR="./tests"
INPUT_PATH="input"
OUTPUT_PATH="output"
ACTUAL_OUTPUT_PATH="temp"
LOG_PATH="./logs"

TIMEOUT_DURATION=8

mkdir $PYTHON_PATH

for task in $CODE_PATH/*; do
    taskname=$(basename "$task") 
    python_file=$PYTHON_PATH/$taskname
    sed 's/```//g' $task > $python_file

    log_file=$LOG_PATH/$taskname
    mkdir $TEST_TASK_DIR/$taskname/$ACTUAL_OUTPUT_PATH

    for file in $TEST_TASK_DIR/$taskname/$INPUT_PATH/*; do
        # Extract the filename from the full path
        filename=$(basename "$file")

        actual_output=$TEST_TASK_DIR/$taskname/$ACTUAL_OUTPUT_PATH/$filename
        expected_output=$TEST_TASK_DIR/$taskname/$OUTPUT_PATH/$filename

        # Remove the string from the file and save to the output directory
        timeout $TIMEOUT_DURATION python3 $python_file < $file > $actual_output

        if [ $? -eq 124 ]; then
            echo "Timed out when executing $filename"
            echo "TIMEOUT" >> $log_file
        else
            # Compare the actual output with the expected output
            if diff -q $actual_output $expected_output > /dev/null; then
                echo "PASSED" >> $log_file
            else
                echo "FAILED" >> $log_file
                echo "Expected Output:"
                cat $expected_output
                echo "Actual Output:"
                cat $actual_output
            fi
        fi

        echo "Processed $filename"
        rm $actual_output
    done

    rm $python_file
    rmdir $TEST_TASK_DIR/$taskname/$ACTUAL_OUTPUT_PATH
done

rmdir $PYTHON_PATH
