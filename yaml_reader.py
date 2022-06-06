import importlib

import yaml
from multiprocessing import Queue


class YamlPipelineExecutor:
    def __init__(self, pipeline_location):
        self._pipeline_location = pipeline_location
        self._queues = {}
        self._workers = {}

    def _load_pipeline(self):
        with open(self._pipeline_location, 'r') as file:
            self._yaml_data = yaml.safe_load(file)

    def _initialize_queues(self):
        for queue in self._yaml_data['queues']:
            queue_name = queue["name"]
            self._queues[queue_name] = Queue()

    def _initialize_workers(self):
        for worker in self._yaml_data["workers"]:
            worker_class = getattr(importlib.import_module(worker["location"]), worker["class"])
            input_queue = worker.get("input_queue")
            output_queue = worker.get("output_queue")

            num_instances = worker.get('instances', 1)

            init_params = {
                "queue": self._queues.get(input_queue),
                "output_queue": self._queues.get(output_queue)
                }
            self._workers[worker['name']] = []
            for _ in range(num_instances):
                self._workers[worker['name']].append(worker_class(**init_params))

    def _join_workers(self):
        for worker_name in self._workers:
            for thread in self._workers[worker_name]:
                thread.join()

    def process_pipeline(self):
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()

