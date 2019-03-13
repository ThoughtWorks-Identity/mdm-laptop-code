import logging
import logging.handlers
import subprocess


class SumologicHandler(logging.handlers.HTTPHandler):
    def emit(self, record):
        print(record)
        log_entry = self.format(record)

        log_url = f'https://{self.host}{self.url}'
        command = ['curl', '-s', '-X', 'POST', log_url, '-H', 'content-type: application/json', '-d', log_entry]
        return subprocess.check_output(command)
