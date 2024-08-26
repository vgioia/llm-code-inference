#!/bin/bash

RUN_NAME="202408260837_llama3_1_70b"
CODE_PATH="./runs/$RUN_NAME"
PYTHON_PATH="./temp/$RUN_NAME"
TEST_TASK_DIR="./tests"
INPUT_PATH="input"
OUTPUT_PATH="output"
ACTUAL_OUTPUT_PATH="temp"
LOG_PATH="./logs/$RUN_NAME"

TIMEOUT_DURATION=8

mkdir -p $PYTHON_PATH

for task in $CODE_PATH/*; do
    taskname=$(basename "$task")
    mkdir $PYTHON_PATH/$taskname

    for run in $task/*; do
        runname=$(basename "$run")
        
        python_file="$PYTHON_PATH/$taskname/$runname.py"
        sed 's/```//g ; s/python//g'  $run > $python_file

        mkdir -p $LOG_PATH/$taskname
        log_file=$LOG_PATH/$taskname/$runname

        mkdir -p $TEST_TASK_DIR/$taskname/$runname/$ACTUAL_OUTPUT_PATH

        for file in $TEST_TASK_DIR/$taskname/$INPUT_PATH/*; do
            filename=$(basename "$file")

            actual_output=$TEST_TASK_DIR/$taskname/$runname/$ACTUAL_OUTPUT_PATH/$filename
            expected_output=$TEST_TASK_DIR/$taskname/$OUTPUT_PATH/$filename

            timeout $TIMEOUT_DURATION python3 $python_file < $file > $actual_output

            if [ $? -eq 124 ]; then
                echo "Timed out when executing $filename"
                echo "TIMEOUT" >> $log_file
            else
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

        rm -r $TEST_TASK_DIR/$taskname/$runname
    done
done

rm -r $PYTHON_PATH
