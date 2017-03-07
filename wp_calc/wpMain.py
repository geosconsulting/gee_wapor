import argparse
import datetime
# import sys
import json

from wpCalc import L1WaterProductivity


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main(args=None):

    parser = argparse.ArgumentParser(description='Water Productivity using Google Earth Engine')
    groupTimePeriod = parser.add_mutually_exclusive_group()
    groupTimePeriod.add_argument("-a",
                                 "--annual",
                                 metavar='Year',
                                 type=int,
                                 help="Calculate Water Productivity Annually"
                                      " - Year must be provided",
                                 default=0)

    groupTimePeriod.add_argument("-d",
                                 "--dekadal",
                                 metavar="Start End Dates",
                                 help="Calculate Water Productivity for dekads"
                                      " - Starting and ending date must"
                                      " be provided with the following "
                                      "format YYYY-MM-DD",
                                 nargs=2,
                                 type=valid_date)

    group_output = parser.add_mutually_exclusive_group()
    group_output.add_argument("-c",
                              "--chart",
                              help="Each calculated component (AGBP, AET, WPm)"
                                   " shown on a chart",
                              action="store_true")
    group_output.add_argument("-m",
                              "--map",
                              help="Show the final output overlaid "
                                   " on Google Map",
                              action="store_true")

    parser.add_argument('-e', '--export', choices=['u', 'd', 'a', 'g', 'n'],
                        help="Choose export to url(-u), drive (-d), "
                             " asset (-t) or geoserver (-g)")

    parser.add_argument('-i', '--map_id',
                        help="Generate map id for generating tiles",
                        action="store_true")

    parser.add_argument('-r', '--replace', type=float,
                        help="Replace the Above Ground Biomass Production with Net Primary Productivity multiplied "
                             "by a constant value. Sending -s 1.25 will set agbp=npp * 1.25. If not provided default "
                             "datasets will be used instead")

    parser.add_argument('-t', '--timeseries',
                        #type=basestring,
                        help="Time Series from data collections stored in GEE for the chose country")

    parser.add_argument('-s', '--arealstat',
                        # type=basestring,
                        help="Zonal statistics form a WaterProductivity layer generated on the fly in GEE for the chosen country")

    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_true")

    results = parser.parse_args()
    print(results)

    elaborazione = L1WaterProductivity()

    if results.annual:
        abpm, aet = elaborazione.image_selection
    elif results.dekadal:
        date_v = [results.dekadal[0], results.dekadal[1]]
        elaborazione.image_selection = date_v
        abpm, aet = elaborazione.image_selection

    if results.replace:
        moltiplicatore = results.replace
        elaborazione.multi_agbp = moltiplicatore
        abpm = elaborazione.multi_agbp

    if results.timeseries:
        elaborazione.generate_ts(results.timeseries, str(results.dekadal[0]), str(results.dekadal[1]))

    if results.arealstat:
        elaborazione.generate_arealstats(results.arealstat, results.dekadal[0], results.dekadal[1])

    L1_AGBP_summed, ETaColl1, ETaColl2, ETaColl3, WPbm = elaborazione.image_processing(abpm, aet)

    if results.map_id:
        print elaborazione.map_id_getter(WPbm)

    if results.chart:
        elaborazione.image_visualization('c', L1_AGBP_summed, ETaColl3, WPbm)
    elif results.map:
        elaborazione.image_visualization('m', L1_AGBP_summed, ETaColl3, WPbm)
    else:
        pass

    elaborazione.image_export(results.export, WPbm)

if __name__ == '__main__':
    main()
