import json

import locust
from locust import HttpUser, task

# from __future__ import absolute_import
# from __future__ import print_function
from locust import User, between, TaskSet, task, events
import time


# def create_conn(conn_string):
#     print("Connecting to MySQL")
#     return create_engine('mysql+pymysql://' + conn_string).connect()

def execute1():
    # _conn = create_conn(conn_string)
    # rs = _conn.execute(query)
    # return rs
    JSON = "{\"errorCode\":0,\"errorMessage\":null,\"dataObject\":\"你好\"}"
    json_object = json.loads(JSON)
    error_code = json_object.get("errorCode")
    if error_code > 0:
        register_success = False
    else:
        register_success = True
    # time.sleep(0.5)
    return register_success


'''
  The MySQL client that wraps the actual query
  https://stackoverflow.com/questions/76016708/locust-events-object-has-no-attribute-request-success
  https://stackoverflow.com/questions/62968986/problem-updating-locust-script-to-1-x-typeerror-init-takes-1-positional
  https://medium.com/analytics-vidhya/create-custom-clients-in-locust-io-to-test-database-performance-fd71235ece6e
'''


class MySqlClient:

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                res = execute1()
                events.request.fire(request_type="mysql",
                                    name=name,
                                    response_time=int((time.time() - start_time) * 1000),
                                    response_length=1,
                                    exception=None,
                                    context={})
            except Exception as e:
                events.request.fire(request_type="mysql",
                                    name=name,
                                    response_time=int((time.time() - start_time) * 1000),
                                    response_length=1,
                                    exception=e,
                                    context={})

                print('error {}'.format(e))

        return wrapper


class HelloWorldUser(User):
    register_success = False

    def __init__(self, parent):
        super().__init__(parent)
        self.client = MySqlClient()

    @task
    def test1(self):
        register_success = self.client.execute1()
