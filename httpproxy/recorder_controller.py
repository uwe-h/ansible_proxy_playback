import os
import sys
import traceback

from mitmproxy import io, http


RECORDING = "RECORDING"
PLAYING = "PLAYING"
STOP = "STOP"

RECORDINGS_DIR = "/recordings"

class RecorderController:
    def __init__(self):
        self.mode = STOP


    def request(self, flow):
        try:
            if self.is_controller_request(flow):
                print(f"Control Request detected")
                self.process_recorder_control_request(flow)
                flow.response =  http.Response.make(
                    200,  # (optional) status code
                    b"everything ok")

            if self.is_relevant_request(flow) and self.mode == PLAYING:
                print("Playback")
                saved_flow = self.request_list.pop(0)
                if self.eq_request(flow.request, saved_flow.request):
                    print("Providing recorded request")
                    flow.response = saved_flow.response
                else:
                    print("Unknown Request")
                    flow.response = http.Response.make(
                        500,  # (optional) status code
                        b"Unexpected request")
        except:
            traceback.print_exc()
            self.response = http.Response.make(
                500,  # (optional) status code
                b"Unexpected error")



    def response(self, flow):
        try:
            if self.is_relevant_request(flow):
                print(f"Processing response: {flow.request.pretty_url}")
                if self.is_relevant_request(flow) and self.mode == RECORDING:
                    print("Recording")
                    self.flow_writer.add(flow)
        except:
            traceback.print_exc()
            self.response = http.Response.make(
                500,  # (optional) status code
                b"Unexpected error")

    def eq_request(self, r1, r2):
        return r1.pretty_url == r2.pretty_url and \
            r1.method == r2.method and \
            r1.content == r2.content

    def process_recorder_control_request(self, flow):
        if "start_recording" == flow.request.path_components[0]:
            self.mode = RECORDING
            self.path = flow.request.path_components[1]
            self.recording_file = open(os.path.join(RECORDINGS_DIR, self.path), "wb")
            self.flow_writer = io.FlowWriter(self.recording_file)

        if "stop_recording" == flow.request.path_components[0]:
            self.recording_file.close()
            self.mode = STOP

        if "start_playing" == flow.request.path_components[0]:
            self.mode = PLAYING
            with open(os.path.join(RECORDINGS_DIR, flow.request.path_components[1]), "rb") as request_file:
                flow_reader = io.FlowReader(request_file)
                self.request_list = [request for request in flow_reader.stream()]

        if "stop_playing" == flow.request.path_components[0]:
            self.mode = STOP



    def is_controller_request(self, flow):
        return "httpproxy.control.io" in flow.request.pretty_host and flow.request.method == 'POST'

    def is_relevant_request(self, flow):
        return flow.request.pretty_host.endswith(".amazonaws.com")


addons = [
    RecorderController()
]