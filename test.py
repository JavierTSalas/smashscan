import argparse
import cv2

# SmashScan libraries
import stage_detection
import percent_matching
import video_analysis


# Run the PM test over a wide range of input parameters.
def run_all_pm_tests(test_type_str, video_location,
    start_fnum, stop_fnum, show_flag, wait_flag):

    # Create a capture object and set the stop frame number if none was given.
    capture = cv2.VideoCapture(video_location)
    if stop_fnum == 0:
        stop_fnum = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Run the PM test over various parameter configurations,
    run_pm_test(capture, test_type_str, start_fnum, stop_fnum,
        show_flag, wait_flag, gray_flag=False)
    run_pm_test(capture, test_type_str, start_fnum, stop_fnum,
        show_flag, wait_flag, gray_flag=True)

    # Release the OpenCV capture object.
    capture.release()


# Run a single PM test over a given group of input parameters.
def run_pm_test(capture, test_type_str, start_fnum, stop_fnum,
    show_flag, wait_flag, gray_flag):

    # Initialize the PM object.
    pm = percent_matching.PercentMatcher(capture, [start_fnum, stop_fnum],
        gray_flag, show_flag, wait_flag)

    # Display the flags used for the current PM test.
    print("==== Percent Matching Test ====")
    print("\tgray_flag={}".format(gray_flag))
    print("\tshow_flag={}".format(show_flag))

    # Run the PM test according to the input test_type_str.
    if test_type_str == "pms":
        pm.sweep_test()
    elif test_type_str == "pmc":
        pm.calibrate_test()
    elif test_type_str == "pmi":
        pm.initialize_test()
    elif test_type_str == "pmt":
        pm.timeline_test()


if __name__ == '__main__':
    # Create a CLI parser and add a video file positional argument.
    parser = argparse.ArgumentParser(description='A testing tool used to \
        analyze the performance of trained DarkNet weights.')
    parser.add_argument('video_name', type=str,
        help='The name of the video file to be tested on.')

    # Add CLI arguments to run various smashscan tests.
    parser.add_argument('-pms', '--pms_test_flag', action='store_true',
        help='A flag used to run the percent matching sweep test.')
    parser.add_argument('-pmc', '--pmc_test_flag', action='store_true',
        help='A flag used to run the percent matching calibrate test.')
    parser.add_argument('-pmi', '--pmi_test_flag', action='store_true',
        help='A flag used to run the percent matching initialize test.')
    parser.add_argument('-pmt', '--pmt_test_flag', action='store_true',
        help='A flag used to run the percent matching timeline test.')
    parser.add_argument('-sdt', '--sdt_test_flag', action='store_true',
        help='A flag used to run the stage detection timeline test.')

    # Add CLI arguments for parameters of the various smashscan tests.
    parser.add_argument('-show', '--show_flag', action='store_true',
        help='A flag used to display the results as each test runs.')
    parser.add_argument('-wait', '--wait_flag', action='store_true',
        help='A flag used to wait for key inputs during displaying frames.')
    parser.add_argument('-save', '--save_flag', action='store_true',
        help='A flag used to determine if frames are saved.')
    parser.add_argument('-start', '--start_fnum', type=int, default=0,
        nargs='?', help='The initial frame to begin testing.')
    parser.add_argument('-stop', '--stop_fnum', type=int, default=0,
        nargs='?', help='The final frame to end testing.')

    # Parse the CLI arguments and create a compact video location string.
    args = parser.parse_args()
    video_location = "{:s}/{:s}".format('videos', args.video_name)

    # Run the smashscan test indicated by the input flags (tfnet by default).
    if args.pms_test_flag:
        run_all_pm_tests("pms", video_location, args.start_fnum,
            args.stop_fnum, args.show_flag, args.wait_flag)
    elif args.pmc_test_flag:
        run_all_pm_tests("pmc", video_location, args.start_fnum,
            args.stop_fnum, args.show_flag, args.wait_flag)
    elif args.pmi_test_flag:
        run_all_pm_tests("pmi", video_location, args.start_fnum,
            args.stop_fnum, args.show_flag, args.wait_flag)
    elif args.pmt_test_flag:
        run_all_pm_tests("pmt", video_location, args.start_fnum,
            args.stop_fnum, args.show_flag, args.wait_flag)
    elif args.sdt_test_flag:
        capture = cv2.VideoCapture(video_location)
        sd = stage_detection.StageDetector(capture,
            args.show_flag, args.save_flag)
        sd.standard_test()
    else:
        va = video_analysis.VideoAnalyzer(video_location, args.show_flag)
        va.standard_test()
