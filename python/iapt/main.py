import threading
from .backend import Backend
from concurrent.futures import ThreadPoolExecutor, as_completed

TIME_BEFORE_TIMEOUT = 5


class IAPT:
    def __init__(self, api_key, process_name, debug=True, message_lines=3):
        self.api_key = api_key
        self.process_name = process_name
        self.debug = debug
        self.message_lines = message_lines
        self._backend = Backend()
        self.flag = 0
        self.lock = threading.Lock()
        self.threads = []

    def __del__(self):
        for thread in self.threads:
            thread.join()
        self._backend.close()

    def __notify(self, message):
        print("Notifying")
        self._backend.send_command({
            "command": "notify",
            "api_key": self.api_key,
            "process_name": self.process_name,
            "message": message
        })

    def output(self, message, should_notify=False):
        print(message)
        if not self.debug and should_notify:
            t = threading.Thread(target=self.__notify,
                                 args=(message,))
            t.start()
            self.threads.append(t)

    def __read_choices_local(self, prompt, choices):
        def timeout():
            raise Exception("Timeout")

        timer = threading.Timer(TIME_BEFORE_TIMEOUT, timeout)
        timer.start()
        print(prompt)
        for i, choice in enumerate(choices):
            print(f"{i + 1}. {choice}")
        choice = None
        while True:
            try:
                c = int(input("Choice: "))
                if c > 0 and c <= len(choices):
                    choice = choices[c - 1]
                    break
            except Exception:
                if self.flag != 0:
                    break
            print("Try again")
        with self.lock:
            self.flag = 1
        return choice

    def __read_choices_remote(self, prompt, choices):
        self._backend.send_command({
            "command": "read_choices",
            "prompt": prompt,
            "choices": choices
        })
        choice = None
        while True:
            try:
                choice = self._backend.recv_data()
                break
            except Exception:
                if self.flag != 0:
                    break
        with self.lock:
            self.flag = 2
        return choice

    def read_choices(self, prompt, choices):
        try:
            choices_strings = [str(choice) for choice in choices]
        except TypeError:
            raise TypeError(
                "Choices must be iterable and elements must be castable to string")

        self.flag = 0

        with ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(
                self.__read_choices_local, prompt, choices_strings)
            if not self.debug:
                future2 = executor.submit(
                    self.__read_choices_remote, prompt, choices_strings)

        if self.flag == 1:
            return future1.result()
        elif self.flag == 2:
            return future2.result()
