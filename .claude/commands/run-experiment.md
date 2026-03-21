I want to run an experiment. The script name is: $ARGUMENTS

Before running, check:
1. The file exists at experiments/$ARGUMENTS
2. It has logging set up (look for csv or DictWriter)
3. It is runnable standalone

Then run: python experiments/$ARGUMENTS

After it finishes, append one line to docs/experiment_log.md in this format:
[today's date] | [script name] | [key result from output] | [opponent type if shown]

Show me the final summary output and confirm the log was updated.
