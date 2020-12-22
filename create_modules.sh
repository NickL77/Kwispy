#!/bin/bash

pacmd load-module module-null-sink sink_name=virtsink format=s16le rate=16000 channels=1 sink_properties=device.description=virtsink

# sleep 5

# pacmd load-module module-remap-source master=virtsink.monitor source_name=kwispy_mic source_properties=device.description=Kwispy

