import argparse
import datetime
import sys

from wpCalc import L1WaterProductivity


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main(args=None):

    parser = argparse.ArgumentParser(
        description='Water Productivity using Google Earth Engine')
    groupTimePeriod = parser.add_mutually_exclusive_group()
    groupTimePeriod.add_argument("-a",
                                 "--annual",
                                 metavar='Year',
                                 type=int,
                                 help="Calculate Water Productivity Annually - \
                                        Year must be provided",
                                 default=0)

    groupTimePeriod.add_argument("-d",
                                 "--dekadal",
                                 metavar='Start Date YYYY-MM-DD, \
                                 End Date YYYY-MM-DD',
                                 help="Calculate Water Productivity for ten days -\
                                       Starting and ending date must be \
                                       provided with the following \
                                       format YYYY-MM-DD",
                                 nargs=2,
                                 type=valid_date)

    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_true")

    group_output = parser.add_mutually_exclusive_group()
    group_output.add_argument("-c",
                              "--chart",
                              help="Each calculated component (AGBP, AET, WPm)\
                               shown on a chart",
                              action="store_true")
    group_output.add_argument("-m",
                              "--map",
                              help="Show the final output overlaid \
                              on Google Map",
                              action="store_true")

    results = parser.parse_args()
    print(results)

    # elaborazione = L1WaterProductivity()

    if results.verbose:
        if results.annual:
            if results.chart:
                print("Water productivy will be calculated for "
                      "year {} and shown as chart ".format(results.annual))
            else:
                print("Water productivy will be calculated for "
                      "year {} and shown as map ".format(results.annual))
        else:
            if results.chart:
                print("Water productivy will be calculated between {} e {} "
                      "and shown as chart".format(results.dekadal[0],
                                                  results.dekadal[1]))

            else:
                print("Water productivy will be calculated between {} e {} "
                      "and shown as map".format(results.dekadal[0],
                                                results.dekadal[1]))
    else:
        if results.annual:
            if results.chart:
                print("Water productivy year {} as "
                      "chart ".format(results.annual))
            else:
                print("Water productivy year {} as "
                      "map ".format(results.annual))
        else:
            if results.chart:
                print("Water productivy between {} e {} as "
                      "chart".format(results.dekadal[0],
                                     results.dekadal[1]))
            else:
                print("Water productivy between {} e {} as map".format(
                    results.dekadal[0],
                    results.dekadal[1]))


if __name__ == '__main__':
    main()
