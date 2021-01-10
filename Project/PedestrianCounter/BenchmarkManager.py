import json
import os


class BenchmarkManager:
    def __init__(self, file_name):
        self.id = -1
        self.benchmarks = None

        self.detectors = ["MobileNet SSD", "YoloV4-tiny"]

        with open(file_name) as json_file:
            data = json.load(json_file)
            self.benchmarks = data["benchmarks-one"]

        self.benchmark_len = len(self.benchmarks)

    def start_next(self, main_process_therad):
        self.id += 1
        if self.id == self.benchmark_len:
            main_process_therad.main_process.benchmark.save_scores()
            print("BENCHMARK END")
            return
        benchmark = self.benchmarks[self.id]
        print("BENCHMARK {}".format(self.id))
        print(
            "Detector: {}, FrameSkip: {}, Conf: {}, MinUpdate: {}".format(
                self.detectors[benchmark["d"]],
                benchmark["sf"],
                benchmark["c"],
                benchmark["mu"],
            )
        )
        main_process_therad.stop_source()
        main_process_therad.main_process.test_name = str(self.id)
        main_process_therad.main_process.set_detector(self.detectors[benchmark["d"]])
        main_process_therad.main_process.set_frames_to_skip(benchmark["sf"])
        main_process_therad.main_process.detector.values["Confidence"].set_value(
            benchmark["c"]
        )
        main_process_therad.main_process.counter.set_min_update_time(benchmark["mu"])
        main_process_therad.change_source("Video")
