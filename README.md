For research purposes all the outputs from scripts are saved in this project. However, you may choose run this locally following the steps.

First you need to unzip files from one of editions of "Maratona de Programação SBC". The logs run saved in repo are from [2023 edition](https://maratona.sbc.org.br/hist/2023/primfase23/). Once the files from "Entradas e Saídas" are unzipped and saved in `packages` folder you are ready to continue.

The zipped inputs and outputs inside `packages` are treated and copied to `tests` folder with `prepare_files.py`, where `run_tests.sh` will later run python code against them from.

Besides preparing tests, you need to clean up raw prompts which have been copied directly from PDF contest to `raw_prompts` beforehand. Run `clean_up_prompts.py` to do this.

Also, you need to install a LLM to inference python code from the contest tasks. The model used is the CLI version of Llama, available to download in [this tutorial](https://github.com/meta-llama/llama-recipes/blob/main/recipes/quickstart/Running_Llama3_Anywhere/Running_Llama_on_Mac_Windows_Linux.ipynb)

Once one its version is running, you are set to run `inference.py`. It will produce outputs inside `runs` which will be later used along with tests.

Now, you are set to run `run_tests.sh`. Once the execution logs are saved in `logs` folder, execute `evaluate_results.py` to obtain metrics about model solving proposed tasks.

Based on local executions, the following `pass@k`s have been observed:
|        | gpt-4o       | llama3.1:70b |
| ------ | ------ | ------------ |
| pass@1       | 36.92%       | 39.04%                   |
| pass@3       | 41.15%       | 39.23%                   |
| pass@5       | 42.82%       | 40.38%                   |
