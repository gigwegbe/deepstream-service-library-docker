################################################################################
# The MIT License
#
# Copyright (c) 2019-2021, Prominence AI, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
################################################################################

#!/usr/bin/env python

import sys
sys.path.insert(0, "../../")
import time

from dsl import *

# Filespecs for the Primary GIE
inferConfigFile = '../../test/configs/config_infer_primary_nano.txt'
modelEngineFile = '../../test/models/Primary_Detector_Nano/resnet10.caffemodel_b8_gpu0_fp16.engine'

## 
# Function to be called on XWindow Delete event
## 
def xwindow_delete_event_handler(client_data):
    print('delete window event')
    dsl_main_loop_quit()

## 
# Function to be called on End-of-Stream (EOS) event
## 
def eos_event_listener(client_data):
    print('Pipeline EOS event')
    dsl_main_loop_quit()

def main(args):

    # Since we're not using args, we can Let DSL initialize GST on first call
    while True:

        # Two URI File Sources - using the same file.
        retval = dsl_source_uri_new('source-1', "../../test/streams/sample_1080p_h264.mp4", False, 0, 2)
        if retval != DSL_RETURN_SUCCESS:
            break
        retval = dsl_source_uri_new('source-2', "../../test/streams/sample_1080p_h264.mp4", False, 0, 2)
        if retval != DSL_RETURN_SUCCESS:
            break

        ## Two new File Sinks with H264 Codec type and MKV conatiner muxer, and bit-rate and frame interval
        retval = dsl_sink_file_new('file-sink', "./2-source.mkv", DSL_CODEC_H264, DSL_CONTAINER_MKV, 2000000, 2)
        if retval != DSL_RETURN_SUCCESS:
            break

        # New Primary GIE using the filespecs above, with infer interval
        retval = dsl_infer_gie_primary_new('primary-gie', inferConfigFile, modelEngineFile, 5)
        if retval != DSL_RETURN_SUCCESS:
            break

        ## New KTL Tracker, setting max width and height of input frame
        retval = dsl_tracker_ktl_new('tracker', 480, 272)
        if retval != DSL_RETURN_SUCCESS:
            break

        # New Tiler with dimensions for two tiles - for the two sources
        retval = dsl_tiler_new('tiler1', 1440, 360)
        if retval != DSL_RETURN_SUCCESS:
            break

        # New OSD with text, clock and bbox display all enabled. 
        retval = dsl_osd_new('on-screen-display', 
            text_enabled=True, clock_enabled=True, bbox_enabled=True, mask_enabled=False)
        if retval != DSL_RETURN_SUCCESS:
            break

        # New Window Sink, with matching dimensions as the Tiler
        retval = dsl_sink_window_new('window-sink', 0, 0, 1440, 360)
        if retval != DSL_RETURN_SUCCESS:
            break

        # New Branch for the PGIE, OSD and Window Sink
        retval = dsl_branch_new('branch1')
        if retval != DSL_RETURN_SUCCESS:
            break

        retval = dsl_branch_component_add_many('branch1', ['primary-gie', 'tracker', 'tiler1', 'on-screen-display', 'window-sink', None])
        if retval != DSL_RETURN_SUCCESS:
            break

        # New Demuxer Tee- 
        retval = dsl_tee_demuxer_new('demuxer')
        if retval != DSL_RETURN_SUCCESS:
            break

        # Add the two file sinks as branches to the demuxer
        retVal = dsl_tee_branch_add_many('demuxer', ['file-sink-1', 'file-sink-2', None])
        if retval != DSL_RETURN_SUCCESS:
            break

        # New Splitter Tee- 
        retval = dsl_tee_splitter_new('splitter')
        if retval != DSL_RETURN_SUCCESS:
            break

        # Add Branch1 and the demuxer (as branch2) to the splitter
        retVal = dsl_tee_branch_add_many('splitter', ['branch1', 'demuxer', None])
        if retval != DSL_RETURN_SUCCESS:
            break

        # New Pipeline to use with the above components
        retval = dsl_pipeline_new('pipeline')
        if retval != DSL_RETURN_SUCCESS:
            break

        # Add the window delete handler and EOS listener callbacks to the Pipeline
        retval = dsl_pipeline_eos_listener_add('pipeline', eos_event_listener, None)
        if retval != DSL_RETURN_SUCCESS:
            break
            
        retval = dsl_pipeline_xwindow_delete_event_handler_add("pipeline", xwindow_delete_event_handler, None)
        if retval != DSL_RETURN_SUCCESS:
            break

        # Add the sources the components to our pipeline
        retval = dsl_pipeline_component_add_many('pipeline', 
            ['source-1', 'source-2', 'splitter', None])
        if retval != DSL_RETURN_SUCCESS:
            break
        
        # Play the pipeline
        retval = dsl_pipeline_play('pipeline')
        if retval != DSL_RETURN_SUCCESS:
            break

        dsl_main_loop_run()
        retval = DSL_RETURN_SUCCESS
        break
        
    # Print out the final result
    print(dsl_return_value_to_string(retval))

    dsl_pipeline_delete_all()
    dsl_component_delete_all()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
