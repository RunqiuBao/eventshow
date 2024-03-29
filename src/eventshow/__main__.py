#!/usr/bin/python3
import argparse
from pathlib import Path

import eventshow
import eventshow.readwrite


def main():
    parser = argparse.ArgumentParser(description = "A commandline tool for transforming or visualizing  event raw file into frame based representations")
    parser.add_argument("input_file", help="Path to the input event raw data file.")
    parser.add_argument("-o", "--output_path", help="Path to save the output data.")
    parser.add_argument("-vo", "--viszonly", help="Only visualize, do not save to disk.")
    parser.add_argument("--dtms", help="Time interval in ms for each frame.")
    parser.add_argument("--numevents", help="Number of events per frame.")
    parser.add_argument("--concentrate", action='store_true', help="use concentrate network to generate sharp frames. Need to set --numevents.")
    parser.add_argument("--numframes", help="Number of event frames for early quit.")
    parser.add_argument("--savelmdb", action='store_true', help="whether save output to lmdb format.")

    official_loaders = [
        loader for loader in dir(eventshow.readwrite) if not loader.startswith("_")
    ]
    parser.add_argument("-m", "--rw_module", default="base", help="official loaders: "f"{official_loaders}")
    args = parser.parse_args()

    if args.dtms and args.numevents:
        print("Error: only one of --dtms and --numevents can be set.")
        return
    
    if args.concentrate and not args.numevents:
        print("Error: --concentrate need to set --numevents.")
        return

    eventshow.eventshow(
        args.rw_module,
        Path(args.input_file),
        Path(args.output_path),
        dt_ms=int(args.dtms) if args.dtms else None,
        numevents_perslice=int(args.numevents) if args.numevents else None,
        is_use_concentrate=args.concentrate if args.concentrate else False,
        num_frames_exit=int(args.numframes) if args.numframes else None,
        is_save_lmdb=args.savelmdb if args.savelmdb else False,
    )


if __name__ == "__main__":
    main()
