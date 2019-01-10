# coding:utf-8
from httprunner import HttpRunner

if __name__ == '__main__':
    runner = HttpRunner()
    runner.run('tests/testcases/testcases_pact.yaml')
    runner.gen_html_report()
