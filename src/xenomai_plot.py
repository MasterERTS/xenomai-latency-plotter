import sys
import os
import optparse
import matplotlib.pyplot as plt


def process_cmd():
    parser = optparse.OptionParser(description="Process the result of xenomai")
    parser.add_option("-f", "--file", dest='result_file', default="")
    opts, args = parser.parse_args()
    args # just to remove warning
    if not os.path.exists(opts.result_file):
        parser.print_help()
        sys.exit(-1)
    return os.path.realpath(opts.result_file)


def process_output(result_file):
    hist_data = []
    avg = 0
    count = 0
    min_latency = 0
    max_latency = 0
    variant = 0
    with open(result_file) as f:
        for line in f.readlines():
            if len(line.strip()) == 0:
                continue

            if line.startswith("#"):
                continue

            lat_value = float(line.strip().split()[0])

            if min_latency == 0:
                min_latency = lat_value

            if lat_value > max_latency:
                max_latency = lat_value

            lat_count = int(line.strip().split()[1])
            avg += lat_value * lat_count
            count += lat_count
            hist_data.append((lat_value, lat_count))

        avg = float(avg / count)

    for item in hist_data:
        variant += ((item[0]-avg)**2)*item[1]

    variant = variant / count
    stdev = variant**(.5)
    # print(variant, stdev)

    return hist_data, min_latency, max_latency, avg, stdev


def draw_figure(hist_data, min_latency, max_latency, avg, stdev):
    x = [item[0] for item in hist_data]
    y = [item[1] for item in hist_data]
    # print(stdev)
    plt.style.use('ggplot')
    plt.bar(x, y, label="avg=%.3f,min_latency=%.3f,max_latency=%.3f,stdev=%.3f" %
            (avg, min_latency, max_latency, stdev))

    plt.legend()
    plt.ylabel("Number of Samples")
    plt.xlabel("Latency (us)")
    plt.savefig('../figs/last_lat_fig.png')
    plt.show()


if __name__ == "__main__":
    file = process_cmd()
    hist, min_latency, max_latency, avg, stdev = process_output(file)
    draw_figure(hist, min_latency, max_latency, avg, stdev)
