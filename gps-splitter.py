#!/usr/bin/env python3

import argparse
import serial
import sys
import time
import traceback

from out.out_buf import out_buf
from out.out_socat import out_socat
from out.OutputError import OutputError

parser = argparse.ArgumentParser(description='Take a hardware serial port as input, and clone it to one or more outputs. Useful for ntpd and gpsd.')

parser.add_argument("--in", "-i", dest="in_port", required=True, help="Input serial port", type=str)
parser.add_argument("--baud", "-b", dest="in_baud", default=9600, help="Baud rate of all serial ports", type=int)
parser.add_argument("--timeout", "-t", dest="in_to", default=10, help="Timeout for serial port open.  Timeout will be ignored once port is open.")
parser.add_argument("--buffer", "-u", default=128, help="Buffer size.  Used for input serial buffering and output socat buffering", type=int)
parser.add_argument("--out", "-o", dest="out_ports", default=[], action="append", help="Output virtual serial port.  Must not exist, can be specified multiple times", type=str)
parser.add_argument("--stdout", "-s", action="store_true", help="Also write serial data to stdout.  Userful for debugging")
parser.add_argument("--sleep", default=0.1, help="Sleep time in the primary loop in seconds", type=int)
args = parser.parse_args()

def run():
    sys.stderr.write("Input serial port: \"{0}\" @ {1} baud\n".format(args.in_port, args.in_baud))
    sys.stderr.write("Output serial ports: {0}\n".format(args.out_ports))
    if args.stdout:
        sys.stderr.write("Cloning to stdout\n")
    with serial.Serial(args.in_port, baudrate=args.in_baud, timeout=args.in_to) as in_port:
        if args.stdout:
            outs = [out_buf("stdout", sys.stdout.buffer, closable=False)]
        else:
            outs = []
        for o in args.out_ports:
            out = out_socat(o,o)
            out.start()
            outs.append(out)
        buffer_size = args.buffer
        running = True
        while(running):
            try:
                if in_port.inWaiting() < buffer_size:
                    local_read = in_port.inWaiting()
                else:
                    local_read = buffer_size
                buf = in_port.read(local_read)
                dead_outs = []
                for i in range(len(outs)):
                    try:
                        outs[i].write(buf)
                        outs[i].flush()
                    except OutputError as e:
                        sys.stderr.write("Error on {0}: {1}\n".format(outs[i].name, e))
                        sys.stderr.write("Gracefully closing {0}...".format(outs[i].name))
                        outs[i].close()
                        sys.stderr.write("done!\n")
                        sys.stderr.write("Flagging {0} for deletion\n".format(outs[i].name))
                        dead_outs.append(i)
                dead_outs = sorted(dead_outs, reverse=True)
                for i in dead_outs:
                    sys.stderr.write("Removing {0} from the output list\n".format(outs[i].name))
                    outs.pop(i)
                time.sleep(args.sleep)
            except KeyboardInterrupt:
                running=False
                sys.stderr.write("exiting...")
            except:
                running=False
                traceback.print_exc()
                sys.stderr.write("crashing...")
        for o in outs:
            try:
                o.close()
            except:
                traceback.print_exc()
        in_port.close()
    sys.stderr.write("done!\n")

if sys.flags.interactive:
    sys.stderr.write("Use the function run() to run the program!\n")
else:
    sys.stderr.write("Starting the gps splitter...\n")
    run()
