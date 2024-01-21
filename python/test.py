from iapt import IAPT

a = IAPT("api_key", "process_name", debug=False, message_lines=3)
# a.output("Hello World", should_notify=True)
result = a.read_choices("Test Choice", ["Choice 1", "Choice 2"])
